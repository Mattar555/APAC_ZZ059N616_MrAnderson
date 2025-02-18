import os
import re
import time
import smtplib
import threading
import panel as pn
from dotenv import load_dotenv
from crew import SalesOnboarding
from crew import chat_interface
from email.mime.text import MIMEText
from email.message import EmailMessage
#from sales_onboarding import SalesOnboarding
#from sales_onboarding import chat_interface
from crewai.agents.agent_builder.base_agent_executor_mixin import CrewAgentExecutorMixin
load_dotenv()

user_input = None
crew_started = False

pn.extension(design='native')
# Probably the most important piece of code can be found below..
pn.config.theme = 'dark'


def get_representative_name():
    seller_info = ""
    with open("db-out.txt", "r") as seller:
        seller_info = seller.read()
    return re.search(r'is(.*?)\.', seller_info).group(1).strip()
    #first_and_last_name = seller_info.split()[-2:]
    #full_name = ''.join(first_and_last_name)
    #full_name = full_name[:-1]
    #return full_name
    

def set_meeting_with_representative(rep_email_address):
    #message = MIMEText(u'<a href="www.google.com">Meeting Link Here!!</a>','html')
    message = MIMEText(u'The new seller would like to schedule a handover meeting with you, looks like Wednesday morning works best for the both of you according to your Calendars: <a href="www.google.com">Meeting Link Here!!</a>','html')
    message['Subject'] = 'Handover session - Meeting Link in Body'
    message['From'] = 'MrAnderson@MrAnderson.agent'
    message['To'] = rep_email_address
    smtp_server = smtplib.SMTP("localhost", 1025)
    smtp_server.sendmail("hello@hello.com", "goodbye@bye.com", message.as_string())
    smtp_server.quit() 

def end_transaction(self, final_answer: dict) -> str:
    global user_input
    chat_interface.send(final_answer, user="Assistant", respond=False)
    seller_name = get_representative_name()
    prompt = f"Would you like me to send a meeting invite to {seller_name}? Y/N "
    chat_interface.send(prompt, user="System", respond=False)
    while user_input == None:
        time.sleep(1)
    if user_input == "Yes":
        set_meeting_with_representative(seller_name + "@ibm.com")
        chat_interface.send("Meeting Invite Sent!", user="Assistant", respond=False)
    human_comments = user_input
    user_input = None
    return human_comments


CrewAgentExecutorMixin._ask_human_input = end_transaction


def initiate_chat(message):
    global crew_started
    crew_started = True
    try:
        inputs = {
            'topic': 'sales',
            'query': message,
            'url': 'http://localhost:8080/marwan.txt'
        }
        crew = SalesOnboarding().crew()
        result = crew.kickoff(inputs=inputs)
    except Exception as e:
        chat_interface.send(f"An error occurred: {e}", user="Assistant", respond=False)


def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    global crew_started
    global user_input
    if not crew_started:
        thread = threading.Thread(target=initiate_chat, args=(contents,))
        thread.start()
    else:
        user_input = contents

chat_interface.callback = callback

chat_interface.send(
    "Welcome! I'm your Sales Onboarding Assistant. What account(s) would you like some information on?",
    user="Assistant",
    respond=False
)

chat_interface.servable()
