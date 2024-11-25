import frappe
from webshop.webshop.shopping_cart.product_info import set_product_info_for_website


@frappe.whitelist(allow_guest=True)
def get_products(start=0, limit=12):
	query = """
		SELECT
			item.item_name,
			bin.item_code,
			bin.actual_qty
		FROM
			`tabBin` AS bin
		JOIN `tabItem` AS item ON item.item_code = bin.item_code
		WHERE
			bin.actual_qty > 0
			AND bin.warehouse = 'Tienda - CL'
		ORDER BY
			item.creation ASC
		LIMIT {start}, {limit};
	""".format(start=start, limit=limit)

	items = frappe.db.sql(query, as_dict=True)

	for item in items:
		set_product_info_for_website(item)  # TODO: Optimize this. calling directly to get_price!

	return items

