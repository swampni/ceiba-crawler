from selenium import webdriver
import parsing
import calender
import sys
import os


# a crawler class that handle all the crawling of webpages
class Crawler():

    def __init__(self, user_name, password):
        driver = 'driver/chromedriver.exe'
        if hasattr(sys, '_MEIPASS'):
            self.driver = os.path.join(sys._MEIPASS, driver)
        else:
            self.driver = driver
        self.browser = webdriver.Chrome(self.driver)
        self.courses = []
        self.login(user_name, password)
        for link in self.links:
            _info = []
            self.browser.get(link)
            course_number = self.browser.current_url[32:38]
            _info.append(course_number)
            self.browser.get("https://ceiba.ntu.edu.tw/modules/index.php?csn=" +
                             str(_info[0])+"&default_fun=info&current_lang=chinese")
            self.browser.switch_to.frame('mainFrame')
            course_name = self.browser.find_element_by_xpath(
                '//body/div/div/div/div/table/tbody/tr/td').text
            course_time = self.browser.find_element_by_xpath(
                '//body/div/div/div/div/table/tbody/tr[6]/td').text
            _info.append(course_name)
            _info.append(course_time)
            _info.append({'homework': [], 'bulletin': []})
            self.courses.append(_info)

    def __len__(self):
        return self.courses.__len__()

    def __repr__(self):
        return self.courses

    def login(self, user_name, password):
        # return the link  of each courses and the logined browser
        self.browser.get("https://ceiba.ntu.edu.tw/index.php")
        self.browser.find_element_by_name("login2").submit()
        name = self.browser.find_element_by_name("user")
        pw = self.browser.find_element_by_name("pass")
        name.send_keys(user_name)
        pw.send_keys(password)
        self.browser.find_element_by_name("p1").submit()
        courses = self.browser.find_elements_by_xpath(
            '//body/div/div/table/tbody/tr')
        if not courses:
            self.halt_browser()
            raise UserNamePassWordError
        self.links = []
        for course in courses[1:-2]:
            self.links.append(course.find_element_by_tag_name(
                'a').get_attribute('href'))

    def get_homework(self, course):
        self.browser.get("https://ceiba.ntu.edu.tw/modules/index.php?csn=" +
                         str(course[0])+"&default_fun=hw&current_lang=chinese")
        try:
            self.browser.switch_to.frame('mainFrame')
            entites = len(self.browser.find_elements_by_xpath(
                '//body/div/div/div/div/table/tbody/tr'))
            for i in range(1, entites):
                self.browser.find_element_by_xpath(
                    '//body/div/div/div/div/table/tbody/tr['+str(i+1)+']/td/a').click()
                self.browser.switch_to.default_content()
                self.browser.switch_to.frame('mainFrame')
                course[3]['homework'].append(self.browser.page_source)
                self.browser.back()
                self.browser.switch_to.frame('mainFrame')
        except:
            print(course[1]+"'doesn't have a homework section")

    def get_bulletin(self, course):
        self.browser.get("https://ceiba.ntu.edu.tw/modules/index.php?csn=" +
                         str(course[0])+"&default_fun=bulletin&current_lang=chinese")
        try:
            self.browser.switch_to.frame('mainFrame')
            entites = len(self.browser.find_elements_by_xpath(
                '//body/div/div/div/div/table/tbody/tr')[1:])
            for i in range(1, entites):
                self.browser.find_element_by_xpath(
                    '//body/div/div/div/div/table/tbody/tr['+str(i+1)+']/td/a').click()
                self.browser.switch_to.default_content()
                self.browser.switch_to.frame('mainFrame')
                course[2]['bulletin'].append(self.browser.page_source)
                self.browser.back()
                self.browser.switch_to.frame('mainFrame')
        except:
            print(course[1]+"'doesn't have a bulletin section")

    def halt_browser(self):
        self.browser.quit()


class Error(Exception):
    pass


class UserNamePassWordError(Error):
    """docstring for UserNamePassWordError"""


if __name__ == '__main__':
    c = Crawler('b05507010', '######')
    c.get_homework(c.courses[1])
    # c.get_bulletin(c.courses[1])
    #print (c.courses[1][3]['homework'])
    c.halt_browser()


# 	print ss.decode('UTF-8')
#	filename = u'webpage'+unicode(sources.index(i))+'.html'
#	with open(filename, 'w') as f:
#		f.write(ss.decode('UTF-8').encode('UTF-8'))
