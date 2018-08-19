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


ter=[]

@frappe.whitelist()
def getAllClusterDocumnetDaily():
	d = datetime.date.today()
	year = d.strftime("%Y")
	month = d.strftime("%B") 
	#return (year,month)
	doc=frappe.get_all("Cluster Business Plan",filters={"year":year,"month":month},fields=["name"])
	#return doc
	count=0

	cc= frappe.db.get_value("Cluster Business Plan Setting","Cluster Business Plan Setting", "email_cc_in_daily")
	subject= frappe.db.get_value("Cluster Business Plan Setting","Cluster Business Plan Setting","daily_email_subject")
	print_format= frappe.db.get_value("Cluster Business Plan Setting","Cluster Business Plan Setting","daily_print_format_name")
	print_letterhead= frappe.db.get_value("Cluster Business Plan Setting","Cluster Business Plan Setting","print_letterhead")	

	for row in doc:
		clster_data=frappe.get_doc("Cluster Business Plan",row.name)
		getClusterData(clster_data.employee_code,year,month,row.name)
		receipient=getUserIdfromEmployeeCode(clster_data.employee_code)
		make(recipients=receipient,cc=cc,subject=subject,doctype='Cluster Business Plan',name=row.name,send_email=1,print_format=print_format,print_letterhead=int(print_letterhead))
		count=count+1
	return count

@frappe.whitelist()
def getAllClusterDocumnetMonthly():
	d = datetime.date.today()
	year = d.strftime("%Y")
	month = d.strftime("%B") 
	doc=frappe.get_all("Cluster Business Plan",filters={"year":year,"month":month},fields=["name"])
	count=0
	for row in doc:
		clster_data=frappe.get_doc("Cluster Business Plan",row.name)
		getClusterData(clster_data.employee_code,year,month,row.name)
		receipient=getUserIdfromEmployeeCode(clster_data.employee_code)
		make(recipients=receipient,cc='bhavesh.javar@brillarescience.com,brillare@brillarescience.com',subject='Monthly Cluster Business Plan',doctype='Cluster Business Plan',name=row.name,send_email=1,print_format='Cluster Business Print',print_letterhead=1)
		count=count+1
	return count
		

@frappe.whitelist()
def getClusterData(emp_code,year,month,name):
	doc=frappe.get_doc("Cluster Business Plan",name)
	doc.today_target=round(flt(doc.secondary_target)/flt(doc.total_working_days))
	doc.today_salon_visit_target=round(flt(doc.visit_target)/flt(doc.total_working_days))
	doc.today_productive_salon_target=round(flt(doc.productive_call_target)/flt(doc.total_working_days))
	doc.today_salon_visit_achievement=round(getTodaySalonVisit(emp_code,year,month))
	doc.today_productive_salon_achievement=round(getTodayProductiveCall(emp_code,year,month))
	doc.today_productive_bds=round(flt(getTodayProductiveBD(emp_code)))
	doc.today_non_productive_bds=round(flt(getNoEmployeeUnderCluster(emp_code)-flt(doc.today_productive_bds)))	
	doc.secondary_achievement=round(flt(getSecondaryAchievment(emp_code,year,month)))
	doc.today_arch=round(flt(getTodaySecondrySalesOrder(emp_code)))
	#doc.cumulative_target=round(flt(getCumulativeTarget(emp_code,year,month,name)))
	doc.cumulative_short_fall=round(flt(doc.cumulative_target)-flt(doc.secondary_achievement))
	doc.short_fall_recovery_target=round(flt(doc.cumulative_target)-flt(doc.secondary_target))
	doc.short_fall_recovery_achievement=round(flt(doc.secondary_target)-flt(doc.secondary_achievement))
	doc.primary_achievement=round(flt(getPrimaryAchievment(emp_code,year,month)))
	doc.brillare_sale_achievement=round(flt(getBrandWiseSale(emp_code,year,month,'BRILLARE SCIENCE')))
	doc.in_salon_sale_achievement=round(flt(getInsalonSale(emp_code,year,month)))
	doc.root_deep_sale_achievement=round(flt(getBrandWiseSale(emp_code,year,month,'ROOT DEEP')))
	doc.hair_care_sale_achievement=round(flt(getCategoryWiseSale(emp_code,year,month,'Hair Care')))
	doc.skin_care_sale_achievement=round(flt(getCategoryWiseSale(emp_code,year,month,'Skin Care')))
	doc.home_care_sale_achievement=round(flt(getInhomecareSale(emp_code,year,month)))
	doc.achieved_typical_accounts=round(flt(getAchievedTypicalAccount(emp_code,year,month)))
	doc.achieved_business_from_typical_accounts=round(flt(getAchievedTypicalAccountBusiness(emp_code,year,month)))
	doc.achieved_standard_account=round(flt(getAchievedStandardAccount(emp_code,year,month)))
	doc.achieved_business_from_standard_accounts=round(flt(getAchievedStandardAccountBusiness(emp_code,year,month)))
	doc.achieved_important_accounts=round(flt(getAchievedImportantAccount(emp_code,year,month)))
	doc.achieved_business_from_important_accounts=round(flt(getAchievedImportantAccountBusiness(emp_code,year,month)))
	doc.achieved_key_accounts=round(flt(getAchievedKeyAccount(emp_code,year,month)))
	doc.achieved_business_from_key_accounts=round(flt(getAchievedKeyAccountBusiness(emp_code,year,month)))
	doc.visit_target_achievement=round(flt(getVisitAchieve(emp_code,year,month)))
	doc.productive_call_target_achievement=round(flt(getProductiveCall(emp_code,year,month)))
	doc.new_salon_target_achievement=round(flt(getNewSalonTarget(emp_code,year,month)))
	doc.achieved_buying_salons_per_bde=round(flt(getAchievedBuyingSalon(emp_code,year,month)))
	doc.achieved_treatment_giving_salons_per_stt=round(flt(getAchievedBuyingSalonTreatment(emp_code,year,month)))
	doc.closing_stock_of_supers=round(flt(getSuperStock(emp_code,year,month)))
	doc.super_nod_achievement=round(flt(getSuperNod(emp_code,year,month)))
	doc.closing_stock_of_distributors=round(flt(getDistributorStock(emp_code,year,month)))
	doc.second_primary_achievement=round(flt(getSecondPrimary(emp_code,year,month)))
	doc.distributor_nod_achievement=round(flt(getDistNod(emp_code,year,month)))
	doc.in_salon_training_achievement=round(flt(getInSalonTrainingAchievement(emp_code,year,month)))
	doc.achieved_3_months_active_salons_base=round(flt(getAchieved3MonthsActiveSalonsBase(emp_code,year,month)))
	doc.achieved_repeat_buying=round(flt(getAchievedRepeatBuyingSalons(emp_code,year,month)))
	if int(len(getBDE(emp_code)))==0:
		doc.ypm_target_per_bde=0
	else:
		doc.ypm_target_per_bde = round(flt(doc.secondary_target) / flt(len(getBDE(emp_code))))
	if int(len(getBDE(emp_code)))==0:
		doc.ypm_ach_per_bde=0
	else:
		doc.ypm_ach_per_bde = round(flt(doc.secondary_achievement) / flt(len(getBDE(emp_code))))
	doc.bde_vacancy=0
	doc.stt_vacancy=0
	doc.date=today()
	if getNoEmployeeUnderCluster(emp_code)==0:
		doc.daily_productivity=0
		doc.monthly_productivity=0
	else:
		doc.daily_productivity=round(flt(doc.productive_call_target)/flt(getNoEmployeeUnderCluster(emp_code)))
		doc.monthly_productivity=round(flt(doc.productive_call_target_achievement)/flt(getNoEmployeeUnderCluster(emp_code)))
	doc.save()
	doc_data=getAllDataBDEWise(emp_code,year,month,name)
	doc_data1=frappe.get_doc("Cluster Business Plan",doc_data)
	doc1=doc_data1.save()
	if doc1:
		return "True"


@frappe.whitelist()
def getTodaySecondrySalesOrder(emp_code):
	ter_list=getTerritoryFromEmployee(emp_code)
	conditions=''
	conditions+="territory in("
	for row in ter_list:
		conditions+="'"+str(row)+"',"
	conditions+= "'b'"+')'
	today_sale=frappe.db.sql("""select sum(clp_total) from `tabSecondary Sales Order` where posting_date='"""+today()+"""' and {0}""".format(conditions))
	if not today_sale[0][0]==None:
		return today_sale[0][0]
	else:
		return 0

@frappe.whitelist()
def getBDE(emp_code):
	ter_list=getTerritoryFromEmployee(emp_code)
	conditions=''
	count=0
	conditions+="territory in("
	for row in ter_list:
		conditions+="'"+str(row)+"',"
	conditions+= "'b'"+')'
	return frappe.db.sql("""select user_id from `tabEmployee` where status='Active' and designation in("Business Development Executive","Senior Business Development Executive","Business Development Manager") and {0}""".format(conditions))

@frappe.whitelist()
def getTodayProductiveBD(emp_code):
	ter_list=getTerritoryFromEmployee(emp_code)
	conditions=''
	count=0
	conditions+="territory in("
	for row in ter_list:
		conditions+="'"+str(row)+"',"
	conditions+= "'b'"+')'
	bde_no=frappe.db.sql("""select user_id from `tabEmployee` where status='Active' and designation in("Business Development Executive","Senior Business Development Executive","Business Development Manager") and {0}""".format(conditions))
	for row in bde_no:
		data=frappe.db.sql("""select count(name) from `tabSecondary Sales Order` where posting_date='"""+today()+"""' and owner=%s""",row[0])
		if not data[0][0]==None:
			if not int(data[0][0])==0:
				count=count+1
	return count


@frappe.whitelist()
def getNoEmployeeUnderCluster(emp_code):
	ter_list=getTerritoryFromEmployee(emp_code)
	conditions=''
	conditions+="territory in("
	for row in ter_list:
		conditions+="'"+str(row)+"',"
	conditions+= "'b'"+')'
	bde_no=frappe.db.sql("""select count(name) from `tabEmployee` where status='Active' and designation in("Business Development Executive","Senior Business Development Executive","Business Development Manager") and {0}""".format(conditions))
	if not bde_no[0][0]==None:
		return bde_no[0][0]
	else:
		return 0

	



@frappe.whitelist()
def getSecondaryAchievment(emp_code,year,month):
	ter_list=getTerritoryFromEmployee(emp_code)
	conditions=''
	conditions+="territory in("
	for row in ter_list:
		conditions+="'"+str(row)+"',"
	conditions+= "'b'"+')'
	secondary_a=frappe.db.sql("""select sum(clp_total) from `tabSecondary Sales Order` where monthname(posting_date)='"""+month+"""' and year(posting_date)='"""+year+"""' and {0}""".format(conditions))
	if not secondary_a[0][0]==None:
		return secondary_a[0][0]
	else:
		return 0

@frappe.whitelist()
def getPrimaryAchievment(emp_code,year,month):
	ter_list=getTerritoryFromEmployee(emp_code)
	conditions=''
	conditions+="territory in("
	for row in ter_list:
		conditions+="'"+str(row)+"',"
	conditions+= "'b'"+')'
	primary_a=frappe.db.sql("""select sum(grand_total) from `tabSales Invoice` where docstatus=1 and monthname(posting_date)='"""+month+"""' and year(posting_date)='"""+year+"""' and {0}""".format(conditions))
	if not primary_a[0][0]==None:
		return primary_a[0][0]
	else:
		return 0


@frappe.whitelist()
def getCumulativeTarget(emp_code,year,month,name):
	year1=0
	month1=0
	if month == 'January':
		year1=int(year) - 1
		month1 = 'December'

	elif month == 'February':
		year1=int(year)
		month1 = 'January'

	elif month == 'March':
		year1=int(year)
		month1 = 'February'

	elif month == 'April':
		year1=int(year)
		month1 = 'March'

	elif month == 'May':
		year1=int(year)
		month1 = 'April'

	elif month == 'June':
		year1=int(year)
		month1 = 'May'

	elif month == 'July':
		year1=int(year)
		month1 = 'June'

	elif month == 'August':
		year1=int(year)
		month1 = 'July'

	elif month == 'September':
		year1=int(year)
		month1 = 'August'

	elif month == 'October':
		year1=int(year)
		month1 = 'September'

	elif month == 'November':
		year1=int(year)
		month1 = 'October'

	elif month == 'December':
		year1=int(year)
		month1 = 'November'
	else:
		year1=int(year)
		month1 = month

	cluster_list=frappe.get_list("Cluster Business Plan",filters={"year":year1,"month":str(month1)},fields=["*"])
	if cluster_list:
		doc=frappe.get_doc("Cluster Business Plan",name)
		return int(cluster_list[0].cumulative_short_fall)+int(doc.secondary_target)



@frappe.whitelist()
def getTerritoryFromEmployee(emp_code):
	empter=frappe.db.get("Employee",{"name":emp_code}).territory
	del ter[:]
	ter.append(empter)
	terList(empter,0)
	return ter



@frappe.whitelist()
def terList(parent,index):
	childList=frappe.db.sql("select territory_name from tabTerritory where parent_territory = %s",str(parent))
	#frappe.msgprint(parent)conditions
	if childList:	
		for child in childList:
			ter.append(child[0])
	if len(ter)>index+1:	
		terList(ter[index+1],index+1)
	else:
		return;

@frappe.whitelist()
def getBrandWiseSale(emp_code,year,month,brand):
	ter_list=getTerritoryFromEmployee(emp_code)
	conditions=''
	conditions+="sso.territory in("
	for row in ter_list:
		conditions+="'"+str(row)+"',"
	conditions+= "'b'"+')'
	if brand=="BRILLARE SCIENCE":
		brillaresale=frappe.db.sql("""select sum(ss.clp_amount) from `tabSecondary Sales Order` as sso inner join `tabSecondary Sales Order Item` as ss on sso.name=ss.parent inner join `tabItem` as item on ss.item_code=item.name  where not item.brand='ROOT DEEP' and monthname(sso.posting_date)='"""+month+"""' and year(sso.posting_date)='"""+year+"""' and {0}""".format(conditions))
		if not brillaresale[0][0]==None:
			return brillaresale[0][0]
		else:
			return 0
	else:
		brillaresale=frappe.db.sql("""select sum(ss.clp_amount) from `tabSecondary Sales Order` as sso inner join `tabSecondary Sales Order Item` as ss on sso.name=ss.parent inner join `tabItem` as item on ss.item_code=item.name  where item.brand='ROOT DEEP' and monthname(sso.posting_date)='"""+month+"""' and year(sso.posting_date)='"""+year+"""' and {0}""".format(conditions))
		if not brillaresale[0][0]==None:
			return brillaresale[0][0]
		else:
			return 0



@frappe.whitelist()
def getInsalonSale(emp_code,year,month):
	ter_list=getTerritoryFromEmployee(emp_code)
	conditions=''
	conditions+="territory in("
	for row in ter_list:
		conditions+="'"+str(row)+"',"
	conditions+= "'b'"+')'
	is_sale=frappe.db.sql("""select sum(ss.clp_amount) from `tabSecondary Sales Order` as sso inner join `tabSecondary Sales Order Item` as ss on sso.name=ss.parent inner join `tabItem` as item on ss.item_code=item.name  where item.item_group Like 'In Salon%' and monthname(sso.posting_date)='"""+month+"""' and year(sso.posting_date)='"""+year+"""' and {0}""".format(conditions))
	if not is_sale[0][0]==None:
		return is_sale[0][0]
	else:
		return 0


@frappe.whitelist()
def getCategoryWiseSale(emp_code,year,month,category):
	ter_list=getTerritoryFromEmployee(emp_code)
	conditions=''
	conditions+="territory in("
	for row in ter_list:
		conditions+="'"+str(row)+"',"
	conditions+= "'b'"+')'
	haircaresale=frappe.db.sql("""select sum(ss.clp_amount) from `tabSecondary Sales Order` as sso inner join `tabSecondary Sales Order Item` as ss on sso.name=ss.parent inner join `tabItem` as item on ss.item_code=item.name  where item.category='"""+category+"""' and monthname(sso.posting_date)='"""+month+"""' and year(sso.posting_date)='"""+year+"""' and {0}""".format(conditions))
	if not haircaresale[0][0]==None:
		return haircaresale[0][0]
	else:
		return 0


@frappe.whitelist()
def getInhomecareSale(emp_code,year,month):
	ter_list=getTerritoryFromEmployee(emp_code)
	conditions=''
	conditions+="territory in("
	for row in ter_list:
		conditions+="'"+str(row)+"',"
	conditions+= "'b'"+')'
	is_sale=frappe.db.sql("""select sum(ss.clp_amount) from `tabSecondary Sales Order` as sso inner join `tabSecondary Sales Order Item` as ss on sso.name=ss.parent inner join `tabItem` as item on ss.item_code=item.name  where item.item_group Like 'Home Care%' and monthname(sso.posting_date)='"""+month+"""' and year(sso.posting_date)='"""+year+"""' and {0}""".format(conditions))
	if not is_sale[0][0]==None:
		return is_sale[0][0]
	else:
		return 0

@frappe.whitelist()
def getAchievedTypicalAccount(emp_code,year,month):
	ter_list=getTerritoryFromEmployee(emp_code)
	conditions=''
	conditions+="territory in("
	for row in ter_list:
		conditions+="'"+str(row)+"',"
	conditions+= "'b'"+')'
	sso_list=frappe.db.sql("""select count(kyc) from `tabSecondary Sales Order` where clp_total<5000 and {0}""".format(conditions))
	if not sso_list[0][0]==None:
		return sso_list[0][0]
	else:
		return 0

@frappe.whitelist()
def getAchievedTypicalAccountBusiness(emp_code,year,month):
	ter_list=getTerritoryFromEmployee(emp_code)
	conditions=''
	conditions+="territory in("
	for row in ter_list:
		conditions+="'"+str(row)+"',"
	conditions+= "'b'"+')'
	typical_business=frappe.db.sql("""select sum(clp_total) from `tabSecondary Sales Order` where clp_total<5000 and {0}""".format(conditions))
	if not typical_business[0][0]==None:
		return typical_business[0][0]
	else:
		return 0


@frappe.whitelist()
def getAchievedStandardAccount(emp_code,year,month):
	ter_list=getTerritoryFromEmployee(emp_code)
	conditions=''
	conditions+="territory in("
	for row in ter_list:
		conditions+="'"+str(row)+"',"
	conditions+= "'b'"+')'
	sso_list=frappe.db.sql("""select count(kyc) from `tabSecondary Sales Order` where clp_total between 5000 and 20000 and {0}""".format(conditions))
	if not sso_list[0][0]==None:
		return sso_list[0][0]
	else:
		return 0

@frappe.whitelist()
def getAchievedStandardAccountBusiness(emp_code,year,month):
	ter_list=getTerritoryFromEmployee(emp_code)
	conditions=''
	conditions+="territory in("
	for row in ter_list:
		conditions+="'"+str(row)+"',"
	conditions+= "'b'"+')'
	standard_business=frappe.db.sql("""select sum(clp_total) from `tabSecondary Sales Order` where clp_total between 5000 and 20000 and {0}""".format(conditions))
	if not standard_business[0][0]==None:
		return standard_business[0][0]
	else:
		return 0


@frappe.whitelist()
def getAchievedImportantAccount(emp_code,year,month):
	ter_list=getTerritoryFromEmployee(emp_code)
	conditions=''
	conditions+="territory in("
	for row in ter_list:
		conditions+="'"+str(row)+"',"
	conditions+= "'b'"+')'
	sso_list=frappe.db.sql("""select count(kyc) from `tabSecondary Sales Order` where clp_total between 20000 and 40000 and {0}""".format(conditions))
	if not sso_list[0][0]==None:
		return sso_list[0][0]
	else:
		return 0

@frappe.whitelist()
def getAchievedImportantAccountBusiness(emp_code,year,month):
	ter_list=getTerritoryFromEmployee(emp_code)
	conditions=''
	conditions+="territory in("
	for row in ter_list:
		conditions+="'"+str(row)+"',"
	conditions+= "'b'"+')'
	important_business=frappe.db.sql("""select sum(clp_total) from `tabSecondary Sales Order` where clp_total between 20000 and 40000 and {0}""".format(conditions))
	if not important_business[0][0]:
		return important_business[0][0]
	else:
		return 0


@frappe.whitelist()
def getAchievedKeyAccount(emp_code,year,month):
	ter_list=getTerritoryFromEmployee(emp_code)
	conditions=''
	conditions+="territory in("
	for row in ter_list:
		conditions+="'"+str(row)+"',"
	conditions+= "'b'"+')'
	sso_list=frappe.db.sql("""select count(kyc) from `tabSecondary Sales Order` where clp_total>=40000 and {0}""".format(conditions))
	return sso_list[0][0]

@frappe.whitelist()
def getAchievedKeyAccountBusiness(emp_code,year,month):
	ter_list=getTerritoryFromEmployee(emp_code)
	conditions=''
	conditions+="territory in("
	for row in ter_list:
		conditions+="'"+str(row)+"',"
	conditions+= "'b'"+')'
	key_business=frappe.db.sql("""select sum(clp_total) from `tabSecondary Sales Order` where clp_total>=40000 and {0}""".format(conditions))	
	if not key_business[0][0]==None:
		return key_business[0][0]
	else:
		return 0


@frappe.whitelist()
def getVisitAchieve(emp_code,year,month):
	ter_list=getTerritoryFromEmployee(emp_code)
	conditions=''
	conditions+="ky.territory in("
	for row in ter_list:
		conditions+="'"+str(row)+"',"
	conditions+= "'b'"+')'
	visit=frappe.db.sql("""select count(vs.name) from `tabVisit` as vs inner join `tabKYC` as ky on vs.kyc=ky.name where monthname(vs.date)='"""+month+"""' and year(vs.date)='"""+year+"""' and {0}""".format(conditions))
	if not visit[0][0]==None:
		return visit[0][0]
	else:
		return 0

@frappe.whitelist()
def getTodaySalonVisit(emp_code,year,month):
	ter_list=getTerritoryFromEmployee(emp_code)
	conditions=''
	conditions+="ky.territory in("
	for row in ter_list:
		conditions+="'"+str(row)+"',"
	conditions+= "'b'"+')'
	visit=frappe.db.sql("""select count(vs.name) from `tabVisit` as vs inner join `tabKYC` as ky on vs.kyc=ky.name where vs.date='"""+today()+"""' and {0}""".format(conditions))
	if not visit[0][0]==None:
		return visit[0][0]
	else:
		return 0


@frappe.whitelist()
def getProductiveCall(emp_code,year,month):
	ter_list=getTerritoryFromEmployee(emp_code)
	conditions=''
	conditions+="territory in("
	for row in ter_list:
		conditions+="'"+str(row)+"',"
	conditions+= "'b'"+')'
	p_call=frappe.db.sql("""select count(kyc) from `tabSecondary Sales Order` where monthname(posting_date)='"""+month+"""' and year(posting_date)='"""+year+"""' and {0}""".format(conditions))
	if not p_call[0][0]==None:
		return p_call[0][0]
	else:
		return 0

@frappe.whitelist()
def getTodayProductiveCall(emp_code,year,month):
	ter_list=getTerritoryFromEmployee(emp_code)
	conditions=''
	conditions+="territory in("
	for row in ter_list:
		conditions+="'"+str(row)+"',"
	conditions+= "'b'"+')'
	p_call=frappe.db.sql("""select count(kyc) from `tabSecondary Sales Order` where posting_date='"""+today()+"""' and {0}""".format(conditions))
	if not p_call[0][0]==None:
		return p_call[0][0]
	else:
		return 0



@frappe.whitelist()
def getNewSalonTarget1(emp_code,year,month):
	ter_list=getTerritoryFromEmployee(emp_code)
	conditions=''
	conditions+="territory in("
	for row in ter_list:
		conditions+="'"+str(row)+"',"
	conditions+= "'b'"+')'
	salon_list=frappe.db.sql("""select count(name) from `tabKYC` where monthname(creation)='"""+month+"""' and year(creation)='"""+year+"""' and {0}""".format(conditions))
	if not salon_list[0][0]==None:
		return salon_list[0][0]
	else:
		return 0


@frappe.whitelist()
def getNewSalonTarget(emp_code,year,month):
	count=0
	ter_list=getTerritoryFromEmployee(emp_code)
	conditions=''
	conditions+="territory in("
	for row in ter_list:
		conditions+="'"+str(row)+"',"
	conditions+= "'b'"+')'
	object_list=[]
	monthList = ['January','Febuary','March','April','May','June','July','Augest','September','October','November','December']
	index= (monthList.index(month))
	sales_order_list=frappe.db.sql("""select kyc from `tabSecondary Sales Order` where monthname(creation)='"""+month+"""' and year(creation)='"""+year+"""' and {0}""".format(conditions))
	for row in sales_order_list:
		first_order_date=frappe.db.sql("""select posting_date from `tabSecondary Sales Order` where kyc='"""+row[0]+"""'""")

		if not first_order_date[0][0]==None:
			d = collections.OrderedDict()
			d["kyc"]=str(row[0])
			d["first_date"]=str(first_order_date[0][0])
			object_list.append(d)
			if str(first_order_date[0][0])=='0000-00-00':
				count=count
			else:
				mydate = datetime.datetime.strptime(str(first_order_date[0][0]),'%Y-%m-%d')
				month1=mydate.month
				year1=mydate.year
				#return (month1,index)
				if int(year1)==int(year):
					if int(index)==int(month1):
						count=count+1
						

	return count




@frappe.whitelist()
def getAchievedBuyingSalon(emp_code,year,month):
	ter_list=getTerritoryFromEmployee(emp_code)
	conditions=''
	conditions+="territory in("
	for row in ter_list:
		conditions+="'"+str(row)+"',"
	conditions+= "'b'"+')'	
	bde_count=0
	bde_no=frappe.db.sql("""select count(name) from `tabEmployee` where status='Active' and designation in("Business Development Executive","Senior Business Development Executive","Business Development Manager") and {0}""".format(conditions))
	if not bde_no[0][0]==None:
		bde_count=bde_no[0][0]
	else:
		bde_count=0

	salon_order_count=frappe.db.sql("""select distinct count(kyc) from `tabSecondary Sales Order` where monthname(posting_date)='"""+month+"""' and year(posting_date)='"""+year+"""' and {0}""".format(conditions))
	if not bde_count==0:
		if not salon_order_count[0][0]==None:
			return salon_order_count[0][0]/bde_count
		else:
			return 0
	else:
		return 0


@frappe.whitelist()
def getAchievedBuyingSalonTreatment(emp_code,year,month):
	ter_list=getTerritoryFromEmployee(emp_code)
	conditions=''
	conditions+="ky.territory in("
	for row in ter_list:
		conditions+="'"+str(row)+"',"
	conditions+= "'b'"+')'	

	conditions1=''
	conditions1+="territory in("
	for row in ter_list:
		conditions1+="'"+str(row)+"',"
	conditions1+= "'b'"+')'	

	tt_count=0
	tt_no=frappe.db.sql("""select count(name) from `tabEmployee` where status='Active' and designation in("Technical Trainer","Senior Technical Trainer","Regional Technical Manager") and {0}""".format(conditions1))
	if not tt_no[0][0]==None:
		tt_count=tt_no[0][0]
	else:
		tt_count=0

	tech_count=frappe.db.sql("""select distinct count(td.salon_parlor_spa) from `tabTechnical - Daily Activity` as td inner join `tabKYC` as ky on td.salon_parlor_spa=ky.name where td.type_of_client='Existing' and monthname(td.date)='"""+month+"""' and year(td.date)='"""+year+"""' and {0}""".format(conditions))
	if tech_count[0][0]==None:
		return 0
	if int(tt_count)==0:
		return 0
	else:
		return tech_count[0][0]/tt_count

@frappe.whitelist()
def getSuperStock(emp_code,year,month):
	year1=getPreviousYear(month,year)
	month1=getPreviousMonth(month)
	total=0
	super_doc=frappe.get_all("Stocks and Sales Report",filters={"year":year1,"month":month1,"cluster_head_name":emp_code,"types_of_stockist":'Super Distributor'},fields=["name"])
	for row in super_doc:
		doc_value=frappe.db.sql("""select sum(clp_amount) from `tabStocks N Sales` where parent=%s""",row["name"])
		if doc_value:
			total=total+doc_value[0][0]
	return total



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
def getSuperNod(emp_code,year,month):
	year1=getPreviousYear(month,year)
	month1=getPreviousMonth(month)
	total=0
	sell_total=0
	super_doc=frappe.get_all("Stocks and Sales Report",filters={"year":year1,"month":month1,"cluster_head_name":emp_code,"types_of_stockist":'Super Distributor'},fields=["name"])
	for row in super_doc:
		doc_value=frappe.db.sql("""select sum(clp_amount) from `tabStocks N Sales` where parent=%s""",row["name"])
		if doc_value:
			total=total+doc_value[0][0]
	#return super_doc

	for row1 in super_doc:
		doc_value1=frappe.db.sql("""select sum(sale_amount) from `tabStocks N Sales` where parent=%s""",row1["name"])
		if doc_value1:
			sell_total=sell_total+doc_value1[0][0]

	if not int(sell_total)==0:
		return round((total*30)/sell_total,2)
	else:
		return 0


@frappe.whitelist()
def getDistributorStock(emp_code,year,month):
	year1=getPreviousYear(month,year)
	month1=getPreviousMonth(month)
	total=0
	super_doc=frappe.get_all("Stocks and Sales Report",filters={"year":year1,"month":month1,"cluster_head_name":emp_code,"types_of_stockist":'Distributor'},fields=["name"])
	for row in super_doc:
		doc_value=frappe.db.sql("""select sum(clp_amount) from `tabStocks N Sales` where parent=%s""",row["name"])
		if doc_value:
			total=total+doc_value[0][0]
	return total


@frappe.whitelist()
def getSecondPrimary(emp_code,year,month):
	year1=getPreviousYear(month,year)
	month1=getPreviousMonth(month)
	total=0
	super_doc=frappe.get_all("Stocks and Sales Report",filters={"year":year1,"month":month1,"cluster_head_name":emp_code,"types_of_stockist":'Distributor'},fields=["name"])
	for row in super_doc:
		doc_value=frappe.db.sql("""select sum(clp_amount) from `tabStocks N Sales` where parent=%s""",row["name"])
		if doc_value:
			total=total+doc_value[0][0]
	return total


@frappe.whitelist()
def getDistNod(emp_code,year,month):
	year1=getPreviousYear(month,year)
	month1=getPreviousMonth(month)
	total=0
	sell_total=0
	super_doc=frappe.get_all("Stocks and Sales Report",filters={"year":year1,"month":month1,"cluster_head_name":emp_code,"types_of_stockist":'Distributor'},fields=["name"])
	for row in super_doc:
		doc_value=frappe.db.sql("""select sum(clp_amount) from `tabStocks N Sales` where parent=%s""",row["name"])
		if doc_value:
			total=total+doc_value[0][0]
	#return super_doc

	for row1 in super_doc:
		doc_value1=frappe.db.sql("""select sum(sale_amount) from `tabStocks N Sales` where parent=%s""",row1["name"])
		if doc_value1:
			sell_total=sell_total+doc_value1[0][0]

	if not int(sell_total)==0:
		return round((total*30)/sell_total,2)
	else:
		return 0



		
@frappe.whitelist()
def getClusterBusinessPlanWiseDetail(name):
	cluster_plan=frappe.get_doc("Cluster Business Plan", name)
	employee_list=getChildEmployeeList(cluster_plan.employee_code)
	total_sso_amount=getAllEmployeeSSOAmount(employee_list,cluster_plan.year,cluster_plan.month)

	# Secondary Target Start
def getUserIdfromEmployeeCode(emp_code):
	return frappe.db.get("Employee",{"name":emp_code}).user_id
		
def getChildEmployeeList(emp_code):
	user_list=frappe.get_list("User Permission",filters={"user":getUserIdfromEmployeeCode(emp_code),"allow":'Employee'},fields=["for_value"])
	return user_list
		
def getAllEmployeeSSOAmount(emp_list,year,month):
	total_sso_amount = 0
	for employee in getEmployeeWiseSSOAmount:
		total_sso_amount += getEmployeeWiseSSOAmount(employee.for_value)
	return total_sso_amount
		
def getEmployeeWiseSSOAmount(emp_code,year,month):
	return frappe.db.sql("""select sum(clp_total) from `tabSecondary Sales Order` where owner=%s and monthname(posting_date)=%s and year(posting_date)=%s""",(getUserIdfromEmployeeCode(emp_code,month,year)),as_dict=1).clp_total
		
	# Secondary Target end
	# Cumulative Target Start
@frappe.whitelist()
def getPreviousMonthClusterWiseShortFall(cluster_name,year,month):
	year1=0
	month1=0
	if int(month) == 1:
		year1=int(year) - 1
		month1 = 12
	else:
		year1=int(year)
		month1 = int(month)
	cluster_list=frappe.get_list("Cluster Business Plan",filter={"year":year1,"month":month1},fields=["*"])
	if cluster_list:
		return cluster_list[0].cumulative_short_fall
# Cumulative Target end
# In Salon Training Achievement Start
@frappe.whitelist()
def getInSalonTrainingAchievement(cluster_head,year,month):
	emp_list=getChildEmployeeList(cluster_head)
	achievement_counter=0
	for emp in emp_list:
		achievement_counter += len(getEmployeeTechnicalDailyActivity(emp.for_value,year,month))
	return achievement_counter

@frappe.whitelist()
def getEmployeeTechnicalDailyActivity(emp_code,year,month):
	return frappe.db.sql("""select * from `tabTechnical - Daily Activity` where trainer=%s and monthname(date)='"""+month+"""' and year(date)='"""+year+"""'""",emp_code,as_dict=1)
# In Salon Training Achievement end	
# Achieved 3 Months Active Salons Base start

@frappe.whitelist()
def getTwoPreviousMonth(month):
	return getPreviousMonth(getPreviousMonth(month))

@frappe.whitelist()
def getTwoPreviousMonthBasedYear(month,year):	
	if month=="January" or month=="February":
		return int(year)-1
	else:
		return year
		
@frappe.whitelist()
def getAchieved3MonthsActiveSalonsBase(emp_code,year,month):
	territory_list = getTerritoryFromEmployee(emp_code)
	stri= "("
	for territory in territory_list:
		stri += ("'"+str(territory)+"',")
	stri += "'b'"+")"
	counter = 0
	active_salon = frappe.db.sql("""select count(DISTINCT kyc) as salon_total from `tabSecondary Sales Order` where (monthname(posting_date)=%s and year(posting_date)=%s) or (monthname(posting_date)=%s and year(posting_date)=%s) or (monthname(posting_date)=%s and year(posting_date)=%s) and territory IN """+stri+""" """,(month,year,getPreviousMonth(month),getPreviousYear(month,year),getTwoPreviousMonth(month),getTwoPreviousMonthBasedYear(month,year)),as_dict=1 )
	return active_salon[0].salon_total
# Achieved 3 Months Active Salons Base end
	
# Achieved Repeat Buying Salons start
# @frappe.whitelist()
# def getTerritoryFromEmployee(emp_code):
# 	empter=frappe.db.get("Employee",{"name":emp_code}).territory
# 	del ter[:]
# 	ter.append(empter)
# 	terList(empter,0)
# 	return ter
 
# def terList(parent,index):
# 	childList=frappe.db.sql("""select territory_name from tabTerritory where parent_territory = %s""",str(parent))
# 	#frappe.msgprint(parent)conditions
# 	if childList:	
# 		for child in childList:
# 			ter.append(child[0])
# 	if len(ter)>index+1:	
# 		terList(ter[index+1],index+1)
# 	else:
# 		return;
		
		
# @frappe.whitelist()
# def getPreviousMonth(month):
# 	monthList = ['January','Febuary','March','April','May','June','July','Augest','September','October','November','December']
# 	index= (monthList.index(month))
# 	if(index==0):
# 		return monthList[11]
# 	else:
# 		return monthList[index-1]

# def getPreviousYear(month,year):
# 	if month=="January":
# 		return int(year)-1
# 	else:
# 		return year
		
@frappe.whitelist()
def getAchievedRepeatBuyingSalons(emp_code,year,month):
	territory_list = getTerritoryFromEmployee(emp_code)
	stri= "("
	for territory in territory_list:
		stri += ("'"+str(territory)+"',")
	stri += "'b'"+")"
	#return "select DISTINCT kyc from `tabSecondary Sales Order` where monthname(posting_date)=s and year(posting_date)=s and territory IN "+ stri
	#return stri
	counter = 0
	current_month_salon = frappe.db.sql("""select DISTINCT kyc from `tabSecondary Sales Order` where monthname(posting_date)=%s and year(posting_date)=%s and territory IN """+stri+""" """,(month,year),as_dict=1 )
	#return current_month_salon
	previous_month_salon = frappe.db.sql("""select DISTINCT kyc from `tabSecondary Sales Order` where monthname(posting_date)=%s and year(posting_date)=%s and territory IN """+stri+""" """,(getPreviousMonth(month),getPreviousYear(month,year)),as_dict=1 )
	#return previous_month_salon
	for salon in current_month_salon:
	#	return salon
		for salon1 in previous_month_salon:
	#		return salon1
			if salon.kyc == salon1.kyc:
				#return salon1
				counter += 1
	return counter
# Achieved Repeat Buying Salons end



##BDE WIse Second page

@frappe.whitelist()
def getEmployee(emp_code):
	ter_list=getTerritoryFromEmployee(emp_code)
	conditions=''
	conditions+="territory in("
	for row in ter_list:
		conditions+="'"+str(row)+"',"
	conditions+= "'b'"+')'
	employee_data=frappe.db.sql("""select name from `tabEmployee` where status='Active' and designation in("Business Development Executive","Senior Business Development Executive","Business Development Manager") and {0}""".format(conditions))
	return employee_data


@frappe.whitelist()
def getUserFromEmployee(emp_code):
	user=frappe.db.sql("""select user_id from `tabEmployee` where name='"""+emp_code+"""'""",as_dict=1)
	if user:
		return user[0].user_id
	else:
		frappe.throw("No Such User Exist")

@frappe.whitelist()
def getTodaySSO_BDE(emp_code):
	user=getUserFromEmployee(emp_code)
	secondary_achievement=frappe.db.sql("""select sum(clp_total) as secondary_achievement from `tabSecondary Sales Order` where posting_date='"""+today()+"""' and owner='"""+user+"""'""",as_dict=1)
	if not secondary_achievement[0].secondary_achievement==None:
		return secondary_achievement[0].secondary_achievement
	else:
		return 0

@frappe.whitelist()
def getTillDateSSO_BDE(emp_code,year,month):
	user=getUserFromEmployee(emp_code)
	secondary_achievement=frappe.db.sql("""select sum(clp_total) as secondary_achievement from `tabSecondary Sales Order` where monthname(posting_date)='"""+month+"""' and year(posting_date)='"""+year+"""' and owner='"""+user+"""'""",as_dict=1)
	if not secondary_achievement[0].secondary_achievement==None:
		return secondary_achievement[0].secondary_achievement
	else:
		return 0
	
@frappe.whitelist()
def getSSOTarget_BDE(emp_code,year,month):
	target_sso=frappe.db.sql("""select monthly_sales_target_total from `tabBDE Target and Incentive Plan` where employee_code='"""+emp_code+"""' and year='"""+year+"""' and month='"""+month+"""'""",as_dict=1)
	if target_sso:
		if not target_sso[0].monthly_sales_target_total==None:
			return target_sso[0].monthly_sales_target_total	
	else:
		return 0

@frappe.whitelist()
def getVisitTarget_BDE(emp_code,year,month):
	target_visit=frappe.db.sql("""select salon_visit_target from `tabBDE Target and Incentive Plan` where employee_code='"""+emp_code+"""' and year='"""+year+"""' and month='"""+month+"""'""",as_dict=1)
	if target_visit:
		if not target_visit[0].salon_visit_target==None:
			return target_visit[0].salon_visit_target
	else:
		return 0

@frappe.whitelist()
def getBillingTarget_BDE(emp_code,year,month):
	target_billing=frappe.db.sql("""select salon_billing_target from `tabBDE Target and Incentive Plan` where employee_code='"""+emp_code+"""' and year='"""+year+"""' and month='"""+month+"""'""",as_dict=1)
	if target_billing:
		if not target_billing[0].salon_billing_target==None:
			return target_billing[0].salon_billing_target
	else:
		return 0

@frappe.whitelist()
def getTodayVisit_BDE(emp_code):
	user=getUserFromEmployee(emp_code)
	visit=frappe.db.sql("""select count(name) as number from `tabVisit` where date='"""+today()+"""' and owner='"""+user+"""'""",as_dict=1)
	if not visit[0].number==None:
		return visit[0].number
	else:
		return 0
@frappe.whitelist()
def getTillDateVisit_BDE(emp_code,year,month):
	user=getUserFromEmployee(emp_code)
	visit=frappe.db.sql("""select count(name) as number from `tabVisit` where monthname(date)='"""+month+"""' and year(date)='"""+year+"""' and owner='"""+user+"""'""",as_dict=1)
	if not visit[0].number==None:
		return visit[0].number
	else:
		return 0


@frappe.whitelist()
def getTodayBilling_BDE(emp_code):
	user=getUserFromEmployee(emp_code)
	billing=frappe.db.sql("""select count(distinct kyc) as number from `tabSecondary Sales Order` where posting_date='"""+today()+"""' and owner='"""+user+"""'""",as_dict=1)
	if not billing[0].number==None:
		return billing[0].number
	else:
		return 0

@frappe.whitelist()
def getTillDateBilling_BDE(emp_code,year,month):
	user=getUserFromEmployee(emp_code)
	billing=frappe.db.sql("""select count(distinct kyc) as number from `tabSecondary Sales Order` where monthname(posting_date)='"""+month+"""' and year(posting_date)='"""+year+"""' and owner='"""+user+"""'""",as_dict=1)
	if not billing[0].number==None:
		return billing[0].number
	else:
		return 0



@frappe.whitelist()
def getAllDataBDEWise(emp_code,year,month,name):
	bde_data=getEmployee(emp_code)
	response=[]
	count=0
	cluster_data=frappe.get_doc("Cluster Business Plan",name)
	cluster_data.bde_wise_data=[]
	cluster_data.save()
	for row in bde_data:
	#	d = collections.OrderedDict()
	#	d["bde"]=str(row[0])
	#	d["today_sale"]=getTodaySSO_BDE(row[0])
	#	d["tilldate_sale"]=getTillDateSSO_BDE(row[0],year,month)
	#	d["monthly_target_sso"]=getSSOTarget_BDE(row[0],year,month)
	#	d["today_visit"]=getTodayVisit_BDE(row[0])
	#	d["tilldate_visit"]=getTillDateVisit_BDE(row[0],year,month)
	#	d["monthly_target_visit"]=getVisitTarget_BDE(row[0],year,month)
	#	d["today_billing"]=getTodayBilling_BDE(row[0])
	#	d["tilldate_billing"]=getTillDateBilling_BDE(row[0],year,month)
	#	d["monthly_target_billing"]=getBillingTarget_BDE(row[0],year,month)
		doc=frappe.get_doc({
					"docstatus": 0,
					"doctype": "BDE Of Cluster",
					"name": "New BDE Of Cluster 1",
					"owner":"Administrator",
					"bde":str(row[0]),
					"parent":str(name),
					"parentfield": "bde_wise_data",
					"parenttype": "Cluster Business Plan",
					"monthly_sale_trg":str((int(getSSOTarget_BDE(row[0],year,month)))),
					"monthly_visit_trg": str((int(getVisitTarget_BDE(row[0],year,month)))),
					"monthly_billing_trg": str((int(getBillingTarget_BDE(row[0],year,month)))),
					"today_sale_ach":str((int(getTodaySSO_BDE(row[0])))),
					"tilldate_sale_ach":str((int(getTillDateSSO_BDE(row[0],year,month)))),
					"today_visit_ach":str((int(getTodayVisit_BDE(row[0])))),
					"tilldate_visit_ach":str((int(getTillDateVisit_BDE(row[0],year,month)))),
					"today_billing_ach":str((int(getTodayBilling_BDE(row[0])))),
					"tilldate_billing_ach":str((int(getTillDateBilling_BDE(row[0],year,month))))
				})
		doc1=doc.insert(ignore_permissions=True)
	data=frappe.get_doc("Cluster Business Plan",name)
	data1=data.save()
	return data1.name
			
	#final_doc=frappe.get_doc("Cluster Business Plan",name)
	#return count
		
		
		











