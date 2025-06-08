# Functions for saving files
def save_file(uploaded_audio):
    if not hasattr(uploaded_audio, 'name'):
        raise ValueError("The uploaded file must have a 'name' attribute.")
    
    file_path = uploaded_audio.name
    with open(file_path, "wb") as f:
        f.write(uploaded_audio.read())
    print("Uploaded file Saved Sussfully")
    return file_path



import cv2
import os

def save_all_frames(video_path, output_dir, save_middle_frame=True):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Open the video file
    video = cv2.VideoCapture(video_path)
    
    # Get the total number of frames
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Calculate the middle frame index
    middle_frame_index = total_frames // 2
    
    # Initialize frame counter
    frame_index = 0
    
    # Loop through all the frames
    while True:
        success, frame = video.read()
        if not success:
            break
        
        # Save each frame as an image
        frame_filename = os.path.join(output_dir, f"frame_{frame_index:04d}.jpg")
        cv2.imwrite(frame_filename, frame)
        
        # Save the middle frame separately, if requested
        if save_middle_frame and frame_index == middle_frame_index:
            middle_frame_filename = os.path.join(output_dir, "middle_frame.jpg")
            cv2.imwrite(middle_frame_filename, frame)
            print(f"Middle frame saved as {middle_frame_filename}")
        
        frame_index += 1
    
    print(f"All frames saved in {output_dir}")
    
    # Release the video
    video.release()
