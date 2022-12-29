"""
Author(s): Henry Keena
Date: 
Release: 0.1
Description: Flask Configuration Class File
    Provides configuration options for both development and production environments.
    Includes Flask and SMTP server configuration options.
"""

"""
Class: DevelopmentConfig
Description: Class for Development Flask Configuration
"""
class DevelopmentConfig():
    #Flask Application Configuration Options
    DEBUG = True
    IP = '0.0.0.0'
    PORT = '8080'
    ENV = 'development'
    SECRET_KEY = ''
    #Flask Email Configurations
    MAIL_SERVER = ''
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''


"""
Class: ProductionConfig
Description: Class for Production Flask Configuration
"""
class ProductionConfig():
    #Flask Application Configuration Options
    DEBUG = False
    IP = '0.0.0.0'
    PORT = '8080'
    ENV = 'production'
    SECRET_KEY = ''
    #Flask Email Configurations
    MAIL_SERVER = ''
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''

"""
"""
class AWSConfig():
    ACCESS_KEY_ID = ''
    SECRET_ACCESS_KEY = ''
    SESSION_TOKEN = ''
    REGION = 'us-east-1'