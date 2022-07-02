'''
Author: Rijfas
Date: 2-Jul-2022
'''

import os.path

from os import system

from sys import platform


import base64
from email.message import EmailMessage

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/gmail.send']


def login_with_creds(credential_file_name='credentials.json', token_file_name='token.json'):
    '''login with given credentials and returns the cred object if success

    '''
    creds = None
    if os.path.exists(token_file_name):
        creds = Credentials.from_authorized_user_file(
            token_file_name, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credential_file_name, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_file_name, 'w') as token:
            token.write(creds.to_json())
    return creds


def send_mail(creds, to, subject, content):
    '''sends email to the given `to` address with given `subject` and `content`

    '''
    service = build('gmail', 'v1', credentials=creds)
    message = EmailMessage()
    message.set_content(content)
    message['To'] = to
    message['From'] = 'fccoders@gmail.com'
    message['Subject'] = subject
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    create_message = {
        'raw': encoded_message
    }
    try:
        results = service.users().messages().send(
            userId='me', body=create_message).execute()
        return (True, 'Success')
    except HttpError as error:
        return (False, error)


def read_csv(filename):
    '''Reads the given csv file as a dict of rows
    '''
    try:
        data = open(filename)

    except FileNotFoundError:
        return (False, 'File Not Found')

    lines = data.readlines()

    header = lines[0].strip().split(',')

    items = []
    for line in lines[1:]:
        d = {}
        try:
            for key, value in zip(header, line.strip().split(','), strict=True):
                d[key] = value
        except ValueError:
            return (False, 'CSV File Format Error')
        items.append(d)

    return items


def read_template_file(filename):
    try:
        file = open(filename)
        return (True, file.read())
    except FileNotFoundError:
        return (False, f'ERROR: File {filename} does not exist')


def generate_messages_from_template(template_str, data_list):
    generated_messages = []
    for data in data_list:
        message = template_str.format(**data)
        generated_messages.append(message)
    return generated_messages


def clear_screen():
    if platform == "linux" or platform == "linux2" or platform == "darwin":
        system('clear')
    elif platform == "win32":
        system('cls')
