import cv2
from skimage.metrics import structural_similarity as ssim
import numpy as np

# Chemins des vidéos originale et compressée
chemin_video_originale = "C:/Users/pc/Desktop/Test_Video/video.mp4"
chemin_video_compressée = "C:/Users/pc/Desktop/Test_Video/video_compresser.mp4"

# Charger les vidéos
video_originale = cv2.VideoCapture(chemin_video_originale)
video_compressée = cv2.VideoCapture(chemin_video_compressée)

# Initialiser les tableaux pour stocker les résultats
mse_scores = []
psnr_scores = []
ssim_scores = []

# Lire les images de chaque vidéo et calculer les scores
while True:
    ret1, frame1 = video_originale.read()
    ret2, frame2 = video_compressée.read()

    if not ret1 or not ret2:
        break

    # Convertir les images en niveaux de gris
    frame1_gris = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    frame2_gris = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    # Calculer le MSE (Mean Squared Error)
    mse = np.mean((frame1_gris - frame2_gris) ** 2)
    mse_scores.append(mse)

    # Calculer le PSNR (Peak Signal to Noise Ratio)
    psnr = cv2.PSNR(frame1_gris, frame2_gris)
    psnr_scores.append(psnr)

    # Calculer le SSIM (Structural SIMilarity)
    ssim_score, _ = ssim(frame1_gris, frame2_gris, full=True)
    ssim_scores.append(ssim_score)

# Fermer les vidéos
video_originale.release()
video_compressée.release()

# Calculer les scores moyens
mse_moyen = np.mean(mse_scores)
psnr_moyen = np.mean(psnr_scores)
ssim_moyen = np.mean(ssim_scores)

# Afficher les résultats moyens
print(f"MSE moyen: {mse_moyen}")
print(f"PSNR moyen: {psnr_moyen} dB")
print(f"SSIM moyen: {ssim_moyen}")
