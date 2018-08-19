# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt

ter = []

def execute(filters=None):
	if not filters: filters = {}

	columns = get_columns()
	data = get_order(filters)
	return columns, data

def get_columns():
	return [
		_("Total") + ":Data/200"
	]

def get_order(filters):
	conditions = get_conditions(filters)
	#frappe.msgprint(conditions)
	return frappe.db.sql("""select sum(grand_total) from `tabSecondary Sales Order` %s""" % conditions)


def get_conditions(filters):
	conditions = "where "

	if filters.get("territory"):
		del ter[:]
		territory=filters.get("territory")
		ter.append(territory)
		#ter.clear() 
		#frappe.msgprint("c"+str(ter[0]))
		
		terList(territory,0)
		conditions+="territory in("
		for child in ter:
			conditions+="'"+str(child)+"',"
		conditions+= "'b'"+')'



	if filters.get("to_date") and filters.get("from_date"):
		from_date=filters.get("from_date")
		to_date=filters.get("to_date")
		conditions+=" and posting_date between '%s'" % from_date
		conditions+=" and '%s'" % to_date


		
		
	#if filters.get("territory"):
	#	territory=filters.get("territory")
	#	territory_list=frappe.db.sql("select territory_name from tabTerritory where parent_territory=%s",territory)
	#	conditions+=" and territory='%s' and" % territory
	#	if territory_list:
	#		for row in territory_list:
	#			conditions="(territory='%s' or" % row[0]
	#			t_list1=frappe.db.sql("select territory_name from tabTerritory where parent_territory=%s",row[0])
	#			if t_list1:
	#					conditions="territory='%s' or" % row1[0]
	#					t_list2=frappe.db.sql("select territory_name from tabTerritory where parent_territory=%s",row1[0])
	#					if t_list2:
	#						for row2 in t_list2:
	#							conditions=" or territory='%s'" % row2[0]
	#							t_list3=frappe.db.sql("select territory_name from tabTerritory where parent_territory=%s",row2[0])
	return conditions

def terList(parent,index):
		
	childList=frappe.db.sql("select territory_name from tabTerritory where parent_territory = %s",str(parent))
	#frappe.msgprint(parent)
	if childList:	
		for child in childList:
			ter.append(child[0])
	if len(ter)>index+1:	
		terList(ter[index+1],index+1)
	else:
		return;

		
