import cv2
import matplotlib.pyplot as plt

def plot_histogram(image, title):
    # Calculate histogram
    hist = cv2.calcHist([image], [0], None, [256], [0, 256])

    # Plot histogram with bars
    plt.figure()
    plt.title(title)
    plt.xlabel("Pixel Value")
    plt.ylabel("Frequency")
    plt.bar(range(len(hist)), hist[:,0], width=1.0)
    plt.xlim([0, 256])
    plt.show()

def display_histograms(original_frame, crypted_frame):
    # Convert the frames to grayscale
    original_frame_gray = cv2.cvtColor(original_frame, cv2.COLOR_BGR2GRAY)
    crypted_frame_gray = cv2.cvtColor(crypted_frame, cv2.COLOR_BGR2GRAY)

    # Calculate histograms
    original_hist = cv2.calcHist([original_frame_gray], [0], None, [256], [0, 256])
    crypted_hist = cv2.calcHist([crypted_frame_gray], [0], None, [256], [0, 256])

    # Plot histograms
    plt.figure(figsize=(12, 4))

    plt.subplot(1, 2, 1)
    plt.bar(range(len(original_hist)), original_hist[:,0], width=1.0)
    plt.title("Original Frame Histogram")
    plt.xlabel("Pixel Value")
    plt.ylabel("Frequency")

    plt.subplot(1, 2, 2)
    plt.bar(range(len(crypted_hist)), crypted_hist[:,0], width=1.0)
    plt.title("Crypted Frame Histogram")
    plt.xlabel("Pixel Value")
    plt.ylabel("Frequency")

    plt.tight_layout()
    plt.show()

# Charger les images originales et chiffrées
original_frame = cv2.imread("C:/Users/pc/Desktop/frames_medicales/frame5.jpg")
crypted_frame = cv2.imread("C:/Users/pc/Desktop/Cryptages_frames/frame5.bmp")

if original_frame is not None and crypted_frame is not None:
    display_histograms(original_frame, crypted_frame)
else:
    print("Erreur lors du chargement des images.")
