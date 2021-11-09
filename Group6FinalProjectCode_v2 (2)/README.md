*********************** FEDERATED LEARNING DEMO ********************************
Reynaldo Ramirez & Eric Huddleston

The set of programs composed of:
  server_fl.py
  erics_client.py
  erics_client2.py

are all part of an example demonstration that we implemented to further explore
the way federated learning works, its composition and its mechanisms.

To run these programs you will need to have python3 installed as well as PyGad.

To install PyGad you can run the following command on Mac and Linux.

  pip3 install pygad

and
  pip install pygad

  on windows.

These set of programs should be run in the following manner to recreate
a correct demo.

  python3 server_fl
  python3 erics_client.py
  python3 erics_client2.py

This will start the client which will start a new thread to handle every client
making a connection to the server program. The inner workings of the server program
are further described in the server_fl.py source code. This implementation of FL
is a model that will predict the answer to a simple XOR problem.

  The inputs can be:
    [0,0]
    [0,1]
    [1,0]
    [1,1]

  And the corresponding answers can be:

    [0]
    [1]
    [1]
    [0]

That is how an XOR gate works.

erics_client contains two of the possible inputs and erics_client2 contains the other two.

As the model becomes trained, it might take some time for it to be 100% accurate.
In the end the server will stop sending the new averaged model to the clients once it
has been completely trained and 100% accurate. After this the clients will timeout
and exit.

This demo utilizes sockets to send and request info from the server or clients.



*******************************************************************************
# Checkpoint Algorithms

This model of federated learning, provides a substantial update to the shared model of Federated Learning,  using several algorithms executed in random succession
in order to secure a given system as much as possible. By using a randomly adapting model, we were able to create a response time that is as low as possible. Additionally because the functions used in this implementation have relatively inexpensive algorithms, power consumption is also low.

## Installation

The only installation required is for those users who do not have python3 installed, from Linux the command would be:
```bash
sudo apt-get install python3
```
For mac users, first they must open 'Terminal' and execute this command to install homebrew:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
```
Then the homebrew directory can be inserted at the top of the PATH environment variable by adding the following line at the bottom of the '~/.profile' file:
```bash
export PATH="/usr/local/opt/python/libexec/bin:$PATH"
```
Then, from 'Terminal' python3 can be installed using the following command:
```bash
brew install python
```
Windows users can open powershell and use the following command to check if they have the most current version of python installed as so:
```bash
python -V
```
If a version less than 3.8.4 is shown, they can simply update python through either the windows store or the full python installer.
## Usage

```python
Input plain text: _______________
```
