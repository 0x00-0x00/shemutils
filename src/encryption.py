import os
import time
import random
import hashlib
import getpass
import sys
import struct
import rsa
import multiprocessing
from Crypto.Cipher import AES
from shemutils.logger import Logger


class Key(object):
    """
    Class Key written by shemhazai
    This method generates a random key, unencoded or encoded in base64.
    """
    def __init__(self, bits):
        self.key_size = bits
        if self._parse_bits() != 0:
            self.key = None
        else:
            self.key = self._generate_key()

    def _parse_bits(self):
        """Parse if the input int is divisible by 2"""
        if self.key_size % 2 != 0:
            return -1
        return 0

    def _generate_key(self):
        """Generate random bytes and join them into a single string"""
        return ''.join(chr(random.randint(0, 0xFF)) for i in range(self.key_size))

    def get(self, encoded=False):
        """
        Method for returning the generated key
        :param encoded: Boolean
        :return: key string
        """
        if encoded is True:
            return base64.b64encode(self.key)

        return self.key


class Encryption:
    """This module uses pycrypto for AES encryption"""

    def __init__(self):
        pass

    @staticmethod
    def create_iv():
        iv = os.urandom(16)
        return iv

    @staticmethod
    def hash256(string):
        if type(string) is str:
            return hashlib.sha256(string.encode()).digest()
        else:
            return hashlib.sha256(string).digest()

    @staticmethod
    def hash512(string):
        if type(string) is str:
            return hashlib.sha512(string.encode()).digest()
        else:
            return hashlib.sha512(string).digest()

    @staticmethod
    def hashmd5(string):
        if type(string) is str:
            return hashlib.md5(string.encode()).digest()
        else:
            return hashlib.md5(string).digest()

    @staticmethod
    def get_key(bits=256):
        sys.stderr.write("Bit-size selected: %d\n" % bits)
        k = str()
        c = str("c")
        while k != c:
            if k == c:
                break
            k = getpass.getpass("Type your key: ", sys.stderr)
            c = getpass.getpass("Confirm your key: ", sys.stderr)
        if bits == 256:
            sys.stderr.write("Generating 256-bit key ...\n")
            return Encryption.hash256(k)
        elif bits == 128:
            sys.stderr.write("Generating 128-bit key ...\n")
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
                        chunk += " ".encode() * (16 - len(chunk) % 16)
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
        """
        Function to encrypt a plaintext message.
        Also checks if IV length is correct.
        """
        psize = sys.getsizeof(plaintext)
        if len(iv) != 16:
            return "Error: Invalid IV size."
        encryptor = AES.new(key, AES.MODE_CBC, iv)
        cipher = bytes()
        cipher += struct.pack("<Q", psize)
        cipher += iv
        for chunk in Encryption.split_string(plaintext):
            cipher += encryptor.encrypt(chunk)
        return cipher

    @staticmethod
    def decrypt_message(cipher, key):
        """
        Function to decrypt data from input.
        Also checks if IV length is correct.
        """
        iv = cipher[struct.calcsize("Q"):struct.calcsize("3Q")]
        if len(iv) != 16:
            return "Error: Invalid IV size."
        decryptor = AES.new(key, AES.MODE_CBC, iv)
        plaintext = str()
        for chunk in Encryption.split_string(cipher[struct.calcsize("3Q"):]):
            plaintext += decryptor.decrypt(chunk).decode()
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

    def generate_keypair(self, bits=4096, v=True):
        if v is not False:
            self.logger.info("Generating new %d-bits key pair ..." % bits)
        t1 = time.time()
        self.public_key, self.private_key = rsa.newkeys(bits, poolsize=self.cpu_count)
        t2 = time.time()
        if v is not False:
            self.logger.info("Key pair generation took {0} seconds.".format(t2-t1))
        return True

    def encrypt_message(self, message, v=False):
        """

        :param message: string
        :param v: boolean  # stands for verbose
        :return:
        """
        if v is not False:
            self.logger.info("Encrypting message ...")
        s1 = time.time()
        crypto = rsa.encrypt(message, self.public_key)
        s2 = time.time()
        if v is not False:
            self.logger.info("Encryption success.")
            self.logger.info("Procedure took {0} seconds.".format(s2-s1))
        return crypto

    def decrypt_message(self, cipher, v=False):
        if v is not False:
            self.logger.info("Decrypting cipher ...")
        s1 = time.time()
        decrypto = rsa.decrypt(cipher, self.private_key)
        s2 = time.time()
        if v is not False:
            self.logger.info("Decryption success.")
            self.logger.info("Procedure took %d seconds." % (s2 - s1))
        return decrypto

    def save_keys(self, priv_f="private_key.pem",  pub_f="public_key.pem", v=False):
        if self.public_key is None:
            self.logger.error("Public Key does not exists. Generate it.")
            return False
        if self.private_key is None:
            self.logger.error("Private Key does not exists. Generate it.")
            return False
        with open(priv_f, "w") as priv:
            priv.write(self.private_key.save_pkcs1().decode())
            self.logger.info("Private key saved to file '%s'" % priv_f)
        with open(pub_f, "w") as pub:
            pub.write(self.public_key.save_pkcs1().decode())
            if v is True:
                self.logger.info("Public key saved to file '%s" % pub_f)
        return True

    def load_keys(self, priv_f, pub_f, v=False):
        if not os.path.isfile(priv_f):
            self.logger.error("Private key file does not exists.")
        if not os.path.isfile(pub_f):
            self.logger.error("Public key file does not exists.")
        with open(priv_f, "rb") as priv:
            priv_data = priv.read()
        with open(pub_f, "rb") as pub:
            pub_data = pub.read()
        self.private_key = rsa.PrivateKey.load_pkcs1(priv_data)
        self.public_key = rsa.PublicKey.load_pkcs1(pub_data)
        if v is True:
            self.logger.info("Key pair successfully loaded.")
        return True

