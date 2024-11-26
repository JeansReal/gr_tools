import frappe
from erpnext.utilities.product import get_price


@frappe.whitelist(allow_guest=True)
def get_products(item_code: str = None, start: int = 0, limit: int = 15):
	"""
	Get a list of available products or a specific product by item_code.
	Copy from: get_product_info_for_website

	Parameters:
		item_code (str): If provided, fetches only the specific product.
		start (int): Pagination start index.
		limit (int): Number of products to fetch.

	Returns:
		List of products or a single product.
	"""

	# TODO: Set a Default Warehouse, Maybe for each item?
	# FIXME: Dont Show Reserved Stock!
	# FIXME: Show BackOrder Products(For future sales or pre-orders)

	query = """
		SELECT
			item.item_name,
			item.image,
			item.item_group,
			bin.item_code,
			bin.actual_qty
		FROM `tabBin` AS bin
		JOIN `tabItem` AS item ON item.item_code = bin.item_code
		WHERE bin.actual_qty > 0 AND bin.warehouse = 'Tienda - CL'
	"""

	if item_code:
		query += " AND item.item_code = %(item_code)s LIMIT 1"
		items = frappe.db.sql(query, {'item_code': item_code}, as_dict=True)
	else:
		query += " ORDER BY item.creation DESC LIMIT %(start)s, %(limit)s;"
		items = frappe.db.sql(query, {"start": start, "limit": limit}, as_dict=True)

	[[price_list, company]] = frappe.db.get_values_from_single(['price_list', 'company'], None, 'WebShop Settings')

	for item in items:
		item.price = get_price(item.item_code, price_list=price_list, customer_group='', company=company)

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
