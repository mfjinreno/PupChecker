import difflib
import SendEmail
import re
import HTMLParser


current_file = open("Adoptable Animals.html", "r")
new_file = open("Adoptable Animals Mod.html", "r")

email = ""
for line in difflib.unified_diff(str(current_file.readlines()), str(new_file.readlines())):
     if not re.match(r'-', line):
          email += str(line.strip('+-!'))

name_list = HTMLParser.parse_html(email)
SendEmail.authorize_and_send_message(str(name_list))

print(name_list)
