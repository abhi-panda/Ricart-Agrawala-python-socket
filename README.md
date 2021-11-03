# Ricart-Agrawala-python-socket
Python Socket programming to simulate Distributed system and show the implementation of Ricart-Agrawala algorithm without any enhancements.

## Author
Abhishek Panda, India

## Platform/System requirements
This should work on Python3 across platforms, without any extra pip modules to be installed. The code is created and tested on :
1. Windows 11
2. Python 3.7.4 

## Files
1. server.py
2. client.py

## How to run 
```
[NOTE] Server uses static port number 5050 and clients use dynamic ports. So please make sure 5050 is unused before starting the server code.
```
```
[NOTE] Make sure you use the python pointing to the correct python version. 
```
```
[NOTE] The client code is written with a blocking input infinite loop. So an input would be required to proceed / update messages.
```
### Steps : 
1. Run the server.py first and keep the terminal open.
```
python server.py
```
2. Open as many terminals as you want to depict the number of processes, run the below command and keep the terminals open for interactions
```
python client.py
```
3. You could keep the Server terminal in view or minimize it.

4. Once you have all the process terminals open :
    1. Type 1 and Press Enter(Return) key to request Critical Section (CS) for the current process.
    2. Press Enter(Return) key to check updates / recieve messages . Pressing Enter(Return) on each process terminal is required to update proceedings.

5. Once the requirement is done close all the terminals.

### Output :
All the output are self explanatory. Below are the images attached. 

First Connection :

![First Connection](https://github.com/abhi-panda/Ricart-Agrawala-python-socket/raw/main/images/1.png "First Connection")

One process requesting cs getting reply and executing : 

![One process requesting cs getting reply and executing](https://github.com/abhi-panda/Ricart-Agrawala-python-socket/raw/main/images/4.png "One process requesting cs getting reply and executing")

Multiple processes requesting so prioritizing and use of rdi :

![Multiple processes requesting so prioritizing and use of rdi](https://github.com/abhi-panda/Ricart-Agrawala-python-socket/raw/main/images/2.png "Multiple processes requesting so prioritizing and use of rdi")

Multiple processes requesting so prioritizing using of rdi and executing :

![Multiple processes requesting so prioritizing using of rdi and executing](https://github.com/abhi-panda/Ricart-Agrawala-python-socket/raw/main/images/3.png "Multiple processes requesting so prioritizing using of rdi and executing")


# Algorithm 
Follows https://www.geeksforgeeks.org/ricart-agrawala-algorithm-in-mutual-exclusion-in-distributed-system/
The code makes use of RDi[] array, appending to this array based on priority.

## Assumptions
* Channels are FIFO (for simulation)
* Process numbers are assigned based on the creation times of the process.
* Priority is decided based on the process numbers and request creation time.
