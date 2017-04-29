
from __future__ import print_function
import httplib2
import os
import sys

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'driver/client_secret.json'
if hasattr(sys, '_MEIPASS'):
    CLIENT_SECRET_FILE_ = os.path.join(sys._MEIPASS, CLIENT_SECRET_FILE)
else:
    CLIENT_SECRET_FILE_ = CLIENT_SECRET_FILE

APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(
        credential_dir, 'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE_, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def main(EVENTs, calendar_id):
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    for EVENT in EVENTs:
        e = service.events().insert(calendarId=calendar_id,
                                    sendNotifications=True, body=EVENT).execute()
        print('''*** %r event added:
        Start: %s
        fileurl: %s
    ''' % (e['summary'].encode('utf-8'),
           e['start']['dateTime'], e['description']))


def deleteMe(calendar_id):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    page_token = None
    while True:
        events = service.events().list(calendarId=calendar_id,
                                       pageToken=page_token).execute()
        for event in events['items']:
            e = service.events().delete(calendarId=calendar_id,
                                        eventId=event['id']).execute()
        page_token = events.get('nextPageToken')
        if not page_token:
            break
    print('刪光光了')


def make_calender():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    summary_list = {}
    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            summary_list.update(
                {calendar_list_entry['summary']: calendar_list_entry['id']})
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break
    if 'NTUceiba' not in summary_list.keys():
        calendar = {
            'summary': 'NTUceiba',
            'timeZone': 'Asia/Taipei'
        }
        created_calendar = service.calendars().insert(body=calendar).execute()
        return created_calendar['id']
    else:
        return summary_list['NTUceiba']


if __name__ == '__main__':
    cal_id = make_calender()
    deleteMe(cal_id)
