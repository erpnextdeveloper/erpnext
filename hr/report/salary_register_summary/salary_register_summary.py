# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import flt
from frappe import _

def execute(filters=None):
	if not filters: filters = {}
	salary_slips = get_salary_slips(filters)
	columns, earning_types, ded_types = get_columns(salary_slips,filters)
	ss_earning_map = get_ss_earning_map(salary_slips,filters)
	ss_ded_map = get_ss_ded_map(salary_slips,filters)


	data = []
	#frappe.msgprint(salary_slips)
	if filters.get("group_by_employee"):
		for ss in salary_slips:
			#frappe.msgprint(ss[1])
			row = [ss[1], ss[2], ss[3], ss[4], ss[5],ss[6], ss[7], ss[8], ss[9], ss[10]]
			if not ss[3] == None:columns[3] = columns[3].replace('-1','120')
			if not ss[4]  == None: columns[4] = columns[4].replace('-1','120')
			if not ss[5]  == None: columns[5] = columns[5].replace('-1','120')
			if not ss[9]  == None: columns[9] = columns[9].replace('-1','130')
			

			for e in earning_types:
				row.append(ss_earning_map.get(ss[1], {}).get(e))

			row += [ss[11]]

			for d in ded_types:
				row.append(ss_ded_map.get(ss[1], {}).get(d))

			row += [ss[12], ss[13]]

			data.append(row)
	else:
		for ss in salary_slips:
			row = [ss.name, ss.employee, ss.employee_name, ss.branch, ss.department, ss.designation,
				ss.company, ss.start_date, ss.end_date, ss.leave_withut_pay, ss.payment_days]

			if not ss.branch == None:columns[3] = columns[3].replace('-1','120')
			if not ss.department  == None: columns[4] = columns[4].replace('-1','120')
			if not ss.designation  == None: columns[5] = columns[5].replace('-1','120')
			if not ss.leave_withut_pay  == None: columns[9] = columns[9].replace('-1','130')
			

			for e in earning_types:
				row.append(ss_earning_map.get(ss.name, {}).get(e))

			row += [ss.gross_pay]
	
			for d in ded_types:
				row.append(ss_ded_map.get(ss.name, {}).get(d))
	
			row += [ss.total_deduction, ss.net_pay]
	
			data.append(row)

	return columns, data

def get_columns(salary_slips,filters=None):
	"""
	columns = [
		_("Salary Slip ID") + ":Link/Salary Slip:150",_("Employee") + ":Link/Employee:120", _("Employee Name") + "::140", _("Branch") + ":Link/Branch:120",
		_("Department") + ":Link/Department:120", _("Designation") + ":Link/Designation:120",
		_("Company") + ":Link/Company:120", _("Start Date") + "::80", _("End Date") + "::80", _("Leave Without Pay") + ":Float:130",
		_("Payment Days") + ":Float:120"
	]
	"""
	if filters.get("group_by_employee"):
		columns = [
		_("Employee") + ":Link/Employee:120", _("Employee Name") + "::140", _("Branch") + ":Link/Branch:-1",
		_("Department") + ":Link/Department:-1", _("Designation") + ":Link/Designation:-1",
		_("Company") + ":Link/Company:120", _("Start Date") + "::80", _("End Date") + "::80", _("Leave Without Pay") + ":Float:-1",
		_("Payment Days") + ":Float:120"
	]	
	else:
		columns = [
		_("Salary Slip ID") + ":Link/Salary Slip:150",_("Employee") + ":Link/Employee:120", _("Employee Name") + "::140", _("Branch") + ":Link/Branch:-1",
		_("Department") + ":Link/Department:-1", _("Designation") + ":Link/Designation:-1",
		_("Company") + ":Link/Company:120", _("Start Date") + "::80", _("End Date") + "::80", _("Leave Without Pay") + ":Float:-1",
		_("Payment Days") + ":Float:120"
	]	

	salary_components = {_("Earning"): [], _("Deduction"): []}
	if filters.get("group_by_employee"):
		filters.update({"from_date": filters.get("date_range")[0], "to_date":filters.get("date_range")[1]})
		conditions, filters = get_conditions(filters)
		salary_slip = frappe.db.sql("""select * from `tabSalary Slip` where docstatus = 1 %s
		order by employee""" % conditions, filters, as_dict=1)
	
		for component in frappe.db.sql("""select distinct sd.salary_component, sc.type
			from `tabSalary Detail` sd, `tabSalary Component` sc
			where sc.name=sd.salary_component and sd.amount != 0 and sd.parent in (%s)""" %
			(', '.join(['%s']*len(salary_slip))), tuple([d.name for d in salary_slip]), as_dict=1):
			salary_components[_(component.type)].append(component.salary_component)
	else:
		for component in frappe.db.sql("""select distinct sd.salary_component, sc.type
			from `tabSalary Detail` sd, `tabSalary Component` sc
			where sc.name=sd.salary_component and sd.amount != 0 and sd.parent in (%s)""" %
			(', '.join(['%s']*len(salary_slips))), tuple([d.name for d in salary_slips]), as_dict=1):
			salary_components[_(component.type)].append(component.salary_component)
		

	columns = columns + [(e + ":Currency:120") for e in salary_components[_("Earning")]] + \
		[_("Gross Pay") + ":Currency:120"] + [(d + ":Currency:120") for d in salary_components[_("Deduction")]] + \
		[_("Total Deduction") + ":Currency:120", _("Net Pay") + ":Currency:120"]

	return columns, salary_components[_("Earning")], salary_components[_("Deduction")]

def get_salary_slips(filters):
	filters.update({"from_date": filters.get("date_range")[0], "to_date":filters.get("date_range")[1]})
	conditions, filters = get_conditions(filters)
	if filters.get("group_by_employee"):
		start_date=filters.get("date_range")
		end_date=filters.get("date_range")
		salary_slips=frappe.db.sql("""select name,employee,employee_name,max(branch) as branch,max(department) as department,max(designation) as designation,
			max(company) as company,min(start_date) as start_date,max(end_date) as end_date,sum(leave_without_pay) as leave_without_pay,sum(payment_days) as payment_days,sum(gross_pay) as gross_pay,sum(total_deduction) as total_deduction,sum(net_pay) as net_pay from `tabSalary Slip` where docstatus = 1 %s group by employee"""% conditions, filters)
	else:
		salary_slips = frappe.db.sql("""select * from `tabSalary Slip` where docstatus = 1 %s
		order by employee""" % conditions, filters, as_dict=1)

	if not salary_slips:
		frappe.throw(_("No salary slip found between {0} and {1}").format(
			filters.get("from_date"), filters.get("to_date")))
	return salary_slips

def get_conditions(filters):
	if filters.get("group_by_employee"):
		conditions = ""
		if filters.get("date_range"): conditions += " and start_date >= %(from_date)s"
		if filters.get("date_range"): conditions += " and end_date <= %(to_date)s"
		return conditions, filters
	else:
		conditions = ""
		if filters.get("date_range"): conditions += " and start_date >= %(from_date)s"
		if filters.get("date_range"): conditions += " and end_date <= %(to_date)s"
		if filters.get("company"): conditions += " and company = %(company)s"
		if filters.get("employee"): conditions += " and employee = %(employee)s"
		#if filters.get("group_by_employee"): conditions += " group by employee0"
		return conditions, filters

def get_ss_earning_map(salary_slips,filters=None):
	filters.update({"from_date": filters.get("date_range")[0], "to_date":filters.get("date_range")[1]})
	conditions, filters = get_conditions(filters)
	if filters.get("group_by_employee"):
		salary_slip = frappe.db.sql("""select * from `tabSalary Slip` where docstatus = 1 %s
		order by employee""" % conditions, filters, as_dict=1)
		
		ss_earnings = frappe.db.sql("""select substring(parent,10,8) as parent,max(salary_component) as salary_component,sum(amount) as amount
		from `tabSalary Detail` where parent in (%s) group by substring(parent,10,8),salary_component""" %
		(', '.join(['%s']*len(salary_slip))), tuple([d.name for d in salary_slip]), as_dict=1)
	else:
	
		ss_earnings = frappe.db.sql("""select parent,salary_component, amount
		from `tabSalary Detail` where parent in (%s)""" %
		(', '.join(['%s']*len(salary_slips))), tuple([d.name for d in salary_slips]), as_dict=1)

	ss_earning_map = {}
	for d in ss_earnings:
		ss_earning_map.setdefault(d.parent, frappe._dict()).setdefault(d.salary_component, [])
		ss_earning_map[d.parent][d.salary_component] = flt(d.amount)

	return ss_earning_map

def get_ss_ded_map(salary_slips,filters=None):
	filters.update({"from_date": filters.get("date_range")[0], "to_date":filters.get("date_range")[1]})
	conditions, filters = get_conditions(filters)
	if filters.get("group_by_employee"):
		salary_slip = frappe.db.sql("""select * from `tabSalary Slip` where docstatus = 1 %s
		order by employee""" % conditions, filters, as_dict=1)
		
		ss_deductions = frappe.db.sql("""select substring(parent,10,8) as parent, max(salary_component) as salary_component, sum(amount) as amount
			from `tabSalary Detail` where parent in (%s) group by substring(parent,10,8),salary_component""" %
			(', '.join(['%s']*len(salary_slip))), tuple([d.name for d in salary_slip]), as_dict=1)
	else:
		ss_deductions = frappe.db.sql("""select parent, salary_component, amount
		from `tabSalary Detail` where parent in (%s)""" %
		(', '.join(['%s']*len(salary_slips))), tuple([d.name for d in salary_slips]), as_dict=1)

	ss_ded_map = {}
	for d in ss_deductions:
		ss_ded_map.setdefault(d.parent, frappe._dict()).setdefault(d.salary_component, [])
		ss_ded_map[d.parent][d.salary_component] = flt(d.amount)

	return ss_ded_map
