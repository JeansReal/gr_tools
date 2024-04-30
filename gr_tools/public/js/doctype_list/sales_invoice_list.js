const sales_invoice_onload = frappe.listview_settings['Sales Invoice'].onload;

$.extend(frappe.listview_settings['Sales Invoice'], {
	hide_name_filter: true,
	onload: function(listview) {
		listview.page.sidebar.toggle(false);
		sales_invoice_onload(listview);
	}
});
