import os
from mailer_module.postman import Gmailer

my_gmailer = Gmailer(
    # Your login credentials
    {
      "username":os.environ["GMAIL_USER"],
      "password":os.environ["GMAIL_PWD"]
    },
    # Recipient list
    [os.environ["GMAIL_USER"]],
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
      "table_text":"http://www.ancestry.com/",  # <- Url in table text is automatically converted to link
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
      "table_text":"Who knew a kid from Queens was descended from royalty?", # <- Note: Leave "" if not table title to be generated
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