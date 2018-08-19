# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

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
	columns= [
		_("Employee") + ":Link/Employee:120", _("Territory") + ":Link/Territory:200", _("Owner")+ ":Data:100",
		_("CLP Total") + ":Float:120"
	]
	from_date=filters.get("from_date")
	to_date=filters.get("to_date")
	while from_date<= to_date:
		label=""
		label = label+str(from_date) 
		columns.append(label+":Float:120")
		from_date=add_days(from_date,1)
	return columns

def get_data(filters):
	#conditions = get_conditions(filters)
	from_date=filters.get("from_date")
	to_date=filters.get("to_date")
	data_obj = []
	data=frappe.db.sql("""select emp.employee_name,emp.territory,sso.owner,sum(sso.clp_total) from `tabEmployee` emp inner join `tabSecondary Sales Order` sso on sso.owner = emp.user_id where sso.posting_date between %s and %s group by sso.owner""",(from_date,to_date))

	for row in data:
		row1=[]
		row1 = [row[0],row[1],row[2],row[3]]
		from_date=filters.get("from_date")
		while from_date<=to_date:
			empdata=frappe.db.sql("""select sum(clp_total) from `tabSecondary Sales Order` where posting_date=%s and owner=%s group by posting_date""",(from_date,row[2]))
			#frappe.msgprint(str(empdata[0][0]))
			if not empdata:
				total=0
			else:
				total=empdata[0][0]

			row1.append(total)
			from_date=add_days(from_date,1)
		data_obj.append(row1)
	return data_obj
			


#def getDateWiseData(filters):
#	from_date=filters.get("from_date")
#	to_date=filters.get("to_date")
#	employeeData=frappe.db.sql("""select owner,sum(clp_total) from `tabSecondary Sales Order` where posting_date between %s and %s group by owner""",(from_date,to_date))
#	return employeeData

	
	

