from tkinter import filedialog
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

def generer_cle():
    # Générer une paire de clés ECC
    cle_privee = ec.generate_private_key(ec.SECP256R1(), default_backend())
    cle_publique = cle_privee.public_key()

    # Sérialiser les clés au format PEM
    cle_privee_pem = cle_privee.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    cle_publique_pem = cle_publique.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Écrire les clés dans des fichiers
    with open("C:/Users/pc/Desktop/Test_Video/keys/cle_privee.pem", "wb") as f:
        f.write(cle_privee_pem)

    with open("C:/Users/pc/Desktop/Test_Video/keys/cle_publique.pem", "wb") as f:
        f.write(cle_publique_pem)

def chiffrement(texte_clair):
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

    # Réaliser un échange de clés ECDH pour générer une clé partagée
    echange_cle = cle_privee.exchange(ec.ECDH(), cle_publique)
    iv = os.urandom(16)
    # Utiliser la clé partagée comme clé de chiffrement
    cipher = Cipher(algorithms.AES(echange_cle), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    texte_chiffre = encryptor.update(texte_clair) + encryptor.finalize()

    # Écrire le texte chiffré dans un fichier spécifique
    chemin_fichier_chiffre = "C:/Users/pc/Desktop/Test_Video/keys/fichier_chiffre.txt"
    with open(chemin_fichier_chiffre, "wb") as file:
        file.write(iv)
        file.write(texte_chiffre)

def chiffrementFichier():
    # Générer une paire de clés ECC 
    generer_cle()

    # Choix du fichier texte à chiffrer
    chemin_fichier_clair = filedialog.askopenfilename(title="Choisir un fichier texte à chiffrer")

    # Si un fichier a été spécifié
    if chemin_fichier_clair:
        with open(chemin_fichier_clair, "rb") as f:
            texte_clair = f.read()
        chiffrement(texte_clair)

                
#chiffrementFichier()
