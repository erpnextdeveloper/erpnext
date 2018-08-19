from __future__ import unicode_literals
import frappe
from frappe.custom.doctype.property_setter.property_setter import make_property_setter
from datetime import date, datetime
from frappe.utils import getdate, validate_email_add, today, add_years,add_days,format_datetime
from frappe.model.naming import make_autoname
from frappe import throw, _, scrub
import frappe.permissions
from frappe.model.document import Document
import json
import collections
from frappe.model.mapper import get_mapped_doc
import random
import logging
import string



@frappe.whitelist()
def make_company(source_name, target_doc=None):
	return _make_company(source_name, target_doc)

def _make_company(source_name, target_doc=None, ignore_permissions=True):
	def set_missing_values(source, target):
		
		
		target.customer_type = source.customer_group
		if source.super_distributor:
			target.company = source.super_distributor
		else:
			target.company = "Brillare Science Private Limited"

	doclist = get_mapped_doc("Customer", source_name,
		{"Customer": {
			"doctype": "Customer To Company",
			"field_map": {
				"customer": "customer_name"
			}
		}}, target_doc, set_missing_values, ignore_permissions=ignore_permissions)

	if doclist.customer_type=="Distributor":
		d1=frappe.db.sql("""select customer from `tabCustomer To Company` where customer=%s""",doclist.company)
		if not d1:
			frappe.throw("Please Create Company For Super Distributor")


	d=frappe.db.sql("""select customer from `tabCustomer To Company` where customer=%s""",doclist.customer)
	if d:
		frappe.throw("Company Already Created")
	else:
		#add=[]
		email1=frappe.db.get("Dynamic Link",{"link_name":doclist.customer}).parent
		email2=frappe.db.get("Address",{"name":email1}).email_id
		#add_name=frappe.db.sql("""select parent from `tabDynamic Link` where link_name=%s""",doclist.customer)
		#if add_name:
		#	for row2 in add_name:
		#		address=frappe.db.sql("""select pincode,is_your_company_address,address_line2,city,address_line1,address_title,state,gstin,address_type,place_of_supply,phone,state_code,gst_state,country,is_shipping_address from `tabAddress` where name=%s""",row2[0],as_dict=True)
		#		address[0]["customer"] = doclist.customer
		#		add.append(address[0])
		if email2:
			doclist.email=email2
		#	frappe.msgprint(json.dumps(add))
		#	doclist.address_company=add
			data=doclist.insert(ignore_permissions=True)
			if data:
				if data.customer_type=="Distributor":
					logging.warning("kyc customer create+")
					frappe.msgprint("kyc customr created")
					get_customerList_for_distributor_kyc(data.customer,data.customer_type)
				else:
					logging.warning("customer create+")
					frappe.msgprint("normal customer")
					get_customerList_for_distributor2(data.customer,data.customer_type)
				frappe.msgprint("Company Created")
			else:
				frappe.msgprint("Something Went Wrong")
		else:
			frappe.throw("Email Does Not Exist")







@frappe.whitelist(allow_guest=True)
def createSalesOrder(data):
	company=json.loads(data)
	logging.warning("blank+"+str(company))
	from frappe.auth import LoginManager
	login_manager = LoginManager()
	login_manager.authenticate("Administrator","Brillare09*")
	login_manager.post_login()
	#logging.warning("user+"+str(login_manager.user)+"info+"+str(login_manager.info)+"full name+"+str(login_manager.full_name)+"user type+"+str(login_manager.user_type))
	logging.warning("info+"+str(login_manager.info))
	#remote = FrappeClient("http://35.194.1.49:8000", "Administrator", "Brillare09*")
	doc=frappe.get_doc({
			"docstatus": 0,
			"doctype": "Sales Order",
			"name": "New Sales Order 1",
			"__islocal": 1,
			"__unsaved": 1,
			"owner": "Administrator",
			"order_type": "Sales",
			"company": company["supplier"],
			"transaction_date": company["transaction_date"],
			"items": [],
			"taxes_and_charges": company["taxes_and_charges"],
			"customer_name": company["company"],
			"customer": company["company"],
			"delivery_date": company["schedule_date"]
		})
	d=doc.insert(ignore_permissions=True)
	if d:
		for row in company["items"]:
			logging.warning("Item"+row["item_code"])
			d1=frappe.get_doc({
				"docstatus": 0,
				"doctype": "Sales Order Item",
				"name": "New Sales Order Item 1",
				"__islocal": 1,
				"__unsaved": 1,
				"owner": "Administrator",
				"parent": str(d.name),
				"parentfield": "items",
				"parenttype": "Sales Order",
				"qty": row["qty"],
				"rate": row["rate"],
				"delivery_date":company["transaction_date"],
				"item_code": row["item_code"],
				"schedule_date": company["schedule_date"],
				"warehouse": "Finish Goods Warehouse - BSPL",
				"batch_no": "123"
			})
			d1.insert()
		d2=frappe.get_doc("Sales Order",d.name)
		d2.save()



# @frappe.whitelist()
# def get_customerList_for_distributor(distributor_name,customer_type):
#     #return "abc"
#     if customer_type=="Super Distributor":
#         data=frappe.get_all('Customer', filters={'super_distributor': distributor_name}, fields=['name', 'customer_name','customer_group','super_distributor'])
#         for cust in data:
#             customer=frappe.get_doc("Customer",{"name":cust.name})
#             address_name=frappe.get_all("Dynamic Link",filters={"link_name":cust.customer_name},fields=['parent'])
#             addresslist = []
#             for addressList1 in address_name:
#                 address=frappe.get_doc("Address",{"name":addressList1.parent})
#                 addresslist.append(address)

#             json_data = frappe.get_doc({
#                                    "docstatus":0,
#                                    "doctype":"Sup to Customer",
#                                    "name":"New Sup to Customer 1",
#                                    "__islocal":1,
#                                    "__unsaved":1,
#                                    "owner":"Administrator",
#                                    "customer_data":json.dumps(cust,default=json_serial),
#                                    "address_data":json.dumps(addresslist,default=lambda o: (o.__dict__))
#                                    })
#             inserted_json=json_data.insert()
#         return inserted_json



# @frappe.whitelist()
# def get_customerList_for_distributor1(distributor_name,customer_type):
# 	# if customer_type=="Super Distributor":\
# 	if customer_type=="Super Distributor":
#    		data=frappe.db.sql("""select name from `tabCustomer` where super_distributor=%s""",distributor_name)
#    		if data:
#    			for row in data:
#    				#customer=frappe.get_doc("Customer",row[0])
#    				customer_obj=[]
#    				customer=frappe.db.sql("""select name,customer_name,customer_group,super_distributor from `tabCustomer` where name=%s""",row[0])
#    				for row1 in customer:
#    					d = collections.OrderedDict()
#    					d["name"]=str(row1[0])
#    					d["customer_name"]=str(row1[1])
#    					d["customer_group"]=str(row1[2])
#    					d["super_distributor"]=str(row1[3])
#    					customer_obj.append(d)


#    				address_obj=[]
#    				address_name=frappe.db.get("Dynamic Link",{"link_name":row[0]}).parent
#    				address=frappe.db.sql("""select pincode,is_your_company_address,address_line2,city,address_line1,address_title,state,gstin,address_type,place_of_supply,phone,state_code,gst_state,country,is_shipping_address from `tabAddress` where name=%s""",address_name)
#    				for row2 in address:
#    					d = collections.OrderedDict()
#    					d["pincode"]=str(row2[0])
#    					d["is_your_company_address"]=str(row2[1])
#    					d["address_line2"]=str(row2[2])
#    					d["city"]=str(row2[3])
#    					d["address_line1"]=str(row2[4])
#    					d["address_title"]=str(row2[5])
#    					d["state"]=str(row2[6])
#    					d["gstin"]=str(row2[7])
#    					d["address_type"]=str(row2[8])
#    					d["place_of_supply"]=str(row2[9])
#    					d["phone"]=str(row2[10])
#    					d["state_code"]=str(row2[11])
#    					d["gst_state"]=str(row2[12])
#    					d["country"]=str(row2[13])
#    					d["is_shipping_address"]=str(row2[14])
#    					address_obj.append(d)
#    				#address_data=frappe.get_doc("Address",address_name)

#    				json_data=frappe.get_doc({
# 									"docstatus": 0,
# 									"doctype": "Sup to Customer",
# 									"name": "New Sup to Customer 1",
# 									"__islocal": 1,
# 									"__unsaved": 1,
# 									"owner": "Administrator",
# 									"customer_data":json.dumps(customer_obj),
# 									"address_data":json.dumps(address_obj)
# 								})
#    				json_data_insert=json_data.insert(ignore_permissions=True)


@frappe.whitelist()
def get_customerList_for_distributor1(distributor_name,customer_type):
	doc=frappe.get_doc({
						"docstatus": 0,
						"doctype": "Dis to Customer",
						"name": "New Dis to Customer 1",
						"__islocal": 1,
						"__unsaved": 1,
						"owner": "Administrator",
						"distributor": str(distributor_name)
					})
	doc1=doc.insert(ignore_permissions=True)
	if doc1:

   		data=frappe.db.sql("""select name from `tabCustomer` where super_distributor=%s""",distributor_name)
   		if data:
   			for row in data:
   				customer=frappe.db.sql("""select name,customer_name,customer_group,super_distributor from `tabCustomer` where name=%s""",row[0])
   				if customer:
   					for row1 in customer:
						doc2=frappe.get_doc({
									"docstatus": 0,
									"doctype": "Customer Child",
									"name": "New Customer Child 1",
									"__islocal": 1,
									"__unsaved": 1,
									"owner": "Administrator",
									"customer_group": str(row1[2]),
									"parent": doc1.name,
									"parentfield": "customers",
									"parenttype": "Dis to Customer",
									"name1": str(row1[0]),
									"customer_name": str(row1[1]),
									"super_distributor": str(row1[3])
								})
						doc3=doc2.insert(ignore_permissions=True)
				address_name=frappe.db.get("Dynamic Link",{"link_name":row[0]}).parent
				add_name=frappe.db.sql("""select parent from `tabDynamic Link` where link_name=%s""",row[0])
				if add_name:
					for row2 in add_name:
   						address=frappe.db.sql("""select pincode,is_your_company_address,address_line2,city,address_line1,address_title,state,gstin,address_type,place_of_supply,phone,state_code,gst_state,country,is_shipping_address from `tabAddress` where name=%s""",address_name)	
   						if address:
   							for row2 in address:
   								row2[1]
   								doc4=frappe.get_doc({
											"docstatus": 0,
											"doctype": "Address Child",
											"name": "New Address Child 2",
											"__islocal": 1,
											"__unsaved": 1,
											"owner": "Administrator",
											"parent": str(doc1.name),
											"parentfield": "address",
											"parenttype": "Dis to Customer",
											"customer":str(row[0]) ,
											"is_shipping_address": str(row2[14]),
											"is_company_address": row2[1],
											"address_type": str(row2[8]),
											"address_title": row2[5],
											"address_line_1": row2[4],
											"address_line_2": row2[2],
											"city": row2[3],
											"state": row2[6],
											"country": str(row2[13]),
											"pincode": str(row2[0]),
											"place_of_supply": str(row2[9]),
											"phone": str(row2[10]),
											"gstin": row2[7],
											"state_code":str(row2[11]) ,
											"gst_state": str(row2[12])
										})
   								doc5=doc4.insert(ignore_permissions=True)

   	final_doc=frappe.get_doc("Dis to Customer",doc1.name)
   	if final_doc:
   		final_doc.save(ignore_permissions=True)

@frappe.whitelist()
def get_customerList_for_distributor2(distributor_name,customer_type):
    customer = []
    address = []
    data=frappe.db.sql("""select name from `tabCustomer` where super_distributor=%s or name=%s""",(distributor_name,distributor_name))
    if data:
        for row in data:
            customer1=frappe.db.sql("""select name,customer_name,customer_group,super_distributor from `tabCustomer` where name=%s""",row[0],as_dict=True)
            #customer1[0]["doctype"] = "Customer Child"
            #customer1[0]["name"] = "New Customer Child 1"
            #customer1[0]["parent"] = "New Dis to Customer 1"
            #customer1[0]["parentfield"] = "customers"
            #customer1[0]["parenttype"]= "Dis to Customer"
            if not customer1[0]["name"]==distributor_name:
            	customer.append(customer1[0])
            address_name=frappe.db.get("Dynamic Link",{"link_name":row[0]}).parent
            add_name=frappe.db.sql("""select parent from `tabDynamic Link` where link_name=%s""",row[0])
            if add_name:
                for row2 in add_name:
                	if not row[0]==distributor_name:
                		address1=frappe.db.sql("""select pincode,is_your_company_address,address_line2,city,address_line1,address_title,state,gstin,address_type,place_of_supply,phone,state_code,gst_state,country,is_shipping_address from `tabAddress` where name=%s""",address_name,as_dict=True)
                		address1[0]["customer"] = customer1[0].name
                		address1[0]["link_name"]="Customer"
                		address.append(address1[0])
                	else:
                		address1=frappe.db.sql("""select pincode,is_your_company_address,address_line2,city,address_line1,address_title,state,gstin,address_type,place_of_supply,phone,state_code,gst_state,country,is_shipping_address from `tabAddress` where name=%s""",address_name,as_dict=True)
                		address1[0]["customer"] = customer1[0].name
                		address1[0]["is_your_company_address"]=1
                		address1[0]["is_shipping_address"]=0
                		address1[0]["link_name"]="Company"
                		address.append(address1[0])


    #address_name1=frappe.db.get("Dynamic Link",{"link_name":distributor_name}).parent
    # add_name1=frappe.db.sql("""select parent from `tabDynamic Link` where link_name=%s""",distributor_name)
    # for row3 in add_name1:
    # 	address2=frappe.db.sql("""select pincode,is_your_company_address,address_line2,city,address_line1,address_title,state,gstin,address_type,place_of_supply,phone,state_code,gst_state,country,is_shipping_address from `tabAddress` where name=%s""",row3[0],as_dict=True)
    # 	address2[0]["customer"]=distributor_name
    # 	address.append(address2[0])
                        #return (customer,address)
        doc=frappe.get_doc({
                          "docstatus": 0,
                          "doctype": "Dis to Customer",
                          "name": "New Dis to Customer 1",
                          "__islocal": 1,
                          "__unsaved": 1,
                          "owner": "Administrator",
                          "distributor": str(distributor_name),
                          "customers":customer,
                          "address":address
                          })
        doc1=doc.save(ignore_permissions=True)
        return (customer,doc1)

@frappe.whitelist()
def get_customerList_for_distributor_kyc(distributor_name,customer_type):
	customer = []
	address = []
	if customer_type=="Distributor":
		logging.warning(" 1 get_customerList_for_distributor_kyc")

		add_kyc_cust(distributor_name,customer_type)
	# if customer_type=="Super Distributor":
	# 	data=frappe.db.sql("""select name from `tabCustomer` where super_distributor=%s""",distributor_name)
	# 	if data:
	# 		for row in data:
	# 			customer1=frappe.db.sql("""select name,customer_name,customer_group,super_distributor from `tabCustomer` where name=%s""",row[0],as_dict=True)
	# 			customer.append(customer1[0])
	# 			address_name=frappe.db.get("Dynamic Link",{"link_name":row[0]}).parent
	# 			add_name=frappe.db.sql("""select parent from `tabDynamic Link` where link_name=%s""",row[0])
	# 			if add_name:
	# 				for row2 in add_name:
	# 					address1=frappe.db.sql("""select pincode,is_your_company_address,address_line2,city,address_line1,address_title,state,gstin,address_type,place_of_supply,phone,state_code,gst_state,country,is_shipping_address from `tabAddress` where name=%s""",address_name,as_dict=True)
	# 					address1[0]["customer"] = customer1[0].name
	# 					address1[0]["link_name"]="Customer"
	# 					address.append(address1[0])
	# 		doc=frappe.get_doc({
	#                           "docstatus": 0,
	#                           "doctype": "Dis to Customer",
	#                           "name": "New Dis to Customer 1",
	#                           "__islocal": 1,
	#                           "__unsaved": 1,
	#                           "owner": "Administrator",
	#                           "distributor": str(distributor_name),
	#                           "customers":customer,
	#                           "address":address
	#                           })
	# 		doc1=doc.save(ignore_permissions=True)
	# 		return customer







@frappe.whitelist()
def add_kyc_cust(distributor_name,customer_type):
	customer=[]
	address=[]
	
	data=frappe.db.sql("""select name from `tabKYC` where distributor=%s""",distributor_name)
	logging.warning("no kyc data found+"+str(data))
	
	if data:
		for row in data:
			customer1=frappe.db.sql("""select salon_parlor_spa_name as 'customer_name',distributor as 'super_distributor' from `tabKYC` where name=%s""",row[0],as_dict=True)
			customer1[0]["name"] = customer1[0].customer_name
			customer1[0]["customer_group"]="Salon"
			customer.append(customer1[0])
			address1=frappe.db.sql("""select salon_parlor_spa_name as 'customer',pin as 'pincode',door_building_plot_number as 'address_line1',street as 'address_line2',city_town as 'city',state as 'state',contact_number as 'phone' from `tabKYC` where name=%s""",row[0],as_dict=True)
			address1[0]["is_your_company_address"]=0
			address1[0]["address_title"]=str(customer1[0].customer_name)
			address1[0]["gstin"]='NA'
			address1[0]["address_type"]='Billing'
			address1[0]["place_of_supply"]=str()
			address1[0]["state_code"]=str()
			address1[0]["gst_state"]=str()
			address1[0]["country"]=str()
			address1[0]["is_shipping_address"]=0
			address1[0]["link_name"]="Customer"
			address.append(address1[0])

		# address_name=frappe.db.get("Dynamic Link",{"link_name":distributor_name}).parent
		# address2=frappe.db.sql("""select pincode,is_your_company_address,address_line2,city,address_line1,address_title,state,gstin,address_type,place_of_supply,phone,state_code,gst_state,country,is_shipping_address from `tabAddress` where name=%s""",address_name,as_dict=True)
		# address2[0]["customer"]=distributor_name
		# address2[0]["is_your_company_address"]=1
		# address2[0]["is_shipping_address"]=0
		# address2[0]["link_name"]="Company"
		# address.append(address2[0])


		doc=frappe.get_doc({
	                        "docstatus": 0,
	                        "doctype": "Dis to Customer",
	                        "name": "New Dis to Customer 1",
	                        "__islocal": 1,
	                        "__unsaved": 1,
	                        "owner": "Administrator",
	                        "distributor": str(distributor_name),
	                        "customers":customer,
	                        "address":address
	                        })
		doc1=doc.save(ignore_permissions=True)
		return doc1









	# if customer_type=="Super Distributor":\
	# if customer_type=="Super Distributor":
 #   		data=frappe.db.sql("""select name from `tabCustomer` where super_distributor=%s""",distributor_name)
 #   		if data:
 #   			for row in data:
 #   				#customer=frappe.get_doc("Customer",row[0])
 #   				customer_obj=[]
 #   				customer=frappe.db.sql("""select name,customer_name,customer_group,super_distributor from `tabCustomer` where name=%s""",row[0])
 #   				for row1 in customer:
 #   					d = collections.OrderedDict()
 #   					d["name"]=str(row1[0])
 #   					d["customer_name"]=str(row1[1])
 #   					d["customer_group"]=str(row1[2])
 #   					d["super_distributor"]=str(row1[3])
 #   					customer_obj.append(d)


 #   				address_obj=[]
 #   				address_name=frappe.db.get("Dynamic Link",{"link_name":row[0]}).parent
 #   				address=frappe.db.sql("""select pincode,is_your_company_address,address_line2,city,address_line1,address_title,state,gstin,address_type,place_of_supply,phone,state_code,gst_state,country,is_shipping_address from `tabAddress` where name=%s""",address_name)
 #   				for row2 in address:
 #   					d = collections.OrderedDict()
 #   					d["pincode"]=str(row2[0])
 #   					d["is_your_company_address"]=str(row2[1])
 #   					d["address_line2"]=str(row2[2])
 #   					d["city"]=str(row2[3])
 #   					d["address_line1"]=str(row2[4])
 #   					d["address_title"]=str(row2[5])
 #   					d["state"]=str(row2[6])
 #   					d["gstin"]=str(row2[7])
 #   					d["address_type"]=str(row2[8])
 #   					d["place_of_supply"]=str(row2[9])
 #   					d["phone"]=str(row2[10])
 #   					d["state_code"]=str(row2[11])
 #   					d["gst_state"]=str(row2[12])
 #   					d["country"]=str(row2[13])
 #   					d["is_shipping_address"]=str(row2[14])
 #   					address_obj.append(d)
 #   				#address_data=frappe.get_doc("Address",address_name)

 #   				json_data=frappe.get_doc({
	# 								"docstatus": 0,
	# 								"doctype": "Sup to Customer",
	# 								"name": "New Sup to Customer 1",
	# 								"__islocal": 1,
	# 								"__unsaved": 1,
	# 								"owner": "Administrator",
	# 								"customer_data":json.dumps(customer_obj),
	# 								"address_data":json.dumps(address_obj)
	# 							})
 #   				json_data_insert=json_data.insert(ignore_permissions=True)
   				

   		# customer=frappe.get_doc("Customer",data[0][0])
   		# address_name=frappe.db.get("Dynamic Link",{"link_name":data[0][0]}).parent
   		# address_data=frappe.get_doc("Address",address_name)
     #    return address_data
   		# if data:
   		# 	for cust in data:
   		# 		customer=frappe.get_doc("Customer",cust[0])
   		# 		address_name=frappe.db.get("Dynamic Link",{"link_name":cust[0]}).parent
   		# 		address_data=frappe.get_doc("Address",address_name)
     #    	    return address_data

        	    # json_data=frappe.get_doc({
        	    #                        "docstatus":0,
        	    #                        "doctype":"Sup to Customer",
        	    #                        "name":"New Sup to Customer 1",
        	    #                        "__islocal":1,
        	    #                        "__unsaved":1,
        	    #                        "owner":"Administrator",
        	    #                        "customer_data":str(customer),
        	    #                        "address_data":str(address_data)
        	    #                        })
        	 #    inserted_json=json_data.insert()
        		# if inserted_json:
        		# 	return "True"


    
    
    
#        for cust in data:
#            addresslist = []
#            address_name=frappe.get_all("Dynamic Link",filters={"link_name":cust.customer_name},fields=['parent'])
#            for addressList1 in address_name:
                #return frappe.get_doc("Address",{"name":addressList1.parent})
#                address=frappe.get_doc("Address",{"name":addressList1.parent})
#                custlink = []
#                for links in address.links:
#                    custlink.append[links.__dict__]
#                address.links = custlink
#                addresslist.append(address)
#            cust.address = addresslist

#        json_data = frappe.get_doc({
#                              "docstatus":0,
#                              "doctype":"Sup to Customer",
#                              "name":"New Sup to Customer 1",
#                              "__islocal":1,
#                              "__unsaved":1,
#                              "owner":"Administrator",
#                              "customer_data":json.dumps(data,default=lambda o: (o.__dict__)),
#                              "address_data":""
#                              })
#        inserted_json=json_data.insert()
#        return inserted_json
#    elif customer_type=="Distributor":
#        frappe.get_all('KYC', filters={'status': 'Open'}, fields=['name', 'description'])


# def json_serial(obj):
    
#     if isinstance(obj, (datetime, date)):
#         return obj.isoformat()
#     else:
#         return obj.__dict__
# #raise TypeError ("Type %s not serializable" % type(obj))


















