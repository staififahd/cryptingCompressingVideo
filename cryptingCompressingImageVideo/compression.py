from matplotlib.image import imread, imsave 
import numpy as np
import pywt
import os
import matplotlib.pyplot as plt


def compress_video():
    
    input_dir = 'C:/Users/pc/Desktop/Test_Video/Extraire_frames'
    output_dir = 'C:/Users/pc/Desktop/Test_Video/Compression_frames'
    
    level = 5  
    wavelet = 'db1'  

    for filename in sorted(os.listdir(input_dir)):
        if filename.endswith('.jpg'):
            filepath = os.path.join(input_dir, filename)
            print(f"Processing: {filepath}")

            # Read image as RGB
            image = imread(filepath)

            coeffs = []
            for channel in range(image.shape[2]):
                channel_data = image[:, :, channel]
                coeffs.append(pywt.wavedec2(channel_data, wavelet=wavelet, level=level))

            thresh = 0.1  

            thresholded_coeffs = []
            for channel_coeffs in coeffs:
                coeff_arr, coeff_slices = pywt.coeffs_to_array(channel_coeffs)
                thresholded_arr = np.where(np.abs(coeff_arr) > thresh, coeff_arr, 0)
                thresholded_coeffs.append(pywt.array_to_coeffs(thresholded_arr, coeff_slices, output_format='wavedec2'))

            # Reconstruct image from thresholded coefficients
            reconstructed_image = np.empty_like(image)
            for channel in range(image.shape[2]):
                reconstructed_image[:, :, channel] = pywt.waverec2(thresholded_coeffs[channel], wavelet=wavelet)

            # Save compressed image with BMP extension
            output_path = os.path.join(output_dir, os.path.splitext(filename)[0] + '.bmp')
            imsave(output_path, reconstructed_image.astype('uint8'))
            plt.close()


#compress_video()
