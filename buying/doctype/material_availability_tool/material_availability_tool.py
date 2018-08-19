#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import frappe
from frappe.utils import flt, getdate, nowdate
from frappe import msgprint, _
from frappe.model.document import Document

form_grid_templates = \
    {'order_entries': 'templates/material_availability_tool_grid.html'}


class MaterialAvailabilityTool(Document):

    def get_order_entries(self):
        if not (self.warehouse and self.from_date and self.to_date):
            msgprint('Warehouse, From Date and To Date are Mandatory')
            return

        condition = ''
        if not self.include_reconciled_entries:
            condition = \
                "and (expected_delivery_date is null or expected_delivery_date='0000-00-00')"

        order_entries = \
            frappe.db.sql("""
			select 
				parent as purchase_order,item_name as item, schedule_date, expected_delivery_date, qty
			from
				`tabPurchase Order Item`
			where
				docstatus=1 and warehouse = %s
				and schedule_date >= %s and schedule_date <= %s 
			order by schedule_date ASC, item_name DESC
		""".format(condition),
                          (self.warehouse, self.from_date,
                          self.to_date), as_dict=1)

        entries = sorted(list(order_entries), key=lambda k: \
                         k['schedule_date'] or getdate(nowdate()))

        self.set('order_entries', [])

        for d in entries:
            row = self.append('order_entries', {})
            row.update(d)

    def update_expected_date(self):
        expected_date_updated = False
        for d in self.get('order_entries'):

            if d.expected_delivery_date or self.include_reconciled_entries:
                if not d.expected_delivery_date:
                    d.expected_delivery_date = None

                frappe.db.set_value(d.payment_document,
                                    d.payment_entry, 'clearance_date',
                                    d.expected_delivery_date)
                frappe.db.sql("""update `tabPurchase Order Item` set expected_delivery_date = %s, modified = %s 
					where parent=%s and item_name=%s""".format(d.expected_delivery_date, nowdate(),
                              d.purchase_order,d.item))

                clearance_date_updated = True

        if clearance_date_updated:
            self.get_payment_entries()
            msgprint(_('Clearance Date updated'))
        else:
            msgprint(_('Clearance Date not mentioned'))



			
