frappe.provide('frappe.ui.form');

// let d = new frappe.ui.Dialog({
// 	title: __('Payment Entry'),
// 	fields: [
// 		{
// 			label: "Mode Of Payment",
// 			fieldname: 'mode_of_payment',
// 			fieldtype: 'MultiCheckSingle',
// 			options: [{value: 'USD', label: 'USD'}, {value: 'EUR', label: 'EUR'}]
// 		}
// 	],
// 	primary_action(values) {
// 		console.log(values)
// 	}
// });


frappe.ui.form.PaymentEntryQuickEntryForm = class PaymentEntryQuickEntryForm extends frappe.ui.form.QuickEntryForm {
	constructor(doctype, after_insert, init_callback, doc, force) {
		super(doctype, after_insert, init_callback, doc, force);
	}
}
