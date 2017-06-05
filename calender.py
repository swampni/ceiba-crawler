
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

u_id=[]
def main(olduser,EVENTs, calendar_id):
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    if bool(olduser) == False:
        for EVENT in EVENTs:
            e = service.events().insert(calendarId=calendar_id,
                                        sendNotifications=True, body=EVENT).execute()
            print('''*** %r event added:
            Start: %s
            fileurl: %s
        ''' % (e['summary'].encode('utf-8'),
                e['start']['dateTime'], e['description']))
            u_id.append(e['id'])
        return
    else:
        new_events=[]
        #u_id=[]
        for given_event in EVENTs:
            page_token = None
            updated = False
            
            #hw
            while True:
                known_events = service.events().list(calendarId=calendar_id,
                                       pageToken=page_token).execute()
            
                for known_event in known_events['items']:            
                    if 'recurrence' not in given_event.keys(): #Then it is homework
                        if given_event['summary'] == known_event['summary']:
                            for key in given_event.keys():
                                
                                if key == 'reminders': 
                                    if given_event[key]['overrides'] == [] and olduser == 2:
                                        try:
                                            given_event[key]['overrides'] = known_event[key]['overrides']
                                        except KeyError:
                                            given_event[key]['overrides'] =[]


                                if given_event[key] == '' or given_event[key] == ' ':
                                    if key not in known_event or known_event[key] == ' ':    #空對空  都是空
                                        pass
                                    else :                                                   #空對有  刪除
                                        print('deleted attribute',key,':', known_event[key])
                                elif key not in known_event:                                 #有對空  增加
                                    print('new attribute',key, ':',given_event[key])
                                elif given_event[key] != known_event[key] :                  #有對有，不一樣  更動
                                    print(key, 'attribute of ', known_event['summary'],' at ',known_event['start']['dateTime'], ' is changed from ', known_event[key] ,'to',given_event[key])
                                else:                                                        #有對有，一樣  不變
                                    pass

                            u = service.events().update(calendarId=calendar_id,
                                            eventId=known_event['id'],body=given_event).execute()
                            u_id.append(u['id'])
                            updated = True
                            break
                    else: #it is class
                        if given_event['summary'] == known_event['summary'] and classtime(given_event) == classtime(known_event):
                            for key in given_event.keys():
                                if given_event[key] == '' or given_event[key] == ' ':
                                    if key not in known_event or known_event[key] == ' ':
                                        pass
                                    else:
                                        print('deleted attribute',key,':', known_event[key])
                                elif key not in known_event:
                                    print('new attribute', key,':', given_event[key])
                                elif given_event[key] != known_event[key] :
                                    print(key, 'attribute of ', known_event['summary'],' at ',known_event['start']['dateTime'], ' is changed from ', known_event[key] ,'to',given_event[key])
                                else:
                                    pass

                            u = service.events().update(calendarId=calendar_id,
                                            eventId=known_event['id'],body=given_event).execute()
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
            if updated == False: #no correspoding events
                print('new event')
                main(0, [given_event],calendar_id)
        
        return u_id
            
            #print('j',EVENT)
        




def deleteMe(calendar_id,confirmed):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    page_token = None
    while True:
        events = service.events().list(calendarId=calendar_id,
                                       pageToken=page_token).execute()
        for event in events['items']:
            if event['id'] not in confirmed:
                print('deleted ', event['summary'],' at ', event['start']['dateTime'])
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
        print('新的使用者',user,'，您好')
        calendar = {
            'summary': 'NTUceiba',
            'timeZone': 'Asia/Taipei'
        }
        created_calendar = service.calendars().insert(body=calendar).execute()
        return [created_calendar['id'],0]
    else:
        print('使用者',user,'，您好')
        return [summary_list['NTUceiba'],1]

def classtime(event):
    year = int(event['start']['dateTime'][0:4])
    month = int(event['start']['dateTime'][5:7])
    day = int(event['start']['dateTime'][8:10])
    time = event['start']['dateTime'][11:]
    time_end = event['end']['dateTime'][11:]
    return [datetime.date(year,month,day).weekday(), time, time_end]


# Print the updated date.


#if __name__ == '__main__':
#    cal_id = make_calender()
#    deleteMe(cal_id)
