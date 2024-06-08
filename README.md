
# SB_Home_Assignment

The goal of this assignment (project) is to develop an agent that will allow the remote execution of tasks.
The agent is built with a FastAPI framework and responses for various requests.
To see the supported request, you may 

The project has couple of built-in tests which can be found under the src.tests folder (at tests_tasks.py):
 - test_perform_tasks
 - test_run_parallel

Both tests validate the same various functionality of the agent.
The test_run_parallel execute the same api request (as the other test), but do it simultaneously, in order to check
the ability to use the agent in parallel.

The framework for executing the tests is **pytest**.
All tests are planed to pass successfully, whether the request response ended with response status 200 or 402.

## Project structure:

Tests input placed under **src.cfg.cft_tests** in the json files which resides there. 

The agent code resides under **src.clients.fastapi** folder.
Other code which support the api request within the FastAPI agent resides under **src.clients.clients_utils**

Logs are printed to the console and also being saved to **logs** folder under the project's root.
if no logs folder, it is created during execution.

## Before running the tests:
  - clone it from Github to your local environment.
  - Create a Python virtual environment and activate it (instruction can be found later in the text below)
  - upgrade the pip package by: **python -m pip install --upgrade pip**
  - install setup.py by: **python -m install .** (include the dot at the end) - see elaboration below.

## install setup.py 
    The setup.py file is placed at the root of the Python project directory. It primarily serves two purposes:
    - It includes choices and metadata about the program, such as the package name, version, author, license, 
    minimal dependencies, entry points, data files, and so on.
    - Secondly, it serves as the command line interface via which packaging commands may be executed.

## To run the tests via pytest (for both Windows and Linux)
- First, install the setup.py as mentions before 
- To run the test via cli, while being in the project's root tree, type (and virtualenv is activated):
  **python -m pytests**
 

# To create a virtualenv (and activate it):
## On Windows:
* create a virtualenv
- **c:\path\to\python -m venv c:\path\to\myenv\venv**
- or while residing in the root of the Python project directory (assuming python.exe is callable):
  **python -m venv .\venv**
 * activate the virtualenv
 While residing in the root of the Python project directory:
 **.\venv\Scripts\Activate.ps1**
      
## on Linux (Debian - Ubuntu)
* update your Ubuntu environment first:
**apt-get update** ( you may add this flag:   --fix-missing  if problem is consist).
* install virtuenv package
**sudo apt install python3-venv**
* create the virtualenv
**/usr/bin/python3 -m venv /path/to/root/of/project/venv**
i.e., **python3 -m venv /mnt/d/Finubit/venv**
## To activate virtual env (Linux)
While residing in the root of the Python project directory:
**source venv/bin/activate**

## To exit virtual env (for both Linux and Windows)
type: deactivate

