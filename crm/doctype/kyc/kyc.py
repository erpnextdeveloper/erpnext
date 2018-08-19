# -*- coding: utf-8 -*-
# Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import getdate, validate_email_add, today, add_years
from frappe import throw, _
import frappe.permissions
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc



@frappe.whitelist()
def make_customer1(source_name, target_doc=None):
	return _make_customer(source_name, target_doc)

def _make_customer(source_name, target_doc=None, ignore_permissions=False):
	def set_missing_values(source, target):
		
		
		target.customer_type = "Individual"
		target.customer_name = source.salon_parlor_spa_name

		target.customer_group = frappe.db.get_default("Customer Group")

	doclist = get_mapped_doc("KYC", source_name,
		{"KYC": {
			"doctype": "Customer",
			"field_map": {
				"name": "full_name",
				"company_name": "salon_parlor_spa_name",
				"contact_no": "contact_number",
				"territory": "territory"
			}
		}}, target_doc, set_missing_values, ignore_permissions=ignore_permissions)

	return doclist