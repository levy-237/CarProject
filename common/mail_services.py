import os
import requests
def send_email(to_name, to_email, subject, text):
  	return requests.post(
  		"https://api.mailgun.net/v3/sandbox3a001c008ad1436ba11840eea211caed.mailgun.org/messages",
  		auth=("api", os.getenv('MAILGUN_API_KEY', 'MAILGUN_API_KEY')),
  		data={"from": "Mailgun Sandbox <postmaster@sandbox3a001c008ad1436ba11840eea211caed.mailgun.org>",
			"to": f"{to_name} <{to_email}>",
  			"subject": subject,
  			"text": text
     })