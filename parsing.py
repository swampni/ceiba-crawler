from datetime import date 
from datetime import timedelta as delta
####parsing the webpage
week = {
	'星期一':1,
	'星期二':2,
	'星期三':3,
	'星期四':4,
	'星期五':5,
	'星期六':6,
	'星期天':7,
	'星期日':7
}

classTime = {
	'0':['07:10','08:00'],
	'1':['08:10','09:00'],
	'2':['09:10','10:00'],
	'3':['10:20','11:10'],
	'4':['11:20','12:10'],
	'5':['12:20','13:10'],
	'6':['13:20','14:10'],
	'7':['14:20','15:10'],
	'8':['15:30','16:20'],
	'9':['16:30','17:20'],
	'10':['17:30','18:20'],
	'A':['18:25','19:15'],
	'B':['19:20','20:10'],
	'C':['20:15','21:05'],
	'D':['21:10','22:00']
}
def parse(soup, title):
	name = soup.body.div.div.find(id='section').div.table.tbody.find_all('tr')[0].td.string.lstrip().rstrip()
	deadline = soup.body.div.div.find(id='section').div.table.tbody.find_all('tr')[7].td.string.lstrip().rstrip()
	link_tag = soup.body.div.div.find(id='section').div.table.tbody.find_all('tr')[2].td.a
	if link_tag:
		link = link_tag.get('href')
	else:
		link = 'no file'
	if deadline[-2:] == '24':
		time = deadline[:-1].replace(' ', 'T')+"3:59:59"
	else:
		time = deadline.replace(' ', 'T')+":00:00"
	description = '相關網址:'+'\n'+link
	payload = { 
			'summary':title+name,
			'start':{'dateTime': time, 'timeZone':'Asia/Taipei'},
			'end':{'dateTime':time, 'timeZone':'Asia/Taipei'},
			'description': description,
			'reminders':{
    					'useDefault': False,
    					'overrides':[
      								{'method': 'popup', 'minutes': 24 * 60},
      								{'method': 'popup', 'minutes': 24 * 60 * 2},
    								],
 						 },
			'colorId':'1'
			}
	return payload

def parse_time(course_time, title):
	split_course_time = course_time.split()
	day = delta(days =1)
	now = date.isoweekday(date.today())
	cTime = []
	payloads = []
	for i in range(0,len(split_course_time),2):		
		distance = (week[split_course_time[i]]-now+7)%7
		start_day = date.today()+distance*day
		num = split_course_time[i+1].split(',')
		start_time = start_day.isoformat()+'T'+classTime[num[0]][0]+":00"
		end_time = start_day.isoformat()+'T'+classTime[num[-1]][1]+":00"		
		payload = {
				'summary':title,
				'start': {'dateTime': start_time, 'timeZone':'Asia/Taipei'},
				'end':{'dateTime':end_time, 'timeZone':'Asia/Taipei'},
				'recurrence': ['RRULE:FREQ=WEEKLY;UNTIL=20170701T170000Z'],
				'description': ' ',
				'colorId':'2'
				}
		payloads.append(payload)
	return payloads





