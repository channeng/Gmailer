# What is Gmailer:

   Gmailer simplifies the sending standard html email reports from any Gmail account.

# Setting up:

####1. Set up your gmail account to allow less secure apps
   https://www.google.com/settings/security/lesssecureapps  
If you turned on two-factor authentication, create an app and generate a one-time password specific for the app.  
This will allow Gmailer to send emails from Gmail.

####2. Set up environment variables for Gmail account and password
   (you can skip this step if you prefer to explicitly input your username and password)

   In terminal, type:
```
export GMAIL_USER=myusername@gmail.com
export GMAIL_PWD=mysecretpassword
```
My suggestion is to set the env vars to be persistent so you don't have to type it each terminal session. You can do that by inserting the export commands in .profile in your root.

# How to use the module

####3. Create a python script in the same directory as 'Gmailer' (and this README.md)
Define the following in your script
`from mailer_module.postman import Gmailer`  
If you have set the env vars, then also include:
```
import os
username = os.environ["GMAIL_USER"]
password = os.environ["GMAIL_PWD"]
```

####4. Create the report tables that you would like to email

As arguments, Gmailer class accepts the following:

#####1. gmail_credentials: Dictionary of username and password
```
    {"username":"my_username@gmail.com",
    "password":"my_password"}
```

#####2. recipient_list: list of strings 
```
    ["user1@gmail.com","user2@gmail.com", ...]
```

#####3. message_params: Dictionary of message parameters
```
    {"from_name":"John",
    "subject":"This are my family members",
    "header":"My Family"}
```

Following the above arguments,

#####4. any number of *args dictionaries following the format below:
- Dictionaries, consisting of the following keywords:
  1. table_title : string  (required - leave "" if none)
  2. table_link : url string  (required - leave "" if none)
  3. generate_sn : Boolean  (required - True or False)
  4. generate_summary: integer (required -'Column number that you want to generate a summary of')
  5. table : List of lists (required - A 2-D array containing headers)
    * Each table must be a list of lists, where the first list element must contain the headers of the table
    * Each list within the list must have the same number of elements
    * All urls within the table will automatically be converted into links, and displayed as "Link"
      * Urls must begin with 'http://' or 'https://', followed by a domain/localhost/ip address
    * Table will be generated in the same order as the list

5. Execute Gmailer

Initiate the Gmailer class object
`Mailer = Gmailer(username,password,recipient_list,dict_1,dict_2,dict_3...)`
Call the send_mail method
`Mailer.send_mail()`

Full Example.
```
my_gmailer = Gmailer(
  {
    "username":"my_username@gmail.com",
    "password":"my_password"
  },
  ["user1@gmail.com","user2@gmail.com"],
  {
    "from_name":"John"
    "subject":"This are my family members",
    "header":"My Family"
  },
  {
    "table_title":"Family Members",
    "generate_sn":False,
    "generate_summary": 3
    "table":
      [
        ["s/n","Name","Gender","Age"],
        [1,"John","M","23"],
        [2,"Lucy","F","13"],
        [3,"Jack","M","64"]
      ]
  }
)

my_gmailer.send_mail()
```

Gmailer will output the following in the email:
```
------------------------------
From:    John "my_username@gmail.com"
To:      user1@gmail.com; user2@gmail.com;
Subject: This are my family members
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

Table link
```

6. Templates and styling
- Email templates should be named "template.html" and kept within mailer module.
- CSS Styling can be applied within the template header:
- All tables generated are automatically classed as 'table_wrapper'
- All table titles generated are automatically classed as 'title_wrapper'