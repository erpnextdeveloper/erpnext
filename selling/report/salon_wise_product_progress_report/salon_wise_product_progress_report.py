# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import getdate, validate_email_add, today, add_years,add_days,format_datetime
from frappe.utils import flt

def execute(filters=None):
	if not filters: filters = {}

	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data


def get_columns(filters):
	
	columns= [_("BSRN NO") + ":Link/KYC:120",_("Salon Name") + "::200", _("Territory") + ":Link/Territory:200",_("Item Name") + "::200", _("Brand") + "::100", _("Category") + "::150", _("Apr-Qty") + ":Float:60", _("Apr-Total") + ":Float:60", _("May-Qty") + ":Float:60", _("May-Total") + ":Float:60", _("Jun-Qty") + ":Float:60", _("Jun-Total") + ":Float:60",_("Jul-Qty") + ":Float:60", _("Jul-Total") + ":Float:60", _("Aug-Qty") + ":Float:60", _("Aug-Total") + ":Float:60", _("Sep-Qty") + ":Float:60", _("Sep-Total") + ":Float:60", _("Oct-Qty") + ":Float:60", _("Oct-Total") + ":Float:60", _("Nov-Qty") + ":Float:60", _("Nov-Total") + ":Float:60", _("Dec-Qty") + ":Float:60", _("Dec-Total") + ":Float:60", _("Jan-Qty") + ":Float:60", _("Jan-Total") + ":Float:60", _("Feb-Qty") + ":Float:60", _("Feb-Total") + ":Float:60", _("Mar-Qty") + ":Float:60", _("Mar-Total") + ":Float:60",_("Total-Qty") + ":Float:60", _("Total-Total") + ":Float:60",_("Employee") + ":Link/Employee:120"]
	return columns

		
		

def get_data(filters):
	#conditions = get_conditions(filters)
	year=filters.get("fiscal_year")
	data=frappe.db.sql("""select so.kyc as "BSRN NO",so.salon_parlor_spa_name as "Salon Name",so.territory as "Territory",soi.item_name as "Item Name",it.brand as "Brand",it.category as "Category",SUM(CASE WHEN MONTH(so.posting_date) = 4  THEN soi.qty ELSE 0 END) as "Apr-Qty",SUM(CASE WHEN MONTH(so.posting_date) = 4  THEN soi.CLP_amount ELSE 0 END) as "Apr-Total",
SUM(CASE WHEN MONTH(so.posting_date) = 5  THEN soi.qty ELSE 0 END) as "May-Qty",
SUM(CASE WHEN MONTH(so.posting_date) = 5  THEN soi.CLP_amount ELSE 0 END) as "May-Total",
SUM(CASE WHEN MONTH(so.posting_date) = 6  THEN soi.qty ELSE 0 END) as "Jun-Qty",
SUM(CASE WHEN MONTH(so.posting_date) = 6  THEN soi.CLP_amount ELSE 0 END) as "Jun-Total",
SUM(CASE WHEN MONTH(so.posting_date) = 7  THEN soi.qty ELSE 0 END) as "Jul-Qty",
SUM(CASE WHEN MONTH(so.posting_date) = 7  THEN soi.CLP_amount ELSE 0 END) as "Jul-Total",
SUM(CASE WHEN MONTH(so.posting_date) = 8  THEN soi.qty ELSE 0 END) as "Aug-Qty",
SUM(CASE WHEN MONTH(so.posting_date) = 8  THEN soi.CLP_amount ELSE 0 END) as "Aug-Total",
SUM(CASE WHEN MONTH(so.posting_date) = 9  THEN soi.qty ELSE 0 END) as "Sep-Qty",
SUM(CASE WHEN MONTH(so.posting_date) = 9  THEN soi.CLP_amount ELSE 0 END) as "Sep-Total",
SUM(CASE WHEN MONTH(so.posting_date) = 10  THEN soi.qty ELSE 0 END) as "Oct-Qty",
SUM(CASE WHEN MONTH(so.posting_date) = 10 THEN soi.CLP_amount ELSE 0 END) as "Oct-Total",
SUM(CASE WHEN MONTH(so.posting_date) = 11  THEN soi.qty ELSE 0 END) as "Nov-Qty",
SUM(CASE WHEN MONTH(so.posting_date) = 11  THEN soi.CLP_amount ELSE 0 END) as "Nov-Total",
SUM(CASE WHEN MONTH(so.posting_date) = 12  THEN soi.qty ELSE 0 END) as "Dec-Qty",
SUM(CASE WHEN MONTH(so.posting_date) = 12 THEN soi.CLP_amount ELSE 0 END) as "Dec-Total",
SUM(CASE WHEN MONTH(so.posting_date) = 1  THEN soi.qty ELSE 0 END) as "Jan-Qty",
SUM(CASE WHEN MONTH(so.posting_date) = 1  THEN soi.CLP_amount ELSE 0 END) as "Jan-Total",
SUM(CASE WHEN MONTH(so.posting_date) = 2  THEN soi.qty ELSE 0 END) as "Feb-Qty",
SUM(CASE WHEN MONTH(so.posting_date) = 2  THEN soi.CLP_amount ELSE 0 END) as "Feb-Total",
SUM(CASE WHEN MONTH(so.posting_date) = 3  THEN soi.qty ELSE 0 END) as "Mar-Qty",
SUM(CASE WHEN MONTH(so.posting_date) = 3  THEN soi.CLP_amount ELSE 0 END) as "Mar-Total",
SUM(CASE WHEN MONTH(so.posting_date) between 1 and 12  THEN soi.qty ELSE 0 END) as "Total-Qty",
SUM(CASE WHEN MONTH(so.posting_date) between 1 and 12  THEN soi.CLP_amount ELSE 0 END) as "Total-Total",
(select employee_name from `tabEmployee` where user_id=so.owner limit 1) as "Employee"


from `tabSecondary Sales Order Item` soi inner join `tabSecondary Sales Order` so inner join `tabItem` it where soi.item_name = it.item_name and soi.parent = so.name and so.posting_date between (select year_start_date from `tabFiscal Year` where name = %s) and (select year_end_date from `tabFiscal Year` where name = %s)  group by soi.item_name,it.brand,it.category,so.salon_parlor_spa_name ORDER BY salon_parlor_spa_name
""",(year,year))
	return data
			

