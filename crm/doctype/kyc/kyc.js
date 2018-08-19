// Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt



frappe.provide("erpnext");


erpnext.KYCController = frappe.ui.form.Controller.extend({
	onload: function() {
		},

	refresh: function() {
		var doc = this.frm.doc;
		erpnext.toggle_naming_series();

		if(!this.frm.doc.__islocal) {
			this.frm.add_custom_button(__("Customer"), this.create_customer, __("Make"));
		}

	},
	create_customer: function() {
		frappe.model.open_mapped_doc({
			method: "erpnext.crm.doctype.kyc.kyc.make_customer1",
			frm: cur_frm
		})
	}
	

});

$.extend(cur_frm.cscript, new erpnext.KYCController({frm: cur_frm}));



