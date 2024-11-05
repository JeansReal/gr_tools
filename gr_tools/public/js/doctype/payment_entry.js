// TODO: Work in Progress!
frappe.ui.form.on("Payment Entry", {

	setup(frm) {

		frappe.db.get_list('Mode of Payment', {
			filters: {'enabled': true}
		}).then((mode_of_payments) => {

			frappe.ui.form.make_control({
				parent: frm.fields_dict['mode_of_payment'].parent,
				df: {
					...frm.fields_dict['mode_of_payment'].df,
					...{
						fieldtype: 'MultiCheckSingle', columns: 3,
						options: mode_of_payments.map(c => c.name),
						on_change: (selected) => frm.set_value('mode_of_payment', selected)
					}
				},
				render_input: true,
			});

		});
	},

	posting_date(frm) {
		console.log('Posting Date of the Custom Script');

		frm.set_value('reference_date', frm.doc.posting_date); // Equal Values
	}

});
