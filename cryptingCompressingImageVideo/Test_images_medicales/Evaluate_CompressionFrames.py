import cv2
from skimage.metrics import structural_similarity as ssim
import numpy as np

# Chemins des images originales et compressées
chemin_image_originale = "C:/Users/pc/Desktop/frames_medicales/frame5.jpg"
chemin_image_compressée = "C:/Users/pc/Desktop/Compression_frames_medicales/frame5.bmp"

# Charger les images
image_originale = cv2.imread(chemin_image_originale)
image_compressée = cv2.imread(chemin_image_compressée)

# Vérifier si les images sont valides
if image_originale is not None and image_compressée is not None:
    # Convertir les images en niveaux de gris
    image_originale_gris = cv2.cvtColor(image_originale, cv2.COLOR_BGR2GRAY)
    image_compressée_gris = cv2.cvtColor(image_compressée, cv2.COLOR_BGR2GRAY)

    # Calculer le MSE (Mean Squared Error)
    mse = np.mean((image_originale_gris - image_compressée_gris) ** 2)

    # Calculer le PSNR (Peak Signal to Noise Ratio)
    psnr = cv2.PSNR(image_originale_gris, image_compressée_gris)

    # Calculer le SSIM (Structural SIMilarity)
    ssim_score, _ = ssim(image_originale_gris, image_compressée_gris, full=True)

    # Afficher les résultats
    print(f"MSE: {mse}")
    print(f"PSNR: {psnr} dB")
    print(f"SSIM: {ssim_score}")
else:
    print("Erreur lors du chargement des images.")



