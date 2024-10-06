import cv2
import os

def extraire_frames():
  
    fichier_video = "C:/Users/pc/Desktop/Test_Video/video_crypter.mp4"
    dossier_destination = "C:/Users/pc/Desktop/Test_Video/Extraire_frames_Crypted"
    # Vérifier si les chemins sont valides
    if not fichier_video or not dossier_destination:
        return

    # Obtenir le nom de la vidéo sans extension
    nom_video, extension = os.path.splitext(fichier_video)

    # Créer le dossier de destination si nécessaire
    if not os.path.exists(dossier_destination):
        os.makedirs(dossier_destination)

    # Initialiser le compteur de frames
    compteur_frames = 0

    try:
        # Ouvrir la vidéo
        cap = cv2.VideoCapture(fichier_video)

        # Vérifier si l'ouverture de la vidéo a réussi
        if not cap.isOpened():
            raise Exception(f"Erreur lors de l'ouverture de la vidéo : {fichier_video}")

        while True:
            # Lire la frame suivante
            ret, frame = cap.read()

            # Vérifier si la fin de la vidéo a été atteinte
            if not ret:
                break

            # Enregistrer la frame dans le dossier de destination
            cv2.imwrite(f"{dossier_destination}/frame{compteur_frames}.bmp", frame)

            # Incrémenter le compteur de frames
            compteur_frames += 1

    except Exception as e:
        # Gérer les erreurs
        print(f"Erreur : {e}")

    finally:
        # Libérer les ressources
        cap.release()


#extraire_frames()
