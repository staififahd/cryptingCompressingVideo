from tkinter import filedialog
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os


def dechiffrement(chemin_fichier_chiffre):
    # Charger la clé privée depuis le fichier
    with open("C:/Users/pc/Desktop/Test_Video/keys/cle_privee.pem", "rb") as key_file:
        cle_privee_pem = key_file.read()
        cle_privee = serialization.load_pem_private_key(
            cle_privee_pem,
            password=None,
            backend=default_backend()
        )
    # Charger la clé publique depuis le fichier
    with open("C:/Users/pc/Desktop/Test_Video/keys/cle_publique.pem", "rb") as key_file:
        cle_publique_pem = key_file.read()
        cle_publique = serialization.load_pem_public_key(
            cle_publique_pem,
            backend=default_backend()
        )

    # Charger le texte chiffré et l'IV depuis le fichier
    with open(chemin_fichier_chiffre, "rb") as file:
        iv = file.read(16)
        texte_chiffre = file.read()

    # Réaliser un échange de clés ECDH pour générer une clé partagée
    echange_cle = cle_privee.exchange(ec.ECDH(), cle_publique)

    # Utiliser la clé partagée comme clé de déchiffrement
    cipher = Cipher(algorithms.AES(echange_cle), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor() 
    texte_clair = decryptor.update(texte_chiffre) + decryptor.finalize()

    # Écrire le texte déchiffré dans un fichier spécifique
    chemin_fichier_dechiffre = "C:/Users/pc/Desktop/Test_Video/keys/fichier_dechiffre.txt"
    with open(chemin_fichier_dechiffre, "wb") as f:
        f.write(texte_clair)

def dechiffrementFichier():
    # Choix du fichier texte chiffré à déchiffrer
    chemin_fichier_chiffre = filedialog.askopenfilename(title="Choisir un fichier texte chiffré à déchiffrer")

    # Si un fichier a été spécifié
    if chemin_fichier_chiffre:
        dechiffrement(chemin_fichier_chiffre)
        
        

#dechiffrementFichier()        