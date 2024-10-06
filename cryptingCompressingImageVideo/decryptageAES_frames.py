import binascii
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import os
from tkinter import Tk, filedialog


def get_decryption_key_from_file():
    root = Tk()
    root.withdraw()

    key_file = filedialog.askopenfilename(title="Choisissez un fichier contenant la clé de déchiffrement (.txt)", filetypes=[("Text files", "*.txt")])

    if not key_file:  # Si l'utilisateur annule la sélection du fichier
        print("Aucun fichier sélectionné.")
        return None

    with open(key_file, 'r') as f:
        key = f.read().strip()  # Lire la clé depuis le fichier
    
    # Convertir la clé en bytes
    key_bytes = key.encode('utf-8')
    return key_bytes

def decrypt_images_in_folder(key):
    # Chemins des dossiers d'entrée et de sortie
    input_folder = "C:/Users/pc/Desktop/Test_Video/Cryptage_frames"
    output_folder = "C:/Users/pc/Desktop/Test_Video/Decryptage_frames"

    # Vecteur d'initialisation (doit être le même que celle utilisés pour le cryptage)
    iv = b'1234567890123456'
    
    #Decrypts all AES CBC encrypted BMP images in the input folder and saves them in the output folder.
    for filename in os.listdir(input_folder):
        if filename.endswith(".bmp"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, f"{filename}")

            bmp_manager = BmpManager(input_path, key, iv)
            bmp_manager.decrypt(output_path)
            print(f"Image {filename} decrypted and saved as {filename}")

class BmpManager:
    def __init__(self, image, key, iv):
        self.imageEncrypted = image
        self.getHeader()
        self.IV = iv
        self.KEY = key
        self.mode = AES.MODE_CBC
    
    def getHeader(self):
        with open(self.imageEncrypted, 'rb') as imgBin:
            bmpheader = imgBin.read(14)
            dibheader = imgBin.read(40)
            self.__get_sizes__(dibheader)
            self._bmpheader = bmpheader
            self._dibheader = dibheader

    def __get_sizes__(self, dibheader):
        DIBheader = []
        for i in range(0, 80, 2):
            DIBheader.append(int(binascii.hexlify(dibheader)[i:i+2], 16))
        self.width = sum([DIBheader[i+4]*256**i for i in range(0, 4)])
        self.height = sum([DIBheader[i+8]*256**i for i in range(0, 4)])

    def decrypt(self, output_path):
        BLOCK_SIZE = 16
        with open(self.imageEncrypted, 'rb') as f_in, open(output_path, 'wb') as f_out:
            f_out.write(self._bmpheader)
            f_out.write(self._dibheader)
            image_data = f_in.read()[54:]
            decryptor = AES.new(self.KEY, self.mode, self.IV)
            decrypted_data = decryptor.decrypt(image_data)
            decrypted_data = unpad(decrypted_data, BLOCK_SIZE)
            f_out.write(decrypted_data)


def déchiffrement():
    # Obtenir la clé de déchiffrement depuis un fichier (doit être le même que celle utilisés pour le cryptage)
    decryption_key = get_decryption_key_from_file()

    if decryption_key:
        decrypt_images_in_folder(decryption_key)
        
        
        
#déchiffrement()