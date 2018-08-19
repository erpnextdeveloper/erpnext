# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt,cint, get_gravatar, format_datetime, now_datetime,add_days,today,formatdate,date_diff,getdate,get_last_day
from datetime import datetime




def execute(filters=None):
	if not filters: filters = {}

	float_precision = cint(frappe.db.get_default("float_precision")) or 3

	columns = get_columns(filters)
	item_map = get_item_details(filters)
	iwb_map = get_item_warehouse_batch_map(filters, float_precision)

	data = []
	for item in sorted(iwb_map):
		for wh in sorted(iwb_map[item]):
			for batch in sorted(iwb_map[item][wh]):
				qty_dict = iwb_map[item][wh][batch]
				if qty_dict.opening_qty or qty_dict.in_qty or qty_dict.out_qty or qty_dict.bal_qty:
					data.append([item, item_map[item]["item_name"],item_map[item]["brand"],getCategory(item),wh,item_map[item]["item_group"], batch,
						flt(qty_dict.bal_qty, float_precision),
						 item_map[item]["stock_uom"],flt(qty_dict.val_rate,float_precision)*flt(qty_dict.bal_qty, float_precision),get_posting_date(item,batch),frappe.utils.data.date_diff(today(),get_posting_date(item,batch))
					])

	return columns, data

def get_columns(filters):
	"""return columns based on filters"""

	columns = [_("Item") + ":Link/Item:100"] + [_("Item Name") + "::150"] +[_("Brand")+":Data:90"]+[_("Category")+":Data:90"]+ \
	[_("Warehouse") + ":Link/Warehouse:100"] +[_("Item Group") + ":Link/Item Group:100"]+ [_("Batch") + ":Link/Batch:100"] + [_("Balance Qty") + ":Float:90"] + \
	[_("UOM") + "::90"] + [_("Balance Value")] + [_("Posting Date") + ":Date:80"] + [_("Days") + ":Float:60"]


	return columns

def get_conditions(filters):
	conditions = ""
	if not filters.get("from_date"):
		frappe.throw(_("'From Date' is required"))

	if filters.get("to_date"):
		conditions += " and posting_date <= '%s'" % filters["to_date"]
	else:
		frappe.throw(_("'To Date' is required"))

	return conditions

#get all details
def get_stock_ledger_entries(filters):
	conditions = get_conditions(filters)
	return frappe.db.sql("""select se.item_code, se.batch_no, se.warehouse,se.posting_date, se.actual_qty, se.valuation_rate from `tabStock Ledger Entry` se where  se.docstatus = 1 %s  order by se.item_code, se.warehouse""" %
		conditions, as_dict=1)

def get_item_warehouse_batch_map(filters, float_precision):
	sle = get_stock_ledger_entries(filters)
	iwb_map = {}

	from_date = getdate(filters["from_date"])
	to_date = getdate(filters["to_date"])

	for d in sle:
		iwb_map.setdefault(d.item_code, {}).setdefault(d.warehouse, {})\
			.setdefault(d.batch_no, frappe._dict({
				"opening_qty": 0.0, "in_qty": 0.0, "out_qty": 0.0, "bal_qty": 0.0,"val_rate":0.0, "expiry_date": "1-1-2018"
			}))
		qty_dict = iwb_map[d.item_code][d.warehouse][d.batch_no]
		if d.posting_date < from_date:
			qty_dict.opening_qty = flt(qty_dict.opening_qty, float_precision) \
				+ flt(d.actual_qty, float_precision)
			
		elif d.posting_date >= from_date and d.posting_date <= to_date:
			if flt(d.actual_qty) > 0:
				qty_dict.in_qty = flt(qty_dict.in_qty, float_precision) + flt(d.actual_qty, float_precision)
			else:
				qty_dict.out_qty = flt(qty_dict.out_qty, float_precision) \
					+ abs(flt(d.actual_qty, float_precision))

		qty_dict.bal_qty = flt(qty_dict.bal_qty, float_precision) + flt(d.actual_qty, float_precision)
		qty_dict.val_rate=d.valuation_rate
		qty_dict.expiry_date = d.expiry_date

	return iwb_map

def get_item_details(filters):
	item_map = {}
	for d in frappe.db.sql("select name, item_name,brand,description, stock_uom,item_group from tabItem", as_dict=1):
		item_map.setdefault(d.name, d)

	return item_map

def get_posting_date(i,b):
	podate=0
	p_date=frappe.db.sql("""select posting_date from `tabStock Ledger Entry` where voucher_type="Purchase Receipt" and item_code=%s and batch_no=%s order by posting_date desc limit 1""",
	(i, b))
	if len(p_date):
		podate=p_date[0][0]
	else:
		m_date=frappe.db.sql("""select mfg_date from `tabBatch` where name=%s""",b)
		if len(m_date):
			podate=m_date[0][0]
		else:
			return str()
	return podate

def getCategory(name):
	data=frappe.db.sql("""select category from `tabItem` where name=%s""",name)
	if data:
		return data[0][0]
	else:
		return ""