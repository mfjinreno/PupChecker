from __future__ import print_function

import base64
from email.mime.text import MIMEText

import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
from oauth2client import file

try:
    import argparse

    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = "https://mail.google.com/"
CLIENT_SECRET_FILE = 'credentials.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'
url = "https://ws.petango.com/webservices/adoptablesearch/wsAdoptableAnimals.aspx?species=Dog&gender=A&agegroup=UnderYear&location=&site=&onhold=A&orderby=name&colnum=3&css=http://ws.petango.com/WebServices/adoptablesearch/css/styles.css&authkey=io53xfw8b0k2ocet3yb83666507n2168taf513lkxrqe681kf8&recAmount=&detailsInPopup=No&featuredPet=Include&stageID=&wmode=opaque"


def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


# create a message
def CreateMessage(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': ((base64.b64encode(message.as_string().encode('utf-8')).decode('utf-8')).replace("+","-")).replace("/","_")}




# send message
def SendMessage(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        # print 'Message Id: %s' % message['id']
        return message
    except Exception as e:
        print("Exception encountered: " + str(e))


def authorize_and_send_message(additional_contents, email, source_email):

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    msg_body = "A new pup has been posted to Wright way. \n\nList of pup names added: " + str(additional_contents) + "\nLink to pups:" + str(url)

    message = CreateMessage(source_email, email, "New Pup Alert!", msg_body)

    SendMessage(service, "me", message)


if __name__ == '__main__':
    authorize_and_send_message()
