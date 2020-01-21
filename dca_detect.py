#!/usr/bin/env python3
''' DCA Detect
This script will with a provided case number, year, and district court email you
with the updates to the case you are interested in as an inline HTML table. You
must also provide an email in which it can send notification emails from, along
with the email you wish for it to be sent to.
Copyright 2018 (c) Logan Lopez
'''

import requests
import smtplib
from email.headerregistry import Address
from email.message import EmailMessage
import logging
from datetime import datetime, date
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format='%(levelname)-8s %(message)s')

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0'}

def send_email(table, subject):
    # Table header
    htmlTable = '<table><tr><th>Date Docketed</th><th>Description</th><th>Date Due</th><th>Filed</th><th>Notes</th></tr>'
    # Creating the actual table
    for r in table:
        htmlTable += '<tr>'
        for t in r:
            htmlTable += '<td>' + t + '</td>'
        htmlTable += '</tr>\n'
    htmlTable += '</table>'
    logging.debug('Attempting to connect')
    # IF YOU ARE USING GMAIL: make sure to enable 'app passwords'
    mailserver = smtplib.SMTP('smtp.gmail.com', 587) # change to your mail server
    mailserver.ehlo()
    logging.debug('Sending first EHLO')
    mailserver.starttls()
    logging.debug('Setting up secure connection')
    mailserver.ehlo()
    logging.debug('Sending second EHLO')
    username = 'email@gmail.com' # change to your email account
    password = 'password' # change to your password
    mailserver.login(username, password)
    logging.debug('Authenticating to server')

    # Create the base text message.
    msg = EmailMessage()
    msg['Subject'] = "Notification: " + subject
    msg['From'] = Address("Notification System", "email", "gmail.com") # Change this line to notification address
    msg['To'] = (Address("User", "you", "yahoo.com")) # change this line to your name and email
    msg.set_content( '''
    UPDATE NOTIFICATION\n
    Hello,\n
    Please find in the HTML version an update on the current status of the enclosed subject.\n
    ''')

    #Add the html version.  This converts the message into a multipart/alternative
    #container, with the original text message as the first part and the new html
    #message as the second part.
    msg.add_alternative('''
    <center><h1>Notification</h1></center>
    <p>Hello,\n
    Please find below an update on the current status of the enclosed subject.</p>
    <br />
    {0}
    <br />
    <i>DCA Detect</i>
    '''.format(htmlTable), subtype='html')

    mailserver.send_message(msg)
    mailserver.quit()
    logging.debug('Message sent')

def check_diff(url, filename):
    with open(filename + "_lastchk.txt", "r+") as stamp:
        oldDate = datetime.strptime(stamp.readline().strip(), "%Y-%m-%d")
        oldDate = oldDate.date()
        session = requests.session()
        site = session.get(url, headers=headers)
        soup = BeautifulSoup(site.content, "lxml")
        docket = soup.find_all('table')[6] # find 
        table = []
        # strips out extra space and makes 2d array from docket table
        for rows in docket.find_all('tr'):
            row = []
            for t in rows.find_all('td'):
                row.append(t.text.strip())
            table.append(row)
        result = []
        # checks if anything is greater than the date put in the _lastchk.txt file
        for r in table:
            if len(r) > 0:
                resDt = datetime.strptime(r[0], "%m/%d/%Y")
                dt = resDt.date()
                if(dt > oldDate):
                    result.append(r)
        # if we have any updates, then send off to send_email for notification
        if(len(result) > 0):
            logging.debug("website updated")
            send_email(result, filename)
            resDt = datetime.strptime(result[len(result) - 1][0], "%m/%d/%Y")
            dt = resDt.date()
            stamp.seek(0)
            stamp.write(dt.isoformat())
        else:
            logging.debug("website unchanged")


check_diff('http://onlinedocketsdca.flcourts.org/DCAResults/CaseByYear?CaseYear=CASE_YEAR&CaseNumber=CASE_NUM&Court=COURT_NUM', '2dca') # Replace CASE_YEAR, CASE_NUM, and COURT_NUM
