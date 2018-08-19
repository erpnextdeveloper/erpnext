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
from erpnext.accounts.utils import get_fiscal_year, getdate, nowdate

ter=[]

@frappe.whitelist()
def getAllBDEDataDaily():
	d = datetime.date.today()
	year = d.strftime("%Y")
	month = d.strftime("%B") 
	#return (year,month)
	doc=frappe.get_all("BDE Target and Incentive Plan",filters={"year":year,"month":month},fields=["name"])
	count=0

	cc= frappe.db.get_value("BDE Target and Incentive Plan Setting","BDE Target and Incentive Plan Setting", "email_cc_in_daily")
	subject= frappe.db.get_value("BDE Target and Incentive Plan Setting","BDE Target and Incentive Plan Setting","daily_email_subject")
	print_format= frappe.db.get_value("BDE Target and Incentive Plan Setting","BDE Target and Incentive Plan Setting","daily_print_format_name")
	print_letterhead= frappe.db.get_value("BDE Target and Incentive Plan Setting","BDE Target and Incentive Plan Setting","print_letterhead")	

	for row in doc:
		clster_data=frappe.get_doc("BDE Target and Incentive Plan",row.name)
		getBDEData(clster_data.employee_code,year,month,row.name)
		receipient=getUserIdfromEmployeeCode(clster_data.employee_code)
		make(recipients=receipient,cc=cc,subject=subject,doctype='BDE Target and Incentive Plan', name=row.name, send_email=1, print_format=print_format, print_letterhead=int(print_letterhead))
		count=count+1
	return count

@frappe.whitelist()
def getAllBDEDataMonthly():
	d = datetime.date.today()
	year = d.strftime("%Y")
	month = d.strftime("%B") 
	doc=frappe.get_all("BDE Target and Incentive Plan",filters={"year":year,"month":month},fields=["name"])
	count=0

	cc= frappe.db.get_value("BDE Target and Incentive Plan Setting","BDE Target and Incentive Plan Setting", "email_cc_in_monthly")
	subject= frappe.db.get_value("BDE Target and Incentive Plan Setting","BDE Target and Incentive Plan Setting","monthly_email_subject")
	print_format= frappe.db.get_value("BDE Target and Incentive Plan Setting","BDE Target and Incentive Plan Setting","monthly_print_format_name")
	print_letterhead= frappe.db.get_value("BDE Target and Incentive Plan Setting","BDE Target and Incentive Plan Setting","print_letterhead")	

	for row in doc:
		clster_data=frappe.get_doc("BDE Target and Incentive Plan",row.name)
		getBDEData(clster_data.employee_code,year,month,row.name)
		receipient=getUserIdfromEmployeeCode(clster_data.employee_code)
		make(recipients=receipient,cc=cc,subject=subject,doctype='BDE Target and Incentive Plan', name=row.name, send_email=1, print_format=print_format, print_letterhead=int(print_letterhead))
		count=count+1
	return count

def getUserIdfromEmployeeCode(emp_code):
	return frappe.db.get("Employee",{"name":emp_code}).user_id

@frappe.whitelist()
def getBDEData(emp_code,year,month,name):

	doc=frappe.get_doc("BDE Target and Incentive Plan",name)
	emp_code = doc.employee_code
	year= doc.year
	month=doc.month
	if doc.working_days and doc.monthly_sales_target_total:
		doc.secondary_trg = round(int(doc.monthly_sales_target_total) / int(doc.working_days))
	if doc.working_days and doc.salon_visit_target:
		doc.salon_visit_trg = round(int(doc.salon_visit_target) / int(doc.working_days))
	if doc.working_days and doc.salon_billing_target:
		doc.salon_billing_trg = round(int(doc.salon_billing_target) / int(doc.working_days)) 
	doc.secondary_ach =secondary_ach(emp_code)
	doc.salon_visit_ach = salon_visit_ach(emp_code) 
	doc.salon_billing_ach = salon_billing_ach(emp_code)
	doc.secondary_achievement=secondary_achievement(emp_code,year,month)
	doc.ytd_secondary_sales_achievement=round(flt(ytd_secondary_sales_achievement(emp_code)))
	doc.ytd_secondary_deficit_recovery_achievement=ytd_secondary_deficit_recovery_achievement(emp_code,year,month)
	doc.salon_visit_achievement=getVisitAchieve(emp_code,year,month)
	doc.salon_billing_achievement = salon_billing_achievement(emp_code,year,month)
	doc.new_salon_billing_achievement = new_salon_billing_achievement(emp_code,year,month)
	doc.repeat_salon_billing_achievement = round(flt(getAchievedRepeatBuyingSalons(emp_code,year,month)))
	doc.brillare_achievement=round(flt(getBrillareBrandWiseSale(emp_code,year,month,'ROOT DEEP')))
	doc.root_deep_achievement=round(flt(getBrandWiseSale(emp_code,year,month,'ROOT DEEP')))
	doc.in_salon_achievement=round(flt(getInsalonSale(emp_code,year,month)))
	doc.home_care_achievement=round(flt(getCategoryWiseSale(emp_code,year,month,'Home Care')))
	doc.hair_care_achievement=round(flt(getCategoryWiseSale(emp_code,year,month,'hair Care')))
	doc.skin_care_achievement=round(flt(getCategoryWiseSale(emp_code,year,month,'Skin Care')))
	if round(flt(doc.secondary_achievement)) > round(flt(doc.monthly_sales_target_total)):
		doc.incentive_claimed= round(flt(doc.monthly_sales_target_total)) * 0.017
		doc.incentive_reserve=0
		doc.incentive_deficit=0
		doc.incentive_surplus= round(flt(doc.secondary_achievement)) - round(flt(doc.monthly_sales_target_total))
	else:	
		doc.incentive_deficit=round(flt(doc.monthly_sales_target_total)) - round(flt(doc.secondary_achievement))
		doc.incentive_surplus=0
		doc.incentive_claimed=0
		doc.incentive_reserve=round(flt(doc.monthly_sales_target_total)) * 0.017
	
	doc.save()
	doc_data=getincentiveSummary(emp_code,month,year,name)
	doc_data1=frappe.get_doc("BDE Target and Incentive Plan",doc_data)
	doc1=doc_data1.save()
	if doc1:	
		return "true"
	
	
@frappe.whitelist()
def getUserFromEmployee(emp_code):
	user=frappe.db.sql("""select user_id from `tabEmployee` where name='"""+emp_code+"""'""",as_dict=1)
	if user:
		return user[0].user_id
	else:
		frappe.throw("No Such User Exist")

@frappe.whitelist()
def secondary_ach(emp_code):
	secondary_achievement=frappe.db.sql("""select sum(clp_total) as secondary_achievement from `tabSecondary Sales Order` as sso where sso.posting_date='"""+today()+"""' and owner=%s""",(getUserFromEmployee(emp_code)),as_dict=1)
	if not secondary_achievement[0].secondary_achievement==None:
		return secondary_achievement[0].secondary_achievement
	else:
		return 0


@frappe.whitelist()
def secondary_achievement(emp_code,year,month):
	secondary_achievement=frappe.db.sql("""select sum(clp_total) as secondary_achievement from `tabSecondary Sales Order` as sso where monthname(sso.posting_date)='"""+month+"""' and year(sso.posting_date)='"""+year+"""' and owner=%s""",(getUserFromEmployee(emp_code)),as_dict=1)
	if not secondary_achievement[0].secondary_achievement==None:
		return secondary_achievement[0].secondary_achievement
	else:
		return 0


@frappe.whitelist()
def ytd_secondary_sales_achievement(emp_code):
	current_fiscal_year = get_fiscal_year(nowdate(), as_dict=True)
	secondary_achievement=frappe.db.sql("""select sum(clp_total) as secondary_achievement from `tabSecondary Sales Order` where (posting_date BETWEEN '"""+str(current_fiscal_year.year_start_date)+"""' AND '"""+ str(current_fiscal_year.year_end_date)+"""' ) and owner=%s""",(getUserFromEmployee(emp_code)),as_dict=1)
	if not secondary_achievement[0].secondary_achievement==None:
		return secondary_achievement[0].secondary_achievement
	else:
		return 0

@frappe.whitelist()
def getVisitAchieve(emp_code,year,month):
	visit=frappe.db.sql("""select count(vs.name) as number from `tabVisit` as vs inner join `tabKYC` as ky on vs.kyc=ky.name where monthname(vs.date)='"""+month+"""' and year(vs.date)='"""+year+"""' and vs.owner=%s""",(getUserFromEmployee(emp_code)),as_dict=1)
	if not visit[0].number==None:
		return visit[0].number
	else:
		return 0

@frappe.whitelist()
def salon_visit_ach(emp_code):
	visit=frappe.db.sql("""select count(vs.name) as number from `tabVisit` as vs inner join `tabKYC` as ky on vs.kyc=ky.name where vs.date='"""+today()+"""' and vs.owner=%s""",(getUserFromEmployee(emp_code)),as_dict=1)
	if not visit[0].number==None:
		return visit[0].number
	else:
		return 0

@frappe.whitelist()
def getCategoryWiseSale(emp_code,year,month,category):
	haircaresale=frappe.db.sql("""select sum(ss.clp_amount) as number from `tabSecondary Sales Order` as sso inner join `tabSecondary Sales Order Item` as ss on sso.name=ss.parent inner join `tabItem` as item on ss.item_code=item.name  where item.category='"""+category+"""' and monthname(sso.posting_date)='"""+month+"""' and year(sso.posting_date)='"""+year+"""' and sso.owner=%s""",(getUserFromEmployee(emp_code)),as_dict=1)
	if not haircaresale[0].number==None:
		return haircaresale[0].number
	else:
		return 0

@frappe.whitelist()
def getBrandWiseSale(emp_code,year,month,brand):
	brillaresale=frappe.db.sql("""select sum(ss.clp_amount) as number from `tabSecondary Sales Order` as sso inner join `tabSecondary Sales Order Item` as ss on sso.name=ss.parent inner join `tabItem` as item on ss.item_code=item.name  where item.brand='"""+brand+"""' and monthname(sso.posting_date)='"""+month+"""' and year(sso.posting_date)='"""+year+"""' and sso.owner=%s""",(getUserFromEmployee(emp_code)),as_dict=1)
	if not brillaresale[0].number==None:
		return brillaresale[0].number
	else:
		return 0
@frappe.whitelist()
def getBrillareBrandWiseSale(emp_code,year,month,brand):
	brillaresale=frappe.db.sql("""select sum(ss.clp_amount) as number from `tabSecondary Sales Order` as sso inner join `tabSecondary Sales Order Item` as ss on sso.name=ss.parent inner join `tabItem` as item on ss.item_code=item.name  where item.brand <> '"""+brand+"""' and monthname(sso.posting_date)='"""+month+"""' and year(sso.posting_date)='"""+year+"""' and sso.owner=%s""",(getUserFromEmployee(emp_code)),as_dict=1)
	if not brillaresale[0].number==None:
		return brillaresale[0].number
	else:
		return 0

@frappe.whitelist()
def getInsalonSale(emp_code,year,month):
	is_sale=frappe.db.sql("""select sum(ss.clp_amount) as number from `tabSecondary Sales Order` as sso inner join `tabSecondary Sales Order Item` as ss on sso.name=ss.parent inner join `tabItem` as item on ss.item_code=item.name  where item.item_group Like %s and monthname(sso.posting_date)=%s and year(sso.posting_date)=%s and sso.owner=%s""",('%in salon%%',month,year,getUserFromEmployee(emp_code)),as_dict=1)
	if not is_sale[0].number==None:
		return is_sale[0].number
	else:
		return 0

@frappe.whitelist()
def getAchievedRepeatBuyingSalons(emp_code,year,month):
	counter = 0
	current_month_salon = frappe.db.sql("""select DISTINCT kyc from `tabSecondary Sales Order` where monthname(posting_date)=%s and year(posting_date)=%s and owner='"""+getUserFromEmployee(emp_code)+"""'""",(month,year),as_dict=1 )
	#return current_month_salon
	previous_month_salon = frappe.db.sql("""select DISTINCT kyc from `tabSecondary Sales Order` where monthname(posting_date)=%s and year(posting_date)=%s and owner='"""+getUserFromEmployee(emp_code)+"""'""",(getPreviousMonth(month),getPreviousYear(month,year)),as_dict=1 )
	#return previous_month_salon
	for salon in current_month_salon:
	#	return salon
		for salon1 in previous_month_salon:
	#		return salon1
			if salon.kyc == salon1.kyc:
				#return salon1
				counter += 1
	return counter

@frappe.whitelist()
def salon_billing_achievement(emp_code,year,month):
	p_call=frappe.db.sql("""select count(kyc) as number from `tabSecondary Sales Order` where monthname(posting_date)=%s and year(posting_date)=%s and owner=%s""",(month,year,getUserFromEmployee(emp_code)),as_dict=1)
	if p_call:
		if not p_call[0].number==None:
			return p_call[0].number
		else:
			return 0
	else:
		return 0

@frappe.whitelist()
def salon_billing_ach(emp_code):
	p_call=frappe.db.sql("""select count(kyc) as number from `tabSecondary Sales Order` where posting_date=%s and owner=%s""",(today(),getUserFromEmployee(emp_code)),as_dict=1)
	if p_call:
		if not p_call[0].number==None:
			return p_call[0].number
		else:
			return 0
	else:
		return 0

@frappe.whitelist()
def new_salon_billing_achievement(emp_code,year,month):
	p_call=frappe.db.sql("""select DISTINCT kyc from `tabSecondary Sales Order` where owner=%s and monthname(posting_date)=%s and year(posting_date)=%s ORDER BY posting_date ASC""",(getUserFromEmployee(emp_code),month,year),as_dict=1)
	if p_call:
		if not p_call[0].number==None:
			return p_call[0].number
		else:
			return 0
	else:
		return 0


@frappe.whitelist()
def ytd_secondary_deficit_recovery_achievement(emp_code,year,month):
	monthList = ['January','Febuary','March','April','May','June','July','Augest','September','October','November','December']
	if month==monthList[0] or month==monthList[1] or month==monthList[2]:
		incentive_deficit_current=frappe.db.sql(""" select sum(incentive_deficit) as number from `tabBDE Target and Incentive Plan` where year=%s and employee_code=%s""",(year,emp_code),as_dict=1)
		year=int(year)-1
		incentive_deficit=frappe.db.sql(""" select sum(incentive_deficit) as number from `tabBDE Target and Incentive Plan` where year=%s and employee_code=%s and month  NOT IN ('January', 'Febuary', 'March')""",(year,emp_code),as_dict=1)
		return incentive_deficit_current[0].number + incentive_deficit[0].number
	else:
		incentive_deficit=frappe.db.sql(""" select sum(incentive_deficit) as number from `tabBDE Target and Incentive Plan` where year=%s and employee_code=%s  and month  NOT IN 	('January', 'Febuary', 'March')""",(year,emp_code),as_dict=1)
		return incentive_deficit[0].number

@frappe.whitelist()
def getPreviousMonth(month):
	monthList = ['January','Febuary','March','April','May','June','July','Augest','September','October','November','December']
	index= (monthList.index(month))
	if(index==0):
		return monthList[11]
	else:
		return monthList[index-1]


@frappe.whitelist()
def getPreviousYear(month,year):
	if month=="January":
		return int(year)-1
	else:
		return year

@frappe.whitelist()
def getincentiveSummary(emp_code,month,year,name):
	Bde_data=frappe.get_doc("BDE Target and Incentive Plan",name)
	Bde_data.incentive_summary_detail=[]
	Bde_data.save()
	
	monthList = ['April','May','June','July','Augest','September','October','November','December','January','Febuary','March']
	start_month=(monthList.index('April'))
	end_month= (monthList.index(month))
	count=1
	response=[]
	while start_month<=end_month:
		#d = collections.OrderedDict()
		listtarget=frappe.db.sql("""select name from `tabBDE Target and Incentive Plan` where employee_code='"""+emp_code+"""' and year='"""+year+"""' and month='"""+monthList[start_month]+"""'""")
		#d["name"]=listtarget[0][0]
		if listtarget:
			doc_name=frappe.get_doc("BDE Target and Incentive Plan",listtarget[0][0])
			doc=frappe.get_doc({
						"docstatus": 0,
						"doctype": "Incentive Summary",
						"name": "New Incentive Summary 1",
						"owner": "Administrator",
						"month":str(monthList[start_month]),
						"parent":str(name),
						"idx":str(count),
						"parentfield": "incentive_summary_detail",
						"parenttype": "BDE Target and Incentive Plan",
						"secondary_trg":str(doc_name.monthly_sales_target_total),
						"secondary_ach":str(doc_name.secondary_achievement),
						"deficit":str(doc_name.incentive_deficit),
						"surplus":str(doc_name.incentive_surplus),
						"incentive_proposed":str(doc_name.incentive),
						"incentive_claimed":str(doc_name.incentive_claimed),
						"incentive_reserve":str(doc_name.incentive_reserve)
					})
			doc.insert(ignore_permissions=True)
		start_month=start_month+1
		count=count+1
		#response.append(d)
	data=frappe.get_doc("BDE Target and Incentive Plan",name)
	data1=data.save()
	return data1.name
			


