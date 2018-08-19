from __future__ import unicode_literals
import frappe
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

from datetime import datetime
from frappe.utils import flt,getdate, validate_email_add, today, add_years,add_days,format_datetime
from frappe.model.naming import make_autoname
from frappe import throw, _, scrub
import frappe.permissions
from frappe.model.document import Document
import json
import collections
from frappe.core.doctype.sms_settings.sms_settings import send_sms
from frappe.client import delete
from frappe.desk.form.save import cancel



def test(employee,method):
		for l in employee.get("leave_approvers")[:]:
			frappe.permissions.add_user_permission("Employee",employee.name,l.leave_approver)

		
		if employee.status == "Left":
			frappe.db.sql("""UPDATE tabUser set enabled=0 where name=%s""",employee.user_id)
			frappe.msgprint("testing")

		user=employee.get("user_id")
		frappe.msgprint(user)
		territory_name=employee.get("territory")
     		frappe.permissions.add_user_permission("Territory",territory_name,user)    
    		territory_list=frappe.db.sql("select territory_name from tabTerritory where parent_territory=%s",territory_name)
  		territory_list1=json.dumps(territory_list)	
       		territory_list2=json.loads(territory_list1)
  		for i,list in enumerate(territory_list2):
  			frappe.permissions.add_user_permission("Territory",list[0],user)
 		        child_territory_list=frappe.db.sql("select territory_name from tabTerritory where parent_territory=%s",list[0])
            		child_territory_list1=json.dumps(child_territory_list)
		        child_territory_list2=json.loads(child_territory_list1)
                 	for j,list in enumerate(child_territory_list2):
               			frappe.permissions.add_user_permission("Territory",list[0],user)

@frappe.whitelist()
def set_property(field_name):
	make_property_setter('Stock Entry Detail',field_name, "in_list_view",1, "Check")

@frappe.whitelist()
def set_property1(field_name):
	make_property_setter('Stock Entry Detail',field_name, "in_list_view",0, "Check")

def user_create(employee,method):
	
	if employee.company_email:
		if not employee.user_id:
			employee_name = employee.employee_name.split(" ")
			middle_name = last_name = ""
		
			if len(employee_name) >= 3:
				last_name = " ".join(employee_name[2:])
				middle_name = employee_name[1]
			elif len(employee_name) == 2:
				last_name = employee_name[1]
		
			first_name = employee_name[0]
			
			d = frappe.get_doc({
					"docstatus": 0,
					"doctype": "User",
					"name": "New User 1",
					"__islocal": 1,
					"__unsaved": 1,
					"enabled": 1,
					"send_welcome_email": 1,
					"gender":employee.gender,
					"thread_notify": 1,
					"email":employee.company_email,
					"first_name":first_name,
					"mobile_no": employee.cell_number,
					"birth_date": employee.date_of_birth
					})
			d.insert(ignore_permissions=True)
			employee.user_id=employee.company_email	

@frappe.whitelist(allow_guest=True)
def test1():
	return frappe.db.sql("""select salon_parlor_spa_name,door_building_plot_number,street,landmark,pin,city_town,state,contact_number from tabKYC where status='Active'""")
	
@frappe.whitelist()
def get_permission_query_conditions():
    return "(tabevent.event_type='public' or tabevent.owner='{user}'".format(user=frappe.session.user)

@frappe.whitelist()
def get_confirmation_date(date_of_joining=None):
	ret = {}
	if date_of_joining:
		try:
			confirmation_date = int(frappe.db.get_single_value("HR Settings", "confirmation_date") or 60)
			dt = 	frappe.utils.data.add_months(getdate(date_of_joining),confirmation_date)
			ret = {'final_confirmation_date': dt.strftime('%Y-%m-%d')}
		except ValueError:
			# invalid date
			ret = {}

	return ret

@frappe.whitelist()
def kyc_address(kname):
	address = frappe.get_all("KYC",{"name":kname},["door_building_plot_number","street","landmark","area","city_town","pin","state","contact_number"])
	return address


@frappe.whitelist(allow_guest=True)
def test2():
	return frappe.db.sql("""select name from tabCustomer""")

@frappe.whitelist(allow_guest=True)
def put_Cust_Data(gst,pan,coname,conum,arnnum,cust_name):
	 return frappe.db.sql("""update tabCustomer set gst_number=%s,pan=%s,contact_person_name=%s,contact_person_cell_number=%s,arn_number=%s where name=%s""",(gst,pan,coname,conum,arnnum,cust_name))

@frappe.whitelist(allow_guest=True)
def put_Cust_Data1(mobile,email,cust_name):
	 return frappe.db.sql("""update tabAddress set phone=%s,email_id=%s where customer_name=%s""",(mobile,email,cust_name))




@frappe.whitelist(allow_guest=True)
def get_Cust_Data(cust_name):
	 return frappe.db.sql("""select address_line1,address_line2,concat(city,',',state),concat(country,'-',pincode),phone,email_id from tabAddress where customer_name=%s""",cust_name)

@frappe.whitelist(allow_guest=True)
def get_Cust_Data1(cust_name):
	 return frappe.db.sql("""select pan,gst_number,contact_person_name,contact_person_cell_number,arn_number from tabCustomer where customer_name=%s""",cust_name)





@frappe.whitelist(allow_guest=True)
def put_Sup_Data(gst,pan,coname,conum,arnnum,sup_name):
	 return frappe.db.sql("""update tabSupplier set gst_number=%s,pan=%s,contact_person_name=%s,contact_person_cell_number=%s,arn_number=%s where name=%s""",(gst,pan,coname,conum,arnnum,sup_name))

@frappe.whitelist(allow_guest=True)
def put_Sup_Data1(mobile,email,sup_name):
	 return frappe.db.sql("""update tabAddress set phone=%s,email_id=%s where supplier=%s""",(mobile,email,sup_name))




@frappe.whitelist(allow_guest=True)
def get_Sup_Data(sup_name):
	 return frappe.db.sql("""select address_line1,address_line2,concat(city,',',state),concat(country,'-',pincode),phone,email_id from tabAddress where supplier=%s""",sup_name)

@frappe.whitelist(allow_guest=True)
def get_Sup_Data1(sup_name):
	 return frappe.db.sql("""select pan,gst_number,contact_person_name,contact_person_cell_number,arn_number from tabSupplier where supplier_name=%s""",sup_name)




@frappe.whitelist() 
def getUserProfile():

		user_detail = frappe.get_all("User",{"name":frappe.session.user}, ["first_name", "last_name", "user_image", "email"])
 		return user_detail
			

@frappe.whitelist() 
def getEmployeeProfile():
		
	try:
		
		user_detail = frappe.get_all("Employee",{"user_id":frappe.session.user}, ["name","date_of_birth","permanent_address","user_id","employment_type","personal_email","reports_to","department","designation","status","company","employee_name","current_address","cell_number","gender","territory"])
 		return user_detail
			
	except Exception,e:
		 print str(e)
		 return _(False)

@frappe.whitelist() 
def getLeaveApprover():
		ecode=frappe.db.get("Employee",{"user_id":frappe.session.user}).name
		la=frappe.get_all("Employee Leave Approver",{"parent":ecode},["leave_approver"])
		return la 

@frappe.whitelist()
def getLeaveApp():
		ecode=frappe.db.get("Employee",{"user_id":frappe.session.user}).name
		data=frappe.db.sql("""select leave_approver from `tabEmployee Leave Approver` where parent=%s""",ecode)
		return data

@frappe.whitelist()
def getEmpDetail():
		ecode=frappe.db.get("Employee",{"user_id":frappe.session.user}).name
		data=frappe.db.sql("""select name,employee_name from `tabEmployee` where name=%s""",ecode)
		return data

		
@frappe.whitelist() 
def get_kyc_list():
		
	try:
		
		kyc = frappe.get_list("KYC",["name","salon_parlor_spa_name","door_building_plot_number","street","landmark","area","city_town","pin","state","territory","contact_number","alternate_number","full_name","creation"])
 		return kyc
			
	except Exception,e:
		 print str(e)
		 return _(False)

@frappe.whitelist()
def bill_add(bname):
	return frappe.get_all("Address",{"name":bname},["address_line1","address_line2","city","pincode","state","country","phone","email_id","gstin","email_id"])
			


@frappe.whitelist(allow_guest=True)
def token():
	test=frappe.sessions.get_csrf_token()
	return test
						


#d = frappe.get_doc({
#					"doctype":"KYC",
#					"docstatus":0,
#					"owner":"bhavesh.javar@brillarescience.com",
#					"gender":"Lady",
#					"state":"",
#					"territory":"All Territories",
#					"annual_business_agreement":"",
#					"account_type":"General",
#					"workflow_state":"Draft",
#					"salon_parlor_spa_name":"mitulchandarana123",
#					"full_name":"testfllname",
#					"door_building_plot_number":"testbuildingplot",
#					"contact_number":"9876543210",
#					"city_town":"cityahmedbag",
#					})
#			d.insert(ignore_permissions=True)		

@frappe.whitelist()
def kyc_insert(gender,state,territory,salon_name,fullname,building,contact,city):
			d = frappe.get_doc({
				"doctype":"KYC",
				"docstatus":0,
				"owner":str(frappe.session.user),
				"gender":gender,
				"state":state,
				"territory":territory,
				"annual_business_agreement":"",
				"account_type":"General",
				"workflow_state":"Draft",
				"salon_parlor_spa_name":salon_name,
				"full_name":fullname,
				"door_building_plot_number":building,
				"contact_number":contact,
				"city_town":city,
				})
			d.insert(ignore_permissions=True)	

@frappe.whitelist()
def iostest(name):
	return name



@frappe.whitelist()
def validate_price(b_no):
	item_mrp=frappe.db.get("Batch",{"name":b_no}).mrp
	return item_mrp


#def validate_mrp(doc,method):
#	frappe.msgprint("hello")


@frappe.whitelist() 
def get_sales_order_list():
		
	try:
		
		sales_order = frappe.get_all("Secondary Sales Order",{"owner":frappe.session.user}, ["salon_parlor_spa_name","docstatus","grand_total","name","clp_total","slp_total"])
 		return sales_order
			
	except Exception,e:
		 print str(e)
		 return _(False)


@frappe.whitelist() 
def getHolidayList():
		
		holiday = frappe.get_all("Employee",{"user_id":frappe.session.user}, ["holiday_list"])
		return holiday
		
@frappe.whitelist() 
def get_technical_trainer_list():
		
		tec_trainer = frappe.get_all("Employee",filters=[["department","in",["Technical Training","Technical Sales"]],["status","=","Active"]], fields=["employee_name","name"])
		return tec_trainer

	
@frappe.whitelist() 
def dashboard_kyc(date1):
		kyc=frappe.db.sql("""select name,salon_parlor_spa_name,city_town,state,territory from `tabKYC` where Date(creation)=%s and owner=%s""",(date1,frappe.session.user))
		return kyc
 			
@frappe.whitelist() 
def dashboard_sso(date1):
		sso=frappe.db.sql("""select salon_parlor_spa_name,name,docstatus,grand_total from `tabSecondary Sales Order` where Date(creation)=%s and owner=%s""",(date1,frappe.session.user))
		return sso

@frappe.whitelist() 
def dashboard_sso1(date1):
		sso=frappe.db.sql("""select salon_parlor_spa_name,name,docstatus,grand_total from `tabSecondary Sales Order` where posting_date=%s and owner=%s""",(date1,frappe.session.user))
		return sso
 			

@frappe.whitelist() 
def dashboard_demo(date1):
		demo=frappe.db.sql("""select salon_parlor_spa_name,date,time,name from `tabDemo Booking` where date=%s and owner=%s""",(date1,frappe.session.user))
		return demo

@frappe.whitelist() 
def dashboard_expence(date1):
		ex=frappe.db.sql("""select expense_type,claim_amount,description,name from `tabExpense Claim Detail` where expense_date=%s and owner=%s""",(date1,frappe.session.user))
		return ex



@frappe.whitelist()
def claim():
		c=frappe.db.sql("""select name from `tabExpense Claim Type`""")
		return c


@frappe.whitelist()
def att_insert(lat,lang):
		name=frappe.db.get("Employee",{"user_id":frappe.session.user}).name
		d1 = frappe.get_doc({
				"docstatus": 0,
				"doctype": "Attendance",
				"__islocal": 1,
				"__unsaved": 1,
				"owner":str(frappe.session.user),
				"employee":name,
				"naming_series": "ATT-",
				"status": "Present",
				"company": "Brillare Science Private Limited",
				"start_a_day_time": str(frappe.utils.data.nowtime()),
				"stop_a_day_time":"0:00:00",
				"workflow_state": "Applied",
				"attendance_date": str(frappe.utils.data.nowdate()),
				"day_started_latitude":lat,
				"day_started_longitude":lang
			})
		return d1.insert()

@frappe.whitelist()
def att_update(lat,lang):
	user=frappe.db.get("Employee",{"user_id":frappe.session.user}).name
	name=frappe.db.get("Attendance",{"attendance_date":str(frappe.utils.data.nowdate()),"employee":str(user)}).name
	return frappe.db.set_value("Attendance",name,{"stop_a_day_time":frappe.utils.data.nowtime(),"day_stopped_latitude":lat,"day_stopped_longitude":lang},None)

@frappe.whitelist()
def time_test():
	date=frappe.utils.data.nowtime()
	return date;
	


@frappe.whitelist()
def testup():
	frappe.db.sql("""update `tabSecondary Sales Order` set full_name='Test Fullname' where name='SSO-00014'""")


@frappe.whitelist()
def expense_month_list():
	return frappe.db.sql("""SELECT name,posting_date,total_claimed_amount FROM `tabExpense Claim` where owner=%s ORDER BY posting_date DESC LIMIT 12""",frappe.session.user)

@frappe.whitelist()
def expense_date_list(expnum):
	exp_date_list=frappe.db.sql("""select expense_date,sum(claim_amount) as claim_amount from `tabExpense Claim Detail` where parent=%s group by(expense_date)""",expnum)
	return exp_date_list
	


@frappe.whitelist()
def expense_detail(expnum,exdate):
	ex_date=datetime.strptime(exdate,'%d-%m-%Y')
	exp_date=datetime.strftime(ex_date,'%Y-%m-%d')
	return frappe.db.sql("""select expense_type,description,claim_amount,name from `tabExpense Claim Detail` where parent=%s AND expense_date=%s""",(expnum,exp_date))


@frappe.whitelist()
def expense_delete(id):
	return frappe.db.sql("""delete *from `tabExpense Claim Detail` where name=%s""",id)




@frappe.whitelist()
def expense_date_list1(expnum):
	return frappe.db.sql("""select expense_date from `tabExpense Claim Detail` where parent=%s order by expense_date""",expnum)


@frappe.whitelist()
def expense_detail_new(expnum):
	#test=frappe.db.sql("""select expense_date from `tabExpense Claim Detail` order by expense_date""")
	#for j in list(test):
	#	return j[0]

	test=frappe.get_all("Expense Claim Detail",{"parent":expnum}, ["expense_date"])
	for j,list in enumerate(test):
		return list["expense_date"]
	
@frappe.whitelist() 
def test_update():
	#frappe.db.sql("""update `tabCustom DocPerm` set apply_user_permissions='0' where user_permission_doctypes='["Company","Employee"]' AND parent='Employee'""")
	return frappe.utils.data.nowtime() 


@frappe.whitelist()
def employee_jentry(ename):
	emp_name=frappe.get_all("Employee",{"name":ename},["employee_name"])
	for j,list in enumerate(emp_name):
		return list["employee_name"]

@frappe.whitelist()
def compo_leave(attendance,method):
	if attedance.workflow_state=="Approved":
		frappe.msgprint("Hello World!")

		

@frappe.whitelist()
def change_status(status,name):
	# frappe.db.set_value("Secondary Sales Order",{"name":name},{"docstatus":status},None)
	# frappe.db.set_value("Secondary Sales Order Item",{"parent":name},{"docstatus":status},None)
	if int(status)==1:
		doc=frappe.get_doc("Secondary Sales Order",name)
		doc.status=status
		doc1=doc.submit()
		if doc1:
			return "Succesfully submited"
	if int(status)==2:
		frappe.db.set_value("Secondary Sales Order",{"name":name},{"docstatus":status},None)
		frappe.db.set_value("Secondary Sales Order Item",{"parent":name},{"docstatus":status},None)
	
	

@frappe.whitelist()
def insert_expense(des,exp_date,exp_type,amount):
	emp=frappe.db.get("Employee",{"user_id":frappe.session.user}).name
	dt = getdate(exp_date)
	check=frappe.db.sql("""select name from `tabExpense Claim` where month(posting_date)=%s and year(posting_date)=%s and employee=%s""",(dt.month,dt.year,emp))
	if check:
		for i,list in enumerate(check):
			parent=list[0]

		d = frappe.get_doc({
				"docstatus": 0,
				"doctype": "Expense Claim Detail",
				"name": "New Expense Claim Detail 1",
				"parent": parent,
				"parentfield": "expenses",
				"parenttype": "Expense Claim",
				"description": str(des),
				"expense_date": exp_date,
				"expense_type": str(exp_type),
				"default_account": "Field Expense - BSPL",
				"claim_amount": amount
			})
		d.insert(ignore_permissions=True)
		doc1=frappe.get_doc("Expense Claim",parent)
		return doc1.save(ignore_permissions=True)
		
			
	else:
		doc=frappe.get_doc({
					"docstatus": 0,
					"doctype": "Expense Claim",
					"name": "New Expense Claim 1",
					"naming_series": "EXP",
					"posting_date": exp_date,
					"expenses": [{
							"docstatus": 0,
							"doctype": "Expense Claim Detail",
							"name": "New Expense Claim Detail 1",
							"description": str(des),
							"parentfield": "expenses",
							"parenttype": "Expense Claim",
							"expense_date": exp_date,
							"expense_type": str(exp_type),
							"claim_amount": amount
						}],
					"employee": emp,
				})
		return doc.insert(ignore_permissions=True)
	


@frappe.whitelist()
def update_expense(doc_id,des,exp_date,amount,exp_type):
		parent=frappe.db.get("Expense Claim Detail",{"name":doc_id}).parent
		doc=frappe.get_doc("Expense Claim Detail",doc_id)
		d = frappe.get_doc({
					"docstatus": 0,
					"doctype": "Expense Claim Detail",
					"name": doc_id,
					"parent": parent,
					"parentfield": "expenses",
					"parenttype": "Expense Claim",
					"idx": 1,
					"description": str(des),
					"expense_date": exp_date,
					"expense_type": str(exp_type),
					"default_account": "Field Expense - BSPL",
					"claim_amount": amount,
					"modified":doc.modified
				})
		d.save(ignore_permissions=True)
		doc1=frappe.get_doc("Expense Claim",parent)
		return doc1.save(ignore_permissions=True)



@frappe.whitelist()
def territory_list():
	test=frappe.get_all("Territorry",{"parent":expnum}, ["expense_date"])

@frappe.whitelist()	
def test_date():
	days=70
	count=0
	start_date=today()
	end_date=add_days(today(), days)
	
	while start_date<end_date:
			d1 = frappe.get_doc({
				"docstatus":0,
				"doctype":"Demo Booking",
				"name":"New Demo Booking 1",
				"__islocal":1,
				"__unsaved":1,
				"owner":"bhavesh.javar@brillarescience.com",
				"trainer":"EMP/0189",
				"booked_by":"EMP/0189",
				"select_demo_type":"Skin",
				"time":"12:58:3",
				"date":start_date,
				"salon_parlor_spa_name":"Ravi Salon",
				"kyc":"BSRN02371"
				})
			d1.insert()
			start_date=add_days(start_date,1)

@frappe.whitelist()
def sso_moc_list(to_date,from_date):
	return frappe.get_list("Secondary Sales Order",[["Secondary Sales Order","posting_date","Between",[to_date,from_date]]] ,["name"])

		
@frappe.whitelist()
def save_visit(visit_date,time,kyc,comments):
	emp_id=frappe.db.get("Employee",{"user_id":frappe.session.user}).name
	emp_name=frappe.db.get("Employee",{"user_id":frappe.session.user}).employee_name
	salon_name=frappe.db.get("KYC",{"name":kyc}).salon_parlor_spa_name
	
	d1 = frappe.get_doc({
		"docstatus": 0,
		"doctype": "Visit",
		"name": "New Visit 1",
		"__islocal": 1,
		"__unsaved": 1,
		"owner": frappe.session.user,
		"time":time,
		"salon_name": str(salon_name),
		"kyc": str(kyc),
		"date": visit_date,
		"sales_person_name": str(emp_name),
		"sales_person": str(emp_id),
		"comments": str(comments),
		"status":"Completed"
		})
	result=d1.insert()
	result.submit()
	if result:
		return "Visit Added"
	else:
		return "Something Went Wrong"

@frappe.whitelist()
def save_visitlatlong(visit_date,time,kyc,comments,lat,lang):
	emp_id=frappe.db.get("Employee",{"user_id":frappe.session.user}).name
	emp_name=frappe.db.get("Employee",{"user_id":frappe.session.user}).employee_name
	salon_name=frappe.db.get("KYC",{"name":kyc}).salon_parlor_spa_name
	
	d1 = frappe.get_doc({
		"docstatus": 0,
		"doctype": "Visit",
		"name": "New Visit 1",
		"__islocal": 1,
		"__unsaved": 1,
		"owner": frappe.session.user,
		"time":time,
		"salon_name": str(salon_name),
		"kyc": str(kyc),
		"date": visit_date,
		"sales_person_name": str(emp_name),
		"sales_person": str(emp_id),
		"comments": str(comments),
		"latitude":str(lat),
		"longitude":str(lang),
		"status":"Completed"
		})
	result=d1.insert()
	result.submit()
	if result:
		return "Visit Added"
	else:
		return "Something Went Wrong"




@frappe.whitelist()
def save_usersetting(platform,osversion,appversion,device_name):
	#user_setting=frappe.db.get("User Setting",{"user":frappe.session.user}).name
	user_setting=frappe.db.sql("""select name from `tabUser Setting` where name=%s""",frappe.session.user)
	if user_setting:
		setting_data=frappe.get_doc("User Setting",frappe.session.user)
		d1 = frappe.get_doc({
			"docstatus": 0,
			"doctype": "User Setting",
			"name": setting_data.name,
			"modified":setting_data.modified,
			"platform": str(platform),
			"os_version": str(osversion),
			"app_version": str(appversion),
			"device_name": str(device_name)
			})
		result=d1.save()
		if result:
			return get_version_detail()
			
		else:
			return "Something Went Wrong"
	else:
		d2 = frappe.get_doc({
					"docstatus": 0,
					"doctype": "User Setting",	
					"name": "New User Setting 1",
					"__islocal": 1,
					"__unsaved": 1,
					"owner":str(frappe.session.user),
					"user": str(frappe.session.user),
					"platform": str(platform),
					"os_version": str(osversion),
					"app_version": str(appversion),
					"device_name": str(device_name)
				   })
		result=d2.insert()
		if result:
			return get_version_detail()
		else:
			return "Something Went Wrong"





def get_version_detail():
	data1=frappe.db.sql("""select android_version,iphone_version,android_detail,iphone_detail,slogan from `tabApplication Version` where name='AV00001'""")
	data={}
	data["Android Version"]=data1[0][0]
	data["Iphone Version"]=data1[0][1]
	data["Android Detail"]=data1[0][2]
	data["Iphone Detail"]=data1[0][3]
	data["slogan"]=data1[0][4]
	return data
	


@frappe.whitelist()
def item_list():
	item_list=frappe.get_list("Item",filters=[["Item","show_in_website","=",1],["Item","disabled","=",0]],fields=["item_name", "item_code", "standard_rate", "net_weight", "item_group", "brand", "image", "thumbnail", "description","product_for","website_image","clp","slp"])
	return item_list

@frappe.whitelist()
def demo_list():
	demo_list=frappe.get_list("Demo Booking",filters=[["owner","=",str(frappe.session.user)]],fields=["salon_parlor_spa_name","date","time","trainer_name","name","select_demo_type","name","booked_by_name","comment"])
	if demo_list:
		return demo_list
	else:
		return "Demo Does Not Exist"

@frappe.whitelist()
def sso_month_list():
	sso_month=frappe.db.sql("""select distinct(DATE_FORMAT(posting_date,'%Y-%m') ) as "Month List" from `tabSecondary Sales Order` where (posting_date Is Not Null) and (posting_date Not in("0000-00")) and owner='"""+frappe.session.user+"""'""")
	if sso_month:
		return sso_month
	else:
		return "Does Not Exist"

@frappe.whitelist()
def sso_date_list(month,year):
	#sso_date_result=frappe.get_list("Secondary Sales Order",filters=[["posting_date","=",str(frappe.session.user)]],fields=["salon_parlor_spa_name","posting_date","docstatus"])
	#if demo_list:
	

	result=frappe.db.sql("""select posting_date,salon_parlor_spa_name,docstatus,grand_total,name,slp_total,clp_total from `tabSecondary Sales Order` where month(posting_date)=%s and year(posting_date)=%s and owner=%s""",(month,year,frappe.session.user))
	objects_list = []
	for row in result:
	    d = collections.OrderedDict()
	    d["posting_date"]=str(row[0])
	    d['salon_parlor_spa_name'] = row[1]
	    d['docstatus'] = str(row[2])
	    d['grand_total']=str(row[3])
	    d['name']=row[4]
            d['slp_total']=str(row[5])
	    d['clp_total']=str(row[6])
	  #  d['LastName'] = row[0][2]
	    objects_list.append(d)
	return objects_list	


@frappe.whitelist()
def day_summary(date1):
		sso=frappe.db.sql("""select salon_parlor_spa_name,grand_total,name from `tabSecondary Sales Order` where posting_date=%s and owner=%s""",(date1,frappe.session.user))
		kyc=frappe.db.sql("""select salon_parlor_spa_name,city_town,name from `tabKYC` where Date(creation)=%s and owner=%s""",(date1,frappe.session.user))
		expense=frappe.db.sql("""select expense_type,claim_amount from `tabExpense Claim Detail` where expense_date=%s and owner=%s""",(date1,frappe.session.user))
		demo=frappe.db.sql("""select salon_parlor_spa_name,date from `tabDemo Booking` where date=%s and owner=%s""",(date1,frappe.session.user))
		objects_list_sso = []
		for row in sso:
		    d = collections.OrderedDict()
		    d["salon_parlor_spa_name"]=str(row[0])
		    d['grand_total'] = row[1]
		    d['name'] = str(row[2])
		    objects_list_sso.append(d)

		objects_list_kyc = []
		for row in kyc:
		    d = collections.OrderedDict()
		    d["salon_parlor_spa_name"]=str(row[0])
		    d['city_town'] = row[1]
		    d['name'] = str(row[2])
		    objects_list_kyc.append(d)

		objects_list_expense = []
		for row in expense:
		    d = collections.OrderedDict()
		    d["expense_type"]=str(row[0])
		    d['claim_amount'] = row[1]
		    objects_list_expense.append(d)

		objects_list_demo = []
		for row in demo:
		    d = collections.OrderedDict()
		    d["salon_parlor_spa_name"]=str(row[0])
		    d['date'] = row[1]
		    objects_list_demo.append(d)
	
		
		
		
		d = collections.OrderedDict()
		d["secondary_sales_order"]=objects_list_sso
		d['kyc'] = objects_list_kyc
		d['expense'] = objects_list_expense
		d['demo']=objects_list_demo
		
	
		return d


@frappe.whitelist()
def drf(user):
	return frappe.db.sql("""select employee_name,name,current_address,cell_number from tabEmployee where user_id=%s""",user)
	#return frappe.db.get("Employee",{"user_id":user}).employee_name

@frappe.whitelist()
def drf1(user1):
	return frappe.db.get("Employee",{"user_id":user1}).employee_name

@frappe.whitelist()
def priorityCheck(doc,method):
	if doc.priority1_status=="":
		frappe.throw(_("Please Enter Priority 1 Status"))

	if doc.priority2_status=="":
		frappe.throw(_("Please Enter Priority 2 Status"))

	if doc.priority3_status=="":
		frappe.throw(_("Please Enter Priority 3 Status"))

@frappe.whitelist()
def visit_list():
	visit_list=frappe.get_list("Visit",filters=[["owner","=",str(frappe.session.user)]],fields=["salon_name","kyc","date","time","comments","name"])
	if visit_list:
		return visit_list
	else:
		return "Visit Does Not Exist"


@frappe.whitelist()
def salesPersonList():
    try:
        data=frappe.db.sql("""select name,employee_name,cell_number from `tabEmployee` where status='Active'""")
        if data:
            object_list_emp=[]
            for employee in data:
                d = collections.OrderedDict()
                d["employee"]=str(employee[0])
                d["employee_name"]=str(employee[1])
                d["Mobile Number"]=str(employee[2])
                object_list_emp.append(d)
            return object_list_emp
        else:
            return _(False)
    except:
        return _(False)


@frappe.whitelist()
def addTechnicalDailyActivity(data_obj):
    data=json.loads(data_obj)
    trainer=frappe.db.get("Employee",{"user_id":frappe.session.user}).name
    name_of_trainer=frappe.db.get("Employee",{"user_id":frappe.session.user}).employee_name
    salon_parlor_spa_name=frappe.db.get("KYC",{"name":data["salon_parlor_spa"]}).salon_parlor_spa_name
    contact_person=frappe.db.get("KYC",{"name":data["salon_parlor_spa"]}).full_name
    contact_number=frappe.db.get("KYC",{"name":data["salon_parlor_spa"]}).contact_number
    address_data=kyc_address(data["salon_parlor_spa"])
    msg=""
    msg =msg+ address_data[0].door_building_plot_number+"<br/>" \
        if not address_data[0].door_building_plot_number==None else " "
    msg = msg + address_data[0].street+"," \
        if not address_data[0].street==None else " "
    msg=msg+ address_data[0].landmark+"<br/>" \
        if not address_data[0].landmark==None else " " +"<br/>"
    msg = msg + address_data[0].area+"<br/>" \
        if not address_data[0].area==None else " "
    msg = msg + address_data[0].city_town + '-'  \
        if not address_data[0].city_town==None else " "
    msg = msg + address_data[0].pin + "<br/>" \
        if not address_data[0].pin==None else " "
    msg = msg + address_data[0].state + "<br/>" \
        if not address_data[0].state==None else " "

    doc=frappe.get_doc({
                       "docstatus": 0,
                       "doctype": "Technical - Daily Activity",
                       "name": "New Technical - Daily Activity 1",
                       "__islocal": 1,
                       "__unsaved": 1,
                       "owner": str(frappe.session.user),
                       "naming_series": "DAR/.date./.###",
                       "trainer": str(trainer),
                       "date": str(data["date"]),
                       "type_of_client": str(data["type_of_client"]),
                       "name_of_trainer": str(name_of_trainer),
                       "salon_parlor_spa_name": data["salon_parlor_spa_name"],
                       "contact_person": str(contact_person),
                       "contact_number": str(contact_number),
                       "salon_parlor_spa": str(data["salon_parlor_spa"]),
                       "address": str(msg),
                       "sales_person_name":str(data["sales_person_name"]),
                       "demonstration": data["demonstration"],
                       "training": data["training"],
                       "visit": data["visit"],
                       "day_celebration_skin_mixology": data["day_celebration_skin_mixology"],
                       "day_celebration_nutrimixology": data["day_celebration_nutrimixology"],
                       "day_celebration_root_deep": data["day_celebration_root_deep"],
                       "demo_details": data["demo_details"],
                       "skin_mixology_training": data["skin_mixology_training"],
                       "nutrimixology_training": data["nutrimixology_training"],
                       "root_deep_training": data["root_deep_training"],
                       "feedback_text": data["feedback_text"]
                       })
    save_data=doc.insert()
    if save_data:
        return _(True)
    else:
        return _(False)


@frappe.whitelist()
def technicalDailyActivityList():
    try:
        data_list=frappe.get_list("Technical - Daily Activity",["trainer","name_of_trainer","salon_parlor_spa_name","salon_parlor_spa","date","sales_person_name","feedback_text"])
        if data_list:
            return data_list
        else:
            return _(False)

    except:
        return _(False)


@frappe.whitelist()
def dashboard_visit(date1):
        visit=frappe.db.sql("""select salon_name,kyc,date,time,comments,name from `tabVisit` where date=%s and owner=%s""",(date1,frappe.session.user))
        object_list_visit=[]
        for row in visit:
            d = collections.OrderedDict()
            d["salon_name"]=str(row[0])
            d['kyc'] = str(row[1])
            d['date'] = str(row[2])
            d['time']=str(row[3])
            d['comments']=str(row[4])
            d['name']=str(row[5])
            object_list_visit.append(d)
        return object_list_visit

@frappe.whitelist()
def getNatureDetail(item):
	data=frappe.db.sql("""select natural_praportion,syntetic_praportion from `tabItem` where item_code=%s""",item,as_dict=True)
	if len(data):
		if data[0]["natural_praportion"]==None:
			data[0]["natural_praportion"]=0
		if data[0]["syntetic_praportion"]==None:
			data[0]["syntetic_praportion"]=0
			
		return data[0]
	else:
		return _(False)


@frappe.whitelist()
def getDistributorList():
	data=frappe.db.sql("""select name,customer_name,customer_group from `tabCustomer` where customer_group='Super Distributor' or customer_group='Distributor'""",as_dict=True)
	if len(data):
		return data
	else:
		return str()


@frappe.whitelist()
def get_mfr(name):
	data=frappe.db.sql("""select item,material_name,proportion from `tabmaterials` where parent=%s""",name)
	if data:
		object_list_emp=[]
		for row in data:
			data1=getNatureDetail(row[0])
			d = collections.OrderedDict()
			d["item"]=str(row[0])
			d["material_name"]=str(row[1])
			d["proportion"]=str(row[2])
			d["s_p"]=data1.syntetic_praportion
			d["n_p"]=data1.natural_praportion
			object_list_emp.append(d)
		return object_list_emp

@frappe.whitelist()
def get_cost_sheet_mfr(name):
	mfr=frappe.get_doc("Master Formula Record",name)
	for child in mfr.materials:
		child.rate = get_supplier_quotation(child.item)
	return mfr

@frappe.whitelist()
def get_cost_sheet_mpr(name):
	mpr=frappe.get_doc("Master Packaging Record",name)
	for child in mpr.master_packing_record:
		child.rate = get_supplier_quotation(child.packaging_material)
	return mpr
	

@frappe.whitelist()
def get_supplier_quotation(itemname):
	item_price= frappe.db.sql(""" select rate from `tabSupplier Quotation Item` WHERE item_code=%s ORDER BY creation DESC limit 1 """,itemname)
	if item_price:
		return item_price[0][0]
	else:
		return 0

@frappe.whitelist()
def getItemgroup(item):
	data=frappe.db.sql("""select item_group from `tabItem` where item_code=%s""",item)
	if data:
		return data[0][0]
	else:
		return _(False)

@frappe.whitelist()
def sendSMS(sso,method):
	mobileList=[]
	mobileList.append(str(sso.contact_number))
	msg="Thank you for ordering Brillare products.Your total order value is "
	msg=msg+str(sso.slp_total)+"Rs. You can call on 18002330603 or whatsapp on 9638666000 if you need any help.\n\nThank You\nBrillare Team"
	send_sms(mobileList,msg)



@frappe.whitelist()
def updateLatitudeLongitudeKyc(kyc,latitude,longitude):
	doc=frappe.get_doc("KYC",kyc)
	doc.latitude=str(latitude)
	doc.longitude=str(longitude)
	result=doc.save()
	if result:
		return _(True)
	else:
		return _(False)

@frappe.whitelist()
def gatKycLatLongStatus(kyc):
	doc=frappe.get_doc("KYC",kyc)
	if doc.latitude and doc.longitude:
		return _(True)
	else:
		return _(False)


# @frappe.whitelist()
# def validateSSO(self,method):
# 	if getdate(self.posting_date)<getdate(today()):
# 		frappe.throw("Please Select Today Or Greater than today date")
	



@frappe.whitelist()
def getTime():
	return frappe.utils.data.get_datetime()


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
def KRA_list(designation):
	try:
		KRA=frappe.get_list("KRA FORMAT",filters={"designation":designation},fields=["*"])
		#KRA=frappe.get_doc("KRA FORMAT", designation)
		if KRA:
			return generateResponse("S",message="KRA Found Successfully.",data=KRA[0])
		else:
			return generateResponse("S",message="Data Not Available",data=None)
	except Exception as e:
		return generateResponse("F",error=e)
@frappe.whitelist()
def appErrorLog(title,error):
	d = frappe.get_doc({
			"doctype": "App Error Log",
			"title":str("User:")+str(title+" "+"App Name:Brillare FF App"),
			"error":error
		})
	d = d.insert(ignore_permissions=True)
	return d



@frappe.whitelist()
def saveDemo(kyc,trainer,demo_type,date,time,comment):
	try:
		salon_name=frappe.db.get("KYC",{"name":kyc}).salon_parlor_spa_name
		trainer_name=frappe.db.get("Employee",{"name":trainer}).employee_name
		territory=frappe.db.get("KYC",{"name":kyc}).territory
		booked_by=frappe.db.get("Employee",{"user_id":frappe.session.user}).name
		booked_by_name=frappe.db.get("Employee",{"user_id":frappe.session.user}).employee_name
		doc=frappe.get_doc({
					"docstatus": 0,
					"doctype": "Demo Booking",
					"name": "New Demo Booking 2",
					"owner": frappe.session.users,
					"trainer":trainer,
					"trainer_name":trainer_name,
					"booked_by": booked_by,
					"booked_by_name":booked_by_name,
					"status": "Completed",
					"select_demo_type":demo_type,
					"time":str(time),
					"date": str(date),
					"salon_parlor_spa_name":salon_name,
					"kyc":kyc,
					"comment": comment,
					"territory":territory
				})
		doc1=doc.insert()
		if doc1:
			return generateResponse("S",message="Success",data=doc1)
		else:
			return generateResponse("S",message="Data Not Available",data=None)

	except Exception as e:
		return generateResponse("F",error=e)
	
	
		


		
	












