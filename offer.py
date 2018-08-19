from __future__ import unicode_literals
import frappe
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
from frappe.core.doctype.sms_settings.sms_settings import send_via_gateway,validate_receiver_nos

ter=[]

'''

@frappe.whitelist()
def addUserPermission(allow_val):
	d=frappe.get_doc({
				 	"docstatus": 0,
				 	"doctype": "User Permission",
				 	"name": "New User Permission 1",
				 	"__islocal": 1,
				 	"__unsaved": 1,
				 	"owner": "Administrator",
				 	"apply_for_all_roles": 0,
				 	"user": str(frappe.session.user),
				 	"allow":"Customer",
				 	"for_value": str(allow_val)
				 })
	d.insert(ignore_permissions=True)
	




@frappe.whitelist(allow_guest=True)
def save_sales_order(transaction_date,customer_code,item_object):
	response= {}
	try:
		d1=frappe.get_doc({
					"docstatus": 0,
					"doctype": "Sales Order",
					"name": "New Sales Order 1",
					"__islocal": 1,
					"__unsaved": 1,
					"order_type": "Sales",
					"company": "Brillare Science Private Limited",
					"transaction_date": str(transaction_date),
					"customer_group": "Individual",
					"territory": "India",
					"currency": "INR",
					"selling_price_list": "Standard Selling",
					"price_list_currency": "INR",
					"apply_discount_on": "Net Total",
					"party_account_currency": "INR",
					"status": "Draft",
					"items": [],
					"delivery_date":str(transaction_date),
					"terms": "",
					"customer": str(customer_code)
				})
		d2=d1.insert(ignore_permissions=True)
		item_data=json.loads(item_object)
		for row in item_data:
			save_sales_order_item(d2.name,row["item_code"],row["qty"],transaction_date)

		sales_order_data=frappe.get_doc("Sales Order",d2.name)
		sales_order_data.docstatus=0
		final=sales_order_data.save()
		response["status"]="200"
		response["message"]="Success"
		response["data"]=final
		return response
	except Exception as e:
		error_log=app_error_log(frappe.session.user,str(e))
		response["status"]="500"
		response["message"]="Something went wrong. Try again."
		response["data"]=None
		return response

	


@frappe.whitelist()
def save_sales_order_item(sid,item_id,item_qty,date):
	item_doc=frappe.get_doc({
							"docstatus": 0,
							"doctype": "Sales Order Item",
							"name": "New Sales Order Item 1",
							"__islocal": 1,
							"__unsaved": 1,
							"owner": str(frappe.session.user),
							"parent": str(sid),
							"parentfield": "items",
							"parenttype": "Sales Order",
							"idx": 1,
							"qty": str(item_qty),
							"item_code": str(item_id),
							"update_stock": 0,
							"delivery_date":str(date)
						})
	item_save=item_doc.insert()
'''

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
def getOfferList():
	try:
		offers = frappe.get_all('Offer', filters=[["Offer","end_date",">=",str(datetime.today())],["Offer","start_date",">=",str(datetime.today())]], fields=['*'])
		if offers:
			return generateResponse("S",message="offers list found Successfully.",data=offers)
		else:
			return generateResponse("S",message="offers list empty.",data=offers)
	except Exception as e:
		return generateResponse("F",error=e)


@frappe.whitelist()
def findOfferByItem(item_code):
	offers=frappe.get_all('Offer', filters=[["Offer Detail","option","=",str(item_code)],["Offer Detail","type","=","Item"]], fields=['name'])
	if offers:
		return offers
	else:
		return False

@frappe.whitelist()
def findOfferByItem(item_code):
	offers=frappe.get_all('Offer', filters=[["Offer Detail","option","=",str(item_code)],["Offer Detail","type","=","Item"]], fields=['name'])
	if offers:
		return offers
	else:
		return False

@frappe.whitelist()
def findOfferByBrand(brand):
	offers=frappe.get_all('Offer', filters=[["Offer Detail","option","=",str(brand)],["Offer Detail","type","=","Brand"]], fields=['name'])
	if offers:
		return offers
	else:
		return False

@frappe.whitelist()
def findOfferByCategory(category):
	offers=frappe.get_all('Offer', filters=[["Offer Detail","option","=",str(category)],["Offer Detail","type","=","Category"]], fields=['name'])
	if offers:
		return offers
	else:
		return False

@frappe.whitelist()
def findOfferByItemGroup(item_group):
	offers=frappe.get_all('Offer', filters=[["Offer Detail","option","=",str(item_group)],["Offer Detail","type","=","Item Group"]], fields=['name'])
	if offers:
		return offers
	else:
		return False



