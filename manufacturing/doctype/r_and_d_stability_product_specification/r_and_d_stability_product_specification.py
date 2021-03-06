# -*- coding: utf-8 -*-
# Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import cint, cstr, flt

class RandDStabilityProductSpecification(Document):
	def autoname(self):
		names = frappe.db.sql_list("""select name from `tabR and D Stability Product Specification` where item_code=%s""", self.item_code)

		if names:
			# name can be BOM/ITEM/001, BOM/ITEM/001-1, BOM-ITEM-001, BOM-ITEM-001-1

			# split by item
			names = [name.split(self.item_code)[-1][1:] for name in names]

			# split by (-) if cancelled
			names = [cint(name.split('/')[-1]) for name in names]

			idx = max(names) + 1
		else:
			idx = 1

		self.name = 'SPS/' + self.item_code + ('/%.3i' % idx)
		self.spstp = 'SPSTP/' + self.item_code + ('/%.3i' % idx)
