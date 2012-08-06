import sendgrid

import os

import config


try:
	sendgrid_username = os.environ['SENDGRID_USERNAME'];
	sendgrid_password = os.environ['SENDGRID_PASSWORD'];
except:
	try:
		print "Could not determine sendgrid credentials from the operating system environment variables. "
		import secrets
		sendgrid_username = secrets.sendgrid_username 
		sendgrid_password = secrets.sendgrid_password
		print "Determined sendgrid credentials from the secrets.py file. "
	except: 
		print "Could not determine sendgrid credentials from the secrets.py file. "
		raise

try: sendgrid_connection = sendgrid.Sendgrid(sendgrid_username, sendgrid_password, secure=True)
except: 
	print "Couldn't connect to the sendgrid servers using given credentials. "
	raise


def send_mail(send_to, send_from, subject, body, send_to_name = None):
	if config.SEND_EMAILS:
		if config.DEVELOPMENT:
			send_to = config.TESTING_EMAIL
		if not send_to_name:
			send_to_name = send_to
		message = sendgrid.Message(send_from, subject, "This is a PLAIN BODY test", "<b>THIS IS AN HTML TEST</b>")
		#message = sendgrid.Message("catguiceshop@gmail.com", "Testing SUBJECT! ", "This is a PLAIN BODY test", "<b>THIS IS AN HTML TEST</b>")
		message.add_to(send_to, send_to_name)
		sendgrid_connection.web.send(message)