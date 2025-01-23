import frappe
from erpnext.utilities.product import get_price


@frappe.whitelist(allow_guest=True)
def get_products(item_code: str = None, category: str = None, start: int = 0, limit: int = 15):
	"""
	Get a list of available products or a specific product by item_code. Includes filtering by category and its descendants.

	Parameters:
		item_code (str): If provided, fetches only the specific product.
		category (str): If provided, fetches products from the specific category and its child categories.
		start (int): Pagination start index.
		limit (int): Number of products to fetch.

	Returns:
		List of products or a single product.
	"""

	# TODO: Set a Default Warehouse, Maybe for each item?
	# FIXME: Dont Show Reserved Stock!
	# FIXME: Show BackOrder Products(For future sales or pre-orders)
	company = frappe.get_cached_value("Global Defaults", "Global Defaults", "default_company")
	price_list = frappe.get_cached_value('Selling Settings', 'Selling Settings', 'selling_price_list')
	default_warehouse = frappe.get_cached_value('Stock Settings', 'Stock Settings', 'default_warehouse')

	# Query for Available Items. FIXME: projected_qty = actual_qty - reserved_qty | Test: Planned | Requested | Ordered
	# actual_qty = All Items at Warehouse
	# reserved_qty = Sum of Items in Sales Orders(Not Draft) and Stock Reservation
	# projected_qty = actual_qty - reserved_qty
	# reserved_stock = Sum of Items in Stock Reservation
	query = """
		SELECT
			item.item_name,
			item.image,
			item.item_group,
			bin.item_code,
			(bin.actual_qty - bin.reserved_stock) as actual_qty
		FROM `tabBin` AS bin
		JOIN `tabItem` AS item ON item.item_code = bin.item_code
		WHERE (bin.actual_qty - bin.reserved_stock) > 0 AND bin.warehouse = '{warehouse}'
	""".format(warehouse=default_warehouse)

	if item_code:  # Filter by Item Code
		query += " AND item.item_code = %(item_code)s LIMIT 1"
		items = frappe.db.sql(query, {'item_code': item_code}, as_dict=True)
	else:  # Filter by category and its descendants
		if category:
			if categories := get_descendant_categories(category):
				query += " AND item.item_group IN %(categories)s"
			else:
				return []  # Bad Item Group

		# Add Pagination
		items = frappe.db.sql(query + " ORDER BY item.creation DESC LIMIT %(start)s, %(limit)s;", {
			"start": start, "limit": limit,
			"categories": categories if category else None
		}, as_dict=True)

	for item in items:
		item.price = get_price(item.item_code, price_list=price_list, customer_group='', company=company)

	return items


def get_descendant_categories(parent_category: str) -> list[str]:
	# Get all descendant categories
	descendant_groups = frappe.db.sql("""
		WITH RECURSIVE category_tree AS (
			SELECT name FROM `tabItem Group` WHERE name = %(category)s
			UNION ALL
			SELECT ig.name
			FROM `tabItem Group` ig
			INNER JOIN category_tree ct ON ig.parent_item_group = ct.name
		)
		SELECT name FROM category_tree;
		""", {"category": parent_category}, pluck='name')
	return descendant_groups


@frappe.whitelist(allow_guest=True)
def get_categories():
	# FIXME: UNUSED!
	data = frappe.db.get_all(
		'Item Group',
		fields=['name', 'is_group as isLeaf', 'parent_item_group', 'idx as counter'],
		filters={'show_in_website': 1}, order_by='is_group DESC'
	)

	# FIXME: What for? -> frappe.log_error(title="Debug: Data without Filters", message=data)

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
