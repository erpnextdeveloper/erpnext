from __future__ import unicode_literals
import frappe
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

from datetime import datetime
from frappe.utils import flt,getdate, validate_email_add, today, add_years,add_days,format_datetime
from frappe.model.naming import make_autoname
from frappe import throw, _, scrub
import frappe.permissions
from frappe.model.document import Document
import json
import collections
import urllib,urllib2
import requests
import os
import shutil

global dump

@frappe.whitelist(allow_guest=True)
def file_creator():
    global dump
    url = "http://erp.brillarescience.com/api/method/frappe.utils.print_format.download_pdf?doctype=BOM&name=BOM-3PMNMACK-003&format=Standard&no_letterhead=1"
    file = requests.get(url, stream=True)
    dump = file.raw

#@frappe.whitelist(allow_guest=True)
#def file_creator():
#	download_file("http://erp.brillarescience.com/api/method/frappe.utils.print_format.download_pdf?doctype=BOM&name=BOM-3PMNMACK-003&format=Standard&no_letterhead=1")

	
def download_file(download_url):
    response = urllib2.urlopen(download_url)
    file = open("document.pdf", 'w')
    file.write(response.read())
    file.close()

def test(employee,method):
		for l in employee.get("leave_approvers")[:]:
			frappe.permissions.add_user_permission("Employee",employee.name,l.leave_approver)

		
		if employee.status == "Left":
			frappe.db.sql("""UPDATE tabUser set enabled=0 where name=%s""",employee.user_id)
			frappe.msgprint("testing")

		user=employee.get("user_id")
		frappe.msgprint(user)
		territory_name=employee.get("territory")
     		frappe.permissions.add_user_permission("Territory",territory_name,user)    
    		territory_list=frappe.db.sql("select territory_name from tabTerritory where parent_territory=%s",territory_name)
  		territory_list1=json.dumps(territory_list)	
       		territory_list2=json.loads(territory_list1)
  		for i,list in enumerate(territory_list2):
  			frappe.permissions.add_user_permission("Territory",list[0],user)
 		        child_territory_list=frappe.db.sql("select territory_name from tabTerritory where parent_territory=%s",list[0])
            		child_territory_list1=json.dumps(child_territory_list)
		        child_territory_list2=json.loads(child_territory_list1)
                 	for j,list in enumerate(child_territory_list2):
               			frappe.permissions.add_user_permission("Territory",list[0],user)

