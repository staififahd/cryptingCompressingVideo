import cv2
import numpy as np
from scipy.stats import entropy, pearsonr

def calculate_entropy(image):
    # Flatten the image
    flattened_image = image.flatten()

    # Calculate the probability distribution of pixel values
    pixel_probabilities = np.histogram(flattened_image, bins=256, range=[0, 256], density=True)[0]

    # Calculate the entropy
    image_entropy = entropy(pixel_probabilities, base=2)

    return image_entropy

def calculate_correlation(image1, image2):
    # Flatten the images
    flattened_image1 = image1.flatten()
    flattened_image2 = image2.flatten()

    # Calculate the correlation coefficient
    correlation_coefficient, _ = pearsonr(flattened_image1, flattened_image2)

    return correlation_coefficient

def evaluate_encryption_quality(original_image_path, encrypted_image_path):
    try:
        # Load the original image
        original_image = cv2.imread(original_image_path)

        # Load the encrypted image
        encrypted_image = cv2.imread(encrypted_image_path)

        if original_image is None or encrypted_image is None:
            raise ValueError("One or both images could not be loaded.")

        # Convert images to grayscale
        original_image_gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
        encrypted_image_gray = cv2.cvtColor(encrypted_image, cv2.COLOR_BGR2GRAY)

        # Calculate entropy of the original image
        original_entropy = calculate_entropy(original_image_gray)

        # Calculate correlation coefficient between the original and encrypted images
        correlation_coefficient = calculate_correlation(original_image_gray, encrypted_image_gray)

        return original_entropy, correlation_coefficient
    except Exception as e:
        print("Error:", e)
        return None, None

original_image_path = "C:/Users/pc/Desktop/frames_medicales/frame5.jpg"
encrypted_image_path = "C:/Users/pc/Desktop/Cryptages_frames/frame5.bmp"

original_entropy, correlation_coefficient = evaluate_encryption_quality(original_image_path, encrypted_image_path)

if original_entropy is not None and correlation_coefficient is not None:
    print("Original Image Entropy:", original_entropy)
    print("Correlation Coefficient:", correlation_coefficient)
