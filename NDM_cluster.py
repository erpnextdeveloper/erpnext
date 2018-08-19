from __future__ import unicode_literals
import frappe
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

import datetime
from frappe.utils import flt,getdate, validate_email_add, today, add_years,add_days,format_datetime
from frappe.model.naming import make_autoname
from frappe import throw, _, scrub
import frappe.permissions
from frappe.model.document import Document
import json
import collections
from frappe.core.doctype.sms_settings.sms_settings import send_sms
from frappe.core.doctype.communication.email import make

import pdfkit, os, frappe
from frappe.utils import scrub_urls
from frappe import _
from bs4 import BeautifulSoup
from PyPDF2 import PdfFileWriter, PdfFileReader
import re




@frappe.whitelist()
def MonthlyReport():
	d = datetime.date.today()
	year = d.strftime("%Y")
	month = d.strftime("%B") 
	#return (year,month)
	doc=frappe.get_all("NBM Cluster Business Plan",filters={"year":year,"month":month},fields=["name"])
	#return doc
	count=0

	cc= frappe.db.get_value("NBM Cluster Business Plan Setting","NBM Cluster Business Plan Setting", "email_cc_in_monthly")
	subject= frappe.db.get_value("NBM Cluster Business Plan Setting","NBM Cluster Business Plan Setting","monthly_email_subject")
	print_format= frappe.db.get_value("NBM Cluster Business Plan Setting","NBM Cluster Business Plan Setting","monthly_print_format_name")
	print_letterhead= frappe.db.get_value("NBM Cluster Business Plan Setting","NBM Cluster Business Plan Setting","print_letterhead")
	to= frappe.db.get_value("NBM Cluster Business Plan Setting","NBM Cluster Business Plan Setting","to")

	for row in doc:
		clster_data=frappe.get_doc("NBM Cluster Business Plan",row.name)
		getClusterData()
		receipient=to
		make(recipients=receipient,cc=cc,subject=subject,content=generate_multiPDF(),doctype='NBM Cluster Business Plan',name=row.name,send_email=1,print_format=print_format,print_letterhead=int(print_letterhead))
		count=count+1
	return count


@frappe.whitelist()
def DailyReport():
	d = datetime.date.today()
	year = d.strftime("%Y")
	month = d.strftime("%B") 
	#return (year,month)
	doc=frappe.get_all("NBM Cluster Business Plan",filters={"year":year,"month":month},fields=["name"])
	#return doc
	count=0

	cc= frappe.db.get_value("NBM Cluster Business Plan Setting","NBM Cluster Business Plan Setting", "email_cc_in_daily")
	subject= frappe.db.get_value("NBM Cluster Business Plan Setting","NBM Cluster Business Plan Setting","daily_email_subject")
	print_format= frappe.db.get_value("NBM Cluster Business Plan Setting","NBM Cluster Business Plan Setting","daily_print_format_name")
	print_letterhead= frappe.db.get_value("NBM Cluster Business Plan Setting","NBM Cluster Business Plan Setting","print_letterhead")
	to= frappe.db.get_value("NBM Cluster Business Plan Setting","NBM Cluster Business Plan Setting","to")

	for row in doc:
		clster_data=frappe.get_doc("NBM Cluster Business Plan",row.name)
		getClusterData()
		receipient=to
		make(recipients=receipient,cc=cc,subject=subject,content=generate_multiPDF(),doctype='NBM Cluster Business Plan',name=row.name,send_email=1,print_format=print_format,print_letterhead=int(print_letterhead))
		count=count+1
	return count
		

@frappe.whitelist()
def getClusterData():
	d = datetime.date.today()
	year = d.strftime("%Y")
	month = d.strftime("%B")
	today_target=today_salon_visit_target=today_productive_salon_target=0
	today_productive_bds=daily_productivity=ypm_target_per_bde=0
	secondary_target=cumulative_target=short_fall_recovery_target=0
	allocated_bds=allocated_stts=allocated_supers=0
	primary_target=ytd_primary_target=0
	ytd_primary_deficit_recovery_target=super_nod_target=allocate_distributor=0
	second_primary_target=distributor_nod_target=targeted_typical_accounts=0
	targeted_business_from_typical_accounts=targeted_standard_accounts=targeted_business_from_standard_accounts=0
	targeted_important_accounts=targeted_business_from_important_accounts=targeted_key_accounts=0
	targeted_business_from_key_accounts=visit_target=productive_call_target=0
	new_salon_opening_target=targeted_buying_salons_per_bde=targeted_treatment_giving_salons=0
	targeted_repeat_buying=targeted_3_months_active_salons_base=in_salon_training_target=0
	today_arch=today_salon_visit_achievement=today_productive_salon_achievement=0
	today_non_productive_bds=monthly_productivity=ypm_ach_per_bde=0
	secondary_achievement=cumulative_short_fall=short_fall_recovery_achievement=0
	bde_vacancy=stt_vacancy=closing_stock_of_supers=0
	primary_achievement=ytd_primary_achievement=ytd_primary_deficit_recovery_achievement=0
	super_nod_achievement=closing_stock_of_distributors=second_primary_achievement=0
	distributor_nod_achievement=achieved_typical_accounts=achieved_business_from_typical_accounts=0
	achieved_standard_account=achieved_business_from_standard_accounts=achieved_important_accounts=0
	achieved_business_from_important_accounts=achieved_key_accounts=achieved_business_from_key_accounts=0
	visit_target_achievement=productive_call_target_achievement=new_salon_target_achievement=0
	achieved_buying_salons_per_bde=achieved_treatment_giving_salons_per_stt=achieved_repeat_buying=0
	achieved_3_months_active_salons_base=in_salon_training_achievement=brillare_sale=0
	in_salon_sale=root_deep_sale=hair_care_sale=0
	skin_care_sale=home_care_sale=brillare_sale_achievement=0
	in_salon_sale_achievement=root_deep_sale_achievement=hair_care_sale_achievement=0
	skin_care_sale_achievement=home_care_sale_achievement=0
	cluster_count = 0
	docs=frappe.get_all("Cluster Business Plan",filters={"year":year,"month":month},fields=["name"])
	#return docs
	for doc1 in docs:
		doc=frappe.get_doc("Cluster Business Plan",doc1.name)
		today_target += int(doc.today_target or 0)
		today_salon_visit_target += int(doc.today_salon_visit_target or 0)
		today_productive_salon_target += int(doc.today_productive_salon_target or 0)
		today_productive_bds += int(doc.today_productive_bds or 0)
		daily_productivity += int(doc.daily_productivity or 0)
		ypm_target_per_bde += int(doc.ypm_target_per_bde or 0)
		secondary_target += int(doc.secondary_target or 0)
		cumulative_target += int(doc.cumulative_target or 0)
		short_fall_recovery_target += int(doc.short_fall_recovery_target or 0)
		allocated_bds += int(doc.allocated_bds or 0)
		allocated_stts += int(doc.allocated_stts or 0)
		allocated_supers += int(doc.allocated_supers or 0)
		primary_target += int(doc.primary_target or 0)
		ytd_primary_target += int(doc.ytd_primary_target or 0)
		ytd_primary_deficit_recovery_target += int(doc.ytd_primary_deficit_recovery_target or 0)
		super_nod_target += int(doc.super_nod_target or 0)
		allocate_distributor += int(doc.allocate_distributor or 0)
		second_primary_target += int(doc.second_primary_target or 0)
		distributor_nod_target += int(doc.distributor_nod_target or 0)
		targeted_typical_accounts += int(doc.targeted_typical_accounts or 0)
		targeted_business_from_typical_accounts += int(doc.targeted_business_from_typical_accounts or 0)
		targeted_standard_accounts += int(doc.targeted_standard_accounts or 0)
		targeted_business_from_standard_accounts += int(doc.targeted_business_from_standard_accounts or 0)
		targeted_important_accounts += int(doc.targeted_important_accounts or 0)
		targeted_business_from_important_accounts += int(doc.targeted_business_from_important_accounts or 0)
		targeted_key_accounts += int(doc.targeted_key_accounts or 0)
		targeted_business_from_key_accounts += int(doc.targeted_business_from_key_accounts or 0)
		visit_target += int(doc.visit_target or 0)
		productive_call_target += int(doc.productive_call_target or 0)
		new_salon_opening_target += int(doc.new_salon_opening_target or 0)
		targeted_buying_salons_per_bde += int(doc.targeted_buying_salons_per_bde or 0)
		targeted_treatment_giving_salons += int(doc.targeted_treatment_giving_salons or 0)
		targeted_repeat_buying += int(doc.targeted_repeat_buying or 0)
		targeted_3_months_active_salons_base += int(doc.targeted_3_months_active_salons_base or 0)
		in_salon_training_target += int(doc.in_salon_training_target or 0)
		today_arch += int(doc.today_arch or 0)
		today_salon_visit_achievement += int(doc.today_salon_visit_achievement or 0)
		today_productive_salon_achievement += int(doc.today_productive_salon_achievement or 0)
		today_non_productive_bds += int(doc.today_non_productive_bds or 0)
		monthly_productivity += int(doc.monthly_productivity or 0)
		ypm_ach_per_bde += int(doc.ypm_ach_per_bde or 0)
		secondary_achievement += int(doc.secondary_achievement or 0)
		cumulative_short_fall += int(doc.cumulative_short_fall or 0)
		short_fall_recovery_achievement += int(doc.short_fall_recovery_achievement or 0)
		bde_vacancy += int(doc.bde_vacancy or 0)
		stt_vacancy += int(doc.stt_vacancy or 0)
		closing_stock_of_supers += int(doc.closing_stock_of_supers or 0)
		primary_achievement += int(doc.primary_achievement or 0)
		ytd_primary_achievement += int(doc.ytd_primary_achievement or 0)
		ytd_primary_deficit_recovery_achievement += int(doc.ytd_primary_deficit_recovery_achievement or 0)
		super_nod_achievement += int(doc.super_nod_achievement or 0)
		closing_stock_of_distributors += int(doc.closing_stock_of_distributors or 0)
		second_primary_achievement += int(doc.second_primary_achievement or 0)
		distributor_nod_achievement+= int(doc.distributor_nod_achievement or 0)
		achieved_typical_accounts += int(doc.achieved_typical_accounts or 0)
		achieved_business_from_typical_accounts += int(doc.achieved_business_from_typical_accounts or 0)
		achieved_standard_account += int(doc.achieved_standard_account or 0)
		achieved_business_from_standard_accounts += int(doc.achieved_business_from_standard_accounts or 0)
		achieved_important_accounts += int(doc.achieved_important_accounts or 0)
		achieved_business_from_important_accounts += int(doc.achieved_business_from_important_accounts or 0)
		achieved_key_accounts += int(doc.achieved_key_accounts or 0)
		achieved_business_from_key_accounts += int(doc.achieved_business_from_key_accounts or 0)
		visit_target_achievement += int(doc.visit_target_achievement or 0)
		productive_call_target_achievement += int(doc.productive_call_target_achievement or 0)
		new_salon_target_achievement += int(doc.new_salon_target_achievement or 0)
		achieved_buying_salons_per_bde += int(doc.achieved_buying_salons_per_bde or 0)
		achieved_treatment_giving_salons_per_stt += int(doc.achieved_treatment_giving_salons_per_stt or 0)
		achieved_repeat_buying += int(doc.achieved_repeat_buying or 0)
		achieved_3_months_active_salons_base += int(doc.achieved_3_months_active_salons_base or 0)
		in_salon_training_achievement += int(doc.in_salon_training_achievement or 0)
		brillare_sale += int(doc.brillare_sale or 0)
		in_salon_sale += int(doc.in_salon_sale or 0)
		root_deep_sale += int(doc.root_deep_sale or 0)
		hair_care_sale += int(doc.hair_care_sale or 0)
		skin_care_sale += int(doc.skin_care_sale or 0)
		home_care_sale += int(doc.home_care_sale or 0)
		brillare_sale_achievement += int(doc.brillare_sale_achievement or 0)
		in_salon_sale_achievement += int(doc.in_salon_sale_achievement or 0)
		root_deep_sale_achievement += int(doc.root_deep_sale_achievement or 0)
		hair_care_sale_achievement += int(doc.hair_care_sale_achievement or 0)
		skin_care_sale_achievement += int(doc.skin_care_sale_achievement or 0)
		home_care_sale_achievement += int(doc.home_care_sale_achievement or 0)
		cluster_count += 1
	nbm_cluster = frappe.get_all("NBM Cluster Business Plan",filters={"year":year,"month":month},fields=["name"])
	inserted_doc = None
	if len(nbm_cluster)==0:
		#frappe.get_doc("NBM Cluster Business Plan",)
		documents = frappe.get_doc({
			"doctype":"NBM Cluster Business Plan",
			"year": year,
			"month": month,
			"docstatus":0
			})
		inserted_doc=documents.insert(ignore_permissions=True)
		#return ("if",inserted_doc)
	else:
		inserted_doc=frappe.get_doc("NBM Cluster Business Plan",nbm_cluster[0].name)
		#return ("else",inserted_doc)

	#return inserted_doc
	inserted_doc.today_target = today_target

	inserted_doc.today_salon_visit_target = today_salon_visit_target
	inserted_doc.today_productive_salon_target =today_productive_salon_target
	inserted_doc.today_productive_bds = today_productive_bds
	inserted_doc.daily_productivity = daily_productivity
	inserted_doc.ypm_target_per_bde = ypm_target_per_bde / cluster_count
	inserted_doc.secondary_target = secondary_target
	inserted_doc.cumulative_target = cumulative_target
	inserted_doc.short_fall_recovery_target = short_fall_recovery_target
	inserted_doc.allocated_bds = allocated_bds
	inserted_doc.allocated_stts = allocated_stts
	inserted_doc.allocated_supers = allocated_supers
	inserted_doc.primary_target = primary_target
	inserted_doc.ytd_primary_target = ytd_primary_target
	inserted_doc.ytd_primary_deficit_recovery_target = ytd_primary_deficit_recovery_target
	inserted_doc.super_nod_target = super_nod_target
	inserted_doc.allocate_distributor = allocate_distributor
	inserted_doc.second_primary_target = second_primary_target
	inserted_doc.distributor_nod_target = distributor_nod_target
	inserted_doc.targeted_typical_accounts = targeted_typical_accounts
	inserted_doc.targeted_business_from_typical_accounts = targeted_business_from_typical_accounts
	inserted_doc.targeted_standard_accounts = targeted_standard_accounts
	inserted_doc.targeted_business_from_standard_accounts = targeted_business_from_standard_accounts
	inserted_doc.targeted_important_accounts = targeted_important_accounts
	inserted_doc.targeted_business_from_important_accounts = targeted_business_from_important_accounts
	inserted_doc.targeted_key_accounts = targeted_key_accounts
	inserted_doc.targeted_business_from_key_accounts = targeted_business_from_key_accounts
	inserted_doc.visit_target = visit_target
	inserted_doc.productive_call_target = productive_call_target
	inserted_doc.new_salon_opening_target = new_salon_opening_target
	inserted_doc.targeted_buying_salons_per_bde = targeted_buying_salons_per_bde / cluster_count
	inserted_doc.targeted_treatment_giving_salons = targeted_treatment_giving_salons
	inserted_doc.targeted_repeat_buying = targeted_repeat_buying
	inserted_doc.targeted_3_months_active_salons_base = targeted_3_months_active_salons_base
	inserted_doc.in_salon_training_target = in_salon_training_target
	inserted_doc.today_arch = today_arch
	inserted_doc.today_salon_visit_achievement = today_salon_visit_achievement
	inserted_doc.today_productive_salon_achievement = today_productive_salon_achievement
	inserted_doc.today_non_productive_bds = today_non_productive_bds
	inserted_doc.monthly_productivity = monthly_productivity
	inserted_doc.ypm_ach_per_bde = ypm_ach_per_bde / cluster_count
	inserted_doc.secondary_achievement = secondary_achievement
	inserted_doc.cumulative_short_fall = cumulative_short_fall
	inserted_doc.short_fall_recovery_achievement = short_fall_recovery_achievement
	inserted_doc.bde_vacancy = bde_vacancy
	inserted_doc.stt_vacancy = stt_vacancy
	inserted_doc.closing_stock_of_supers = closing_stock_of_supers
	inserted_doc.primary_achievement = primary_achievement
	inserted_doc.ytd_primary_achievement = ytd_primary_achievement
	inserted_doc.ytd_primary_deficit_recovery_achievement = ytd_primary_deficit_recovery_achievement
	inserted_doc.super_nod_achievement = super_nod_achievement
	inserted_doc.closing_stock_of_distributors = closing_stock_of_distributors
	inserted_doc.second_primary_achievement = second_primary_achievement
	inserted_doc.distributor_nod_achievement = distributor_nod_achievement
	inserted_doc.achieved_typical_accounts = achieved_typical_accounts
	inserted_doc.achieved_business_from_typical_accounts = achieved_business_from_typical_accounts
	inserted_doc.achieved_standard_account = achieved_standard_account
	inserted_doc.achieved_business_from_standard_accounts = achieved_business_from_standard_accounts
	inserted_doc.achieved_important_accounts = achieved_important_accounts
	inserted_doc.achieved_business_from_important_accounts = achieved_business_from_important_accounts
	inserted_doc.achieved_key_accounts = achieved_key_accounts
	inserted_doc.achieved_business_from_key_accounts = achieved_business_from_key_accounts
	inserted_doc.visit_target_achievement = visit_target_achievement
	inserted_doc.productive_call_target_achievement = productive_call_target_achievement
	inserted_doc.new_salon_target_achievement = new_salon_target_achievement
	inserted_doc.achieved_buying_salons_per_bde = achieved_buying_salons_per_bde / cluster_count
	inserted_doc.achieved_treatment_giving_salons_per_stt = achieved_treatment_giving_salons_per_stt
	inserted_doc.achieved_repeat_buying = achieved_repeat_buying
	inserted_doc.achieved_3_months_active_salons_base = achieved_3_months_active_salons_base
	inserted_doc.in_salon_training_achievement = in_salon_training_achievement
	inserted_doc.brillare_sale = brillare_sale
	inserted_doc.in_salon_sale = in_salon_sale
	inserted_doc.root_deep_sale = root_deep_sale
	inserted_doc.hair_care_sale = hair_care_sale
	inserted_doc.skin_care_sale = skin_care_sale
	inserted_doc.home_care_sale = home_care_sale
	inserted_doc.brillare_sale_achievement = brillare_sale_achievement
	inserted_doc.in_salon_sale_achievement = in_salon_sale_achievement
	inserted_doc.root_deep_sale_achievement = root_deep_sale_achievement
	inserted_doc.hair_care_sale_achievement = hair_care_sale_achievement
	inserted_doc.skin_care_sale_achievement = skin_care_sale_achievement
	inserted_doc.home_care_sale_achievement = home_care_sale_achievement
	inserted_doc.save()
	return True

@frappe.whitelist()
def download_multi_pdf(doctype, name, format=None,no_letterhead=None):
	# name can include names of many docs of the same doctype.

	import json
	result = json.loads(name)

	# Concatenating pdf files
	output = PdfFileWriter()
	for i, ss in enumerate(result):
		output = frappe.get_print(doctype, ss, format, as_pdf = True, output = output, no_letterhead=no_letterhead)

	frappe.local.response.filename = "{doctype}.pdf".format(doctype=doctype.replace(" ", "-").replace("/", "-"))
	frappe.local.response.filecontent = read_multi_pdf(output)
	frappe.local.response.type = "download"

def read_multi_pdf(output):
	# Get the content of the merged pdf files
	fname = os.path.join("/tmp", "frappe-pdf-{0}.pdf".format(frappe.generate_hash()))
	output.write(open(fname,"wb"))

	with open(fname, "rb") as fileobj:
		filedata = fileobj.read()

	return filedata

@frappe.whitelist()
def generate_multiPDF():
	clster=[]
	#["ATT-15546","ATT-15545"]
	d = datetime.date.today()
	year = d.strftime("%Y")
	month = d.strftime("%B") 
	doc=frappe.get_all("Cluster Business Plan",filters={"year":year,"month":month},fields=["name"])
	
	for row in doc:
		clster.append(row.name)
	print_format= frappe.db.get_value("Cluster Business Plan Setting","Cluster Business Plan Setting","daily_print_format_name")
	return "<a href='http://erp.brillarescience.com/api/method/erpnext.NDM_cluster.download_multi_pdf?doctype=Cluster Business Plan&name="+json.dumps(clster).replace('/','%2F').replace(',','%2C').replace('&','%26')+"&format="+print_format+"&no_letterhead=1'>Click Here For Download a PDF</a>"
	
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		



