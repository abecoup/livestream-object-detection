"""
Author(s): Henry Keena
Date: 
Release: 0.1
Description: Python Flask Frontend for EC2 Abbey Road Application 
"""

#Imports Libraries
import os
import pafy
import cv2
import json
import boto3
import time
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from boto3.dynamodb.conditions import Attr

#Imports Config Objects from Configuration File
from config import AWSConfig


"""
AWS Utilities Class
"""
class AWSUtilities:
    """
    Class Constructor
    """
    def __init__(self):
        self.credentials = AWSConfig()
        self.access_key_id = self.credentials.ACCESS_KEY_ID
        self.secret_key = self.credentials.SECRET_ACCESS_KEY
        self.session_id = self.credentials.SESSION_TOKEN
        self.region = self.credentials.REGION
        self.scheduler = BackgroundScheduler()
        self.REPORT_ID = 1
    
    """
    Fetches Alerts Data
    """
    def fetch_alerts_data(self):
        dynamodb_resource = boto3.resource('dynamodb', 
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.secret_key,
            aws_session_token=self.session_id,
            region_name=self.region
        )
        table = dynamodb_resource.Table('Alert')
        response = table.scan()
        alert_data = response['Items']
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            alert_data.extend(response['Items'])
        return alert_data

    """
    Fetches Report Data
    """
    def fetch_reports_data(self):
        dynamodb_resource = boto3.resource('dynamodb', 
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.secret_key,
            aws_session_token=self.session_id,
            region_name=self.region
        )
        table = dynamodb_resource.Table('Report')
        response = table.scan()
        alert_data = response['Items']
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            alert_data.extend(response['Items'])
        return alert_data

    """
    """
    def sns_subscribe(self, email):        
        sns_client = boto3.client('sns', 
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.secret_key,
            aws_session_token=self.session_id,
            region_name=self.region
        )
        sns_resource = boto3.resource('sns', 
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.secret_key,
            aws_session_token=self.session_id,
            region_name=self.region
        )
        crosswalk_topic = sns_resource.create_topic(Name="crosswalk-topic-8or8cq6m")
        sns_client.subscribe(TopicArn=crosswalk_topic.arn, Protocol="email", Endpoint=email)

    """
    """
    def create_report(self):
        print("Creating Report...")
        dynamodbResource = boto3.resource('dynamodb', 
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.secret_key,
            aws_session_token=self.session_id,
            region_name=self.region
        )
        alertTable = dynamodbResource.Table("Alert")
        reportTable = dynamodbResource.Table("Report")
        
        # Grab reports based on timeframe only
        now = datetime.datetime.now()
        timeframe = now - (datetime.timedelta(minutes=60))

        # Setting to epoch for easy calculations
        now = str(round(now.timestamp()))
        timeframe = str(round(timeframe.timestamp()))
    
        # Filtering alerts that have occured within timeframe
        response = alertTable.scan(FilterExpression=Attr("epoch_timestamp").between(timeframe, now))

        # Parse alerts from response
        alerts = response['Items']
        while response.get('LastEvaluatedKey'):
            response = alertTable.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            alerts.extend(response['Items'])
        
        # Create a report of alerts, put it to Report table
        if alerts:
            reportTable.put_item(Item={'report_id': self.REPORT_ID,
                                        'report': alerts
            })
            self.REPORT_ID = self.REPORT_ID + 1
            print("Report Created...")
        else:
            print("No alerts have occured within the timeframe specified.")
    
    def delete_reports(self):
        try:
            flag = False
            table_name = 'Report'
            dynamodbResource = boto3.resource('dynamodb', 
                aws_access_key_id=self.access_key_id,
                aws_secret_access_key=self.secret_key,
                aws_session_token=self.session_id,
                region_name=self.region
            )
            table = dynamodbResource.Table(table_name)
            scan = table.scan()
            while not flag:
                with table.batch_writer() as batch:
                    for each in scan['Items']:
                        batch.delete_item(
                                 Key={
                                 'report_id': each['report_id']
                                 }
                             )
                    flag = True
        except Exception as e:
           print (e)

    def initiate_report_scheduler(self):
        self.scheduler.configure(timezone='US/Eastern')
        self.scheduler.add_job(self.create_report, 'interval', minutes=3) # <-- runs create_report based on this time interval
        self.scheduler.add_job(self.delete_reports, 'interval', minutes=10) # <-- deletes all reports based on this time interval
        self.scheduler.start()