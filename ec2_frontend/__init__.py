"""
Author: Abraham Couperus
Date: 
Release: 0.1
Description: Python Flask Frontend 
"""

#Imports Flask Libraries
from re import template
from flask import Flask, render_template, request, session, jsonify, redirect, url_for

#Imports Other Libraries
import requests
import os
import json
import signal
import datetime

#Imports AWS Classes
import boto3

#Imports Config Objects from Configuration File
from config import *

#Imports AWS Utility Functions
from aws_utils import *

#Imports OpenCV Functions
from open_cv_thread import *

#Imports Model Objects
from model.alert import *
from model.report import *


logging.basicConfig(level=logging.INFO, force=True)

"""
Class: create_app()
Description: Initialization Function
    This function interprets and starts the EC2 Flask Server based on the configuration options outlined in the configuration file.
"""
def create_app():
    #Declares Flask Application
    app = Flask(__name__)
    #app.config.from_object(DevelopmentConfig)
    
    #Sets AWS Credentials
    #aws_credentials = AWSConfig()
    aws_utilities = AWSUtilities()

    #Detects Flask Environment and Sets Proper Configuration   
    print("----- Setting Configuration -----")
    if app.config.get("ENV") == "development":
        app.config.from_object(DevelopmentConfig)
    elif app.config.get("ENV") == "production":
        app.config.from_object(ProductionConfig)
    print(" * Configuration:", app.config)
    print("----- Configuration Set -----")

    #Ensures Instance Folder Exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    aws_utilities.initiate_report_scheduler()

    opencv_thread = BackgroundThreadFactory.create('opencv')

    # this condition is needed to prevent creating duplicated thread in Flask debug mode
    if not (app.debug or os.environ.get('FLASK_ENV') == 'development') or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        print("Beginning Thread")
        opencv_thread.start()

        original_handler = signal.getsignal(signal.SIGINT)

        def sigint_handler(signum, frame):
            opencv_thread.stop()

            # wait until thread is finished
            if opencv_thread.is_alive():
                opencv_thread.join()

            original_handler(signum, frame)

        try:
            signal.signal(signal.SIGINT, sigint_handler)
        except ValueError as e:
            logging.error(f'{e}. Continuing execution...')

  
    

    task = {"opencv": "opencv"}
    logging.info(f'Received task: {task}')

    TASKS_QUEUE.put(task)


    #Route for Home
    @app.route("/", methods=['GET', 'POST'])
    def index():
        reports_data = aws_utilities.fetch_reports_data()
        report_objects = []

        for report in reports_data:
            new_report = Report(report)
            new_report.print_report()
            report_objects.append(new_report)

        report_objects.sort(key=lambda x: x.report_id)
        
        return render_template('index.html', reports_objects=report_objects)


    @app.route("/submit_email", methods=['GET', 'POST'])
    def submit_email():
        reports_data = aws_utilities.fetch_reports_data()
        report_objects = []

        for report in reports_data:
            new_report = Report(report)
            new_report.print_report()
            report_objects.append(new_report)
        
        report_objects.sort(key=lambda x: x.report_id)

        if request.method == 'POST':
            request_email = request.form['email']
            print(request_email)    
            aws_utilities.sns_subscribe(request_email)

        return render_template('index.html', reports_objects=report_objects)


    return app


if __name__ == "__main__":
    create_app().run(host="0.0.0.0", debug=False, port=8080)