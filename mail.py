import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


sendingEmail = 'sender@gmail.com' #Must be a gmail account, I reccommend setting up a throwaway account for securit reasons. 
sendingPassword = 'testPass' #Reccommend generating a complex password

recievingEmail = 'test@gmail.com'

def sendEmail(image):
	msgRoot = MIMEMultipart('related')
	msgRoot['Subject'] = 'Motion Detected'
	msgRoot['From'] = sendingEmail
	msgRoot['To'] = recievingEmail
	msgRoot.preamble = 'Motion has been detected'

	msgImage = MIMEImage(image)
	msgImage.add_header('Content-ID', '<image1>')
	msgRoot.attach(msgImage)

	smtp = smtplib.SMTP('smtp.gmail.com', 587)
	smtp.starttls()
	smtp.login(fromEmail, fromEmailPassword)
	smtp.sendmail(fromEmail, toEmail, "Hi")
	smtp.quit()
