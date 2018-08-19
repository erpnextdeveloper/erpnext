# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt, getdate

def execute(filters=None):
	if not filters: filters = {}


	columns = get_columns()
	request_map = get_material_request(filters)
	

	data = []
	for (item) in (request_map):
		
		
		actual_qty = get_actual_qty(item["item_code"])
		planned_qty= get_planned_qty(item["item_code"])
		po_qty= get_planned_qty(item["item_code"])

	
		if len(actual_qty) > 0:
			
			aqty = actual_qty[0][0]
		else:
			
			aqty = 0
			
		if len(planned_qty) > 0:
			pqty = planned_qty[0][0]
		else:
			pqty = 0

		if len(po_qty) > 0:
			poqty = po_qty[0][0]
		else:
			poqty = 0


		data.append([item["item_code"], item["item_name"],item["tqty"],aqty,pqty,poqty,item["tqty"]-aqty-pqty])

	return columns, data

def get_columns():
	"""return columns"""

	columns = [
		_("Item")+":Link/Item:100",
		_("Item Name")+"::150",
		_("Requested Qty")+":Float:100",
		_("Actual Qty")+":Float:100",
		_("Planned Qty")+":Float:100",
		_("PO Qty")+":Float:100",
		_("Qty to Order (Requested - Actual - Planned)")+":Float:300"
]

	return columns

def get_conditions(filters):
	conditions = ""
	if filters.get("from_date"):
		conditions = "schedule_date >= '%s'" % frappe.db.escape(filters["from_date"])

	if filters.get("to_date"):
		conditions += " and schedule_date <= '%s'" % frappe.db.escape(filters["to_date"])
	else:
		frappe.throw(_("'To Date' is required"))

	conditions += " and docstatus = 1 and warehouse = 'Finish Goods Warehouse - BSPL' group by item_code,item_name"
	return conditions


def get_material_request(filters):
	print """select
			item_code, item_name, sum(qty) as tqty
		from `tabMaterial Request Item` 
			
		where {conditions}"""\
		.format(conditions=get_conditions(filters))

	return frappe.db.sql("""select
			item_code, item_name, sum(qty) as tqty
		from `tabMaterial Request Item` 
			
		where {conditions}"""\
		.format(conditions=get_conditions(filters)), filters, as_dict=True)


def get_planned_qty(item):
	return frappe.db.sql("""select sum(qty) as qty from `tabProduction Order` where status != 'Completed' and status != 'Closed'  and docstatus = 1  and production_item = '%s' group by production_item""" % item)

def get_actual_qty(item):
	return frappe.db.sql("""select actual_qty as qty from `tabBin` where warehouse='Finish Goods Warehouse - BSPL' and item_code = '%s'""" % item)
def get_po_qty(item):
	return frappe.db.sql("""SELECT sum(qty - received_qty)*conversion_factor as qty FROM `tabPurchase Order Item` where docstatus = 1 and parent in (select name from `tabPurchase Order` where docstatus = 1 and status != "Closed" and status != 'Completed') and item_code = '%s' group by '%s'""" % item %item)
