## Project Overview

Continuously monitors and detects pedestrians on the crosswalks from a [livestream](https://www.youtube.com/watch?v=1EiC9bvVGnk) of a town square in Jackson Hole, Wyoming.

## Key requirements met
* UI should minimally display the live image feed including options to create an alert
* Users should receive an email when the alert is triggered along with a link to view the image that the alert was triggered on
* From the UI, users can also see a report of the alert captured once an hour for up to 3 days. This report should be pulled from a database and displayed in a meaningful format to the user

## Technologies Used:
* EC2 to host the frontend code (Flask/Python)
* S3 to hold images taken from the live feed
* Rekognition to detect pedestrian crossings in the video
* DynamoDB to store and retrieve logs of alerts and reports (i.e. crossings)
* SNS for email alerts/notifications
* Terraform for IAC
* Two lambdas:
1) Captures a frame from the live feed taken at regular 5-second intervals and uploads them to S3. Includes a layer for OpenCV.
2) Triggered from S3 when image is deposited. Calls rekognition, sends alert to SNS for email notification, and stores data in DB.

## Architecture
![Architecture Overview](https://user-images.githubusercontent.com/55066934/209899718-1400b537-c25d-41d3-8100-27d9d228c5b2.png)

## Challenges/Lessons Learned
* API access only vs. publicly available livestream
* Initial challenge of getting data from live feed in real-time (Kinesis)
* Rekognition data flow with videos
* Use of OpenCV + Pafy + Youtube_dl vs. Selenium
* Crosswalk Detection - OpenCV library, SageMaker Ground Truth’s manifest file with Rekognition custom label detection, Drawing Virtual Polyons
* Detect Point in Polygon - Inbuilt library (add a layer), Raycasting Algorithm (even or odd rule)
* Rekognition not being able to identify all labels correctly (sometimes)
* Lambda Layers for dependencies, moved OpenCV to EC2

