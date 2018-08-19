// Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
frappe.provide("erpnext.hr");
frappe.ui.form.on('Annual Appraisal Report For Head Office', {
	onload: function(frm) {
		if(!frm.doc.approver)
		{
			frappe.call({
            method: "erpnext.api.getLeaveApp",
            callback: function (r) {
             	data=r.message;
             	if(data)
             	{
             		frm.set_value("approver",data[0][0])
             	}
            }
        });
	}
		

	}
});
