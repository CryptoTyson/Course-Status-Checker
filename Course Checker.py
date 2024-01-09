# Disclaimer: This is for educational purposes only. I am not responsible for any misuse or damage caused by this script. Use at your own risk.

import time
import requests
from bs4 import BeautifulSoup # run 'pip install beautifulsoup4' in terminal to install
from discordwebhook import Discord # run 'pip install discordwebhook' in terminal to install


class Course:
    def __init__(self, course_id):
        self.course_id = course_id
        self.status = ""
        self.source = ""
        self.cookie = "" # Get this from your browser after logging into myUCF and going to context menu > inspect > network > select any request > headers > cookie
        self.emplid = "" # Enter your employee ID/ PID here
    def get_source_code(self):
        url = f"https://csprod-ss.net.ucf.edu/psc/CSPROD/EMPLOYEE/CSPROD/c/SA_LEARNER_SERVICES.SSR_SSENRL_CART.GBL?Page=SSR_SSENRL_CART&Action=A&ACAD_CAREER=GRAD&EMPLID={self.emplid}&INSTITUTION=UCF01&STRM=1800"

        payload = {}
        headers = {
        'Cookie': self.cookie,
        'Host': 'csprod-ss.net.ucf.edu',
        'Referer': 'https://csprod-ss.net.ucf.edu/psc/CSPROD/EMPLOYEE/CSPROD/c/SA_LEARNER_SERVICES.SSR_SSENRL_CART.GBL?Page=SSR_SSENRL_CART&Action=A&ExactKeys=Y'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        self.soruce = response.text


    # Function to check course status
    def check_course_status(self):
        soup = BeautifulSoup(self.soruce, 'html.parser')
        possible_courses = soup.find_all(string=self.course_id)

        for course in possible_courses:
            parent_tag = course.parent

            status_img = parent_tag.find_next('img')

            if status_img:
                self.status = status_img.get('alt', 'No status found')
                return self.status
        self.status = "Course not found"
        return self.status

def run(course):
    sleep_time = 300
    discord_webhook_url = "" # Enter your discord webhook url here
    discord = Discord(url= discord_webhook_url) # Create a discord webhook and enter the url here > follow this tutorial > https://10mohi6.medium.com/super-easy-python-discord-notifications-api-and-webhook-9c2d85ffced9
    i = 1
    while True:
        print(f"#{i} Checking {course}...")
        bot = Course(course)
        bot.get_source_code()
        bot.check_course_status()
        print(f"Status of {bot.course_id}: {bot.status}")
        if bot.status == "Wait List": # Change this to whatever status you want to be notified for - list of statuses: Open, Wait List, Closed
            discord.post(content=f"Status of {bot.course_id}: {bot.status}") # comment this line out if you don't want to be notified
        time.sleep(sleep_time)
        i += 1


run("CAP 6614-0001") # Change this to whatever course you want to check

