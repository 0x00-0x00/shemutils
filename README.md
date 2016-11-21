# shemutils - python multi-task library 
## About
    This library is designed to ease the code and support quick and 
    flexible programming of your own applications.
 
-----
## Modules


### __Logger__
-----
#### *About*
Module to work on logging information from your programs.
- Color support
- Success, error, information and debug template logging messages
- Option to store logging messages into files

#### *Usage*

To create a logger:

`from shemutils.logger import Logger`
`logger = Logger("Program A")`


To log a debug message:

`logger.debug("Debug Message")`
`01:08:15 [Program A] DEBUG: [#] Debug Message`

    
To log a information message:

`>>> logger.info("Program has started.")`
`01:09:36 [Program A] INFO: [*] Program has started.`

    And there is much more methods for you to explore, like:
    logger.error, logger.step_ok, logger.step_fail, logger.critical.

### __Database__
-----
#### *About*
Module to operate efficiently with sqlite3 databases. 
Keep it simple pythonic functions to work quickly with data storage.

There are two structures to understand to effectively use this module.
The Database() and Table() objects.

#### Database
The database object is the core of the module, it is open in the __init__ function and have control only to save data and close itself.
Have one controller object attached to itself, as a rule.

    Methods:
    save() -> save the changes made to the database.
    close() -> closes the database 

#### Controller
The executioner of queries! Oh mighty, Controller.
Without this object, it`s creator - the Database - should never be able to modify itself with data.
It's responsible for the data flow in and out of the database.
    
    Methods:
    execute(QUERY) -> to execute a query
    get() -> to get the result from the last query executed (this is only for SELECT statements)


#### Table
This objects returns strings, more specifically SQL queries strings, to fuel the controller queue with operations.

    Methods:
    create() -> return a string with formatted CREATE TABLE statement
    insert_data([args*]) -> return a string with formatted INSERT INTO statement
    search(args) -> return a string with formatted SELECT statement
    update_row(args) -> return a string with formatted UPDATE statement
    remove_row(args) -> return a string with formatted DELETE FROM statement
    
    **args are placeholder for actual arguments of each function.
    
#### *Usage*


To create a database named "SimpleDatabase.db" in your local script folder:

`from shemutils.database import *`

`db = Database("SimpleDatabase")`


To create a table CONTACTS with 3 columns (Name Char, Age Int, Sex Char):

`t1 = Table("CONTACTS", 
    {"Name": TEXT,
    "Age": INTEGER,
    "Sex": TEXT})`

`db.controller.execute(t1.create())`

`db.save()`


To insert data into it:

`insertion_query = t1.insert_data(["Bob", 35, "Male"])`

`db.controller.execute(insertion_query)`

`db.save()`


To search data inside:

`search = raw_input("Type a name to search: ")`

`search_query = t1.search("Name", "Bob")`

`db.controller.execute(search_query)`

`results = db.controller.get()`

-----

### Encryption
-----

## Requirements
>> gevent
>> pycrypto
>> getpass
>> rsa


