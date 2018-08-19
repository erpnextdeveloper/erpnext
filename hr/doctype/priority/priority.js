// Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
frappe.provide("erpnext.hr");
frappe.ui.form.on('Priority', {
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
		if(!frm.doc.employee_name)
		{
			frappe.call({
            method: "erpnext.api.getEmpDetail",
            callback: function (r) {
             	data=r.message;
             	frm.set_value("employee",data[0][0]);
             	frm.set_value("employee_name",data[0][1]);

            }
        });
	}

	}
});
