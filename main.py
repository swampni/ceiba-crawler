from timeit import default_timer as timer
start = timer()
import crawling
import calender
import parsing
import getpass
from bs4 import BeautifulSoup as bs
user_name = input('請輸入ceiba帳號')
password = getpass.getpass('請輸入ceiba密碼')
try:
    c = crawling.Crawler(user_name, password)
except crawling.UserNamePassWordError:
    print('Wrong username or password')
    user_name = input('請輸入ceiba帳號')
    password = getpass.getpass('請輸入ceiba密碼')
    c = crawling.Crawler(user_name, password)
for course in c.courses:
    c.get_homework(course)
c.halt_browser()
one = timer()
cal_id = calender.make_calender()
for course in c.courses:
    calender.main((parsing.parse(bs(page, 'html.parser'), course[
                  1]) for page in course[3]['homework']), cal_id)
    calender.main(parsing.parse_time(course[2], course[1]), cal_id)

print('執行完畢')
end = timer()
print(end - start, one-start,  end-one)
