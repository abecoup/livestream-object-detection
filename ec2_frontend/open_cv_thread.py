"""
"""

import pafy
import cv2
import json
import boto3
import time
import logging
import queue
import threading
import time
import random
import string
from queue import Queue
from abc import abstractmethod, ABC
from typing import Dict

#Imports Config Objects from Configuration File
from config import AWSConfig


#Imports AWS Utility Functions
from aws_utils import *


TASKS_QUEUE = Queue()


class BackgroundThread(threading.Thread, ABC):
    def __init__(self):
        super().__init__()
        self._stop_event = threading.Event()

    def stop(self) -> None:
        self._stop_event.set()

    def _stopped(self) -> bool:
        return self._stop_event.is_set()

    @abstractmethod
    def startup(self) -> None:
        """
        Method that is called before the thread starts.
        Initialize all necessary resources here.
        :return: None
        """
        raise NotImplementedError()

    @abstractmethod
    def shutdown(self) -> None:
        """
        Method that is called shortly after stop() method was called.
        Use it to clean up all resources before thread stops.
        :return: None
        """
        raise NotImplementedError()

    @abstractmethod
    def handle(self) -> None:
        """
        Method that should contain business logic of the thread.
        Will be executed in the loop until stop() method is called.
        Must not block for a long time.
        :return: None
        """
        raise NotImplementedError()

    def run(self) -> None:
        """
        This method will be executed in a separate thread
        when start() method is called.
        :return: None
        """
        self.startup()
        while not self._stopped():
            self.handle()
        self.shutdown()


class OpenCVThread(BackgroundThread):
    def startup(self) -> None:
        logging.info('OpenCVThread started')

    def shutdown(self) -> None:
        logging.info('OpenCVThread stopped')

    def handle(self) -> None:
        try:
            task = TASKS_QUEUE.get(block=False)
            print("Running OpenCV Background Operation...")
            s3 = boto3.client('s3', 
                aws_access_key_id=AWSConfig.ACCESS_KEY_ID,
                aws_secret_access_key=AWSConfig.SECRET_ACCESS_KEY,
                aws_session_token=AWSConfig.SESSION_TOKEN,
                region_name=AWSConfig.REGION
            )

            # IMPORTANT: this bucket name must equal the name used for
            # the S3 bucket in main.tf (terraform) file
            bucket_name = "crosswalk-frames-9cxjmbiqteam5"

            # Jackson Hole Wyoming USA Town Square Live Cam
            url = "https://www.youtube.com/watch?v=1EiC9bvVGnk"
            
            # Stores youtube video data
            video = pafy.new(url)
            
            # Retrieve best resolution in mp4 format
            best = video.getbest(preftype="mp4")
            
            count = 1
            while True:
                # Set to while true
                # Open livestream
                livestream = cv2.VideoCapture(best.url)
                if not livestream.isOpened():
                    print("Cannot open livestream.")
                    break
                
                # Read a frame
                success, frame = livestream.read()
                
                if not success:
                    print("Error reading frame. Exiting...")
                    break
                
                # Create image from frame, store in S3
                key = "image{0}.jpg".format(str(count))
                image_string = cv2.imencode('.jpg', frame)[1].tostring()
                s3.put_object(Bucket=bucket_name, Key=key, Body=image_string, ContentType='image/jpeg')
                
                # Close livestream, wait 5 seconds
                count = count + 1
                livestream.release()
                time.sleep(3)
            
            print("OpenCV Operation Complete")
            logging.info(f'Notification for {task} was sent.')
        except queue.Empty:
            time.sleep(1)


class BackgroundThreadFactory:
    @staticmethod
    def create(thread_type: str) -> BackgroundThread:
        if thread_type == 'opencv':
            return OpenCVThread()

        # if thread_type == 'some_other_type':
        #     return SomeOtherThread()

        raise NotImplementedError('Specified thread type is not implemented.')