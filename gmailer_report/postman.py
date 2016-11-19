#!/usr/bin/env python
import smtplib
from .html_generator.generate_html import Generate_email
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Gmailer(object):
    def __init__(self, gmail_credentials):
        # Login credentials
        self.gmail_user = str(gmail_credentials["username"])
        self.gmail_pwd = str(gmail_credentials["password"])

    def send_mail(self, recipients_list, message_params, *table_dicts):
        gmail_user = self.gmail_user
        gmail_pwd = self.gmail_pwd
        # Message parameters
        from_name = str(message_params["from_name"])
        recipients = recipients_list
        subject = str(message_params["subject"])
        # Email parameters
        header = str(message_params["header"])
        unsubscribe_mail_to = str(message_params["unsubscribe_mail_to"])
        list_of_table_dicts = []
        for table_dict in table_dicts:
            list_of_table_dicts += [table_dict]

        # Create message container - the correct MIME type is multipart/alternative.
        message = MIMEMultipart('alternative')
        message['Subject'] = subject
        message['From'] = from_name

        to_who = recipients if type(recipients) is list else [recipients]
        message['To'] = ", ".join(to_who)

        # Create the body of the message (a plain-text and an HTML version).
        text = subject   # Text generation not supported in this module yet. Subject used as placeholder
        html = str(
            Generate_email(
                header,
                list_of_table_dicts,
                unsubscribe_mailto=unsubscribe_mail_to
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

        # Checks if HTML is generated. Returns "None" if no results found.
        if html == "None":
            print 'Report - NO RESULTS found %-20s | From: %-15s  | To : %s' % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), from_name, recipients)
        else:
            try:
                # print "Connecting to SMTP"
                server = smtplib.SMTP('smtp.gmail.com', 587)
                # print "Connected. Establishing ping.."
                server.ehlo()
                # print "ehlo"
                server.starttls()
                server.login(gmail_user, gmail_pwd)
                server.sendmail(gmail_user, recipients, message.as_string())
                server.close()
                print 'Report - SENT             %-20s | From: %-15s  | To : %s' %(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), from_name, recipients)
            except:
                print 'Report - FAILED           %-20s | From: %-15s  | To : %s' %(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), from_name, recipients)

def test():
    from getpass import getpass
    # Initialize Gmailer with login credentials
    username = raw_input("Gmail username    : ")
    password = getpass("Gmail app password: ")
    gmail_credentials = {
        "username": username,
        "password": password
    }

    recipients_list = [username]
    message_params = {
        "from_name": "John",
        "subject": "This are my family members",
        "header": "My Family",
        "unsubscribe_mail_to": "no-reply@ancentry.com?Subject=Unsubscribe"
    }
    table_1 = {
        "table_title": "Family Members",
        "table_text": "http://www.ancestry.com/",  # <- Url in table text is automatically converted to link
        "generate_sn": False,
        "generate_summary": "gender",
        "table":
            [
                ["s/n", "Name", "Gender", "Age"],# <- Headers on the first row
                [1, "John", "M", "23"],
                [2, "Lucy", "F", "13"],
                [3, "Jack", "M", "64"]
            ]
    }
    table_2 = {
        "table_title": "",  # <- Note: Leave "" if not table title to be generated
        "table_text": "Who knew a kid from Queens was descended from royalty?", # <- Note: Leave "" if not table title to be generated
        "generate_sn": False,
        "generate_summary": "",     # <- Note: Leave "" if not summary to be generated
        "table":
            [
                ["s/n", "Name", "Gender", "Age"],
                [1, "John", "M", "23"],
                [2, "Lucy", "F", "13"],
                [3, "Jack", "M", "64"],
                [4, "Jack", "M", "64"]
            ]
    }

    my_gmailer = Gmailer(gmail_credentials)
    my_gmailer.send_mail(
        recipients_list,
        message_params,
        # You can input as many tables as you like, with the following table-dict format
        table_1,
        table_2
    )
