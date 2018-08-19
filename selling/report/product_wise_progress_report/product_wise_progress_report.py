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
	
	columns= [_("Item") + ":Link/Item:120",_("Total Target") + ":Int:100", _("Total Achive") + ":Int:100", _("April Target") + ":Int:100", _("April Achive") + ":Int:100", _("May Target") + ":Int:100", _("May Achive") + ":Int:100", _("June Target") + ":Int:100", _("June Achive") + ":Int:100", _("July Target") + ":Int:100", _("July Achive") + ":Int:100", _("August Target") + ":Int:100", _("August Achive") + ":Int:100", _("September Target") + ":Int:100", _("September Achive") + ":Int:100", _("October Target") + ":Int:100",_("October Achive") + ":Int:100", _("November Target") + ":Int:100", _("November Achive") + ":Int:100", _("December Target") + ":Int:100", _("December Achive") + ":Int:100", _("January Target") + ":Int:100",_("January Achive") + ":Int:100", _("February Target") + ":Int:100",_("February Achive") + ":Int:100", _("March Target") + ":Int:100", _("March Achive") + ":Int:100"]
	return columns

		
		

def get_data(filters):
	#conditions = get_conditions(filters)
	year=filters.get("fiscal_year")
	data_obj = []
	data=frappe.db.sql("""select product from `tabProduct Wise Monthly Target Details` where parent=%s""",(year))
	
	for row in data:
		row1=[]
		row1.append(row[0])
		target_on=filters.get("target_on")
		if target_on=="Quantity":
			targetdata=frappe.db.sql("""select april,(select ifnull(sum(si.qty),0) from `tabSecondary Sales Order Item` as si inner join `tabSecondary Sales Order` as so on si.parent=so.name where si.item_code='"""+row[0]+"""' and month(so.posting_date)='4') as 'april_data',may,(select ifnull(sum(si.qty),0) from `tabSecondary Sales Order Item` as si inner join `tabSecondary Sales Order` as so on si.parent=so.name where si.item_code='"""+row[0]+"""' and month(so.posting_date)='5') as 'may_data',june,(select ifnull(sum(si.qty),0) from `tabSecondary Sales Order Item` as si inner join `tabSecondary Sales Order` as so on si.parent=so.name where si.item_code='"""+row[0]+"""' and month(so.posting_date)='6') as 'june_data',july,(select ifnull(sum(si.qty),0) from `tabSecondary Sales Order Item` as si inner join `tabSecondary Sales Order` as so on si.parent=so.name where si.item_code='"""+row[0]+"""' and month(so.posting_date)='7') as 'july_data',august,(select ifnull(sum(si.qty),0) from `tabSecondary Sales Order Item` as si inner join `tabSecondary Sales Order` as so on si.parent=so.name where si.item_code='"""+row[0]+"""' and month(so.posting_date)='8') as 'august_data',september,(select ifnull(sum(si.qty),0) from `tabSecondary Sales Order Item` as si inner join `tabSecondary Sales Order` as so on si.parent=so.name where si.item_code='"""+row[0]+"""' and month(so.posting_date)='9') as 'september_data',october,(select ifnull(sum(si.qty),0) from `tabSecondary Sales Order Item` as si inner join `tabSecondary Sales Order` as so on si.parent=so.name where si.item_code='"""+row[0]+"""' and month(so.posting_date)='10') as 'october_data',november,(select ifnull(sum(si.qty),0) from `tabSecondary Sales Order Item` as si inner join `tabSecondary Sales Order` as so on si.parent=so.name where si.item_code='"""+row[0]+"""' and month(so.posting_date)='11') as 'november_data',december,(select ifnull(sum(si.qty),0) from `tabSecondary Sales Order Item` as si inner join `tabSecondary Sales Order` as so on si.parent=so.name where si.item_code='"""+row[0]+"""' and month(so.posting_date)='12') as 'december_data',january,(select ifnull(sum(si.qty),0) from `tabSecondary Sales Order Item` as si inner join `tabSecondary Sales Order` as so on si.parent=so.name where si.item_code='"""+row[0]+"""' and month(so.posting_date)='1') as 'january_data',february,(select ifnull(sum(si.qty),0) from `tabSecondary Sales Order Item` as si inner join `tabSecondary Sales Order` as so on si.parent=so.name where si.item_code='"""+row[0]+"""' and month(so.posting_date)='2') as 'feruary_data',march,(select ifnull(sum(si.qty),0) from `tabSecondary Sales Order Item` as si inner join `tabSecondary Sales Order` as so on si.parent=so.name where si.item_code='"""+row[0]+"""' and month(so.posting_date)='3') as 'march_data'  from `tabProduct Wise Monthly Target Details` where product='"""+row[0]+"""'""")
		else:
			targetdata=frappe.db.sql("""select april_clp_value,(select ifnull(sum(si.clp_amount),0) from `tabSecondary Sales Order Item` as si inner join `tabSecondary Sales Order` as so on si.parent=so.name where si.item_code='"""+row[0]+"""' and month(so.posting_date)='4') as 'april_data',may_clp_value,(select ifnull(sum(si.clp_amount),0) from `tabSecondary Sales Order Item` as si inner join `tabSecondary Sales Order` as so on si.parent=so.name where si.item_code='"""+row[0]+"""' and month(so.posting_date)='5') as 'may_data',june_clp_value,(select ifnull(sum(si.clp_amount),0) from `tabSecondary Sales Order Item` as si inner join `tabSecondary Sales Order` as so on si.parent=so.name where si.item_code='"""+row[0]+"""' and month(so.posting_date)='6') as 'june_data',july_clp_value,(select ifnull(sum(si.clp_amount),0) from `tabSecondary Sales Order Item` as si inner join `tabSecondary Sales Order` as so on si.parent=so.name where si.item_code='"""+row[0]+"""' and month(so.posting_date)='7') as 'july_data',august_clp_value,(select ifnull(sum(si.clp_amount),0) from `tabSecondary Sales Order Item` as si inner join `tabSecondary Sales Order` as so on si.parent=so.name where si.item_code='"""+row[0]+"""' and month(so.posting_date)='8') as 'august_data',september_clp_value,(select ifnull(sum(si.clp_amount),0) from `tabSecondary Sales Order Item` as si inner join `tabSecondary Sales Order` as so on si.parent=so.name where si.item_code='"""+row[0]+"""' and month(so.posting_date)='9') as 'september_data',october_clp_value,(select ifnull(sum(si.clp_amount),0) from `tabSecondary Sales Order Item` as si inner join `tabSecondary Sales Order` as so on si.parent=so.name where si.item_code='"""+row[0]+"""' and month(so.posting_date)='10') as 'october_data',november_clp_value,(select ifnull(sum(si.clp_amount),0) from `tabSecondary Sales Order Item` as si inner join `tabSecondary Sales Order` as so on si.parent=so.name where si.item_code='"""+row[0]+"""' and month(so.posting_date)='11') as 'november_data',december_clp_value,(select ifnull(sum(si.clp_amount),0) from `tabSecondary Sales Order Item` as si inner join `tabSecondary Sales Order` as so on si.parent=so.name where si.item_code='"""+row[0]+"""' and month(so.posting_date)='12') as 'december_data',january_clp_value,(select ifnull(sum(si.clp_amount),0) from `tabSecondary Sales Order Item` as si inner join `tabSecondary Sales Order` as so on si.parent=so.name where si.item_code='"""+row[0]+"""' and month(so.posting_date)='1') as 'january_data',february_clp_value,(select ifnull(sum(si.clp_amount),0) from `tabSecondary Sales Order Item` as si inner join `tabSecondary Sales Order` as so on si.parent=so.name where si.item_code='"""+row[0]+"""' and month(so.posting_date)='2') as 'feruary_data',march_clp_value,(select ifnull(sum(si.clp_amount),0) from `tabSecondary Sales Order Item` as si inner join `tabSecondary Sales Order` as so on si.parent=so.name where si.item_code='"""+row[0]+"""' and month(so.posting_date)='3') as 'march_data'  from `tabProduct Wise Monthly Target Details` where product='"""+row[0]+"""'""")
			
			
			
		for sum1 in targetdata:
			total_target=sum1[0]+sum1[2]+sum1[4]+sum1[6]+sum1[8]+sum1[10]+sum1[12]+sum1[14]+sum1[16]+sum1[18]+sum1[20]+sum1[22]
			

			total_archive=sum1[1]+sum1[3]+sum1[5]+sum1[7]+sum1[9]+sum1[11]+sum1[13]+sum1[15]+sum1[17]+sum1[19]+sum1[21]+sum1[23]


			#total_archive=int(val1)+int(val2)+int(val3)+int(val4)+int(val5)+int(val6)+int(val7)+int(val8)+int(val9)+int(val10)+int(val11)+int(val12)
			row1.append(total_target)
			row1.append(total_archive)
			row1.append(sum1[0])
			row1.append(sum1[1])
			row1.append(sum1[2])
			row1.append(sum1[3])
			row1.append(sum1[4])
			row1.append(sum1[5])
			row1.append(sum1[6])
			row1.append(sum1[7])
			row1.append(sum1[8])
			row1.append(sum1[9])
			row1.append(sum1[10])
			row1.append(sum1[11])
			row1.append(sum1[12])
			row1.append(sum1[13])
			row1.append(sum1[14])
			row1.append(sum1[15])
			row1.append(sum1[16])
			row1.append(sum1[17])
			row1.append(sum1[18])
			row1.append(sum1[19])
			row1.append(sum1[20])
			row1.append(sum1[21])
			row1.append(sum1[22])
			row1.append(sum1[23])
			
		data_obj.append(row1)
		#frappe.msgprint(str(data_obj))
	return data_obj
			

