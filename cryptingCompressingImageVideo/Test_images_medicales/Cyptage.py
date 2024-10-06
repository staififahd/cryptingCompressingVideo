import binascii
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os
from tkinter import Tk, filedialog

def get_encryption_key_from_file():
    root = Tk()
    root.withdraw()  # Masquer la fenêtre principale de Tkinter

    key_file = filedialog.askopenfilename(title="Choisissez un fichier contenant la clé (.txt)", filetypes=[("Text files", "*.txt")])

    if not key_file:  # Si l'utilisateur annule la sélection du fichier
        print("Aucun fichier sélectionné.")
        return None

    with open(key_file, 'r') as f:
        key_str = f.read().strip()  # Lire la clé depuis le fichier

    # Convertir la clé en bytes
    key_bytes = key_str.encode('utf-8')
    return key_bytes


def encrypt_images_in_folder(key):
    # Chemins des dossiers d'entrée et de sortie
    input_folder = "C:/Users/pc/Desktop/Test_images_médicales/Compression_frames_medicales"
    output_folder = "C:/Users/pc/Desktop/Test_images_médicales/Cryptages_frames"

# Clé et vecteur d'initialisation
    #key = b'12345678901234567890123456789012'
    iv = b'1234567890123456'
    """Encrypts all BMP images in the input folder and saves them in the output folder."""
    for filename in os.listdir(input_folder):
        if filename.endswith(".bmp"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, f"{filename}")

            bmp_manager = BmpManager(input_path, key, iv)
            bmp_manager.encrypt(output_path)
            print(f"Image {filename} encrypted and saved as {filename}")

class BmpManager:
    def __init__(self, image, key, iv):
        self.imageClear = image
        self.getHeader()
        self.IV = iv
        self.KEY = key
        self.mode = AES.MODE_CBC
    
    def getHeader(self):
        with open(self.imageClear, 'rb') as imgBin:
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

    def encrypt(self, output_path):
        BLOCK_SIZE = 16
        with open(self.imageClear, 'rb') as f_in, open(output_path, 'wb') as f_out:
            f_out.write(self._bmpheader)
            f_out.write(self._dibheader)
            image_data = f_in.read()[54:]
            cleartext = binascii.unhexlify(binascii.hexlify(image_data))
            cleartext = pad(cleartext, BLOCK_SIZE)
            encryptor = AES.new(self.KEY, self.mode, self.IV)
            enc = encryptor.encrypt(cleartext)
            f_out.write(enc)

def chiffrement():
    # Obtenir la clé de chiffrement depuis un fichier
    encryption_key = get_encryption_key_from_file()

    if encryption_key:
        # Exemple d'utilisation :
        encrypt_images_in_folder(encryption_key)

chiffrement()