// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Salary Register Summary"] = {
	"filters": [
		{
			"fieldname":"date_range",
			"label": __("Date Range"),
			"fieldtype": "DateRange",
			"default": [frappe.defaults.get_user_default("year_start_date"), frappe.datetime.get_today()],
			"reqd": 1
		},
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company")
		},
		{
			"fieldname":"group_by_employee",
			"label": __("Group by Employee"),
			"fieldtype": "Check",
			"default": 1
		}
	]
}
