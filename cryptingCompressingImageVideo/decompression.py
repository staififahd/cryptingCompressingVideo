from matplotlib.image import imread, imsave
import numpy as np
import pywt
import os

def decompress_image(compressed_file, output_dir):
   
    try:
        # Extract filename and ensure it's a supported format
        filename = os.path.basename(compressed_file)
        if not filename.endswith('.bmp'):
            raise ValueError("Decompression currently supports only bmp format.")

        # Read compressed image
        compressed_image = imread(compressed_file)

        # Assuming the compression code used the same parameters (wavelet, level)
        wavelet = 'db1' 
        level = 5 

        # Placeholder for extracting coefficients from compressed_image
        coeffs = []
        for channel in range(compressed_image.shape[2]):
            # Apply wavelet decomposition to the channel data
            channel_data = compressed_image[:, :, channel]
            channel_coeffs = pywt.wavedec2(channel_data, wavelet=wavelet, level=level)
            coeffs.append(channel_coeffs)

        # Perform inverse wavelet transform (reconstruction)
        decompressed_image = np.empty_like(compressed_image)
        for channel in range(compressed_image.shape[2]):
            channel_coeffs = coeffs[channel]
            decompressed_image[:, :, channel] = pywt.waverec2(channel_coeffs, wavelet=wavelet)

        # Save decompressed image
        output_path = os.path.join(output_dir, os.path.splitext(filename)[0] + '.bmp')
        imsave(output_path, decompressed_image.astype('uint8'))

        print(f"Decompressed image saved at: {output_path}")

    except Exception as e:
        print(f"Error occurred during decompression of {compressed_file}: {str(e)}")

def decompression():
    
    compressed_dir = 'C:/Users/pc/Desktop/Test_Video/Decryptage_frames'
    decompressed_dir = 'C:/Users/pc/Desktop/Test_Video/Decompression_frames'
    
    for filename in sorted(os.listdir(compressed_dir)):
        if filename.endswith('.bmp'):
            compressed_file = os.path.join(compressed_dir, filename)
            decompress_image(compressed_file, decompressed_dir)
