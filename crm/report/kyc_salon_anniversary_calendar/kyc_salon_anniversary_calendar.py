# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt

def execute(filters=None):
	if not filters: filters = {}

	columns = get_columns()
	data = get_employees(filters)

	return columns, data

def get_columns():
	return [
		_("BSRN") + ":Link/KYC:120", _("Salon / Parlor / Spa Name") + ":Data:200", _("Salon Anniversary")+ ":Date:100",_("Door / Building / Plot Number") + ":Data:160",_("Street") + ":Data:120",_("Landmark") + ":Data:120",_("Area") + ":Data:120",_("City") + ":Data:100",_("PIN") + ":Data:70", _("State") + ":Data:120",_("Territory") + ":Link/Territory:120",_("Owner's Name") + ":Data:120",_("Mobile No.") + ":Data:100",_("email") + ":Data:150"
	]

def get_employees(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql("""select name, salon_parlor_spa_name,salon_anniversary,door_building_plot_number,street,landmark,area,city_town,pin,
	state,territory,full_name,contact_number,email from tabKYC where status = 'Active' %s""" % conditions, as_list=1)

def get_conditions(filters):
	conditions = ""
	if filters.get("month"):
		month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov",
			"Dec"].index(filters["month"]) + 1
		conditions += " and month(salon_anniversary) = '%s'" % month

	return conditions
