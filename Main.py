import hashlib
import urllib.request
import random
import time
import difflib
import SendEmail
import HTMLParser
import re

# url to be scraped
puppies_url = "https://ws.petango.com/webservices/adoptablesearch/wsAdoptableAnimals.aspx?species=Dog&gender=A&agegroup=UnderYear&location=&site=&onhold=A&orderby=name&colnum=3&css=http://ws.petango.com/WebServices/adoptablesearch/css/styles.css&authkey=io53xfw8b0k2ocet3yb83666507n2168taf513lkxrqe681kf8&recAmount=&detailsInPopup=No&featuredPet=Include&stageID=&wmode=opaque"
adult_dogs_url = "https://ws.petango.com/webservices/adoptablesearch/wsAdoptableAnimals.aspx?species=Dog&gender=A&agegroup=OverYear&location=&site=&onhold=A&orderby=name&colnum=3&css=http://ws.petango.com/WebServices/adoptablesearch/css/styles.css&authkey=io53xfw8b0k2ocet3yb83666507n2168taf513lkxrqe681kf8&recAmount=&detailsInPopup=No&featuredPet=Include&stageID=&wmode=opaque"
# time between checks in seconds
sleeptime = 300


def get_hash(url):
    # random integer to select user agent
    randomint = random.randint(0, 7)

    # User_Agents
    # This helps skirt a bit around servers that detect repeated requests from the same machine.
    # This will not prevent your IP from getting banned but will help a bit by pretending to be different browsers
    # and operating systems.
    user_agents = [
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
        'Opera/9.25 (Windows NT 5.1; U; en)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.142 Safari/535.19',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:8.0.1) Gecko/20100101 Firefox/8.0.1',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.151 Safari/535.19'
    ]

    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', user_agents[randomint])]
    response = opener.open(url)
    the_page = response.read()

    return hashlib.sha224(the_page).hexdigest(), the_page

def run(email_list, url, source_email, sleeptime_set=None):
    current_hash, current_file = get_hash(url) # Get the current hash, which is what the website is now
    if sleeptime_set is not None:
        sleeptime = sleeptime_set
    while 1: # Run forever
        added_name_list = []
        removed_name_list = []
        new_hash, new_file = get_hash(url)
        if new_hash == current_hash: # If nothing has changed
            print("nothing changed")

        else: # If something has changed

            current_hash = new_hash
            added_pup_text = ""
            removed_pup_text = ""
            for line in difflib.unified_diff(str(current_file), str(new_file)):
                if not re.match(r'-', line):
                    added_pup_text += str(line.strip('+-!'))
                else:
                    removed_pup_text += str(line.strip('+-!'))

            added_name_list = HTMLParser.parse_html(added_pup_text)
            removed_name_list = HTMLParser.parse_html(removed_pup_text)
            if len(added_name_list) > 0:
                for email in email_list:
                    SendEmail.authorize_and_send_message(str(added_name_list), email, source_email)

                print("Changed with added pups, email sent.")

            if len(removed_name_list) > 0:
                print("--Pups removed: " + str(removed_name_list))

            if len(removed_name_list) <= 0 and len(added_name_list) <= 0:
                print("Changed but no pups added or removed.")
        time.sleep(sleeptime)

if __name__ == '__main__':

    # TODO change emails
    # TODO Click enable gmail API and copy the credentials.json file into the top level directory of the project
    #   Gmail api link: https://developers.google.com/gmail/api/quickstart/python
    email_list = ["michael.johnston@capitalone.com"]
    source_email = "mfjnvbell@gmail.com"
    run(email_list, puppies_url, source_email, sleeptime_set=60)
    # run(email_list, adult_dogs_url)