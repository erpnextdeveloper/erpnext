# -*- coding: utf-8 -*-
# Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class MethodofManufacturing(Document):
	def autoname(self):
		names = frappe.db.sql_list("""select name from `tabMethod of Manufacturing` where product_code=%s""", self.product_code)

		if names:
			# name can be BOM/ITEM/001, BOM/ITEM/001-1, BOM-ITEM-001, BOM-ITEM-001-1

			# split by item
			names = [name.split(self.product_code)[-1][1:] for name in names]

			# split by (-) if cancelled
			names = [cint(name.split('/')[-1]) for name in names]

			idx = max(names) + 1
		else:
			idx = 1

		self.name = 'MOM/' + self.product_code + ('/%.3i' % idx)
