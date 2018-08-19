// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.ui.form.on("Material Availability Tool", {
	
	onload: function(frm) {
		frm.set_value("from_date", frappe.datetime.month_start());
		frm.set_value("to_date", frappe.datetime.month_end());
	},

	refresh: function(frm) {
		frm.disable_save();
	},

	update_clearance_date: function(frm) {
		return frappe.call({
			method: "update_delivery_date",
			doc: frm.doc,
			callback: function(r, rt) {
				frm.refresh_field("order_entries");
				frm.refresh_fields();
			}
		});
	},
	get_order_entries: function(frm) {
		return frappe.call({
			method: "get_order_entries",
			doc: frm.doc,
			callback: function(r, rt) {
				alert(JSON.stringify(frm.doc));
				frm.refresh_field("order_entries");
				frm.refresh_fields();
			}
		});
	}
});
