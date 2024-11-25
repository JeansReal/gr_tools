import frappe
from webshop.webshop.shopping_cart.product_info import set_product_info_for_website


@frappe.whitelist(allow_guest=True)
def get_products(start=0, limit=15):
	query = """
		SELECT
			item.item_name,
			item.image,
			bin.item_code,
			bin.actual_qty
		FROM
			`tabBin` AS bin
		JOIN `tabItem` AS item ON item.item_code = bin.item_code
		WHERE
			bin.actual_qty > 0
			AND bin.warehouse = 'Tienda - CL'
		ORDER BY
			item.creation DESC
		LIMIT {start}, {limit};
	""".format(start=start, limit=limit)

	items = frappe.db.sql(query, as_dict=True)

	for item in items:
		set_product_info_for_website(item)  # TODO: Optimize this. calling directly to get_price!

	return items


@frappe.whitelist(allow_guest=True)
def get_categories():
	data = frappe.db.get_all(
		'Item Group',
		fields=['name', 'is_group as isLeaf', 'parent_item_group', 'idx as counter'],
		filters={'show_in_website': 1}, order_by='is_group DESC'
	)

	frappe.log_error(title="Debug: Data without Filters", message=data)

	# Diccionario para almacenar nodos y sus hijos
	nodes = {}
	tree = []

	# Crear nodos y asociarlos a sus padres
	for item in data:
		nodes[item['name']] = {"key": item['name'].upper().replace(" ", "_"),
			"value": {"label": item['name'], "counter": item['counter']}, "isLeaf": not item['isLeaf'],
			# `is_group` indica si no es hoja
			"children": []}

	# Asignar relaciones jerárquicas
	for item in data:
		node = nodes[item['name']]
		parent_name = item['parent_item_group']
		if parent_name and parent_name in nodes:
			nodes[parent_name]['children'].append(node)
		else:
			# Nodo raíz
			tree.append(node)

	return tree
