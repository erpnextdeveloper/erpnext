from __future__ import unicode_literals
import frappe
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

import datetime
from frappe.utils import flt,getdate, validate_email_add, today, add_years,add_days,format_datetime
from frappe.model.naming import make_autoname
from frappe import throw, _, scrub
import frappe.permissions
from frappe.model.document import Document
import json
import collections
from frappe.core.doctype.sms_settings.sms_settings import send_sms
from frappe.core.doctype.communication.email import make

@frappe.whitelist()
def sendBusinessPlan(doc,method):
	if str(doc.employee_type)=="BDE":
		sendBDETarget(doc.year,doc.month)
	if str(doc.employee_type)=="Cluster":
		sendClusterTarget(doc.year,doc.month)



@frappe.whitelist()
def sendBDETarget(year,month):
	doc=frappe.get_all("BDE Target and Incentive Plan",filters={"year":year,"month":month},fields=["name"])
	if len(doc)==0:
		frappe.throw("No Target Set For This Month")
	#return doc
	count=0
	cc='bhavesh.javar@brillarescience.com'
	subject='Business Plan For '+str(month)+'-'+str(year)
	print_format="BDE Target"
	#print_letterhead= frappe.db.get_value("Cluster Business Plan Setting","Cluster Business Plan Setting","print_letterhead")	

	for row in doc:
		bde_data=frappe.get_doc("BDE Target and Incentive Plan",row.name)
		receipient=getUserIdfromEmployeeCode(bde_data.employee_code)
		make(recipients=receipient,cc=cc,subject=subject,doctype='BDE Target and Incentive Plan',name=row.name,send_email=1,print_format=print_format,print_letterhead=0)
		count=count+1
	return count

@frappe.whitelist()
def sendClusterTarget(year,month):
	doc=frappe.get_all("Cluster Business Plan",filters={"year":year,"month":month},fields=["name"])
	#return doc
	if len(doc)==0:
		frappe.throw("No Target Set For This Month")
	count=0

	cc=frappe.db.get_value("Cluster Business Plan Setting","Cluster Business Plan Setting", "email_cc_in_daily")
	subject='Business Plan For '+str(month)+'-'+str(year)
	print_format='Cluster Plan'
	print_letterhead=0	

	for row in doc:
		clster_data=frappe.get_doc("Cluster Business Plan",row.name)
		#getClusterData(clster_data.employee_code,year,month,row.name)
		receipient=getUserIdfromEmployeeCode(clster_data.employee_code)
		make(recipients=receipient,cc=cc,subject=subject,doctype='Cluster Business Plan',name=row.name,send_email=1,print_format=print_format,print_letterhead=int(print_letterhead))
		count=count+1
	return count


@frappe.whitelist()
def getUserIdfromEmployeeCode(emp_code):
	return frappe.db.get("Employee",{"name":emp_code}).user_id

@frappe.whitelist()
def test(doc,method):
	frappe.msgprint("Test")

	
