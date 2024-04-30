// TODO: Work in Progress!
frappe.ui.form.on("Payment Entry", {

	onload(frm) {
		console.log('onload');

		frappe.db.get_list('Mode of Payment').then((results) => {

			let custom_control_df = Object.assign(frm.fields_dict['mode_of_payment'].df, {
				fieldtype: 'MultiCheckSingle', columns: 2, options: results.map(c => c.name),
				on_change: (selected) => frm.set_value('mode_of_payment', selected)
			});

			frappe.ui.form.make_control({
				parent: frm.fields_dict.mode_of_payment.$wrapper,
				df: custom_control_df,
				render_input: true,
			});

		});
	},

	posting_date(frm) {
		console.log('Posting Date of the Custom Script');

		frm.set_value('reference_date', frm.doc.posting_date); // Equal Values
	}

});
