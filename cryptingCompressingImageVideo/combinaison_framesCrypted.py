import os


def merge_video():
    
    frame_folder_path = "C:/Users/pc/Desktop/Test_Video/Cryptage_frames"
    output_video_path = "C:/Users/pc/Desktop/Test_Video/video_crypter.mp4"
    
    # Get the list of frames sorted by frame number
    frame_names = os.listdir(frame_folder_path)
    frame_names.sort(key=lambda x: int(x.split(".")[0][5:]))
    
    # Create a video file and write encrypted image data to it
    with open(output_video_path, 'wb') as video_file:
        for frame_name in frame_names:
            frame_path = os.path.join(frame_folder_path, frame_name)
            with open(frame_path, "rb") as f:
                image_data = f.read()
                video_file.write(image_data)
    

#merge_video()   