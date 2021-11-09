#!/bin/python3
# ******************* server_fl.py *************************
# Reynaldo Ramirez, tdi572
# This python code sets up the simulated central server of a
# federeated learning system. This program listens on the port
# determined by the global variable listening_port currently 12321
#
# When it recieves a connection, it starts a new thread. This way, we
# can simultaneously handle different clients sending or requesting a model.
#
# This program utilizes PyGad to create a population of Neural Networks
#
# To keep it simple, this program demonstrates a model being trained for an XOR
# problem (just like an XOR gate). The clients will send their own trained
# models and this server_fl program will average those models so that no raw data
# is ever put at risk of an attacker while being transmitted to the server. This
# is the idea of federated learning.
#
# This program will send a dictionary containing the server model to the clients.
#
# This dictionary has only two keys: data and subject.
#
# When the subject is set to model, the server will be sending the model to the client
# so that the client can train it with its own local data.
#
# When the subject is set to echo, the server will reply with the same message recieved from client
#
# The error variable seen throughout the reply funciton in the Sthread class is the accuracy of the model
# Once it is 0, it means that the averaged model is 100% accurate and were done!
#
# When the subject is done, the server is basically letting the client know that the model
# has been successfully trained. And this concludes all programs.
#
# The final result should be a model with [0,1,1,0] values. These are the answers to the XOR problem


# Imports
import time         # For timeouts
import socket       # For networking
import pickle       # To encode/decode the model/data
import numpy        # For arrays
import threading    # To start multiple threads

# Imports for Neural Network
import pygad
import pygad.nn
import pygad.gann

# Global Variables utilized across functions
listening_port = 12321
buffer_size = 1024
timeout = 10

model = None
NN_model = None
inputs = None
outputs = None


# Class to create new thread that
# handles a new connection
#
class SThread(threading.Thread):
    # Thread Constructor
    #
    def __init__(self, connection, client, buff_sz=1024, timeout=5):
        threading.Thread.__init__(self)
        self.connection = connection
        self.client = client
        self.buff_sz= buffer_size
        self.timeout = timeout

    # Recieve function
    #
    def recieve(self):
        r_data = b''
        while True:
            # Attempt to receieve data from socket
            try:
                data = self.connection.recv(self.buff_sz)
                r_data += data

                # If we recieved literally nothing
                if data == b'':
                    r_data = b''
                    # Check the timeout and handle it accordingly
                    if(time.time() - self.r_start_time > self.timeout):
                        return None, 0

                # If we recieved the data correctly (Using a period as delimiter)
                elif str(data)[-2] == '.':
                    print("        Data correctly recieved from client!")

                    # Decode it & return it!
                    r_data = pickle.loads(r_data)
                    return r_data, 1

                # Restart the timeout, since we did recieve data
                else:
                    self.r_start_time = time.time()

            # If unsuccessful at attempting to recieve data, exit
            except BaseException as exc:
                print("        Error while attempting to recieve data from client!")
                print("            {}".format(exc))
                return None, 0

    # This function determines what to send back to the client
    #
    def reply(self, r_data):
        global NN_model, inputs, outputs, model

        if(type(r_data) is dict):
            if(('data' in r_data.keys()) and ('subject' in r_data.keys())):
                subject = r_data['subject']
                print("        Client's data has subject {}.".format(subject))
                print("        Replying...")

                # If client sent echo
                if subject == "echo":
                    if model is None:
                        data = {"subject": "model","data": NN_model}
                    else:
                        predictions = pygad.nn.predict(last_layer=model, data_inputs=inputs)
                        error = numpy.sum(numpy.abs(predictions - outputs))

                        #If error is 0 make no changes to model
                        if error == 0:
                            data = {"subject": "model","data": None}
                            print("        Client asked for model, but it is fully trained. Not sending it")
                        else:
                            data = {"subject": "model", "data": NN_model}

                    # Encode it
                    reply = pickle.dumps(data)

                elif subject == 'model':
                    #print("In Model")
                    try:
                        NN_model = r_data['data']
                        best_model_idx = r_data["best_solution_idx"]

                        best_model = NN_model.population_networks[best_model_idx]
                        #print("in try")
                        if model is None: # If this is the first model recieved, set it as best
                            model = best_model
                            #print('model is none')
                        else:
                            #print("in else")
                            predictions = pygad.nn.predict(last_layer=model, data_inputs=inputs)
                            error = numpy.sum(numpy.abs(predictions - outputs))

                            if error == 0:
                                data = {"subject": "done", "data": None}
                                reply = pickle.dumps(data)
                                print("The model is trained successfully and theres no need to send the model for retraining!")
                                return
                            self.avg_model(model, best_model)

                        #print("After if")
                        predictions = pygad.nn.predict(last_layer=model, data_inputs=inputs)
                        print("Model Predictions: {}".format(predictions))

                        error = numpy.sum(numpy.abs(predictions - outputs))
                        print("Error = {}\n".format(error))

                        if error != 0:
                            data = {"subject": "model", "data": NN_model}
                            reply = pickle.dumps(data)
                        else:
                            data = {"subject": "done", "data": None}
                            reply = pickle.dumps(data)
                            print("\n*****The Model is Trained Successfully*****\n\n")

                    except BaseException as exc:
                        print("Error Decoding the Client's Data: {}.\n".format(exc))
                else:
                    reply = pickle.dumps("Response from the Server")

                try:
                    self.connection.sendall(reply)
                except BaseException as exc:
                    print("Error Sending Data to the Client: {}.\n".format(exc))

            else:
                print("The received dictionary from the client must have the 'subject' and 'data' keys available. The existing keys are {}.".format(r_data.keys()))

        else:
            print("A dictionary is expected to be received from the client but {} received.".format(type(r_data)))



    # Averages the models and updates the main one
    #
    def avg_model(self, model, r_model):
        # Get the current weights associated with each model
        weights = pygad.nn.layers_weights(last_layer=model, initial=False)
        r_weights = pygad.nn.layers_weights(last_layer=r_model, initial=False)

        # take the average
        n_weights = numpy.array(weights + r_weights)/2

        #Update the model
        pygad.nn.update_layers_trained_weights(last_layer=model, final_weights=n_weights)



    # Main function for thread running!
    #
    def run(self):
        print("        Running socket thread for client {}".format(self.client))

        while True:
            # Setup so we cant wait for data until timeout
            self.r_start_time = time.time()

            # Recieve data
            r_data, status = self.recieve()

            # If we failed to recieve data
            if status == 0:
                print("        Did not recieve data from client {} or an error occurred!".format(self.client))
                self.connection.close()
                break

            self.reply(r_data)


# Main function ***********************************************************************
def main():
    print("\nInitializing Server...")
    global listening_port, buffer_size, timeout, model, NN_model, inputs, outputs
    data = b''

    # Setting up initial population of neural networks
    # This is an XOR example, hence the inputs & outputs
    #
    print("    Setting up initial model...", end='')
    model = None
    inputs = numpy.array([[1, 1],[1, 0],[0, 1],[0, 0]])
    outputs = numpy.array([0,1,1,0])
    NN_model = pygad.gann.GANN(num_solutions=6,
                        num_neurons_input=2,
                        num_neurons_hidden_layers=[2],
                        num_neurons_output=2,
                        hidden_activations=["relu"],
                        output_activation="softmax")
    print(" Done.")

    # Set up socket to recieve and send packets!
    #
    print("    Creating & Binding socket...",end='')
    s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    s.settimeout(timeout)
    s.bind(('localhost', listening_port))
    print(" Done.")
    s.listen(1)
    print("    * Socket is listening on 'localhost' port {} *".format(listening_port))

    # Stay listening for connections!!!
    while True:
        try:# If we establish a connection start a thread for it!
            connection, client = s.accept()
            print("\n        Established connection with {}!".format(client))
            new_socket_thread = SThread(connection=connection,
                                        client=client,
                                        buff_sz=buffer_size,
                                        timeout=timeout)
            print("    *Socket thread set up!*")
            new_socket_thread.start()

        except:
            s.close()
            print("    No connections recieved during timeout!\nExiting!")
            break

if __name__ == '__main__':
    main()
