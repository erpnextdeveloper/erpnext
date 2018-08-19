// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.provide("erpnext");


erpnext.CandidateInformationFormController = frappe.ui.form.Controller.extend({
	onload: function() {
		},

	refresh: function() {
		var doc = this.frm.doc;
		erpnext.toggle_naming_series();

		if(!this.frm.doc.__islocal) {
			this.frm.add_custom_button(__("Employee"), this.create_employee, __("Make"));
		}

	},
	create_employee: function() {
		frappe.model.open_mapped_doc({
			method: "erpnext.hr.doctype.candidate_information_form.candidate_information_form.make_employee",	
			frm: cur_frm
		})
	}
	

});

$.extend(cur_frm.cscript, new erpnext.CandidateInformationFormController({frm: cur_frm}));


