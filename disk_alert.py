import subprocess
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
threshold = 85
partition = "/"
today = datetime.today ()

def report_via_email(disk_name):
	msg = MIMEMultipart()
	html = """\
	<html>
  	<head></head>
  	<body>
    	<p>Hi!<br><br>
       	Server running out of disk space for """+disk_name+""" partition on """+str(today)+""" <br><br>
	Thanks<br>
	XYZ<br>
	+1234567890<br>
    	</p>
  	</body>
	</html>
	"""
	msg.attach(MIMEText(html, 'html'))
	sender = "SENDER EMAIL"
	recipients = "RECEIVER EMAIL"
	msg["Subject"] = "Low disk space warning"
	msg["From"] = sender
	msg["To"] = recipients
	with smtplib.SMTP("HOST", PORT) as server:
			server.ehlo()
			#server.starttls()
			server.login("USER","PASSWORD")
			server.sendmail(sender, recipients.split(','), msg.as_string())
def check_once_sda3():
	df = subprocess.Popen(["df","-h","/dev/sda3"], stdout=subprocess.PIPE)
	for line in df.stdout:
		splitline = line.decode().split()
		if splitline[5] == partition:
			if int(splitline[4][:-1]) > threshold:
				report_via_email("/dev/sda3")

check_once_sda3()
