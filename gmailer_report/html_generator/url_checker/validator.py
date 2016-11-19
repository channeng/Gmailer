import re

class check_if_url(object):
  def __init__(self):
    pass
  
  def if_url_convert(self,any_string):
    url_to_check = str(any_string)
    # unicode letters range (must be a unicode string, not a raw string) 
    regex = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if url_to_check is not None and regex.search(url_to_check):
      return '<a href="'+url_to_check+'" target="_blank">Link</a>'
    else:
      return url_to_check
      
if __name__ == '__main__':
  test_url = raw_input("What string would you like to test?\n")
  check_url = check_if_url()
  print check_url.if_url_convert(test_url)