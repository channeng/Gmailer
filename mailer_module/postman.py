#!/usr/bin/env python
import smtplib
import os
from html_generator.generate_html import Generate_email
import datetime
import csv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText 

class Gmailer(object):
  def __init__(self,gmail_credentials,recipients_list,message_params,*table_dicts):
    # Login credentials
    self.gmail_user = str(gmail_credentials["username"])
    self.gmail_pwd = str(gmail_credentials["password"])
    # Message parameters
    self.from_name = str(message_params["from_name"])
    self.recipients = recipients_list
    self.subject = str(message_params["subject"])
    # Email parameters
    self.header = str(message_params["header"])
    self.tables = []
    for table_dict in table_dicts:
      self.tables += [table_dict]
      
  def send_mail(self):
    gmail_user = self.gmail_user
    gmail_pwd = self.gmail_pwd
    recipients = self.recipients
    header = self.header
    list_of_table_dicts = self.tables
    
    # Create message container - the correct MIME type is multipart/alternative.
    message = MIMEMultipart('alternative')
    message['Subject'] = self.subject
    message['From'] = self.from_name
    
    to_who = recipients if type(recipients) is list else [recipients]
    message['To'] = ", ".join(to_who)

    # Create the body of the message (a plain-text and an HTML version).
    text = self.subject   # Text generation not supported in this module yet. Subject used as placeholder
    html = str(
      Generate_email(
        header,
        list_of_table_dicts
      ).html()
    )
    
    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    
    message.attach(part1)
    message.attach(part2)
    # print "Attached message"
    # Prepare actual message
    # message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
    #     """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    if html == "None": # Checks if HTML is generated. Returns "None" if no results found.
      print 'Report - NO RESULTS found %-20s | From: %-15s  | To : %s' %(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),self.from_name,self.recipients)
    else:
      try:
        # print "Connecting to SMTP"
        server = smtplib.SMTP('smtp.gmail.com',587) #587
        # print "Connected. Establishing ping.."
        server.ehlo()
        # print "ehlo"
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(gmail_user, recipients, message.as_string())
        server.close()
        print 'Report - SENT             %-20s | From: %-15s  | To : %s' %(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),self.from_name,self.recipients)
      except:
        print 'Report - FAILED           %-20s | From: %-15s  | To : %s' %(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),self.from_name,self.recipients)

if __name__ == '__main__':
  my_gmailer = Gmailer(
    # Your login credentials
    {
      "username":os.environ["GMAIL_USER"],
      "password":os.environ["GMAIL_PWD"]
    },
    # Recipient list
    [os.environ["GMAIL_USER"],
    # Message parameters
    {
      "from_name":"John",
      "subject":"This are my family members",
      "header":"My Family"
    },
    # You can input as many tables as you like, with the following table-dict format
    # Table 1
    {
      "table_title":"Family Members",
      "generate_sn":False,
      "generate_summary": "gender",
      "table":
        [
          ["s/n","Name","Gender","Age"], # <- Headers on the first row
          [1,"John","M","23"],
          [2,"Lucy","F","13"],
          [3,"Jack","M","64"]
        ]
    },
    # Table 2
    {
      "table_title":"", # <- Note: Leave "" if not table title to be generated
      "generate_sn":False,
      "generate_summary": "", # <- Note: Leave "" if not summary to be generated
      "table":
        [
          ["s/n","Name","Gender","Age"],
          [1,"John","M","23"],
          [2,"Lucy","F","13"],
          [3,"Jack","M","64"],
          [4,"Jack","M","64"]
        ]
    }
  )

  my_gmailer.send_mail()