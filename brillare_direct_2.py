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


@frappe.whitelist()
def app_error_log(title,error):
	d = frappe.get_doc({
			"doctype": "App Error Log",
			"title":str("User:")+str(title+" "+"App Name:Salon App"),
			"error":error
		})
	d = d.insert(ignore_permissions=True)
	return d	


@frappe.whitelist(allow_guest=True)
def userSignup(phoneNo,firstName,lastName,designation):
	response= {}
	try:
		otpobj=frappe.db.get("UserOTP", {"mobile": phoneNo})
		user = frappe.db.get("User", {"name": phoneNo})
		print otpobj.otp
		print user
		if user:
			frappe.db.sql("""UPDATE `tabUser` SET `last_name`='"""+lastName+"""', `first_name`='"""+firstName+"""' WHERE `name`='"""+phoneNo+"""'""")
				 
		else:

						
			#return frappe.db.sql("""insert into tabUser (`name`,`first_name`,`last_name`) VALUES ('9852417445','asasd','adcd')""")
			frappe.db.sql("""INSERT INTO `tabUser` (`name`, `creation`, `modified`, `modified_by`, `owner`, `docstatus`, `parent`, `parentfield`, `parenttype`, `idx`, `last_ip`, `user_type`, `github_username`, `reset_password_key`, `last_name`, `google_userid`, `last_known_versions`, `user_image`, `thread_notify`, `first_name`, `middle_name`, `new_password`, `last_login`, `location`, `github_userid`, `login_after`, `email`, `restrict_ip`, `username`, `send_welcome_email`, `fb_userid`, `background_style`, `background_image`, `send_password_update_notification`, `email_signature`, `language`, `mute_sounds`, `gender`, `login_before`, `enabled`, `time_zone`, `fb_username`, `unsubscribed`, `bio`,`designation`) VALUES ('"""+phoneNo+"""', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'Guest', 'Guest', '0', '', '', '', '0', '', 'System User', '', '', '"""+lastName+"""', '', '', 'https://secure.gravatar.com/avatar/adb831a7fdd83dd1e2a309ce7591dff8?d=retro', '1', '"""+firstName+"""', '', '', '', '', '', '0', '"""+phoneNo+"""@example.com', '', '"""+phoneNo+"""', '1', '', 'Fill Screen', '', '0', '', '', '0', '', '0', '1', '', '', '0', '','"""+designation+"""')""")

			frappe.db.sql("""INSERT INTO `tabUserRole` (`name`, `creation`, `modified`, `modified_by`, `owner`, `docstatus`, `parent`, `parentfield`, `parenttype`, `idx`, `role`) VALUES ('"""+id_generator(10)+"""', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, '"""+phoneNo+"""', '"""+phoneNo+"""', '0', '"""+phoneNo+"""', 'user_roles', 'User', '1', 'KYC')""")
			frappe.db.sql("""INSERT INTO `tabHas Role` (`name`, `creation`, `modified`, `modified_by`, `owner`, `docstatus`, `parent`, `parentfield`, `parenttype`, `idx`, `role`) VALUES ('"""+id_generator(10)+"""', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, '"""+phoneNo+"""', '"""+phoneNo+"""', '0', '"""+phoneNo+"""', 'roles', 'User', '1', 'KYC')""")
			
			
		#	frappe.db.sql("""INSERT INTO `tabUserRole` (`name`, `creation`, `modified`, `modified_by`, `owner`, `docstatus`, `parent`, `parentfield`, `parenttype`, `idx`, `role`) VALUES ('"""+id_generator(10)+"""', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, '"""+phoneNo+"""', '"""+phoneNo+"""', '0', '"""+phoneNo+"""', 'user_roles', 'User', '1', 'Customer')""")
		#	frappe.db.sql("""INSERT INTO `tabHas Role` (`name`, `creation`, `modified`, `modified_by`, `owner`, `docstatus`, `parent`, `parentfield`, `parenttype`, `idx`, `role`) VALUES ('"""+id_generator(10)+"""', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, '"""+phoneNo+"""', '"""+phoneNo+"""', '0', '"""+phoneNo+"""', 'roles', 'User', '1', 'Customer')""")
			
		_update_password(phoneNo,otpobj.otp)
		response["status"]="200"
		response["message"]="User Added Succesfully"
		response["data"]="True"
		return response

	except Exception as e:
		error_log=app_error_log(frappe.session.user,str(e))
		response["status"]="500"
		response["message"]="Something went wrong. Try again."
		response["data"]=None
		return response

		 

        #frappe.db.sql("""delete from tabUserOTP where mobile='"""+phoneNo+"""'""")

def id_generator(size):
   return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))



@frappe.whitelist(allow_guest=True)
def SendSMSByMobile(phoneNo):
	try:
		otpobj=frappe.db.get("UserOTP", {"mobile": phoneNo})
		if otpobj:
			frappe.db.sql("""delete from tabUserOTP where mobile='"""+phoneNo+"""'""")
		OPTCODE=id_generator(6)
		mess=OPTCODE+" is your Brillare App verification code"
		mobileList=[]
		mobileList.append(str(phoneNo))
		respon=send_sms(mobileList,mess)
		#jj=json.loads(respon)
		if phoneNo=="1234567890":
			OPTCODE = "123456"
			return generateResponse("S",message="SMS Sent Successfully",data=respon)
		else:			
			userOTP = frappe.get_doc({
				"doctype":"UserOTP",
				"name":phoneNo,
				"mobile":phoneNo,
				"otp":OPTCODE
			})
			userOTP.flags.ignore_permissions = True
			userOTP.insert()
			return generateResponse("S",message="SMS Sent Successfully",data=respon)
	except Exception as e:
		return generateResponse("F",error=e)
	
	
##Verify OTP
@frappe.whitelist(allow_guest=True)
def VerifyOTPCode(phoneNo, OTPCode):
	try:
		otpobj=frappe.db.get("UserOTP", {"mobile": phoneNo})
		if otpobj.otp==OTPCode:
			return generateResponse("S",message="Verified",data=None)
		else:		
			return generateResponse("S",status="417",message="Authentication Failed",data=None)
	except Exception as e:
		return generateResponse("F",error=e)


@frappe.whitelist()
def send_sms(receiver_list, msg, sender_name = '', success_msg = True):

	import json
	if isinstance(receiver_list, string_types):
		receiver_list = json.loads(receiver_list)
		if not isinstance(receiver_list, list):
			receiver_list = [receiver_list]

	receiver_list = validate_receiver_nos(receiver_list)

	arg = {
		'receiver_list' : receiver_list,
		'message'		: unicode(msg).encode('utf-8'),
		'success_msg'	: success_msg
	}

	if frappe.db.get_value('SMS Settings', None, 'sms_gateway_url'):
		send_via_gateway(arg)
		if arg.get('success_msg'):
			return "True"
		else:
			return "False"
	else:
		msgprint(_("Please Update SMS Settings"))


@frappe.whitelist()
def getKYCNotAllocateToUser():
	response= {}
	try:
		salonData=frappe.db.sql("""Select name,salon_parlor_spa_name,territory,contact_number from `tabKYC` where is_customer=0 and contact_number='"""+frappe.session.user+"""'""",as_dict=True)
		if salonData:
			return generateResponse("S",message="KYC Data get Successfully",data=salonData)
		else:
			return generateResponse("S",message="No KYC Available",data=None)
	except Exception as e:
		return generateResponse("F",error=e)


@frappe.whitelist()
def makeKYCToCustomer(kyc_obj):
	response= {}
	try:
		kyc=json.loads(kyc_obj)
		for row in kyc:
			kyc_data=frappe.get_doc("KYC",row["kyc"])
			doc=frappe.get_doc({
					"docstatus": 0,
					"doctype": "Customer",
					"name": "New Customer 1",
					"owner": frappe.session.user,
					"naming_series":"CUST-",
					"customer_type":"Individual",
					"customer_group":"Retail",
					"territory": kyc_data.territory,
					"disabled": 0,
					"language": "en",
					"company": "Brillare Science Private Limited",
					"customer_name": kyc_data.salon_parlor_spa_name
				})
			customer=doc.insert(ignore_permissions=True)
			if customer:
				addUserPermission(customer.name)
				doc1=frappe.get_doc({
							"docstatus": 0,
							"doctype": "Address",
							"name": "New Address 1",
							"owner": frappe.session.user,
							"address_type": "Billing",
							"country": "India",
							"gst_state": "",
							"is_primary_address": 1,
							"is_shipping_address": 0,
							"is_your_company_address": 0,
							"links": [{
									"docstatus": 0,
									"doctype": "Dynamic Link",
									"name": "New Dynamic Link 1",
									"owner": frappe.session.user,
									"parent": "New Address 1",
									"parentfield": "links",
									"parenttype": "Address",
									"idx": 1,
									"link_doctype": "Customer",
									"link_name":customer.name
								}],
							"address_line1":kyc_data.street,
							"address_line2":kyc_data.landmark if not kyc_data.landmark==None else 0,
							"city": kyc_data.city_town,
							"pincode":kyc_data.pin,
							"phone": kyc_data.contact_number,
							"gstin":"NA",
							"state_code": "NA",
							"place_of_supply": ""
						})
				doc1.insert(ignore_permissions=True)
			kyc_data.is_customer=1
			kyc_data.customer=customer.name
			kyc_data.save()

		response["status"]="200"
		response["message"]="Success"
		response["data"]="True"
		return response

	except Exception as e:
		error_log=app_error_log(frappe.session.user,str(e))
		response["status"]="500"
		response["message"]="Something went wrong. Try again."
		response["data"]=None
		return response


@frappe.whitelist()
def customerListForSalonUser():
	response= {}
	try:
		data=frappe.get_list("Customer",filters={'disabled':'0'},fields=["name","customer_name","customer_type","customer_group","territory"])
		response["status"]="200"
		response["message"]="Success"
		response["data"]=data
		return response
	except Exception as e:
		error_log=app_error_log(frappe.session.user,str(e))
		response["status"]="500"
		response["message"]="Something went wrong. Try again."
		response["data"]=None
		return response

@frappe.whitelist()
def removeCustomerFromSalonUser(customer):
	response= {}
	try:
		doc=frappe.get_doc("Customer",customer)
		doc.disabled=1
		doc.save()
		kyc=frappe.db.sql("""select name from `tabKYC` where customer=%s""",customer)
		#return kyc
		if not kyc[0][0]==None:
			doc1=frappe.get_doc("KYC",kyc[0][0])
			doc1.customer=None
			doc1.is_customer=0
			doc1.save()
		response["status"]="200"
		response["message"]="Success"
		response["data"]="True"
		return response

	except Exception as e:
		error_log=app_error_log(frappe.session.user,str(e))
		response["status"]="500"
		response["message"]="Something went wrong. Try again."
		response["data"]=None
		return response

	
	
	


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







#@frappe.whitelist()
#def send_notification(is_sms,is_mail,is_push_notification):



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
def getBalance():
	balance= 0
	try:
		wallet_entry_list=frappe.get_list('Wallet', filters={'docstatus':1}, fields=['name','wallet_balance'], order_by='date')
		for entry in wallet_entry_list:
			balance = float(balance) + float(entry.wallet_balance)
		return generateResponse("S",message="Balance get Successfully",data=balance)
	except Exception as e:
		return generateResponse("F",error=e)



@frappe.whitelist()
def ShareWallet(from_customer,to_customer,amount):
	response= {}
	frappe.session.user = "9624545985"
	try:
		debit_amount=float(amount)*(-1)
		d = frappe.get_doc({
				"doctype": "Wallet",
				"docstatus":0,
				"customer":str(from_customer),
				"date":str(nowdate()),
				"wallet_balance":float(debit_amount),
				"payable_amount":float(debit_amount),
				"payment_type":"Share Wallet Out",
				"share_to_number":str(to_customer)
			})
		debit_wallet = d.insert(ignore_permissions=True)
		
		d1 = frappe.get_doc({
				"doctype": "Wallet",
 				"docstatus":0,
				"customer":str(to_customer),
				"date":str(nowdate()),
				"wallet_balance":float(amount),
				"payable_amount":float(amount),
				"payment_type":"Share Wallet In",
				"share_from_number":str(from_customer)
			})
		credit_wallet = d1.insert(ignore_permissions=True)
		debit_wallet.submit()
		credit_wallet.submit()	
		return generateResponse("S",message="Balance Shared Successfully",data=(debit_wallet,credit_wallet))	
	except Exception as e:
		return generateResponse("F",error=e)

@frappe.whitelist() 
def saveWalletRecharge(amount,payment_id,payment_type,customer): 
	try: 
		
		d = frappe.get_doc({
				"doctype":"Wallet",
				"customer": str(customer),
				"date": str(datetime.today()),
				"wallet_balance": ""+str(amount),
				"payable_amount" : ""+str(amount),
				"docstatus": 0 ,
				"payment_type" : payment_type,
				"payment_id": str(payment_id)
				})
		wallet = d.insert(ignore_permissions=True)
		wallet.submit()
		return generateResponse("S",message="Wallet Recharge Credited Successfully",data=wallet)
	except Exception as e:
		return generateResponse("F",error=e)

@frappe.whitelist() 
def getUnderLyingCustomer():
	try:
		frappe.session.user = "9624545985"
		customer_list=frappe.get_list("Customer",filters={},fields=["*"])
		#customer_list= frappe.db.sql("""select * from `tabUser Permission` where user='"""+frappe.session.user+"""' and allow='customer' """,as_dict=1)
		return generateResponse("S",message="Customer Data Found Successfully",data=customer_list)
	except Exception as e:
		return generateResponse("F",error=e)

@frappe.whitelist() 
def customerWiseWallet(customer):
	response={}
	balance = 0
	wallet_transactions = frappe.get_list("Wallet",filters={"customer":customer },fields=["*"])
	for wallet in wallet_transactions:
		balance = float(balance) + float(wallet.wallet_balance)
	response["balance"] = balance
	response["customer"] = customer
	response["transaction"]= wallet_transactions
	return response

@frappe.whitelist()
def customerWiseWalletList():
	try:
		wallet_list = []
		frappe.session.user = "9624545985"
		customer_list_response = getUnderLyingCustomer()
		#return customer_list_response
		if customer_list_response:
			for customer in customer_list_response["data"]:
				wallet_list.append(customerWiseWallet(customer.name))
			if wallet_list:
				return generateResponse("S",message="Wallet Data Found Successfully",data=wallet_list)
			else:
				return generateResponse("S",message="Wallet Data Not Available",data=None)
	except Exception as e:
		return generateResponse("F",error=e)



@frappe.whitelist()
def getItemList():
	return frappe.get_list("Item",filters=[["Item","show_in_website","=","1"],["Item","category","!=","Discontinue"],["Item","disabled","=","0"]],fields=["item_name", "item_code", "standard_rate", "net_weight", "item_group", "brand", "image", "thumbnail", "description","product_for","website_image","clp","slp"])


@frappe.whitelist()
def getNotification():
	all_notification = frappe.get_all('Sent Notification', filters={'customer': frappe.session.user}, fields=['title', 'message','date'])
	return all_notification	


@frappe.whitelist(allow_guest=True)
def getUserByName(name):
	try:
		userobj=frappe.db.get("User", {"name": name})
		if userobj:
			return generateResponse("S",message="User Data Found Successfully",data=userobj)
		else:
			return generateResponse("S",message="User Data Not Available",data=None)
	except Exception as e:
		return generateResponse("F",error=e)
@frappe.whitelist()
def getUserByAddress(name):
	address_name=frappe.db.get("Dynamic Link",{"link_name":name})
	if address_name:
		address=address_name.parent
		address_data=frappe.db.get("Address", {"name":address})
		address_data_response = {}
		address_data_response["address_line1"]=address_data.address_line1
		address_data_response["address_line2"]=address_data.address_line2
		address_data_response["city"]=address_data.city
		address_data_response["phone"]=address_data.phone
		address_data_response["pincode"]=address_data.pincode
		address_data_response["email_id"]=address_data.email_id
		return address_data_response
		
		

@frappe.whitelist()
def getProfileInformation():
	try:
		frappe.session.user = "9624545985"
		profileObj = {}
		userobj=frappe.db.get("User", {"name": frappe.session.user})
		if userobj:
			profileObj["first_name"]=userobj.first_name
			profileObj["last_name"]=userobj.last_name
			customer_list_response= getUnderLyingCustomer()
			profileData = []
			for customer in customer_list_response["data"]:
				customer1 = {}
				customer1["name"]=customer.name
				wallet_info=customerWiseWallet(customer.name)
				customer1["wallet"]=wallet_info["balance"]
				customer1["address"]=getUserByAddress(customer.name)
				profileData.append(customer1)
			profileObj["KYC"]=profileData
			return generateResponse("S",message="Profile Data Found Successfully",data=profileObj)
		else:
			return generateResponse("S",message="Profile  Data Not Available",data=None)
	except Exception as e:
		return generateResponse("F",error=e)

'''
@frappe.whitelist()
def createIssue(subject,description):
	try:
		issue = frappe.get_doc({
						"docstatus": 0,
						"doctype": "Issue",
						"__islocal": 1,
						"__unsaved": 1,
						"subject":str("salon App: ") +subject,
						"description":description,
						"name": "New Issue 1",
						"raised_by": frappe.session.user,
						"status": "Open"
					})
		issue=issue.insert()
		return generateResponse("S",message="Issue Created Successfully",data=issue)
	except Exception as e:
		return generateResponse("F",error=e)



@frappe.whitelist()
def send_notification(notification,method):
	api_key= frappe.db.get_value("Notification Setting","Notification Setting", "fcm_key")
	push_service = FCMNotification(api_key=api_key)
	registration_ids =[]
	if notification.send_to == "All User":
		d1 = frappe.db.sql(""" select user.name,setting.token from `tabUser`as user inner join `tabUser Settings` as setting ON user.name=setting.name where user.name IN ('9624545985') """)
		#d1 = frappe.db.sql(""" select user.name,setting.token from `tabUser`as user inner join `tabUser Settings` as setting ON user.name=setting.name where user.name """)
		for d in d1:
			# frappe.msgprint(d[0])
			# frappe.msgprint(d[1])
			d2 = frappe.get_doc({
				"docstatus":0,
				"doctype":"Sent Notification",
				"name":"New Sent Notification 1",
				"__islocal":1,
				"__unsaved":1,
				"owner":frappe.session.user,
				"customer": d[0],
				"category":notification.send_to,
				"title":notification.title,
				"message":notification.message,
				"date":today()
				
			})
			d2.save()
			registration_ids.append(d[1])
		#return registration_ids
		
	message_title = notification.title
	message_body = notification.message
	message_sound = "Default"
	result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title, message_body=message_body, sound=message_sound, badge= 0)

@frappe.whitelist()
def send_notification(doc,method):
	api_key= frappe.db.get_value("Notification Setting","Notification Setting", "fcm_key")
	push_service = FCMNotification(api_key=api_key)
	user_setting_list = frappe.db.sql(""" select user.name,setting.token from `tabUser`as user inner join `tabUser Settings` as setting ON user.name=setting.name where user.name IN ('9624545985') """,as_dict=1)
	registration_ids =[]
	for useruser_setting in user_setting_list:
		d2 = frappe.get_doc({
			"docstatus":0,
			"doctype":"Sent Notification",
			"name":"New Sent Notification 1",
			"__islocal":1,
			"__unsaved":1,
			"owner":frappe.session.user,
			"customer": user_setting.token,
			"category":notification.send_to,
			"title":notification.title,
			"message":notification.message,
			"date":today()
		})
		d2.save()
		registration_ids.append(user_setting.token)
	message_title = notification.title
	message_body = notification.message
	message_sound = "Default"
	result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title, message_body=message_body, sound=message_sound, badge= 0)
'''


