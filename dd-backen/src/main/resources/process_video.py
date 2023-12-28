# process_video.py
import shutil
import sys

save_path = "C:/Users/Tangs/Desktop/dd_uploads"
result_path = "C:/Users/Tangs/Desktop/dd_results"

def process_video(file_name):
    source = f"{save_path}/{file_name}"
    destination = f"{result_path}/{file_name}"

    try:
        shutil.copy(source, destination)
        print(f"File {file_name} copied successfully to {destination}.")
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) == 2:
        process_video(sys.argv[1])
    else:
        print("Invalid arguments. Please provide the file name.")
