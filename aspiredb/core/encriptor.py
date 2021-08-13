# core/encriptor.py

#----------------------------- Data Security Service ----------------------------------
from base64 import b64decode, b64encode
from cryptography.fernet import Fernet as fn
import asyncio 
import sys


class Key:
    key_holster: str = None

    def __init__(self) -> None:
        self.load_key()
    
    @property
    def get_key(self): 
        return self.key_holster.encode()

    def load_key(self):
        ''' '''
        import subprocess
        import uuid  

        current_machine_id = subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()
        self.key_holster = str(uuid.UUID(int=uuid.getnode())).split('-')[-1] + current_machine_id

    @property
    async def generate_hash_key(self):
        key = fn.generate_key()
        hash_key = fn(key)                
        return key
        
    @property
    async def generate_password_hash_key(self):
        self.load_key()

        from base64 import urlsafe_b64encode        
        from cryptography.hazmat.backends import default_backend
        from cryptography.hazmat.primitives.hashes import SHA256
        from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
        
        password = self.get_key # Convert to type bytes
        salt = b'salt_' # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
        kdf = PBKDF2HMAC(
            algorithm=SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = urlsafe_b64encode(kdf.derive(password)) # Can only use kdf once
        return key    


import PySimpleGUI as sg   

class Gui:

    def set_message(self, message):
        self.input_message = message

    def gui_window(self):

        
        # Define the window's contents
        layout = [  [sg.Text("Message to Encrypt?")],     # Part 2 - The Layout
                    [sg.Input()],
                    [sg.Button('Ok')] ]

        # Create the window
        window = sg.Window('Window Title', layout)      # Part 3 - Window Defintion
                                                        
        # Display and interact with the Window
        event, values = window.read()                   # Part 4 - Event loop or Window.read call

        # Do something with the information gathered
        self.set_message(values[0])
        #print('Hello', values[0], "! Thanks for trying PySimpleGUI")

        # Finish up by removing from the screen
        window.close() 


class EncryptMessage( Key, Gui ):

    ciphers:list = []    
    key_file_name:str = 'enc_key.key'

    def __init__(self):
        self.load_key()

    async def encrypt_message(self): 
        ''' For backend storage and for encrypting messages on this machine only'''  
        self.gui_window()     
        key = await self.generate_password_hash_key
        f = fn(key)
        await asyncio.sleep(0.005)
        ds = self.input_message
        print('ds', ds, type(ds.encode()))
        encrypted = f.encrypt(ds.encode('utf-8'))        
        sys.stdout.write(encrypted.decode('utf-8'))
        return encrypted

    async def decrypt_message(self, encrypted_message):
        ''' For decrypting messages that was encrypted on this machine only'''            
        key = await self.generate_password_hash_key
        f = fn(key)
        await asyncio.sleep(0.005)
        decrypted = f.decrypt(encrypted_message)
        
        sys.stdout.write(decrypted.decode())
        return decrypted 

    async def encrypt_net_message(self, message): 
        ''' For backend storage and for encrypting messages on this machine only'''       
        key = await self.generate_hash_key
        f = fn(key)
        await asyncio.sleep(0.005)
        encrypted = f.encrypt(message.encode()) 
        payload = key.decode() + "/" + encrypted.decode()
        print(payload)          
        
        return payload

    async def decrypt_net_message(self, encrypted_message):
        ''' For decrypting messages that was encrypted on this machine only'''
        data =  encrypted_message.split('/')           
        key = data[0].encode()
        f = fn(key)
        await asyncio.sleep(0.005)
        decrypted = f.decrypt(data[1].encode())        
        sys.stdout.write(decrypted.decode())
        return decrypted 



secret = "\nI Have court at 10 today\n"
async def main():
    k = EncryptMessage() 
    #key_ = await k.generate_hash_key   
    #sys.stdout.write(key_.decode('utf-8'))
    enc = await k.encrypt_message()
    #sys.stdout.write(enc)
    dec = await k.decrypt_net_message(enc)
    #sys.stdout.write(dec)

asyncio.run(main())

class EncryptFile (Key):

    async def encrypt_file(self, input_file, outfile_name:str = None):

        key = await self.generate_password_hash_key # Use one of the methods to get a key (it must be the same when decrypting)
        input_file = input_file
        output_file = outfile_name

        with open(input_file, 'rb') as f:
            data = f.read()

        fernet = fn(key)
        encrypted = fernet.encrypt(data)

        with open(output_file, 'wb') as f:
            f.write(encrypted)

        # You can delete input_file if you want
        del(input_file)

    async def decrypt_file(self, input_file, outfile_name:str = None):
        
        key = await self.generate_password_hash_key # Use one of the methods to get a key (it must be the same as used in encrypting)
        input_file = input_file
        output_file = outfile_name

        with open(input_file, 'rb') as f:
            data = f.read()

        fernet = fn(key)
        decrypted = fernet.decrypt(data)

        with open(output_file, 'wb') as f:
            f.write(decrypted)

gui = Gui()
gui.gui_window()