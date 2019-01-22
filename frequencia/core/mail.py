import threading

from django.template.loader import render_to_string
from django.template.defaultfilters import striptags
from django.core.mail import EmailMultiAlternatives, get_connection
from django.conf import settings

class EmailThread(threading.Thread):
	def __init__(self, subject, body='', template_name='', context=None, recipient_list=[], from_email=settings.DEFAULT_FROM_EMAIL, fail_silently=False):
		self.subject = subject
		self.body = body
		self.template_name = template_name
		self.context = context
		self.recipient_list = recipient_list
		self.from_email = from_email
		self.fail_silently = fail_silently
		threading.Thread.__init__(self)
		
	def run(self):		
		if self.template_name:
			message_html = render_to_string(self.template_name, self.context)
			self.body = striptags(message_html)
		
			email = EmailMultiAlternatives(
				subject=self.subject, body=self.body, from_email=self.from_email, to=self.recipient_list)

			email.attach_alternative(message_html, "text/html")
		else:
			email = EmailMultiAlternatives(
				subject=self.subject, body=self.body, from_email=self.from_email, to=self.recipient_list)

		email.send(fail_silently=self.fail_silently)


def send_mail_template(subject, template_name, context, recipient_list, 
	from_email=settings.DEFAULT_FROM_EMAIL, fail_silently=False):
	EmailThread(
		subject=subject,
		template_name=template_name,
		context=context,
		recipient_list=recipient_list,
		from_email=from_email,
		fail_silently=fail_silently).start()

def send_mail_text(subject, body, recipient_list, from_email=settings.DEFAULT_FROM_EMAIL, fail_silently=False):
	EmailThread(
		subject=subject, 
		body=body, 
		recipient_list=recipient_list, 
		from_email=from_email, 
		fail_silently=fail_silently).start()