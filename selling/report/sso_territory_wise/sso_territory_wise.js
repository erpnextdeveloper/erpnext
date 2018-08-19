// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["SSO-Territory Wise"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date"
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date"
		},
		{
			"fieldname":"territory",
			"label": __("Territory"),
			"fieldtype": "Link",
			"options": "Territory",
			"default":"India"
		}
	]
}
