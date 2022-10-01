import smtplib

def send_mail(email,body):

	gmail_user = 'siddharthsrivastav987@gmail.com'
	gmail_password = 'S$id9198900316'

	sent_from = gmail_user
	to = [email]
	subject = 'Reset Password'
	email_text = """\
	From: %s
	To: %s
	Subject: %s

	%s
	""" % (sent_from, ", ".join(to), subject, body)

	server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
	server.ehlo()
	server.login(gmail_user, gmail_password)
	server.sendmail(sent_from, to, email_text)
	server.close()

	print('Email sent!')

