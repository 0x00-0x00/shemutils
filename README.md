# shemutils - python multi-task library 
## About
    This library is designed to ease the code and support quick and 
    flexible programming of your own applications.
 
-----
## Modules



### __Logger Module__
-----
#### *About*
Module to work on logging information from your programs.
+ Color support
+ Success, error, information and debug template logging messages
+ Option to store logging messages into files

##### Logger Object
Object to handle the logging to the screen and to file.

    Methods:
    info()          -> Display message with INFO tag to the screen
    error()         -> Display message with ERROR tag to the screen
    critical()      -> Display message with CRITICAL tag to the screen
    debug()         -> Display message with DEBUG tag to the screen
    step_ok()       -> Display SUCCESS message to a procedure step
    step_fail()     -> Display FAIL message to a procedure step

#### *Usage*
To create a logger:
```python
from shemutils.logger import Logger
logger = Logger("Program A")
```

To log a debug message:
```python
logger.debug("Debug Message")
```
01:08:15 [Program A] DEBUG: [#] Debug Message
    
To log a information message:
```python
logger.info("Program has started.")
```
01:09:36 [Program A] INFO: [*] Program has started.

    And there is much more methods for you to explore, like:
    logger.error, logger.step_ok, logger.step_fail, logger.critical.



-----
### __Database Module__
-----
#### *About*
Module to operate efficiently with sqlite3 databases. 
Keep it simple pythonic functions to work quickly with data storage.

There are two structures to understand to effectively use this module.
The Database() and Table() objects.

##### Database
The database object is the core of the module, it is open in the __init__ function and have control only to save data and close itself.
Have one controller object attached to itself, as a rule.

    Methods:
    save() -> save the changes made to the database.
    close() -> closes the database 

##### Controller
The executioner of queries! Oh mighty, Controller.
Without this object, it`s creator - the Database - should never be able to modify itself with data.
It's responsible for the data flow in and out of the database.
    
    Methods:
    execute(QUERY) -> to execute a query
    get() -> to get the result from the last query executed (this is only for SELECT statements)


##### Table
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
```python
from shemutils.database import *
db = Database("SimpleDatabase")
```

To create a table CONTACTS with 3 columns (Name Char, Age Int, Sex Char):
```python
t1 = Table("CONTACTS", 
    {"Name": TEXT,
    "Age": INTEGER,
    "Sex": TEXT})
db.controller.execute(t1.create())
db.save()
```

To insert data into it:
```python
insertion_query = t1.insert_data(["Bob", 35, "Male"])
db.controller.execute(insertion_query)
db.save()
```


To search data inside:
```python
search_name = raw_input("Type a name to search: ")
search_query = t1.search("Name", search_name)
db.controller.execute(search_query)
results = db.controller.get()
```


-----
### __Encryption Module__
-----
#### About
The Encryption module serves to quickly implement encryption to a certain degree to programs or scripts.
The module supports:
+ AES-128 or AES-256 encryption
+ RSA-4096 encryption
    + RSA Key save and load functions to re-use the key pair.
+ Random key generation
+ Message and file encryption

#### Classes
##### Encryptor
This class is all about AES encryption and key hashing. It supports both message and file encryption with have separate functions to each.
More information about usage in the Usage sector.

##### RSA
With a rather self-explaining name, RSA class stands for RSA encryption in this module. It only supports message encryption, as assymetric encryption suffers heavily from efficiency issues compared to the symmetric encryption. As it stands, it is still possible to encrypt a file with it, but in this module, I recommend as a good practice to use assymetric encryption to exchange symmetric key between peers of communication and then encrypt the data with it.
This class has the ability to save (store in file) and load keys, as generation can be lenghty to some lower potency CPU's.

##### Key
It is a simple class to generate pseudo-random keys, retrieving the key in byte or encoded form.

#### Usage
-----
##### Key generation
Here is the code snippet to generate a key
```python
>>> from shemutils.encryption import Key
>>> k = Key(32)  # 32 stands for key size in bytes. (32 * 8 = 256 bits)
>>> k.get()  # to return the non-encoded key
'\x91\x0e\xb4\xad!\x94\x89\xa8\x05\xddA\xe8R\xd7\x13\x1f\xbd\xdeV\xb5\x90b\xbdX\x02\x80\xf9\\\x96\xa0I\x1b' 
```

##### Encryption



-----
### __Checksum Module__
-----
#### About
#### Usage
-----



-----
## Requirements
1. gevent
2. pycrypto
3. getpass
4. rsa
-----


