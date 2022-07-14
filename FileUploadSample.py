import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import boto3
import os

# Create a amazon s3 object
s3 = boto3.client("s3")
# define the bucket name
bucket_name = "sample-bucket-008"
# define the object name
object_name = "sample-test-1"


class FileMonitor:

    def __init__(self, path):
        # Set the folder path
        self.dir = os.path.abspath(path)
        # Initialize Observer
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.dir, recursive=True)
        # Start the Observer
        self.observer.start()
        try:
            while True:
                # Set the thread sleep time
                time.sleep(5)
        except KeyboardInterrupt:
            # Stop the Observer
            self.observer.stop()
            "Error"
        self.observer.join()


class Handler(FileSystemEventHandler):
    file_path = ""

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # find the file path when a new file added to the specified folder
            file_path = event.src_path
            # validate file present in the specified path
            if os.path.exists(file_path):
                # upload newly added file to s3 bucket
                response = s3.upload_file(file_path, bucket_name, object_name)
                if response is None:
                    # after file uploaded successfully remove the file from the specified folder
                    os.remove(file_path)


if __name__ == '__main__':
    # example file path for user input 'c:\\sample_files'
    folder_path = input('Folder Path: ')
    w = FileMonitor(folder_path)
    w.run()
