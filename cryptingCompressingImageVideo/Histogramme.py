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

def display_histograms(original_video_path, crypted_video_path):
    # Open the original video file for reading
    original_cap = cv2.VideoCapture(original_video_path)

    # Open the Crypted video file for reading
    crypted_cap = cv2.VideoCapture(crypted_video_path)
    
    # Create a figure with two subplots
    fig, axs = plt.subplots(1, 2, figsize=(12, 4))

    # Loop through the frames
    while original_cap.isOpened() and crypted_cap.isOpened():
        # Read the original frame
        ret_original, original_frame = original_cap.read()

        # Read the crypted frame
        ret_crypted, crypted_frame = crypted_cap.read()

        if ret_original and ret_crypted:
            # Convert the frames to grayscale
            original_frame_gray = cv2.cvtColor(original_frame, cv2.COLOR_BGR2GRAY)
            crypted_frame_gray = cv2.cvtColor(crypted_frame, cv2.COLOR_BGR2GRAY)

            # Calculate histograms
            original_hist = cv2.calcHist([original_frame_gray], [0], None, [256], [0, 256])
            crypted_hist = cv2.calcHist([crypted_frame_gray], [0], None, [256], [0, 256])

            # Plot histograms
            axs[0].cla()
            axs[0].bar(range(len(original_hist)), original_hist[:,0], width=1.0)
            axs[0].set_title("Original Frames Histogram")
            axs[0].set_xlabel("Pixel Value")
            axs[0].set_ylabel("Frequency")

            axs[1].cla()
            axs[1].bar(range(len(crypted_hist)), crypted_hist[:,0], width=1.0)
            axs[1].set_title("Crypted Frames Histogram")
            axs[1].set_xlabel("Pixel Value")
            axs[1].set_ylabel("Frequency")

            # Update the plot
            plt.tight_layout()
            plt.pause(0.01)

        else:
            break

    # Release the video capture objects
    original_cap.release()
    crypted_cap.release()

    # Close the plot window
    plt.close(fig)

original_video_path = "C:/Users/pc/Desktop/Test_Video/Video.mp4"
crypted_video_path = "C:/Users/pc/Desktop/Test_Video/video_crypter.mp4"

display_histograms(original_video_path, crypted_video_path)
