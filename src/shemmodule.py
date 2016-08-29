import os
import subprocess
import time
import logging
import random
import hashlib
import getpass
import sys
import struct
import rsa
import multiprocessing
from Crypto.Cipher import AES

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def green(message):
    return bcolors.OKGREEN + message + bcolors.ENDC


def blue(message):
    return bcolors.OKBLUE + message + bcolors.ENDC


def yellow(message):
    return bcolors.WARNING + message + bcolors.ENDC


def red(message):
    return bcolors.FAIL + message + bcolors.ENDC


def bold(message):
    return bcolors.BOLD + message + bcolors.ENDC


def underline(message):
    return bcolors.UNDERLINE + message + bcolors.ENDC


def importationerror(module):
    print "ShemUtils Error: You need to install %s module to use this library." % module
    return


class Persistence:
    """Module written by shemhazai to search for nice spots to hide files on windows system's"""

    def __init__(self):
        self.logger     = Logger("Persistence")

    def _check_os(self):
        return True if os.name == 'nt' else False

    def _check_folder_perm(self, folder):
        """
        We will check permissions from argument folder and return a triple tuple, with write, read and exe-
        cute permissions in boolean representation.
        """
        return map(lambda x: True if os.access(folder, x) else False, [os.W_OK, os.R_OK, os.X_OK])

    def get_logicaldisk(self):
        """Combination of _get_wmic and _check_folder_perm yielding its results. """
        get = self._get_wmic()
        return [get, [self._check_folder_perm(x) for x in get]]

    def _get_wmic(self, x=0, timeout=10):
        """
        We will use wmic to get information about disks, but if never used, wmic needs to install itself.
        So, for that, we open one instance of wmic and give it time to install itself.
        Then, we open another one instance, effectively gathering all our needed information.

        The default timeout for gathering information is 10 seconds. If the system takes too much time
        the operation will be aborted.
        """

        '# Just to ensure the wmic is installed. '
        self.logger.info("Just ensuring wmic is intalled ...")
        proc = subprocess.Popen("wmic /?", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(timeout)
        proc.terminate()

        '# Now the real magic happens'
        self.logger.info("Trying to get logical disk information ...")
        proc = subprocess.Popen("wmic logicaldisk get caption", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while proc.poll() is not 0:
            time.sleep(1)
            x += 1
            if x > (timeout - 1):
                self.logger.error("Timeout occurred trying to get logical disk caption.")
                proc.terminate()
                return False

        proc.terminate()
        return self._parse_wmic_data(proc.communicate()[0])

    def _parse_wmic_data(self, data):
        return filter(lambda x: ":" in x, [str(x).replace(" ", "") for x in data.split("\r\r\n")])


class Logger:
    def __init__(self, logger_name):
        """Logging module wrapper to easily encapsulate code for re-use in my own projects."""
        self.logger_name = logger_name
        self.operational_system = os.name
        self.color_flag = self.set_color_flag()
        self.loggerHandle = self._create_logger()
        self.consoleHandle = self._create_console()
        self.formatter = self._create_formatter()
        self.define_logger_level([self.loggerHandle, self.consoleHandle])
        self.consoleHandle.setFormatter(self.formatter)
        self.loggerHandle.addHandler(self.consoleHandle)

    def set_color_flag(self):
        return True if self.operational_system == "posix" else False

    def define_logger_level(self, objs):
        return [self._setLevel(x) for x in objs]

    def _create_logger(self):
        return logging.getLogger(self.logger_name)

    def _create_console(self):
        return logging.StreamHandler()

    def _create_formatter(self):
        return logging.Formatter("%(asctime)s %(levelname)s - %(message)s","%Y-%m-%d %H:%M:%S")

    def _setLevel(self, loggerObj, level=logging.DEBUG):
        return loggerObj.setLevel(level)

    def info(self, string):
        if self.color_flag:
            self.loggerHandle.info(blue("[*] ") + string)
        else:
            self.loggerHandle.info(string)
        return

    def debug(self, string):
        if self.color_flag:
            self.loggerHandle.debug(yellow("[#] ") + string)
        else:
            self.loggerHandle.debug(string)
        return

    def warning(self, string):
        if self.color_flag:
            self.loggerHandle.warning(yellow("[!] ") + string)
        else:
            self.loggerHandle.warning(string)
        return

    def error(self, string):
        if self.color_flag:
            self.loggerHandle.error(red("[@] ") + string)
        else:
            self.loggerHandle.error(string)
        return

    def critical(self, string):
        if self.color_flag:
            self.loggerHandle.critical(red("[!!] ") + string)
        else:
            self.loggerHandle.critical(string)
        return


class Encryption:
    """This module uses pycrypto for encryption"""

    def __init__(self):
        print "Initializing encryption module ..."
     
    @staticmethod
    def create_iv():
        return ''.join(chr(random.randint(0, 0xFF)) for i in range(16))

    @staticmethod
    def hash256(string):
        return hashlib.sha256(string).digest()

    @staticmethod
    def hash512(string):
        return hashlib.sha512(string).digest()

    @staticmethod
    def hashmd5(string):
        return hashlib.md5(string).digest()

    @staticmethod
    def get_key(bits=256):
        print "Bit-size selected: %d" % bits
        k = str()
        c = str("c")
        while k != c:
            if k == c:
                break
            k = getpass.getpass("Type your key: ")
            c = getpass.getpass("Confirm your key: ")
        if bits == 256:
            print "Generating 256-bit key ..."
            return Encryption.hash256(k)
        elif bits == 128:
            print "Generating 128-bit key ..."
            return Encryption.hashmd5(k)

    @staticmethod
    def encrypt_file(file_name, key, iv, output=None, chunksize=64*1024):
        if not output:
            dire_name = os.path.dirname(file_name)
            base_name = os.path.basename(file_name)
            if dire_name != "":
                output = dire_name + os.sep + base_name + ".enc"
            else:
                output = base_name + ".enc"
        filesize = os.path.getsize(file_name)
        encryptor = AES.new(key, AES.MODE_CBC, iv)
        with open(file_name, "rb") as infile:
            with open(output, "wb") as outfile:
                outfile.write(struct.pack("<Q", filesize))
                outfile.write(iv)
                while True:
                    chunk = infile.read(chunksize)
                    if len(chunk) == 0:
                        break
                    elif len(chunk) % 16 != 0:
                        chunk += " " * (16 - len(chunk) % 16)
                    outfile.write(encryptor.encrypt(chunk))
        return True

    @staticmethod
    def decrypt_file(file_name, key, output=None, chunksize=64*1024):
        if not output:
            root_name, ext = os.path.splitext(file_name)
            if ext != ".enc":
                return False
            dir_name = os.path.dirname(root_name) + os.sep
            f_name = os.path.basename(root_name)
            if dir_name != "/":
                output = dir_name + f_name
            else:
                output = f_name
        with open(file_name, "rb") as infile:
            origsize = struct.unpack("<Q", infile.read(struct.calcsize('Q')))[0]
            iv = infile.read(16)
            decryptor = AES.new(key, AES.MODE_CBC, iv)
            with open(output, "wb") as outfile:
                while True:
                    chunk = infile.read(chunksize)
                    if len(chunk) == 0:
                        break
                    outfile.write(decryptor.decrypt(chunk))
                outfile.truncate(origsize)
        return True

    @staticmethod
    def get_chunk(msg, index, chunksize=16):
        return msg[index:index+chunksize]

    @staticmethod
    def split_string(string, chunksize=16):
        output = []
        for x in range(0, len(string), chunksize):
            part = Encryption.get_chunk(string, x, chunksize=chunksize)
            if len(part) % 16 != 0:
                part += " " * (16 - len(part) % 16)
            output.append(part)
        return output

    @staticmethod
    def encrypt_message(plaintext, key, iv):
        psize = sys.getsizeof(plaintext)
        encryptor = AES.new(key, AES.MODE_CBC, iv)
        cipher = str()
        cipher += struct.pack("<Q", psize)
        cipher += iv
        for chunk in Encryption.split_string(plaintext):
            cipher += encryptor.encrypt(chunk)
        return cipher

    @staticmethod
    def decrypt_message(cipher, key):
        iv = cipher[struct.calcsize("Q"):struct.calcsize("3Q")]
        decryptor = AES.new(key, AES.MODE_CBC, iv)
        plaintext = str()
        for chunk in Encryption.split_string(cipher[struct.calcsize("3Q"):]):
            plaintext += decryptor.decrypt(chunk)
        return plaintext


class RSA:
    """This class have dependencies.
    multiprocessing, rsa modules are needed.
    """
    def __init__(self):
        self.logger = Logger("RSA")
        self.public_key = None
        self.private_key = None
        self.cpu_count = multiprocessing.cpu_count()

    def generate_keypair(self, bits=4096):
        self.logger.info("Generating new %d-bits key pair ..." % bits)
        self.public_key, self.private_key = rsa.newkeys(bits, poolsize=self.cpu_count)
        return True

    def encrypt_message(self, message):
        self.logger.info("Encrypting message ...")
        s1 = time.time()
        crypto = rsa.encrypt(message, self.public_key)
        s2 = time.time()
        self.logger.info("Encryption success.")
        self.logger.info("Procedure took %d seconds." % (s2 - s1))
        return crypto

    def encrypt_message2(self, message, k):
        """
        This method should be preferred over its precessor because it gives opportunity to choose each key
        you want to use to encrypt.
        """
        self.logger.info("Encrypting message ...")
        s1 = time.time()
        if k == 1:
            crypto = rsa.encrypt(message, self.private_key)
        else:
            crypto = rsa.encrypt(message, self.public_key)
        s2 = time.time()
        self.logger.info("Encryption success.")
        self.logger.info("Procedure took %d seconds." % (s2 - s1))
        return crypto

    def decrypt_message(self, cipher):
        self.logger.info("Decrypting cipher ...")
        s1 = time.time()
        decrypto = rsa.decrypt(cipher, self.private_key)
        s2 = time.time()
        self.logger.info("Decryption success.")
        self.logger.info("Procedure took %d seconds." % (s2 - s1))
        return decrypto

    def decrypt_message2(self, cipher, k):
        """
        This method should be preferred over its precessor because it gives opportunity to choose each key
        you want to use to decrypt.
        """
        self.logger.info("Decrypting cipher ...")
        s1 = time.time()
        if k == 1:
            decrypto = rsa.decrypt(cipher, self.private_key)
        else:
            decrypto = rsa.decrypt(cipher, self.public_key)
        s2 = time.time()
        self.logger.info("Decryption success.")
        self.logger.info("Procedure took %d seconds." % (s2 - s1))
        return decrypto

    def save_keys(self, priv_f="private_key.pem",  pub_f="public_key.pem"):
        if self.public_key is None:
            self.logger.error("Public Key does not exists. Generate it.")
            return False
        if self.private_key is None:
            self.logger.error("Private Key does not exists. Generate it.")
            return False
        with open(priv_f, "w") as priv:
            priv.write(self.private_key.save_pkcs1())
            self.logger.info("Private key saved to file '%s'" % priv_f)
        with open(pub_f, "w") as pub:
            pub.write(self.public_key.save_pkcs1())
            self.logger.info("Public key saved to file '%s" % pub_f)
        return True

    def load_keys(self, priv_f, pub_f):
        if not os.path.isfile(priv_f):
            self.logger.error("Private key file does not exists.")
        if not os.path.isfile(pub_f):
            self.logger.error("Public key file does not exists.")
        with open(priv_f, "rb") as priv:
            priv_data = priv.read()
            priv_data = priv_data.encode("ascii")
        with open(pub_f, "rb") as pub:
            pub_data = pub.read()
            pub_data = pub_data.encode("ascii")
        self.private_key = rsa.PrivateKey.load_pkcs1(priv_data)
        self.public_key = rsa.PublicKey.load_pkcs1(pub_data)
        self.logger.info("Key pair successfully loaded.")
        return True
