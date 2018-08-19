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
	
	columns= [_("BSRN") + ":Link/KYC:120",_("Salon") + "::200", _("Distributor") + ":Link/Employee:200",_("First Order") + "::150",_("Territory") + ":Link/Territory:200", _("Apr-Qty") + ":Float:60", _("May-Qty") + ":Float:60",_("Jun-Qty") + ":Float:60",_("Jul-Qty") + ":Float:60",_("Aug-Qty") + ":Float:60",_("Sep-Qty") + ":Float:60",_("Oct-Qty") + ":Float:60",_("Nov-Qty") + ":Float:60",_("Dec-Qty") + ":Float:60",_("Jan-Qty") + ":Float:60",_("Feb-Qty") + ":Float:60",_("Mar-Qty") + ":Float:60",_("Total-Total") + ":Float:60",_("Employee") + ":Link/Employee:120"]
	return columns

		
		

def get_data(filters):
	#conditions = get_conditions(filters)
	year=filters.get("fiscal_year")
	data=frappe.db.sql("""select so.KYC as "BSRN::80",
so.salon_parlor_spa_name as "Salon::250",
(select distributor from `tabKYC` where name=so.KYC) as "Distributor::270",
(select posting_date from `tabSecondary Sales Order` where kyc=so.KYC limit 1) as "First Order::200",
so.territory as "territory::100",
SUM(CASE WHEN MONTH(so.posting_date) = 4  THEN so.CLP_total ELSE 0 END) as "Apr-Qty:Float:60",
SUM(CASE WHEN MONTH(so.posting_date) = 5  THEN so.CLP_total ELSE 0 END) as "May-Qty:Float:60",
SUM(CASE WHEN MONTH(so.posting_date) = 6  THEN so.CLP_total ELSE 0 END) as "Jun-Qty:Float:60",
SUM(CASE WHEN MONTH(so.posting_date) = 7  THEN so.CLP_total ELSE 0 END) as "Jul-Qty:Float:60",
SUM(CASE WHEN MONTH(so.posting_date) = 8  THEN so.CLP_total ELSE 0 END) as "Aug-Qty:Float:60",
SUM(CASE WHEN MONTH(so.posting_date) = 9  THEN so.CLP_total ELSE 0 END) as "Sep-Qty:Float:60",
SUM(CASE WHEN MONTH(so.posting_date) = 10  THEN so.CLP_total ELSE 0 END) as "Oct-Qty:Float:60",
SUM(CASE WHEN MONTH(so.posting_date) = 11  THEN so.CLP_total ELSE 0 END) as "Nov-Qty:Float:60",
SUM(CASE WHEN MONTH(so.posting_date) = 12  THEN so.CLP_total ELSE 0 END) as "Dec-Qty:Float:60",
SUM(CASE WHEN MONTH(so.posting_date) = 1  THEN so.CLP_total ELSE 0 END) as "Jan-Qty:Float:60",
SUM(CASE WHEN MONTH(so.posting_date) = 2  THEN so.CLP_total ELSE 0 END) as "Feb-Qty:Float:60",
SUM(CASE WHEN MONTH(so.posting_date) = 3  THEN so.CLP_total ELSE 0 END) as "Mar-Qty:Float:60",
SUM(CASE WHEN MONTH(so.posting_date) between 1 and 12  THEN so.CLP_total ELSE 0 END) as "Total-Total:Float:60",
(select employee_name from `tabEmployee` where user_id=so.owner limit 1) as "Employee:180"


from `tabSecondary Sales Order` so where so.posting_date between (select year_start_date from `tabFiscal Year` where name = %s) and (select year_end_date from `tabFiscal Year` where name =%s)  group by so.KYC, so.territory, so.salon_parlor_spa_name
""",(year,year))
	return data
			

