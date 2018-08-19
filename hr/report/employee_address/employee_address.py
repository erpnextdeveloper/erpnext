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
		_("Employee") + ":Link/Employee:120", _("Name") + ":Data:200", _("Date of Birth")+ ":Date:100", _("Department") + ":Link/Department:120",
		_("Designation") + ":Link/Designation:120",_("Mobile No.") + ":Data:120",_("Address") + ":Small Text:120"
	]

def get_employees(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql("""select name, employee_name, date_of_birth, department, designation,cell_number,current_address from tabEmployee where status = 'Active' %s""" % conditions, as_list=1)

def get_conditions(filters):
	conditions = ""
	return conditions
