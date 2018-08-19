# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import getdate, validate_email_add, today, add_years
from frappe import throw, _
import frappe.permissions
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc


sender_field = "email_id"


@frappe.whitelist()
def make_employee(source_name, target_doc=None):
	return _make_employee(source_name, target_doc)

def _make_employee(source_name, target_doc=None, ignore_permissions=False):
	doclist = get_mapped_doc("Candidate Information Form", source_name,
		{"Candidate Information Form": {
			"doctype": "Employee",
			"field_map": {
				"name": "name"
			}
		}}, target_doc,ignore_permissions=ignore_permissions)
	
	return doclist


@frappe.whitelist(allow_guest=True)
def heelo():
	return "hello"

