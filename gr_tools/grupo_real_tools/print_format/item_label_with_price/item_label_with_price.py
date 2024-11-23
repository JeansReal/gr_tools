import frappe
from erpnext.utilities.product import get_price


@frappe.whitelist(allow_guest=False, methods='GET')
def get_erpnext_price(item_code):
	# This function is used to get the price of an item with the Pricing Rule Applied if available

	# TODO: Webshop Price List
	# TODO: Customer Price List?
	selling_price_list = frappe.db.get_single_value('Selling Settings', 'selling_price_list')
	default_company = frappe.defaults.get_user_default('Company')  # FIXME: This can be improved

	pricing = get_price(item_code, price_list=selling_price_list, customer_group='', company=default_company)

	pricing.formatted_discount_percent = f"{pricing.discount_percent:.0f}%"

	return pricing
