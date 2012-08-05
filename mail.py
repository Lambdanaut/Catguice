import os

import sendgrid

try:
	sendgrid_username = os.environ['SENDGRID_USERNAME'];
	sendgrid_password = os.environ['SENDGRID_PASSWORD'];
except:
	try:
		print "Could not determine sendgrid credentials from the operating system environment variables. "
		print "Trying to determine sendgrid credentials from the secrets.py file. "
		import secrets
		sendgrid_username = secrets.sendgrid_username 
		sendgrid_password = secrets.sendgrid_password
	except: 
		print "Could not determine sendgrid credentials from the secrets.py file. "
		raise

print sendgrid_username
print sendgrid_password

#s = sendgrid.Sendgrid(sendgrid_username, sendgrid_password, secure=True)
#message = sendgrid.Message("@.com", "subject", "plain body", "<b>Html here</b>")
#message.add_to("someone@example.com", "John Doe")

#s.web.send(message)
