# What is Gmailer:

   Gmailer simplifies the dispatch of standard html email reports that includes tabular data from any Gmail account.

## Installation
```bash
pip install gmailer_report
```

## Setting up:

####Set up your gmail account to allow less secure apps
- To allow Gmailer to send emails from Gmail.
  - For users who turned on two-factor authentication, please create an app-specific password. (Link to generate app-specific password)[https://security.google.com/settings/security/apppasswords]
  - For users who have not turned on two-factor authentication, please register app to allow permission as less secure apps. (Link to setup)[https://www.google.com/settings/security/lesssecureapps]
  

####Set up environment variables for Gmail account and password (Recommended)
   *You can skip this step if you prefer to explicitly input your username and password*
   
   In terminal, type:
```bash
export GMAIL_USER=myusername@gmail.com
export GMAIL_PWD=mysecretpassword
```

   It is recommended to set the env vars to be persistent across each terminal session. You can do that by inserting the export commands above in .profile file in your root directory.

## How to use the module

####Create a python script in the same directory as 'Gmailer' (and this README.md)
Define the following in your script
`from mailer_module.postman import Gmailer`  
If you have set the env vars, then also include:
```python
import os
username = os.environ["GMAIL_USER"]
password = os.environ["GMAIL_PWD"]
```

####Create the report tables that you would like to email

Having set up app access permissions in your Gmail account, initialize Gmailer with your gmail credentials:

#####1. gmail_credentials: Dictionary of username and password
```python
{
    "username": "my_username@gmail.com",
    "password": "my_gmail_app_password"
}
```

You can now send emails with Gmailer.send_mail(), which requires the following arguments respectively:

#####1. recipient_list: list of strings 
```python
[
    "user1@gmail.com",
    "user2@gmail.com", 
    ...
]
```

#####2. message_params: Dictionary of message parameters
```python
{
    "from_name": "John",
    "subject": "This are my family members",
    "header": "My Family"
}
```

Following the above arguments,

#####3. any number of *args dictionaries following the format below:
- Dictionaries, consisting of the following keywords:
  1. **table_title**: string  (required - leave "" if none)
  2. **table_text**: string  (required - leave "" if none)
    * table_text appears at the bottom of the table and may appear as one of either 2 forms:
      * As a link : if a url string is provided
      * As a text paragraph : if no url string is provided
  3. **generate_sn**: Boolean  (required - True or False)
  4. **generate_summary**: string (required - leave "" if none)
    * Header name of column for which you would like to generate a summary of
  5. **table**: List of lists (required - A 2-D array containing headers)
    * Each table must be a list of lists, where the first list element must contain the headers of the table
    * Each list within the list must have the same number of elements
    * All urls within the table will automatically be converted into links, and displayed as "Link"
      * Urls must begin with 'http://' or 'https://', followed by a domain/localhost/ip address
    * Table will be generated in the same order as the list

####Execute Gmailer

Initiate the Gmailer class object with your gmail_credentials above
```python
Mailer = Gmailer(gmail_credentials)
```
Call the send_mail method
```python
Mailer.send_mail(recipient_list, message_params, table_dict_1, table_dict_2, ...)
```

##Full Example
```python
from gmailer_report import Gmailer

# Gmail credentials
username = "my_username@gmail.com"
password = "secret_gmail_app_pwd"
gmail_credentials = {
    "username": username,
    "password": password
}

# List of recipients
recipients_list = ["user1@gmail.com", "user2@gmail.com"]

# Message parameters
message_params = {
    "from_name": "John"
    "subject": "A table of my family members",
    "header": "My Family",
    "unsubscribe_mail_to": "no-reply@ancentry.com?Subject=Unsubscribe"
}

# Table dictionaries
table_1 = {
    "table_title": "Family Members",
    "table_text": "http://www.myfamily.com/",  # <- Url in table text is automatically converted to link
    "generate_sn": False,
    "generate_summary": "gender",
    "table":
        [
            ["s/n", "Name", "Gender", "Age"],   # <- Headers on the first row
            [1, "John", "M", "23"],
            [2, "Lucy", "F", "13"],
            [3, "Jack", "M", "64"]
        ]
}

# Initialize Gmailer with gmail_credentials
my_gmailer = Gmailer(gmail_credentials)

# Send mail with recipient list, message parameters and table dictionaries
my_gmailer.send_mail(
    recipients_list,
    message_params,
    # You can input as many tables as you like, with the following table-dict format
    table_1
)
```

Gmailer will output the following in the email:
```
From:    John "my_username@gmail.com"
To:      user1@gmail.com; user2@gmail.com;
Subject: A table of my family members
```
```
------------------------------
          MY FAMILY
------------------------------
FAMILY MEMBERS
Total: 3  | M: 2 | F: 1 |

s/n    Name    Gender   Age
 1     John      M      23
 2     Lucy      F      13
 3     Jack      M      64

Link <http://www.myfamily.com>
```
To see the package in action, run the following:
```python
from gmailer_report import test

test()
```

##Templates and styling
- Email templates should be named "email.html" and kept within the following directory: `mailer_module/html_generator/template`
- Email templates must be tagged with 2 placeholders: 
  - These placeholders will be replaced with the html generated by the package
  - In the header of the email template, insert:
```
*<-- EMAIL HEADER HERE -->*
```
  - In the body of the email template, include:
```
*<-- TABLES HERE -->*
```
- CSS Styling can be applied within the template header:
  - All tables generated are automatically classed as: `class=table_wrapper`
  - All table titles generated are automatically classed as: `class=title_wrapper`
- Note that some email clients do not load CSS table styling within the template headers.
    - As of last test, Gmail browser client does not load the CSS styling, but it works perfect on Apple iphone mail
    - TO_DO : apply css styling inline

threaded_bq_dump_data - For running postgres to BQ imports in threads.