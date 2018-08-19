from __future__ import unicode_literals
import frappe
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

from datetime import datetime,date, timedelta
from dateutil.relativedelta import relativedelta
from frappe.utils import getdate, validate_email_add, today, add_years,add_days,format_datetime
from frappe.model.naming import make_autoname
from frappe import throw, _, scrub
import frappe.permissions
from frappe.model.document import Document
import json
import collections



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
	frappe.db.set_value("Secondary Sales Order",{"name":name},{"docstatus":status},None)
	frappe.db.set_value("Secondary Sales Order Item",{"parent":name},{"docstatus":status},None)
	return "Succesfully submited"

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
	territory=frappe.db.get("KYC",{"name":kyc}).territory
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
		"territory":str(territory)
		})
	result=d1.insert()
	if result:
		return "Visit Added"
	else:
		return "Something Went Wrong"

@frappe.whitelist()
def visit_list():
	visit_list=frappe.get_list("Visit",filters=[["owner","=",str(frappe.session.user)]],fields=["salon_name","kyc","date","time","comments","name"])
	if visit_list:
		return visit_list
	else:
		return "Visit Does Not Exist"



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
	data1=frappe.db.sql("""select android_version,iphone_version,android_detail,iphone_detail from `tabApplication Version` where name='AV00001'""")
	data={}
	data["Android Version"]=data1[0][0]
	data["Iphone Version"]=data1[0][1]
	data["Android Detail"]=data1[0][2]
	data["Iphone Detail"]=data1[0][3]
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
def usertype():
	usertype=frappe.db.sql("""select designation from `tabEmployee` where status='Active' and user_id='"""+frappe.session.user+"""'""")
	if usertype[0][0]=="Regional Sales Manager" or usertype[0][0]=="Area Sales Manager" or usertype[0][0]=="Cluster Head" or usertype[0][0]=="National Business Manager" or usertype[0][0]=="General Manager" or usertype[0][0]=="Key Account Manager":
		return "Sales Manager"
	
	elif usertype[0][0]=="Sales Officer":
		return "Sales Person"

	elif usertype[0][0]=="Technical Trainer" or usertype[0][0]=="Senior Technical Trainer" or usertype[0][0]=="Regional Technical Manager" or usertype[0][0]=="Corporate Technical Trainer":
		return "Technical Trainer"

	elif usertype[0][0]=="Regional Technical Trainer":
		return "Technical Trainer Manager"

	else:
		return "Normal User"

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
def visit_delete(id):
	return frappe.db.sql("""delete from `tabVisit` where name=%s""",id)

@frappe.whitelist()
def leave_list():
	data=frappe.db.sql("""select name,from_date,to_date,leave_type,half_day,total_leave_days,half_day_slot,description,employee,employee_name,posting_date from `tabLeave Application` where workflow_state='Applied' and leave_approver=%s""",frappe.session.user)
	object_list_leave=[]
	for row in data:
	    d = collections.OrderedDict()
	    d["name"]=str(row[0])
	    d['from_date'] = str(row[1])
	    d['to_date'] = str(row[2])
	    d['leave_type']=str(row[3])
	    d['half_day']=str(row[4])
	    d['total_leave_days']=str(row[5])
	    d["half_day_slot"]=str(row[6])
	    d['description'] = str(row[7])
	    d['employee'] = str(row[8])
	    d['employee_name']=str(row[9])
	    d['posting_date']=str(row[10])
	    object_list_leave.append(d)
	return object_list_leave

@frappe.whitelist()
def leave_approve_manager(name):
	try:
		data=frappe.get_doc("Leave Application",name)
		data.workflow_state="Approved By Manager"
		doc=data.save(ignore_permissions=True)
		if doc:
			return _(True)
	except:
		return _(False)

@frappe.whitelist()
def leave_reject_manager(name):
	try:
		data=frappe.get_doc("Leave Application",name)
		data.workflow_state="Rejected"
		doc=data.save(ignore_permissions=True)
		if doc:
			return _(True)
	except:
		return _(False)


@frappe.whitelist()
def leaveApplicationList_manager(employee,date1):
	data=frappe.db.sql("""select name,from_date,to_date,leave_type,half_day,total_leave_days,half_day_slot,description,employee,employee_name,posting_date,workflow_state from `tabLeave Application` where workflow_state in('Open','Applied') and employee=%s and posting_date=%s""",(employee,date1))
	if data:
		object_list_leave=[]
		for row in data:
		    d = collections.OrderedDict()
		    d["name"]=str(row[0])
		    d["from_date"] = str(row[1])
		    d["to_date"] = str(row[2])
		    d["leave_type"]=str(row[3])
		    d["half_day"]=str(row[4])
		    d["total_leave_days"]=str(row[5])
		    d["half_day_slot"]=str(row[6])
		    d["description"] = str(row[7])
		    d["employee"] = str(row[8])
		    d["employee_name"]=str(row[9])
		    d["posting_date"]=str(row[10])
		    d["workflow_state"]=str(row[11])
		    object_list_leave.append(d)
		return object_list_leave
	else:
		return _(False)
		
@frappe.whitelist()
def expenseList_manager(employee, date1=None):
	if date1 == None:
		data = frappe.db.sql("""select `tabExpense Claim Detail`.expense_type,`tabExpense Claim Detail`.claim_amount,`tabExpense Claim Detail`.description,`tabExpense Claim Detail`.name from `tabExpense Claim` inner join `tabExpense Claim Detail` on `tabExpense Claim`.name=`tabExpense Claim Detail`.parent where employee=%s""",employee)
		if data:
			return data
		else:
			return _(False)
	else:
		data = frappe.db.sql("""select `tabExpense Claim Detail`.expense_type,`tabExpense Claim Detail`.claim_amount,`tabExpense Claim Detail`.description,`tabExpense Claim Detail`.name from `tabExpense Claim` inner join `tabExpense Claim Detail` on `tabExpense Claim`.name=`tabExpense Claim Detail`.parent where employee=%s and `tabExpense Claim Detail`.expense_date=%s""", (employee, date1))
		if data:
			return data
		else:
			return _(False)
#	if data:
#		object_list_exp=[]
#		for row in data:
#		    d = collections.OrderedDict()
#		    d["employee"]=str(row[0])
#		    d["employee_name"] = str(row[1])
#		    d["expense_date"] = str(row[2])
#		    d["expense_type"]=str(row[3])
#		    d["description"]=str(row[4])
#		    d["claim_amount"]=str(row[5])
#		    d["sanctioned_amount"]=str(row[6])
#		    object_list_exp.append(d)
#		return object_list_exp
#	else:
#		return _(False)
 																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																									
	
	


@frappe.whitelist()
def visitList_manager(employee,date1=None):
	#data=frappe.get_list("Visit",fields=["salon_name","kyc","date","time","comments","name","territory","sales_person","sales_person_name"])
	if date1==None:
		data=frappe.db.sql("""select salon_name,kyc,date,time,comments,name,territory,sales_person,sales_person_name from `tabVisit` where sales_person=%s """,employee)
	else:
		data=frappe.db.sql("""select salon_name,kyc,date,time,comments,name,territory,sales_person,sales_person_name from `tabVisit` where sales_person=%s and date=%s""",(employee,date1))

	if data:
		object_list_visit=[]
		for employee in data:
			d = collections.OrderedDict()
			d["salon_name"]=str(employee[0])
			d["kyc"]=str(employee[1])
			d["date"]=str(employee[2])
			d["time"]=str(employee[3])
			d["name"]=str(employee[4])
			d["territory"]=str(employee[5])
			d["sales_person"]=str(employee[6])
			d["sales_person_name"]=str(employee[7])
			object_list_visit.append(d)
		return object_list_visit
	else:
		return _(False)

@frappe.whitelist()
def kycList_manager(employee, date1=None):
	user = frappe.db.get("Employee", {"name": employee}).user_id
	if date1 == None:
		data = frappe.db.sql(
                    """select name,salon_parlor_spa_name,city_town,state,territory from `tabKYC` where owner=%s""", user)
		if data:
			return data
		else:
			return _(False)
	else:
		data = frappe.db.sql(
                    """select name,salon_parlor_spa_name,city_town,state,territory from `tabKYC` where owner=%s and Date(creation)=%s""", (user, date1))
		if data:
			return data
		else:
			return _(False)
	#if data:
	#	object_list_kyc=[]
	#	for employee in data:
	#		d = collections.OrderedDict()
	#		d["name"]=str(employee[0])
	#		d["salon_parlor_spa_name"]=str(employee[1])
	#		d["door_building_plot_number"]=str(employee[2])
	#		d["street"]=str(employee[3])
	#		d["landmark"]=str(employee[4])
	#		d["area"]=str(employee[5])
	#		d["city_town"]=str(employee[6])
	#		d["pin"]=str(employee[7])
	#		d["state"]=str(employee[8])
	#		d["territory"]=str(employee[9])
	#		d["contact_number"]=str(employee[10])
	#		d["alternate_number"]=str(employee[11])
	#		d["full_name"]=str(employee[12])
	#		d["creation"]=str(employee[13])
	#		object_list_kyc.append(d)
	#	return object_list_kyc
	#else:
	#	return _(False)

@frappe.whitelist()
def demoList_manager(employee,date1=None):
	if date1==None:
		data=frappe.db.sql("""select salon_parlor_spa_name,date,time,name from `tabDemo Booking` where trainer=%s""",employee)
		if data:
			return data
		else:
			return _(False)
		
	else:
		data=frappe.db.sql("""select salon_parlor_spa_name,date,time,name from `tabDemo Booking` where trainer=%s and date=%s""",(employee,date1))
		if data:
			return data
		else:
			return _(False)

	#if data:
	#	object_list_demo=[]
	#	for employee in data:
	#		d = collections.OrderedDict()
	#		d["trainer"]=str(employee[0])
	#		d["trainer_name"]=str(employee[1])
	#		d["select_demo_type"]=str(employee[2])
	#		d["date"]=str(employee[3])
	#		d["booked_by"]=str(employee[4])
	#		d["booked_by_name"]=str(employee[5])
	#		d["time"]=str(employee[6])
	#		d["kyc"]=str(employee[7])
	#		d["salon_parlor_spa_name"]=str(employee[8])
	#		d["comment"]=str(employee[9])
	#		object_list_demo.append(d)
	#	return object_list_demo
	#else:
	#	return _(False)

@frappe.whitelist()
def ssoList_manager(employee,date1=None):
	user=frappe.db.get("Employee",{"name":employee}).user_id
	if date1==None:
		data=frappe.db.sql("""select salon_parlor_spa_name,name,docstatus,grand_total from `tabSecondary Sales Order` where owner=%s""",user)
		if data:
			return data
		else:
			return _(False)
	
	else:
		return frappe.db.sql("""select salon_parlor_spa_name,name,docstatus,grand_total from `tabSecondary Sales Order` where owner=%s and posting_date=%s""",(user,date1))
		if data:
			return data
		else:
			return _(False)
	
	#if sso:
	#	object_list_sso=[]
	#	for employee in sso:
	#		d = collections.OrderedDict()
	#		d["salon_parlor_spa_name"]=str(employee[0])
	#		d["name"]=str(employee[1])
	#		d["docstatus"]=str(employee[2])
	#		d["grand_total"]=str(employee[3])
	#		
	#		object_list_sso.append(d)
	#	return object_list_sso
	#else:
	#	return _(False)
	
	



@frappe.whitelist()
def employeeList():
	data=frappe.db.sql("""select for_value from `tabUser Permission` where allow='Employee' and user=%s""",frappe.session.user)
	object_list_emp=[]
	for employee in data:
		d = collections.OrderedDict()
		d["employee"]=str(employee[0])
		d["employee_name"]=getEmployeeName(employee[0])
		d["Mobile No"]=getEmployeeNumber(employee[0])
		object_list_emp.append(d)
	return object_list_emp

##bhavik

@frappe.whitelist()
def employeeAttendanceList():
    data=frappe.db.sql("""select Permission.for_value,Attendance.start_a_day_time,Attendance.stop_a_day_time from `tabUser Permission` as Permission INNER JOIN `tabAttendance` as Attendance on Permission.for_value=Attendance.employee where Permission.allow='Employee' and Permission.user=%s and attendance_date=%s and not Attendance.employee=%s""",(frappe.session.user,today(),getEmployeeID(frappe.session.user)))
    object_list_emp=[]
    for employee in data:
        d = collections.OrderedDict()
        d["emp"]=str(employee[0])
        d["emp_name"]=getEmployeeName(employee[0])
        d["emp_start"]=employee[1]
        d["emp_end No"]=employee[2]
        object_list_emp.append(d)
    d = collections.OrderedDict()
    if len(object_list_emp):
        d["msg"]="Data  Found"
        d["status"]=True
        d["data"]=object_list_emp
    else:
        d["msg"]="Data Not Found"
        d["data"]=None
        d["status"]= False
    return d


@frappe.whitelist()
def employeeMonthlyAttendanceList(empid):
	
	today = date.today()
	d = today - relativedelta(months=1)
	first_date =  date(d.year, d.month+1, 1)
	last_date = date(today.year, today.month+1, 1) - relativedelta(days=1)
	data = frappe.get_list("Attendance", filters=[["Attendance","attendance_date","Between",[first_date,last_date]],["Attendance","employee","=",empid]], fields=['name','status','employee','start_a_day_time','stop_a_day_time','attendance_date','attendance_type','employee_name'])
	d = collections.OrderedDict()
	if len(data):
		d["msg"]="Data  Found"
		d["status"]=True
		d["data"]=data
	else:
		d["msg"]="Data Not Found"
		d["data"]=None
		d["status"]= False
	return d



@frappe.whitelist()
def employeeMonthyVisitList(empid):
	
	# today = date.today()
	# d = today - relativedelta(months=1)
	# first_date =  date(d.year, d.month+1, 1)
	# last_date = date(today.year, today.month+1, 1) - relativedelta(days=1)
	data = frappe.get_list("Visit", filters=[["Visit","sales_person","=",empid]], fields=['name','sales_person','kyc','salon_name','date','territory','time','comments'])
	d = collections.OrderedDict()
	if len(data):
		d["msg"]="Data  Found"
		d["status"]=True
		d["data"]=data
	else:
		d["msg"]="Data Not Found"
		d["data"]=None
		d["status"]= False
	return d


@frappe.whitelist()
def employeeLeaveApplicationList():
    data=frappe.db.sql("""select Permission.for_value,Leave1.employee_name,sum(Leave1.total_leave_days) from `tabUser Permission` as Permission INNER JOIN `tabLeave Application` as Leave1 on Permission.for_value=Leave1.employee where Permission.allow='Employee' and Permission.user=%s and (Leave1.workflow_state="Applied" or Leave1.workflow_state="Open" ) and not Leave1.employee=%s group by Permission.for_value """,(frappe.session.user,getEmployeeID(frappe.session.user)))
    object_list_emp=[]
    for employee in data:
        d = collections.OrderedDict()
        d["emp"]=str(employee[0])
        d["emp_name"]=employee[1]
        d["total_leave_days"] =employee[2]
        object_list_emp.append(d)
	
    if len(object_list_emp):
		d1 = collections.OrderedDict()
		d1["msg"]="Data  Found"
		d1["status"]=True
		d1["data"]=object_list_emp
    else:
		d1 = collections.OrderedDict()
		d1["msg"]="Data Not Found"
		d1["data"]=None
		d1["status"]= False
    return d1


@frappe.whitelist()
def employeeLeaveApplicationListByEmployee(empid):
    data=frappe.db.sql("""select Permission.for_value,Leave1.employee_name,Leave1.leave_type,Leave1.from_date,Leave1.to_date,Leave1.leave_balance,Leave1.name,Leave1.description,Leave1.half_day,Leave1.half_day_slot, Leave1.workflow_state,Leave1.total_leave_days,Leave1.half_day_date from `tabUser Permission` as Permission INNER JOIN `tabLeave Application` as Leave1 on Permission.for_value=Leave1.employee where Permission.allow='Employee' and Permission.user=%s and (Leave1.workflow_state="Applied" or Leave1.workflow_state="Open" ) and not Leave1.employee=%s and Leave1.employee=%s """,(frappe.session.user,getEmployeeID(frappe.session.user),empid))
    object_list_emp=[]
    for employee in data:
        d = collections.OrderedDict()
        d["emp"]=str(employee[0])
        d["emp_name"]=employee[1]
        d["leave_type"]=str(employee[2])
        d["from_date"]=str(employee[3])
        d["to_date"]=str(employee[4])
        d["leave_balance"]=str(employee[5])
        d["name"]=str(employee[6])
        d["reason"]=employee[7]
        d["half_day"]=employee[8]
        d["half_day_slot"] =employee[9]
        d["status"] =employee[10]
        d["total_leave_days"] =employee[11]
        d["half_day_date"] =employee[12]
        object_list_emp.append(d)
    
    if len(object_list_emp):
        d1 = collections.OrderedDict()
        d1["msg"]="Data  Found"
        d1["status"]=True
        d1["data"]=object_list_emp
    else:
        d1 = collections.OrderedDict()
        d1["msg"]="Data Not Found"
        d1["data"]=None
        d1["status"]= False
    return d1



@frappe.whitelist()
def employeeVisitList():
    data=frappe.db.sql("""select Permission.for_value,count(Permission.for_value) as count from `tabUser Permission` as Permission INNER JOIN `tabVisit` as Visit on Permission.for_value=Visit.sales_person where Permission.allow='Employee' and Permission.user=%s and NOT Visit.sales_person=%s and date=%s group by Permission.for_value """,(frappe.session.user,getEmployeeID(frappe.session.user),today()))
    object_list_emp=[]
    for employee in data:
        d = collections.OrderedDict()
        d["emp"]=str(employee[0])
        d["emp_name"]=getEmployeeName(employee[0])
        d["count"]=employee[1]
        object_list_emp.append(d)
    d = collections.OrderedDict()
    if len(object_list_emp):
        d["msg"]="Data  Found"
        d["status"]=True
        d["data"]=object_list_emp
    else:
        d["msg"]="Data Not Found"
        d["data"]=None
        d["status"]= False
    return d



@frappe.whitelist()
def employeeExpenseList():
    data=frappe.db.sql("""select Permission.for_value,Expense.employee_name,Expense.total_claimed_amount,Expense.name from `tabUser Permission` as Permission INNER JOIN `tabExpense Claim` as Expense on Permission.for_value=Expense.employee where Permission.allow='Employee' and Permission.user=%s and NOT Expense.employee=%s """,(frappe.session.user,getEmployeeID(frappe.session.user)))
    object_list_emp=[]
    for employee in data:
        d = collections.OrderedDict()
        d["emp"]=str(employee[0])
        d["emp_name"]=employee[1]
        d["total_claimed_amount"]=str(employee[2])
        d["expense_name"]=str(employee[3])
        object_list_emp.append(d)
	d1 = collections.OrderedDict()
    if len(object_list_emp):
		d1 = collections.OrderedDict()
		d1["msg"]="Data  Found"
		d1["status"]=True
		d1["data"]=object_list_emp
    else:
		d1 = collections.OrderedDict()
		d1["msg"]="Data Not Found"
		d1["data"]=None
		d1["status"]= False
    return d1

@frappe.whitelist()
def employeeMonthlyExpenseList(empid):
	
	# today = date.today()
	# d = today - relativedelta(months=1)
	# first_date =  date(d.year, d.month+1, 1)
	# last_date = date(today.year, today.month+1, 1) - relativedelta(days=1)
	list = frappe.get_list("Expense Claim", filters=[["Expense Claim","employee","=",empid]], fields=['name','employee','employee_name','total_claimed_amount','is_paid','total_sanctioned_amount','posting_date','status'])
	for li in list:
		item = frappe.get_list("Expense Claim Detail", filters=[["Expense Claim Detail","parent","=",li.name]], fields=['expense_date','expense_type','description','claim_amount','sanctioned_amount','name'])
		li.expenses = item
	d = collections.OrderedDict()
	if len(list):
		d["msg"]="Data  Found"
		d["status"]=True
		d["data"]=list
	else:
		d["msg"]="Data Not Found"
		d["data"]=None
		d["status"]= False
	return d

def getEmployeeID(name):
    emp_name=frappe.db.sql("""select employee from `tabEmployee` where user_id=%s""",name)
    return emp_name[0][0]


@frappe.whitelist()
def employeeTargetandIncentiveList():
    data=frappe.db.sql("""select Permission.for_value,TIP.name,TIP.month_and_year,TIP.employee_code,TIP.employee_name,TIP.from,TIP.to,TIP.working_days,TIP.daily_sales_target,TIP.monthly_sales_target,TIP.incentive,TIP.from_first,TIP.second_to,TIP.second_working_days,TIP.second_daily_sales_target,TIP.second_monthly_sales_target_second,TIP.second_incetive_second,TIP.monthly_sales_target_total from `tabUser Permission` as Permission INNER JOIN `tabTarget and Incentive Plan` as TIP on Permission.for_value=TIP.employee_code where Permission.allow='Employee' and Permission.user=%s and NOT TIP.employee_code=%s """,(frappe.session.user,getEmployeeID(frappe.session.user)))
    object_list_emp=[]
    for employee in data:
        d = collections.OrderedDict()
        d["session"]=frappe.session.user
        d["name"]=str(employee[1])
        d["month"]=employee[2]
        d["emp"]=str(employee[3])
        d["emp_name"]=employee[4]
        d["today_date"]=date.today()
        salesdatatoday=frappe.db.sql(""" select sum(clp_total) from `tabSecondary Sales Order` where owner=%s AND posting_date=%s group by posting_date""",(getEmployeeUserID(employee[3]),date.today()))
        if salesdatatoday:
            d["today_sales_achievement"]=str(salesdatatoday[0][0])
        else:
            d["today_sales_achievement"]= 0
        
        
        d["first_slot_from"]=str(employee[5])
        d["first_slot_to"]=employee[6]
        d["first_slot_working_days"]=str(employee[7])
        d["first_slot_daily_sales_target"]=employee[8]
        d["first_slot_sales_target"]=str(employee[9])
        salesdatamonthly=frappe.db.sql(""" select sum(clp_total) from `tabSecondary Sales Order` where owner=%s AND posting_date BETWEEN %s AND %s group by owner""",(getEmployeeUserID(employee[3]),employee[5],employee[6]))
        if salesdatamonthly:
            d["first_slot_sales_achievement"]=str(salesdatamonthly[0][0])
        else:
            d["first_slot_sales_achievement"]= str(0)
        d["incentive"]=employee[10]


        d["second_slot_from"]=str(employee[11])
        d["second_slot_to"]=employee[12]
        d["second_slot_working_days"]=str(employee[13])
        d["second_slot_daily_sales_target"]=employee[14]
        d["second_slot_sales_target"]=employee[15]
#        salesdatatoday1=frappe.db.sql(""" select sum(clp_total) from `tabSecondary Sales Order` where owner=%s AND posting_date=%s group by posting_date""",(employee[3],date.today()))
#        if salesdatatoday1:
#            d["second_today_sales_achievement"]=str(salesdatatoday1[0][0])
#        else:
#            d["second_today_sales_achievement"]= 0
        salesdatamonthly1=frappe.db.sql(""" select sum(clp_total) from `tabSecondary Sales Order` where owner=%s AND posting_date BETWEEN %s AND %s group by posting_date""",(getEmployeeUserID(employee[3]),employee[11],employee[12]))
        if salesdatamonthly1:
            d["second_slot_sales_achievement"]=str(salesdatamonthly1[0][0])
        else:
            d["second_slot_sales_achievement"]= str(0)
        d["second_slot_incetive"]=str(employee[16])
        d["monthly_sales_target_total"]=employee[17]
        d["monthly_sales_achievement_total"] = str(float(d["second_slot_sales_achievement"])+float(d["first_slot_sales_achievement"]))
        object_list_emp.append(d)
    d1 = collections.OrderedDict()
    if len(object_list_emp):
        d1 = collections.OrderedDict()
        d1["msg"]="Data  Found"
        d1["status"]=True
        d1["data"]=object_list_emp
    else:
        d1 = collections.OrderedDict()
        d1["msg"]="Data Not Found"
        d1["data"]=None
        d1["status"]= False
    return d1

@frappe.whitelist()
def getTodaySalesOrderEmployeeWise(emp_id):

	usr=frappe.db.get("Employee",{"name":emp_id}).user_id
	data=frappe.db.sql("""select salon_parlor_spa_name,name,docstatus,grand_total,clp_total,slp_total,posting_date from `tabSecondary Sales Order` where posting_date=%s and owner=%s""",(today(),usr))
	if data:
		object_list_emp=[]
		for employee in data:
			d = collections.OrderedDict()
			d["salon_parlor_spa_name"]=str(employee[0])
			d["name"]=str(employee[1])
			d["docstatus"]=str(employee[2])
			d["grand_total"]=str(employee[3])
			d["clp_total"]=str(employee[4])
			d["slp_total"]=str(employee[5])
			d["posting_date"]=str(employee[6])
			object_list_emp.append(d)
		return object_list_emp
	else:
		return _(False)	

@frappe.whitelist()
def getTodaySalesOrderEmployeeWise_Monthly(emp_id):

	usr=frappe.db.get("Employee",{"name":emp_id}).user_id
	data=frappe.db.sql("""select salon_parlor_spa_name,name,docstatus,grand_total,clp_total,slp_total,posting_date from `tabSecondary Sales Order` where owner=%s""",usr)
	if data:
		object_list_emp=[]
		for employee in data:
			d = collections.OrderedDict()
			d["salon_parlor_spa_name"]=str(employee[0])
			d["name"]=str(employee[1])
			d["docstatus"]=str(employee[2])
			d["grand_total"]=str(employee[3])
			d["clp_total"]=str(employee[4])
			d["slp_total"]=str(employee[5])
			d["posting_date"]=str(employee[6])
			object_list_emp.append(d)
		return object_list_emp
	else:
		return _(False)	




def getEmployeeID(name):
    emp_name=frappe.db.sql("""select employee from `tabEmployee` where user_id=%s""",name)
    return emp_name[0][0]

def getEmployeeUserID(name):
    emp_name=frappe.db.sql("""select user_id from `tabEmployee` where employee=%s""",name)
    return emp_name[0][0]
##bhavik

def getEmployeeName(name):
	emp_name=frappe.db.sql("""select employee_name from `tabEmployee` where name=%s""",name)
	return emp_name[0][0]

def getEmployeeNumber(name):
	emp_num=frappe.db.sql("""select cell_number from `tabEmployee` where name=%s""",name)
	if emp_num:
		return emp_num[0][0]
	else:
		return ""



@frappe.whitelist()
def addSalesOrder(kyc,posting_date):
	territory=frappe.db.get("KYC",{"name":kyc}).territory
	salon_parlor_spa_name=frappe.db.get("KYC",{"name":kyc}).salon_parlor_spa_name
	door_building_plot_number=frappe.db.get("KYC",{"name":kyc}).door_building_plot_number
	street=frappe.db.get("KYC",{"name":kyc}).street
	area=frappe.db.get("KYC",{"name":kyc}).area
	city_town=frappe.db.get("KYC",{"name":kyc}).city_town
	pin=frappe.db.get("KYC",{"name":kyc}).pin
	state=frappe.db.get("KYC",{"name":kyc}).state
	full_name=frappe.db.get("KYBhavesh JavarC",{"name":kyc}).full_name
	alternate_number=frappe.db.get("KYC",{"name":kyc}).alternate_number
	email=frappe.db.get("KYC",{"name":kyc}).email
	landmark=frappe.db.get("KYC",{"name":kyc}).landmark
	doc=frappe.get_doc({
				"docstatus": 0,
				"doctype": "Secondary Sales Order",
				"name": "New Secondary Sales Order 2",
				"__islocal": 1,
				"__unsaved": 1,
				"owner": str(frappe.session.user),
				"naming_series": "SO-",
				"company": "Brillare Science Private Limited",
				"territory": ""+str(territory),
				"currency": "INR",
				"selling_price_list": "Standard Selling",
				"price_list_currency": "INR",
				"delivery_confirmation": "Yes",
				"items": [],
				"posting_date":str(posting_date),
				"salon_parlor_spa_name":""+str(salon_parlor_spa_name),
				"door_building_plot_number":""+str(door_building_plot_number),
				"street": ""+str(street),
				"landmark": ""+str(landmark),
				"area": ""+str(area),
				"city_town": ""+str(city_town),
				"pin": ""+str(pin),
				"state": ""+str(state),
				"full_name": ""+str(full_name),
				"alternate_number": ""+str(alternate_number),
				"email": ""+str(email),
				"customer_group":"Retail",
				"kyc": str(kyc),
				"clp_total": 12,
				"slp_total": 12,
				"taxes_and_charges": "In State GST"
			})
	data=doc.insert()
	return data

def save_sales_order_item(sid,item_id,item_qty,date):
	rate=frappe.db.get("Item",{"name":item_id}).standard_rate
	item_doc=frappe.get_doc({
					"docstatus": 0,
					"doctype": "Secondary Sales Order Item",
					"name": "New Secondary Sales Order Item 2",
					"__islocal": 1,
					"__unsaved": 1,
					"owner": str(frappe.session.user),
					"stock_uom": "Nos",
					"margin_type": "",
					"parent": "New Secondary Sales Order 2",
					"parentfield": "items",
					"parenttype": "Secondary Sales Order",
					"idx": 1,
					"item_code": "1EDSED",
					"qty": 1,
					"rate": 15,
					"description": "test<br>",
					"item_name": "test",
					"uom": "Kg",
					"conversion_factor": 1,
					"slp": "12",
					"clp": "12",
					"slp_amount": "12",
					"clp_amount": "12",
					"warehouse": "Finish Goods Warehouse - BSPL"
				})
	item_save=item_doc.insert()

@frappe.whitelist(allow_guest=True)
def webhook_test(json):
	doc=frappe.get_doc({
				"docstatus": 0,
				"doctype": "Test",
				"name": "New Test 1",
				"__islocal": 1,
				"__unsaved": 1,
				"address": str(json)
			})
	doc.insert()


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
def enterSanctionedAmount(doc_id,amount):
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
			"description": str(doc.description),
			"expense_date": str(doc.expense_date),
			"expense_type": str(doc.expense_type),
			"default_account": "Field Expense - BSPL",
			"claim_amount": str(doc.claim_amount),
			"modified":doc.modified,
			"sanctioned_amount":str(amount)
		})
	d.save(ignore_permissions=True)
	doc1=frappe.get_doc("Expense Claim",parent)
	d2=doc1.save(ignore_permissions=True)
	if d2:
		return _(True)
	else:
		return _(False)


@frappe.whitelist(allow_guest=True)
def getServerDate():
	return today()


@frappe.whitelist()
def employeeListForExpense(date1):
    data=frappe.db.sql("""select Permission.for_value,Expense.employee_name,Expense.total_claimed_amount,Expense.name from `tabUser Permission` as Permission INNER JOIN `tabExpense Claim` as Expense on Permission.for_value=Expense.employee where Permission.allow='Employee' and Permission.user=%s and NOT Expense.employee=%s group by Permission.for_value""",(frappe.session.user,getEmployeeID(frappe.session.user)))
    object_list_emp=[]
    if data:
    	for row in data:
    		data1=frappe.db.sql("""select ec.employee,ec.employee_name,ecd.expense_date,sum(ecd.claim_amount) as 'claim_amount' from `tabExpense Claim Detail` as ecd INNER JOIN `tabExpense Claim` as ec on ecd.parent=ec.name where ec.employee=%s and expense_date=%s group by ec.employee_name limit 1""",(row[0],date1),as_dict=True)
    		if data1:
    			object_list_emp.append(data1[0])
    else:
    	return _(False)

    return object_list_emp

@frappe.whitelist()
def expenseList(employee,date1):
    data1=frappe.db.sql("""select ecd.name,ec.employee,ec.employee_name,ecd.expense_date,ecd.claim_amount,ecd.expense_type,ecd.description from `tabExpense Claim Detail` as ecd INNER JOIN `tabExpense Claim` as ec on ecd.parent=ec.name where ec.employee=%s and expense_date=%s""",(employee,date1),as_dict=True)
    object_list=[]
    if data1:
    	for row in data1:
    		object_list.append(row)

    	return object_list
    else:
		return _(False)

@frappe.whitelist()
def enterSanctioned(object):
	da1=[]
	data=json.loads(object)
	if len(data):
		for row in data:
			enterSanctionedAmount(row["doc_id"],row["amount"])
			
		return _(True)
	else:
		return _(False)





	

	



	












