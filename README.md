# Video Compression and Encryption with AES, ECC and DWT Algorithms

## Overview

This repository contains a Python application for compressing and encrypting videos using the AES-CBC (Advanced Encryption Standard - Cipher Block Chaining) algorithm for encryption and the DWT (Discrete Wavelet Transform) algorithm for compression.

## Features

- Video compression using DWT algorithm
- Video encryption using AES-CBC algorithm
- Decryption and decompression capabilities
- Simple and modular Python implementation

  

## Dependencies

- Python 3.x
- NumPy
- matplotlib
- OpenCV
- Crypto (for AES encryption)
- pywt (for DWT compression)


## Usage


1. **Adjust Parameters:**

    Modify the script files or parameters to customize compression and encryption settings.

   
   
## Workflow

The process of compressing and encrypting videos involves the following steps:

### 1.Encryption and Compression

#### a. Input Video

Start with a video file (`input_video.mp4`) that you want to compress and encrypt.

#### b. Splitting into Frames

The video is split into individual frames to process each frame independently.

#### c. Compression with DWT Algorithm

Apply the Discrete Wavelet Transform (DWT) algorithm to each frame for compression. This reduces the spatial redundancy in the frames.

#### d. Encryption with AES Algorithm

Encrypt each compressed frame using the Advanced Encryption Standard (AES) algorithm in Cipher Block Chaining (CBC) mode. This step ensures the confidentiality and security of the video data.

#### e. Merging Encrypted Frames

Combine all the encrypted frames into a single encrypted video file .

#### 2. Decryption and Decompression

To retrieve the original video:

#### a. Splitting Encrypted Video into Frames

Split the encrypted video (`output_video_encrypted.bin`) back into individual encrypted frames.

#### b. Decrypting Frames

Decrypt each encrypted frame using the same AES key and initialization vector (IV) used for encryption.

#### c. Decompression with DWT

Apply the inverse Discrete Wavelet Transform to decompress each decrypted frame back to its original state.

#### d. Merging Decrypted Frames

Combine all the decrypted frames into a single decrypted video file .

#### e. Output Video

The final result is a decrypted and decompressed video (`output_video_decrypted.mp4`) identical to the original input video.
