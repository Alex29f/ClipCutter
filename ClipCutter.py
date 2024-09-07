import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from moviepy.editor import VideoFileClip

def get_file_size_in_mb(file_path):
    size_in_bytes = os.path.getsize(file_path)
    size_in_mb = size_in_bytes / (1024 * 1024)  # Convert bytes to MB
    return round(size_in_mb)

def process_video_file(file_path, output_directory, bitrate, framerate, cut_length):
    try:
        # Load the video file
        print(f"Loading video file: {file_path}")
        video = VideoFileClip(file_path)
        duration = video.duration
        
        if duration > cut_length:
            start_time = duration - cut_length
            end_time = duration
            last_clip = video.subclip(start_time, end_time)
            
            # Create a temporary output file name
            file_name = os.path.basename(file_path)
            temp_output_file_name = os.path.join(output_directory, f"temp_{file_name}.mp4")
            
            # Stretch the video to 16:9 and resize to 1080p
            last_clip = last_clip.resize((1920, 1080))

            # Start processing
            print(f"Processing {file_name}...")

            # Process video with h.264 codec using user-defined bitrate and framerate
            last_clip.write_videofile(
                temp_output_file_name, 
                codec="libx264", 
                bitrate=bitrate, 
                fps=framerate,
                audio_codec="aac", 
                threads=12  # Utilize up to 12 threads for encoding
            )

            # Calculate the size of the processed video
            final_file_size_mb = get_file_size_in_mb(temp_output_file_name)
            
            # Create the final output file name with the size included
            output_file_name = os.path.join(output_directory, f"{final_file_size_mb}MBCut_{file_name}.mp4")
            
            # Rename the temporary output file to the final name
            os.rename(temp_output_file_name, output_file_name)

            # Display processing information
            print(f"Finished processing {file_name} and saved as {output_file_name}")
            
            # Close the video files
            video.close()
            last_clip.close()
        else:
            print(f"Video is shorter than the specified cut length ({cut_length} seconds): {file_path}")
    except Exception as e:
        print(f"An error occurred while processing {file_name}: {str(e)}")

def scan_and_process_directory(directory, bitrate, framerate, cut_length):
    print(f"Scanning directory: {directory}")
    video_files = [f for f in os.listdir(directory) if f.lower().endswith(('.mp4', '.mov', '.avi', '.mkv'))]
    
    total_files = len(video_files)
    print(f"Found {total_files} video file(s) to process.")

    if total_files == 0:
        print("No videos found in the directory. Exiting...")
        return

    # Create the output directory for cut clips
    output_directory = os.path.join(directory, "Cut Clips")
    os.makedirs(output_directory, exist_ok=True)

    # Process videos in parallel using ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=6) as executor:  # Adjust max_workers based on your CPU cores
        futures = [executor.submit(process_video_file, os.path.join(directory, file_name), output_directory, bitrate, framerate, cut_length) 
                   for file_name in video_files]

        # Wait for all futures to complete
        for future in futures:
            try:
                future.result()
            except Exception as e:
                print(f"An error occurred during processing: {e}")

def validate_bitrate(bitrate):
    try:
        if bitrate[-1].lower() == 'm':
            int(bitrate[:-1])  # Ensure the numeric part is an integer
            return bitrate
        else:
            raise ValueError("Bitrate should end with 'M' (e.g., '2M', '4M').")
    except ValueError:
        raise ValueError("Invalid bitrate format. Please use a format like '2M' or '4M'.")

if __name__ == "__main__":
    # Ensure the directory is where the executable/script is located
    if getattr(sys, 'frozen', False):
        # If the application is run as a bundle (compiled with PyInstaller)
        current_directory = os.path.dirname(sys.executable)
    else:
        # If running as a script
        current_directory = os.path.dirname(os.path.abspath(__file__))
    
    print(f"Current directory is: {current_directory}")
    
    # Ask the user for bitrate and framerate
    while True:
        try:
            bitrate = input("Enter the desired bitrate (e.g., 2M, 4M): ")
            bitrate = validate_bitrate(bitrate)
            break
        except ValueError as ve:
            print(ve)

    while True:
        try:
            framerate = int(input("Enter the desired framerate (e.g., 24, 30, 60): "))
            if framerate <= 0:
                raise ValueError("Framerate must be a positive integer.")
            break
        except ValueError:
            print("Invalid framerate. Please enter a positive integer.")

    while True:
        try:
            cut_length = int(input("Enter the desired length to cut from the end of each video (in seconds): "))
            if cut_length <= 0:
                raise ValueError("Cut length must be a positive integer.")
            break
        except ValueError:
            print("Invalid cut length. Please enter a positive integer.")

    # Scan and process the directory
    scan_and_process_directory(current_directory, bitrate, framerate, cut_length)

    # Keep the console window open after processing
    print("Processing completed. Press Enter to exit.")
    input()
