from timeit import default_timer as timer
start = timer()
import crawling
import calender
import parsing
import getpass
import os
from bs4 import BeautifulSoup as bs


    #check for same event    
    #upload new description
    #upload new event
user_name = input('請輸入ceiba帳號')
password = getpass.getpass('請輸入ceiba密碼')
flag = True
while flag:
    try:
        c = crawling.Crawler(user_name, password)
        flag = False
    except crawling.UserNamePassWordError:
        print('Wrong username or password')
        user_name = input('請輸入ceiba帳號')
        password = getpass.getpass('請輸入ceiba密碼')
for course in c.courses:
    c.get_homework(course)
c.halt_browser()
one = timer()

idnew = calender.make_calender(c.user)
cal_id = idnew[0]
olduser = idnew[1]

if bool(olduser) == True:
    yn = input('作業提醒是否需要重新設定?(Y/N)')
else:
    yn = input('作業是否需要提醒?(Y/N)')
remind = []
if yn == 'Y' or yn == 'y':
    while True :
        remind.append(input('請輸入多久之前提醒(天 = D, 小時 = H, 分鐘 = M)(可設定多次提醒),完全輸入完畢請打end\n'))
        if remind[-1] == 'end':
            del remind[-1]
            break
elif yn == 'N' or yn == 'n':
    if olduser == 1:
        olduser = 2
else:
    print('既然你不在乎那就當作不要吧')
    if olduser == 1:
        olduser = 2


for course in c.courses:
    calender.main(olduser,parsing.parse_time(course[3], course[2], course[1]), cal_id)
    confirmed =  calender.main(olduser, (parsing.parse(bs(page, 'html.parser'), remind,course[
                  1]) for page in course[4]['homework'] ), cal_id)
if bool(olduser) == False:
    calender.deleteMe(cal_id,confirmed)


    
print('執行完畢')
end = timer()
print(end - start, one-start,  end-one)
os.system('pause')
