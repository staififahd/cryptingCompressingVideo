import tkinter as tk
from tkinter import filedialog
import cv2
from skimage.metrics import structural_similarity as ssim
import numpy as np
from scipy.stats import entropy, pearsonr
import extraire_frames
import compression
import cryptageAES_frames
import combinaison_framesCrypted
import CryptageECC
import extraire_framesCrypted
import DecryptageECC
import decryptageAES_frames
import decompression
import Combinaison_framesDecrypted


def calculate_entropy(image):
    flattened_image = image.flatten()
    pixel_probabilities = np.histogram(flattened_image, bins=256, range=[0, 256], density=True)[0]
    image_entropy = entropy(pixel_probabilities, base=2)
    return image_entropy

def calculate_correlation(image1, image2):
    flattened_image1 = image1.flatten()
    flattened_image2 = image2.flatten()
    correlation_coefficient, _ = pearsonr(flattened_image1, flattened_image2)
    return correlation_coefficient

def evaluate_encryption_quality(original_video_path, encrypted_video_path):
    original_cap = cv2.VideoCapture(original_video_path)
    encrypted_cap = cv2.VideoCapture(encrypted_video_path)
    entropy_values = []
    correlation_coefficients = []

    while original_cap.isOpened() and encrypted_cap.isOpened():
        ret_original, original_frame = original_cap.read()
        ret_encrypted, encrypted_frame = encrypted_cap.read()

        if ret_original and ret_encrypted:
            original_frame_gray = cv2.cvtColor(original_frame, cv2.COLOR_BGR2GRAY)
            encrypted_frame_gray = cv2.cvtColor(encrypted_frame, cv2.COLOR_BGR2GRAY)

            original_entropy = calculate_entropy(original_frame_gray)
            entropy_values.append(original_entropy)

            correlation_coefficient = calculate_correlation(original_frame_gray, encrypted_frame_gray)
            correlation_coefficients.append(correlation_coefficient)

        else:
            break

    original_cap.release()
    encrypted_cap.release()

    avg_entropy = np.mean(entropy_values)
    avg_correlation = np.mean(correlation_coefficients)

    return avg_entropy, avg_correlation

def afficher_resultats_cryptage():
    original_video_path = "C:/Users/pc/Desktop/Test_Video/Video.mp4"
    encrypted_video_path = "C:/Users/pc/Desktop/Test_Video/video_crypter.mp4"
    avg_entropy, avg_correlation = evaluate_encryption_quality(original_video_path, encrypted_video_path)

    label_resultat_1.config(text=f"Entropie moyenne: {avg_entropy}\nCoefficient de corrélation moyen: {avg_correlation:.15f}")

def afficher_resultats_compression():
    chemin_video_originale = "C:/Users/pc/Desktop/Test_Video/video.mp4"
    chemin_video_compressée = "C:/Users/pc/Desktop/Test_Video/video_compresser.mp4"
    video_originale = cv2.VideoCapture(chemin_video_originale)
    video_compressée = cv2.VideoCapture(chemin_video_compressée)
    mse_scores = []
    psnr_scores = []
    ssim_scores = []

    while True:
        ret1, frame1 = video_originale.read()
        ret2, frame2 = video_compressée.read()

        if not ret1 or not ret2:
            break

        frame1_gris = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        frame2_gris = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

        mse = np.mean((frame1_gris - frame2_gris) ** 2)
        mse_scores.append(mse)

        psnr = cv2.PSNR(frame1_gris, frame2_gris)
        psnr_scores.append(psnr)

        ssim_score, _ = ssim(frame1_gris, frame2_gris, full=True)
        ssim_scores.append(ssim_score)

    video_originale.release()
    video_compressée.release()

    mse_moyen = np.mean(mse_scores)
    psnr_moyen = np.mean(psnr_scores)
    ssim_moyen = np.mean(ssim_scores)

    label_resultat_2.config(text=f"MSE moyen: {mse_moyen} \nPSNR moyen: {psnr_moyen} dB\nSSIM moyen: {ssim_moyen}")
   

# Création de la fenêtre principale
root = tk.Tk()
root.title("Cryptage / Décryptage")
root.geometry("800x620")

# Layout Cryptage
frame_cryptage = tk.Frame(root, relief=tk.SUNKEN, borderwidth=2, bg='ivory')
frame_cryptage.place(x=20, y=20, width=360, height=420)
label_cryptage = tk.Label(frame_cryptage, text="Cryptage", font=("Arial", 24, "bold"), fg="red",  bg='ivory')
label_cryptage.place(x=10, y=10, width=340)

# Function to open a file dialog and select a video file
def select_file():
    filename = filedialog.askopenfilename(initialdir="/", title="Sélectionner un fichier", filetypes=(("MP4 files", ".mp4"), ("all files", ".*")))
    entry_cryptage.insert(0, filename)

file_label = tk.Label(frame_cryptage, text="la vidéo à compresser et chiffrer:",font=('Helvetica', 12,'bold'),  bg='ivory')
file_label.place(x=10, y=90)
entry_cryptage = tk.Entry(frame_cryptage)
entry_cryptage.place(x=10, y=120, width=340, height=25)

button1 = tk.Button(frame_cryptage, text="Sélectionner une vidéo", command=select_file)
button1.place(x=10, y=160, width=340)
button2 = tk.Button(frame_cryptage, text="Diviser la vidéo", command=extraire_frames.extraire_frames)
button2.place(x=10, y=200, width=340)
button3 = tk.Button(frame_cryptage, text="Compresser les frames", command=compression.compress_video)
button3.place(x=10, y=240, width=340)
button4 = tk.Button(frame_cryptage, text="Chiffrer les frames", command=cryptageAES_frames.chiffrement)
button4.place(x=10, y=280, width=340)
button5 = tk.Button(frame_cryptage, text="Fusionner les frames", command=combinaison_framesCrypted.merge_video)
button5.place(x=10, y=320, width=340)
button6 = tk.Button(frame_cryptage, text="Chiffrer la clé", command=CryptageECC.chiffrementFichier)
button6.place(x=10, y=360, width=340)

# Layout Décryptage
frame_decryptage = tk.Frame(root, relief=tk.SUNKEN, borderwidth=2, bg='ivory')
frame_decryptage.place(x=420, y=20, width=360, height=420)
label_decryptage = tk.Label(frame_decryptage, text="Décryptage", font=("Arial", 24, "bold"), fg="green",  bg='ivory')
label_decryptage.place(x=10, y=10, width=340)

# Function to open a file dialog and select a video file
def selecte_file():
    filename = filedialog.askopenfilename(initialdir="/", title="Sélectionner un fichier", filetypes=(("MP4 files", ".mp4"), ("all files", ".*")))
    entry_decryptage.insert(0, filename)

file_label = tk.Label(frame_decryptage, text="la vidéo à déchiffrer et décompresser:",font=('Helvetica', 12,'bold'), bg='ivory')
file_label.place(x=10, y=90)
entry_decryptage = tk.Entry(frame_decryptage)
entry_decryptage.place(x=10, y=120, width=340, height=25)

button7 = tk.Button(frame_decryptage, text="Sélectionner une vidéo", command=selecte_file)
button7.place(x=10, y=160, width=340)
button8 = tk.Button(frame_decryptage, text="Diviser la vidéo", command=extraire_framesCrypted.extraire_frames)
button8.place(x=10, y=200, width=340)
button9 = tk.Button(frame_decryptage, text="Déchiffrer la clé", command=DecryptageECC.dechiffrementFichier)
button9.place(x=10, y=240, width=340)
button10 = tk.Button(frame_decryptage, text="Déchiffrer les frames ", command=decryptageAES_frames.déchiffrement)
button10.place(x=10, y=280, width=340)
button11 = tk.Button(frame_decryptage, text="Décompresser les frames", command=decompression.decompression)
button11.place(x=10, y=320, width=340)
button12 = tk.Button(frame_decryptage, text="Fusionner les frames", command=Combinaison_framesDecrypted.merge_video)
button12.place(x=10, y=360, width=340)


# Nouveau Layout pour les résultats
frame_resultats = tk.Frame(root, relief=tk.SUNKEN, borderwidth=2, bg='ivory')
frame_resultats.place(x=20, y=460, width=760, height=140)
label_resultats = tk.Label(frame_resultats, text="Résultats d'Evaluation de Compression et Cryptage de vidéo ", font=("Arial", 16, "bold"), fg="steelblue", bg='ivory')
label_resultats.place(x=10, y=10, width=720)
label_resultat_1 = tk.Label(frame_resultats, text="", bg='ivory')
label_resultat_1.place(x=220, y=40, width=310, height=90)
label_resultat_2 = tk.Label(frame_resultats, text="", bg='ivory')
label_resultat_2.place(x=540, y=40, width=200, height=90)

# Boutons pour afficher les résultats
button_resultats_video = tk.Button(frame_resultats, text="Afficher Résultats du Cryptage", command=afficher_resultats_cryptage)
button_resultats_video.place(x=10, y=60, width=200)
button_resultats_cryptage = tk.Button(frame_resultats, text="Afficher Résultats de la Compression", command=afficher_resultats_compression)
button_resultats_cryptage.place(x=10, y=100, width=200)

root.mainloop()