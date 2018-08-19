# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	if not filters: filters = {}
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data

def get_columns(filters):
	
	columns= [_("Date") + "Data::120",_("Trainer Code") + "Data::120",_("Trainer Name") + "Data::120",_("Designation") + "Data::200", _("Head Quarter") + "Data::200",_("Salon Type") + "Data::200", _("New Salons Productivity") + ":Data:60", _("Total New Salon Demo") + ":Data:60",_("Total Existing Salon Demo") + ":Data:60",_("Training") + ":Data:60",_("Visit") + ":Data:60",_("R.D Day") + ":Data:60",_("Mixology Day") + ":Data:60",_("Nutrimixology Day") + ":Data:60",_("Skin Mixology Day") + ":Data:60",_("Nutrimixology Day") + ":Data:60",_("Root Deep") + ":Data:60"]
	return columns
	
def get_data(filters):
	#conditions = get_conditions(filters)
	year=filters.get("fiscal_year")
	data =frappe.db.sql(""" select date,trainer,name_of_trainer,type_of_client,demonstration,training,visit,day_celebration_skin_mixology,day_celebration_nutrimixology,day_celebration_root_deep from `tabTechnical - Daily Activity` inner join `tabEmployee` """)