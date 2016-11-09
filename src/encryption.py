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
from logger import Logger


class Encryption:
    """This module uses pycrypto for encryption"""

    def __init__(self):
        pass

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

    def generate_keypair(self, bits=4096, v=True):
        if v is not False:
            self.logger.info("Generating new %d-bits key pair ..." % bits)
        t1 = time.time()
        self.public_key, self.private_key = rsa.newkeys(bits, poolsize=self.cpu_count)
        t2 = time.time()
        if v is not False:
            self.logger.info("Key pair generation took {0} seconds.".format(t2-t1))
        return True

    def encrypt_message(self, message, v=True):
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

    def decrypt_message(self, cipher, v=True):
        if v is not False:
            self.logger.info("Decrypting cipher ...")
        s1 = time.time()
        decrypto = rsa.decrypt(cipher, self.private_key)
        s2 = time.time()
        if v is not False:
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

