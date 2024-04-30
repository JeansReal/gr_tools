const purchase_invoice_onload = frappe.listview_settings['Purchase Invoice'].onload;

let extended = {
	hide_name_filter: true,
	onload: function(listview) {
		listview.page.sidebar.toggle(false);
		purchase_invoice_onload(listview);
	}
}

$.extend(frappe.listview_settings['Purchase Invoice'], extended);
