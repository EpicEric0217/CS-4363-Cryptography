import socket
import pickle
import numpy

import pygad
import pygad.nn
import pygad.gann


def calc_fitness(solution, sol_idx):
    global GANN_instance, data_in, data_out

    predict = pygad.nn.predict(last_layer=GANN_instance.population_networks[sol_idx],
                                   data_inputs=data_in)
    correct_predictions = numpy.where(predict == data_out)[0].size
    sol_to_fitness = (correct_predictions/data_out.size)*100

    return sol_to_fitness


def call_after_generation(instance):
    global GANN_instance, last_most_fit

    matrices_pop = pygad.gann.population_as_matrices(population_networks=GANN_instance.population_networks,
                                                            population_vectors=instance.population)

    GANN_instance.update_population_trained_weights(population_trained_weights=matrices_pop)

    print("This Generation = {generation}".format(generation=instance.generations_completed))
    print("Fitness Level    = {fitness}".format(fitness=instance.best_solution()[1]))
    print("Change     = {change}".format(change=instance.best_solution()[1] - last_most_fit))

    last_most_fit = instance.best_solution()[1]

last_most_fit = 0


def prepare(GANN_instance):

    vectors_pop = pygad.gann.population_as_vectors(population_networks=GANN_instance.population_networks)

    init_pop = vectors_pop.copy()

    init_low = -2

    init_high = 5

    numb_parents_mating = 4

    numb_generations = 500

    mutation_percent_genes = 5

    parent_selection_type = "sss"

    crossover_type = "single_point"

    mutation_type = "random"

    keep_parents = 1

    ga_instance = pygad.GA(num_generations=numb_generations,
                           num_parents_mating=numb_parents_mating,
                           initial_population=init_pop,
                           fitness_func=calc_fitness,
                           mutation_percent_genes=mutation_percent_genes,
                           init_range_low=init_low,
                           init_range_high=init_high,
                           parent_selection_type=parent_selection_type,
                           crossover_type=crossover_type,
                           mutation_type=mutation_type,
                           keep_parents=keep_parents,
                           callback_generation=call_after_generation)

    return ga_instance


# XOR inputs
data_in = numpy.array([[1, 0],
                           [1, 1]])

# XOR outputs
data_out = numpy.array([1,
                            0])

#Using the pickle library, we can recieve and decode the GANN instance...
def recieve(sockt, buffer_size=1024, recieve_timeout=10):
    data_recv = b""
    while str(data_recv)[-2] != '.':
        try:
            sockt.settimeout(recieve_timeout)
            data_recv += sockt.recv(buffer_size)
        except socket.timeout:
            print(
                "A socket.timeout exception occurred because the server did not send any data for {recieve_timeout} seconds. There may be an error or the model may be trained successfully.".format(
                    recieve_timeout
                    =recieve_timeout))
            return None, 0
        except BaseException as e:
            return None, 0
            print("An error has occurred while attempting to receive data from the server {mssg}.".format(mssg=e))

    try:
        data_recv = pickle.loads(data_recv) #data_recv holds a dictionary of the following contents:
        # 'subject': 'model', 'data': <pygad.gann.gann.GANN at 0x23de2f22208>
    except BaseException as e:
        print("Error Decoding the Client's Data: {mssg}.\n".format(mssg=e))
        return None, 0

    return data_recv, 1


sockt = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
print("Socket Created.\n")

try:
    sockt.connect(("localhost", 12321))
    print("Successful Connection to the Server.\n")
except BaseException as e:
    print("Error Connecting to the Server: {msg}".format(msg=e))
    sockt.close()
    print("Socket Closed.")

subject = "echo"
GANN_instance = None
best_sol_idx = -1

while True:
    data = {"subject": subject, "data": GANN_instance, "best_solution_idx": best_sol_idx}
    data_byte = pickle.dumps(data)

    print("Sending the Model to the Server.\n")
    sockt.sendall(data_byte)

    print("Receiving Reply from the Server.")
    data_recv, status = recieve(sockt=sockt,
                                 buffer_size=1024,
                                 recieve_timeout=10)
    if status == 0:
        print("Nothing Received from the Server.")
        break
    else:
        print(data_recv, end="\n\n")

    subject = data_recv["subject"]
    if subject == "model":
        GANN_instance = data_recv["data"]
    elif subject == "done":
        print("The server said the model is trained successfully and no need for further updates its parameters.")
        break
    else:
        print("Unrecognized message type.")
        break

    instance = prepare(GANN_instance)

    instance.run()

    #instance.plot_result()

    subject = "model"
    best_sol_idx = instance.best_solution()[2]

# predictions = pygad.nn.predict(last_layer=GANN_instance.population_networks[best_sol_idx], data_inputs=data_inputs)

sockt.close()
print("Socket Closed.\n")
