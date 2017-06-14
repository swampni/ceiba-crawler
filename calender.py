
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

u_id = []


def main(olduser, given_events, calendar_id):
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    if bool(olduser) == False:
        for given_event in given_events:

            if 'recurrence' in given_event.keys():
                temp = given_event['description']
                given_event['description'] = []
                e = service.events().insert(calendarId=calendar_id,
                                            sendNotifications=True, body=given_event).execute()
                given_event['description'] = temp
                print('''*** %r event added, Start: %s''' %
                      (cmd(e['summary']), e['start']['dateTime']))
                sub_event(service, calendar_id, given_event, e, 'description')
            else:
                e = service.events().insert(calendarId=calendar_id,
                                            sendNotifications=True, body=given_event).execute()
                print('''*** %r event added, Start: %s''' %
                      (cmd(e['summary']), e['start']['dateTime']))
        return
    else:
        new_events = []
        # u_id=[]
        for given_event in given_events:
            page_token = None
            updated = False

            # hw
            while True:
                known_events = service.events().list(calendarId=calendar_id,
                                                     pageToken=page_token).execute()

                for known_event in known_events['items']:
                    if 'recurringEventId' in known_event.keys():
                        continue
                    elif 'recurrence' not in given_event.keys():  # Then it is homework
                        if given_event['summary'] == known_event['summary']:
                            for key in given_event.keys():

                                if key == 'reminders':
                                    if given_event[key]['overrides'] == []:
                                        if olduser == 2:
                                            try:
                                                given_event[key]['overrides'] = known_event[
                                                    key]['overrides']
                                            except KeyError:
                                                del given_event[
                                                    key]['overrides']
                                        elif olduser == 1:
                                            del given_event[key]['overrides']

                                inform(given_event, known_event, key)

                            u = service.events().update(calendarId=calendar_id,
                                                        eventId=known_event['id'], body=given_event).execute()
                            print(cmd(u['summary']), ' sucessfully updated')
                            u_id.append(u['id'])
                            updated = True
                            break
                    else:  # it is class
                        if given_event['summary'] == known_event['summary'] and given_event['start']['dateTime'] == known_event['start']['dateTime']:
                            for key in given_event.keys():

                                if key == 'description':
                                    sub_event(service, calendar_id,
                                              given_event, known_event, key)
                                    # print(known_event)
                                    continue
                                else:
                                    inform(given_event, known_event, key)

                            del given_event['description']
                            u = service.events().update(calendarId=calendar_id,
                                                        eventId=known_event['id'], body=given_event).execute()
                            print(cmd(u['summary']), ' sucessfully updated')
                            u_id.append(u['id'])
                            updated = True
                            break
                    if updated == True:
                        break
                if updated == True:
                    break
                page_token = known_events.get('nextPageToken')
                if not page_token:
                    break
            if updated == False:  # no correspoding events
                #print('new event')
                main(0, [given_event], calendar_id)

        return u_id


def sub_event(service, calendar_id, given_event, main_event, key):
    page_token = None
    while True:
        subevents = service.events().instances(calendarId=calendar_id,
                                               eventId=main_event['id'], pageToken=page_token).execute()
        sorted_subevents = sorted(subevents['items'], key=lambda k: k['id'])
        for x in range(18):
            # print(sorted_subevents[x])
            inform({key: given_event[key][x]}, sorted_subevents[x], key)
            sorted_subevents[x][key] = given_event[key][x]
            u = service.events().update(calendarId=calendar_id, eventId=sorted_subevents[
                x]['id'], body=sorted_subevents[x]).execute()
            u_id.append(u['id'])
        page_token = subevents.get('nextPageToken')
        if not page_token:
            return


def inform(given_event, known_event, key):
    if given_event[key] == '' or given_event[key] == ' ':
        if key not in known_event or known_event[key] == ' ':  # 空對空  都是空
            pass
        else:  # 空對有  刪除
            print('deleted attribute', key, ':', cmd(known_event[key]))
    elif key not in known_event:  # 有對空  增加
        print('new attribute--', key, ':\n', cmd(given_event[key]))
    elif given_event[key] != known_event[key]:  # 有對有，不一樣  更動
        print(key, 'attribute of ', cmd(known_event['summary']), ' at ', known_event['start'][
              'dateTime'], ' is changed from ', cmd(known_event[key]), 'to', cmd(given_event[key]))
    else:  # 有對有，一樣  不變
        pass


def deleteMe(calendar_id, confirmed):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    page_token = None
    while True:
        events = service.events().list(calendarId=calendar_id,
                                       pageToken=page_token).execute()
        for event in events['items']:
            if 'recurringEventId' in event:
                continue
            if event['id'] not in confirmed:
                print('deleted ', cmd(event['summary']),
                      ' at ', event['start']['dateTime'])
                e = service.events().delete(calendarId=calendar_id,
                                            eventId=event['id']).execute()
        page_token = events.get('nextPageToken')
        if not page_token:
            break


def make_calender(user):
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
        print('新的使用者', cmd(user), '，您好')
        calendar = {
            'summary': 'NTUceiba',
            'timeZone': 'Asia/Taipei'
        }
        created_calendar = service.calendars().insert(body=calendar).execute()
        return [created_calendar['id'], 0]
    else:
        print('使用者', cmd(user), '，您好')
        return [summary_list['NTUceiba'], 1]


def cmd(text):
    return text.encode(sys.stdin.encoding, "replace").decode(sys.stdin.encoding)
