import requests
import json
from dotenv import load_dotenv
import os
import smtplib
from datetime import datetime


load_dotenv()




def get_data():
    key = os.getenv("youtube_key")

    youtube_url = f'https://youtube.googleapis.com/youtube/v3/search?part=snippet&maxResults=15&q=trending&key={key}'

    # lets fetch with a requests object 
    response = requests.get(youtube_url)

    data = json.loads(response.text)

    short_data = data['items']

    return_data = []

    for i in short_data:
        data_dict = {}
        data_dict['title'] = i['snippet']['title']
        data_dict['channel'] = i['snippet']['channelTitle']
        data_dict['publish time'] = i['snippet']['publishTime']

        return_data.append(data_dict)

    return return_data


def send_mail(body):

    # using mail slurp since this is easily available and gmail aint working
    # from https://stackabuse.com/how-to-send-emails-with-gmail-using-python/ 
    # for tls connection https://gist.github.com/jamescalam/93d915e4de12e7f09834ae73bdf37299 

    sender = "YS1BzNvkBmwpEmVP2zh7SKc60CzKYzUq"
    receiver = "soul-62a0f1b7-2edf-4735-aff6-bab89f355788@mailslurp.mx"
    
    password = os.getenv('email_key')
    
    
    time = datetime.now()
    subject = 'Top  trending videos ' + str(time)
    

    email_text = f"""
        From: {sender}
        To: {receiver}
        Subject: {subject}

        {body}
        """

 
    smtp = smtplib.SMTP('mailslurp.mx', 2587)
    smtp.ehlo()   # optional

    smtp.ehlo()  # send the extended hello to our server
    smtp.starttls()  # tell server we want to communicate with TLS encryption
    # ...send emails
    smtp.login(sender, password)
    smtp.sendmail(sender, receiver, email_text)
    smtp.close()

    print("Email Sent")


if __name__ == "__main__":

    print("Getting data for trending videos : ")

    youtube_data = get_data()

    final_data = json.dumps(youtube_data, indent = 2 )

    print(" Sending Email : ")

    send_mail(final_data)




    

