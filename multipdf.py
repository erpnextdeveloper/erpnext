from __future__ import unicode_literals
import frappe, os, copy, json, re
from frappe.utils import cint, get_gravatar, format_datetime, now_datetime,add_days,today,formatdate,date_diff,getdate,get_last_day
from frappe import throw, msgprint, _
from frappe.utils.password import update_password as _update_password
from frappe.desk.notifications import clear_notifications
from frappe.utils.user import get_system_managers
import frappe.permissions
import frappe.share
import re
import string
import random
import json
import time
from pyfcm import FCMNotification
from six import string_types
from datetime import datetime
from datetime import date
from datetime import timedelta
import collections
import math
import urllib	
from frappe.core.doctype.sms_settings.sms_settings import send_via_gateway,validate_receiver_nos
from frappe.core.doctype.communication.email import make
from frappe import _

from frappe.modules import get_doc_path
from jinja2 import TemplateNotFound
from frappe.utils import cint, strip_html
from frappe.utils.pdf import get_pdf
from PyPDF2 import PdfFileWriter, PdfFileReader
import frappe, re, os
from frappe.utils.pdf import get_pdf
from frappe.email.smtp import get_outgoing_email_account
from frappe.utils import (get_url, scrub_urls, strip, expand_relative_urls, cint,
	split_emails, to_markdown, markdown, encode, random_string, parse_addr)
import email.utils
from six import iteritems, text_type, string_types
from email.mime.multipart import MIMEMultipart
from email.header import Header
from __future__ import unicode_literals

import pdfkit, os, frappe
from frappe.utils import scrub_urls
from frappe import _
from bs4 import BeautifulSoup
from PyPDF2 import PdfFileWriter, PdfFileReader
import re

@frappe.whitelist()
def appErrorLog(title,error):
	d = frappe.get_doc({
			"doctype": "App Error Log",
			"title":str("User:")+str(title+" "+"App Name:Salon App"),
			"error":error
		})
	d = d.insert(ignore_permissions=True)
	return d

@frappe.whitelist()
def generateResponse(_type,status=None,message=None,data=None,error=None):
	response= {}
	if _type=="S":
		if status:
			response["status"]=status
		else:
			response["status"]="200"
		response["message"]=message
		response["data"]=data
	else:
		error_log=appErrorLog(frappe.session.user,str(error))
		if status:
			response["status"]=status
		else:
			response["status"]="500"
		if message:
			response["message"]=message
		else:
			response["message"]="Something Went Wrong"		
		response["message"]=message
		response["data"]=None
	return response


@frappe.whitelist()
def download_multi_pdf(doctype, name, format=None,no_letterhead=None):
	# name can include names of many docs of the same doctype.

	import json
	result = json.loads(name)

	# Concatenating pdf files
	output = PdfFileWriter()
	for i, ss in enumerate(result):
		output = frappe.get_print(doctype, ss, format, as_pdf = True, output = output, no_letterhead=no_letterhead)

	frappe.local.response.filename = "{doctype}.pdf".format(doctype=doctype.replace(" ", "-").replace("/", "-"))
	frappe.local.response.filecontent = read_multi_pdf(output)
	frappe.local.response.type = "download"

def read_multi_pdf(output):
	# Get the content of the merged pdf files
	fname = os.path.join("/tmp", "frappe-pdf-{0}.pdf".format(frappe.generate_hash()))
	output.write(open(fname,"wb"))

	with open(fname, "rb") as fileobj:
		filedata = fileobj.read()

	return filedata


def get_filecontent_from_path(path):
	if not path: return

	if path.startswith('/'):
		path = path[1:]

	if path.startswith('assets/'):
		# from public folder
		full_path = os.path.abspath(path)
	elif path.startswith('files/'):
		# public file
		full_path = frappe.get_site_path('public', path)
	elif path.startswith('private/files/'):
		# private file
		full_path = frappe.get_site_path(path)
	else:
		full_path = path

	if os.path.exists(full_path):
		with open(full_path, 'rb') as f:
			filecontent = f.read()

		return filecontent
	else:
		return None


def add_attachment(fname, fcontent, content_type=None,
	parent=None, content_id=None, inline=False):
	"""Add attachment to parent which must an email object"""
	from email.mime.audio import MIMEAudio
	from email.mime.base import MIMEBase
	from email.mime.image import MIMEImage
	from email.mime.text import MIMEText

	import mimetypes
	if not content_type:
		content_type, encoding = mimetypes.guess_type(fname)

	if not parent:
		return

	if content_type is None:
		# No guess could be made, or the file is encoded (compressed), so
		# use a generic bag-of-bits type.
		content_type = 'application/octet-stream'

	maintype, subtype = content_type.split('/', 1)
	if maintype == 'text':
		# Note: we should handle calculating the charset
		if isinstance(fcontent, text_type):
			fcontent = fcontent.encode("utf-8")
		part = MIMEText(fcontent, _subtype=subtype, _charset="utf-8")
	elif maintype == 'image':
		part = MIMEImage(fcontent, _subtype=subtype)
	elif maintype == 'audio':
		part = MIMEAudio(fcontent, _subtype=subtype)
	else:
		part = MIMEBase(maintype, subtype)
		part.set_payload(fcontent)
		# Encode the payload using Base64
		from email import encoders
		encoders.encode_base64(part)

	# Set the filename parameter
	if fname:
		attachment_type = 'inline' if inline else 'attachment'
		part.add_header('Content-Disposition', attachment_type, filename=text_type(fname))
	if content_id:
		part.add_header('Content-ID', '<{0}>'.format(content_id))

	parent.attach(part)


def get_pdf(html, options=None, output = None):
	html = scrub_urls(html)
	html, options = prepare_options(html, options)
	fname = os.path.join("/tmp", "frappe-pdf-{0}.pdf".format(frappe.generate_hash()))

	try:
		pdfkit.from_string(html, fname, options=options or {})
		if output:
			append_pdf(PdfFileReader(file(fname,"rb")),output)
		else:
			with open(fname, "rb") as fileobj:
				filedata = fileobj.read()

	except IOError as e:
		if ("ContentNotFoundError" in e.message
			or "ContentOperationNotPermittedError" in e.message
			or "UnknownContentError" in e.message
			or "RemoteHostClosedError" in e.message):

			# allow pdfs with missing images if file got created
			if os.path.exists(fname):
				if output:
					append_pdf(PdfFileReader(file(fname,"rb")),output)
				else:
					with open(fname, "rb") as fileobj:
						filedata = fileobj.read()

			else:
				frappe.throw(_("PDF generation failed because of broken image links"))
		else:
			raise

	finally:
		cleanup(fname, options)

	if output:
		return output

	return filedata



@frappe.whitelist()
def generate_multiPDF():
	clster=[]
	#["ATT-15546","ATT-15545"]
	d = date.today()
	year = d.strftime("%Y")
	month = d.strftime("%B") 
	doc=frappe.get_all("Cluster Business Plan",filters={"year":year,"month":month},fields=["name"])
	
	for row in doc:
		clster.append(row.name)
	print_format= frappe.db.get_value("Cluster Business Plan Setting","Cluster Business Plan Setting","daily_print_format_name")
	return "http://erp.brillarescience.com/api/method/erpnext.multipdf.download_multi_pdf?doctype=Cluster Business Plan&name="+json.dumps(clster).replace('/','%2F').replace(',','%2C').replace('&','%26')+"&format="+print_format+"&no_letterhead=1"
	'''	
	pdf_link= asd.replace(' "', '"').replace('[','%5B').replace(']','%5D')
	pdf_data=get_filecontent_from_path(pdf_link)
	get_pdf(pdf_data)
	
	cc= frappe.db.get_value("Cluster Business Plan Setting","Cluster Business Plan Setting", "email_cc_in_daily")
	subject= frappe.db.get_value("Cluster Business Plan Setting","Cluster Business Plan Setting","daily_email_subject")
	print_format= frappe.db.get_value("Cluster Business Plan Setting","Cluster Business Plan Setting","daily_print_format_name")
	print_letterhead= frappe.db.get_value("Cluster Business Plan Setting","Cluster Business Plan Setting","print_letterhead")	
	make(recipients="bhavesh.javar@brillarescience.com",cc='bhavesh.javar@brillarescience.com',subject='Test Mail',doctype='Cluster Business Plan',send_email=1,print_format=print_format,print_letterhead=int(print_letterhead),attachments=[{'file_url':asdasd,'file_name':'asdasd','is_private':0}])
	'''
	

