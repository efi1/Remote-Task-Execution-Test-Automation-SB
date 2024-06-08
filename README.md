
# F_Home_Assignment

This assignment includes an automation infrastructure (written in Pyhon) for assuring the quality of the TASKS app which resides on a web server .
The automation infrastructure based in an **api** client - **HandleRequest** and **DB** clients (**DbUtils** and **DataBaseClient**), which responsible for handling
 the DB activities.

 The **DataBaseClient** is responsible for inserted, updating and quering the DB. 
 It is required in for testing a PUT and GET response of a certain task (with a **task_id**).
 All API requests are saved within the DB in **TASK** table and contains the payload data as inserted or updated its records.
 The **DbUtils** DB client is responsible for pre insertion (a single task record and for the tearDown as later described here.)

 The API client (HandleRequest) is responsible for handling these http requests; POST, PUT and GET.
 -- POST - insert a new task.
 -- PUT - update an exist task.
 -- GET - retrieve an exist task.

Handling the various requests has two phases:
-- validating the request and return the relevant status upon the request results.
-- execute the request if validation ends successfully and return the relevant status.

  The two main functions within the **HandleRequest** which responsiblr for the handling requests are:
  -- validate_data - validating
  -- get_request_data - generate the DB query to be use on the various requests, as well as the request's payload data (include the task_id) to be compare later on with the actual DB response.
  - The generated DB queries, are being used at the test's file itself - test_api_requests.py - which resides under src.tests.
 - All project's code, tests, configuration files resides under src folder.

The framework for executing the tests is **pytest**.
Thus, the project has a **conftest** file (src.tests) which contains this majour activities:
- Instantiate the DbUtils (db) client - session level.
- TearDown (at the end of the tests - on the session level - means when all tests are finished to execute.
-- TearDown is responsible to truncate all recordes within the TASK table.
- Instantiate the API client, with all its required args - on function level - means it is re-instantiated before each test starts.
- Tests are parameterized (using pytest framework). all test's parameters (args) are also passed (at conftest) to the API client when it is instantiated.

- The tests - test_api_requests.py (src.tests) - are parameterized.
Parameters are shown above each test, with keywords that help the user understand the test's input.
- Other input resides in files unser src.tests.cfg_tests.
Each of these files has all other data which relevant for the test.
- The two majour data are the requests data ("Headers", "Payloads") and the data query which required for quering the DB TASK table.
- The tests uses thes data to validate the request, execute it against the DB and finally to compare the request's data (as being given in the file) to the DB query response.

- all tests are planed to pass successfully, whether the request response ended with success or an error.
Each test compares the expected data (also if planed to be failed) to the actual request's response.

- The project has a settings file which contains all requires data for the tests to get executes;
folders location, file names, DB query file names, respose messages, etc.

- The request's response is an object which contains theses fields: code, status, data and message.

## Project structure:
    - Clients resides under **src.client** (under api and db folders).
    - sql queries, table's data which is needed for the clients is resides under **src.data.db_queries**.
    - running **log** is created under src folder when running the test. 
    - tests and tests' configuration files (conftest.py, settings.py) are resides under **src.tests** folder.
    - **settings.py** include all reqired parameters which are needed for the project and for its
    - test's data resides ynder **src.tests.cfg_test** folder.


## Before running the test:
  - clone it from Github to your local environment.
  - Create a Python virtual environment.
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
    
# install setup.py 
The setup.py file is placed at the root of the Python project directory. It primarily serves two purposes:
- It includes choices and metadata about the program, such as the package name, version, author, license, minimal dependencies, entry points, data files, and so on.
- Secondly, it serves as the command line interface via which packaging commands may be executed.

- **pre install**
-  Activate the virtualenv
- upgrade pip current version:
  python -m pip install --upgrade pip
  
- **to install (the setup)**
  - Activate the virtualenv
  - Under the root of the Python project directory via cli run this:
    "**python -m pip install .**" (include the dot at the end)

## To run the tests via pytest (for both Windows and Linux)
- First, install the setup.py as mentions before 
- To run the test via cli, while being in the 'src' folder, type (and virtualenv is activated):
**python -m pytests**
      
  
