# shemutils - python multi-task library 
## About
    This library is designed to ease the code and support quick and 
    flexible programming of your own applications.

-----
## Requirements
1. [gevent](https://github.com/gevent/gevent) 
2. pycrypto
3. rsa
 
-----
## Module Index
* [Logger](#logger-module)
* [Database](#database-module)
* [Encryption](#encryption-module)
* [Checksum](#checksum-module)


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
>>> from shemutils.logger import Logger
>>> logger = Logger("Program A")
```

To log a debug message:
```python
>>> logger.debug("Debug Message")
'01:08:15 [Program A] DEBUG: [#] Debug Message'
```

    
To log a information message:
```python
>>> logger.info("Program has started.")
'01:09:36 [Program A] INFO: [*] Program has started.'
```


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
>>> t1 = Table("CONTACTS", 
        {
        1: ('NAME', TEXT),
        2: ('AGE', INTEGER),
        3: ('SEX', TEXT)
        })  # this creates the object and fill it with data
>>> t1  # The object is created but not yet in the database.
<shemutils.database.Table object at 0x7f112168df90>
>>> t1.create()  # Table methods always returns SQL statements.
'CREATE TABLE IF NOT EXISTS CONTACTS (id INTEGER PRIMARY KEY AUTOINCREMENT, NAME TEXT, AGE INTEGER, SEX TEXT)'
>>> db.controller.execute(t1.create())  # You need to pass them into the controller to execute them.
>>> db.save()  # Then save changes.
```

To insert data into it:
```python
>>> insertion_query = t1.insert_data(["Bob", 35, "Male"])
>>> db.controller.execute(insertion_query)
>>> db.save()
```


To search data inside:
```python
>>> search_name = raw_input("Type a name to search: ")
>>> search_query = t1.search("NAME", search_name)  # column, then keyword for search
>>> db.controller.execute(search_query)  # SELECT queries returns results, the controller automatically sends them to the Queue
>>> results = db.controller.get()  # get() method gets the top element of the controller queue.
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
##### Encryption (AES)
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
>>> k.get(encoded=True)  # to return a base64 encoded key
'kQ60rSGUiagF3UHoUtcTH73eVrWQYr1YAoD5XJagSRs='
```

##### Key storage
```python
>>> from shemutils.encryption import RSA  # 
>>> rsa = RSA()
>>> rsa.generate_keypair()  # returns a boolean if key generation was successfull
'11:29:16 [RSA] INFO: [*] Generating new 4096-bits key pair ...'
'11:29:36 [RSA] INFO: [*] Key pair generation took 19.4212200642 seconds.'
True
>>> rsa.save_keys()  # this will save the keys to your local script folder
>>> rsa.save_keys(pubf="/root/.pub.key", privf="/root/.priv.key")  # this will save to another folder

>>> rsa.load_keys(pubf="/root/.pub.key", privf="/root/.priv.key")  # this loads the saved keys.
```


##### Encryption
To encrypt a file using AES (and use an alternative method for generating a key)
```python
>>> from shemutils.encryption import Encryption  # import Encryption class

>>> key = Encryption.get_key()  # This will ask a secret from the user, and generate it as a key;
>>> key
'\x984\x87m\xcf\xb0\\\xb1g\xa5\xc2IS\xeb\xa5\x8cJ\xc8\x9b\x1a\xdfW\xf2\x8f/\x9d\t\xaf\x10~\xe8\xf0'

>>> iv = Encryption.create_iv()  # AES uses initialization vector to encryption. If you dont know what is this, google it. It it easy.
>>> iv
'\x93Ug\xc8\xe4\xf8\xbe\xfd\x81\xaa\xdf\xf3\xc3\x12\xa1\xfb'

>>> file = "test.txt"  # example file
>>> e = Encryption.encrypt_file(file, key, iv)  # This function encrypt the file 'test.txt' and returns a boolean about success;
>>> e
True
```

To encrypt a message using RSA is easy too, follow the snippet:
```python
>>> from shemutils.encryption import RSA  # 
>>> rsa = RSA()
>>> rsa.generate_keypair()  # returns a boolean if key generation was successfull
'11:29:16 [RSA] INFO: [*] Generating new 4096-bits key pair ...'
'11:29:36 [RSA] INFO: [*] Key pair generation took 19.4212200642 seconds.'
True
>>> message = "This is a secret."
>>> rsa.encrypt_message(message)
'11:34:49 [RSA] INFO: [*] Encrypting message ...'
'11:34:49 [RSA] INFO: [*] Encryption success.'
'11:34:49 [RSA] INFO: [*] Procedure took 0.00257611274719 seconds.'
'\xa6\x8e\xcbh\xd7V\xd41~N\xc6z\x86\xbc\x0457h\xff\xb3\x0cE\xc8~7\x9b\xe81\x0e\xd2OV\x06\xd4\xe0\x8a\xa1IU\x80\n5\xe9T\xdcY\x02\xeef\xdf\xf1\xd0\xf1>\x1b\xff\xeeR\x90B\xdfU(\x8b\xd4)\xc5DM\xb7\xad\r\xb4\xbf\xbf\xc1\xaa\xb1\xc0v\x15\x9a\xa4b\xc7Uq\xcb\xec\x83Y\xe6\xbb\x87\xeb\x86\x07\xeb\xe8\xc4\x8f\xab\xedx5\x15\x81\x0c\x96\xed\xfcBE\x1cb\x8f\x0f\xbf\xd3\xa3n\x08\xee\xd6,)\x82\x92\x1b\xb9\x8d\xff\xb6\\)RdO"\xa4\xf8\x9e\x02\x8a\xceL\xa4\xc6\xad\\\x18_\x8c\x1f\x80\xba\xf4\x1eKd\x99\x9a\xfb\xc9\x14\xec_)Ov\xc4n\xa3\xb0\x0e\xef\xf0\xf5\x15\n:}\xcc\xd4\xaa\xf0H\xdd\x1e\xbeB5\xac\xe9I\xd6\xb2\r*\x95\x80\xc3\x9d\x0b\xf7*\r\x90\x8f\x17D;N\xc4\\\xe3\x06\xca\x8c\x1ac\xe7\re\x05uV\xc7@@\x17[d\x16bm\x1f\xe6`KH ({\x16\xe0\xb2\x11\x9d\xb8i\x11_\xed\x80\x99\x08b\xfbQU\xd3\xdb]q\x17\xe7\xa6a\xfd^\x16o=\x96\x96O\xb3\xcc\x15\xac\x96\xf2)\xc6\xf1\xb77Sk\x8a\xcf#F\x12BW\x83<\xe9\xb8\xac\xc8z\xe7\xa1-Q\xc3x\xb0\xce\xb6\xda\x9c\x9aene\x0b\xe5v7+\xab\x01\x89LH\x93\xb4-\xb5z/Q\xad\xa9\xa7\xe1]\xd9J\xb8\xcdx\xa8\x9d\xc7 \xff\x1a\xe1\xe2\xd6\x04a\x0bI\xad\x9e]\xf0\x9f\x7f\xb9\x07D\xe5"M\xd3\n\x172\xa6n\xc7\xbc\x10\x93:7\x0b\x12\xe2\x9a\xeaG\n`\xe2s9\xdb\xdf\x965\x8d\xd2,~\xf7\xc66\x97\xf5\xabb*\x06\x98\xba\x89f0-\xba\xdb\x9b\x1b\x12\xfaa\x11\xd6\r]^4\x9ax\x00d\'\xb0d\xf2\x9d\x7f\xb3PC\xe1\xc6\xcbI\xea-\xeb\xb75\xd7\x81\xef\xbc\xb4\xb9\x9b\xf2\n\xbfj\x91o\x82\xcc\xf1\xff\x92\x14\'\'\x08\xf8\x94\xff\x14\xf2\xb0\x8f\xc5\xc5\x85\x15[\xd4\x13\n\xba\xa8\xc5]R\xcao\x08r&\x18+R{\xb6\x95\xc5"XxHO\xda'
```


-----
### __Checksum Module__
-----
#### About
#### Usage
-----



