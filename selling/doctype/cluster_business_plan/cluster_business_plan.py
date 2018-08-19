# -*- coding: utf-8 -*-
# Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
ter=[]

class ClusterBusinessPlan(Document):
	def autoname(self):
		self.name = 'CBP/' + self.cluster_name + '/'+ self.month+ '/' + self.year

@frappe.whitelist()	
def getAllClusterBusinessPlan():
	business_plan_list =frappe.get_list("Cluster Business Plan",filters={},fields=['name'])
	if business_plan_list:
		for business_plan in business_plan_list:
			getClusterBusinessPlanWiseDetail(business_plan.name)
		
@frappe.whitelist()
def getClusterBusinessPlanWiseDetail(name):
	cluster_plan=frappe.get_doc("Cluster Business Plan", name)
	employee_list=getChildEmployeeList(cluster_plan.employee_code)
	total_sso_amount=getAllEmployeeSSOAmount(employee_list,cluster_plan.year,cluster_plan.month)

	# Secondary Target Start
def getUserIdfromEmployeeCode(emp_code):
	return frappe.db.get("Employee",{"name":emp_code}).user_id
		
def getChildEmployeeList(emp_code):
	user_list=frappe.get_list("User Permission",filter={"user":getUserIdfromEmployeeCode(emp_code),"allow":'Employee'},fields=["for_value"])
	return user_list
		
def getAllEmployeeSSOAmount(emp_list,year,month):
	total_sso_amount = 0
	for employee in getEmployeeWiseSSOAmount:
		total_sso_amount += getEmployeeWiseSSOAmount(employee.for_value)
	return total_sso_amount
		
def getEmployeeWiseSSOAmount(emp_code,year,month):
	return frappe.db.sql("""select sum(slp_total) from `tabSecondary Sales Order` where owner=%s and monthname(posting_date)=%s and year(posting_date)=%s""",(getUserIdfromEmployeeCode(emp_code,month,year)),as_dict=1).slp_total
		
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
		achievement_counter += len(getEmployeeTechnicalDailyActivity(cluster_head,year,month))
	return achievement_counter

@frappe.whitelist()
def getEmployeeTechnicalDailyActivity(emp_code,year,month):
	return frappe.db.sql("""select * from `tabTechnical - Daily Activity` where trainer=%s and monthname(date)=%s and year(date)=%s""",(getUserIdfromEmployeeCode(emp_code,month,year)),as_dict=1)
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
@frappe.whitelist()
def getTerritoryFromEmployee(emp_code):
	empter=frappe.db.get("Employee",{"name":emp_code}).territory
	del ter[:]
	ter.append(empter)
	terList(empter,0)
	return ter
 
def terList(parent,index):
	childList=frappe.db.sql("""select territory_name from tabTerritory where parent_territory = %s""",str(parent))
	#frappe.msgprint(parent)conditions
	if childList:	
		for child in childList:
			ter.append(child[0])
	if len(ter)>index+1:	
		terList(ter[index+1],index+1)
	else:
		return;
		
		
@frappe.whitelist()
def getPreviousMonth(month):
	monthList = ['January','Febuary','March','April','May','June','July','Augest','September','October','November','December']
	index= (monthList.index(month))
	if(index==0):
		return monthList[11]
	else:
		return monthList[index-1]

def getPreviousYear(month,year):
	if month=="January":
		return int(year)-1
	else:
		return year
		
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

