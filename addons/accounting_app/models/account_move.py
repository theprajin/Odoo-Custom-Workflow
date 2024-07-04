import json
from odoo import models, fields, api
from odoo.exceptions import UserError

from ..utils.json_reader import from_json_file


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.model
    def create_documents_from_json(self, json_data):
        try:
            data = json.loads(json_data)
            attachment_ids = []
            for record in data:
                att_data = {
                    "name": record.get("name"),
                    "mimetype": record.get("mimetype"),
                    "datas": record.get("datas"),
                }
                att_id = self.env["ir.attachment"].create(att_data)
                attachment_ids.append(att_id.id)
            action = self.create_document_from_attachment("", attachment_ids)
            return action
        except json.JSONDecodeError:
            raise UserError("Invalid JSON data")

    @api.model
    def action_invoice_from_json(self, invoice_file):
        data = from_json_file()
        customer = data.get("customer")
        customer_partner = self.env["res.partner"].create(
            {
                "name": customer.get("name"),
                "phone": customer.get("phone"),
                "mobile": customer.get("mobile"),
                "email": customer.get("email"),
                "website": customer.get("website"),
                "title": customer.get("title"),
                "street": customer.get("street"),
                "city": customer.get("city"),
                "country_id": self.env["res.country"]
                .search([("name", "=", customer.get("country"))], limit=1)
                .id,
            }
        )

        # create invoice address
        invoice = data.get("invoiceAddress")
        invoice_address = self.create_child_address(
            data=data,
            customer=customer_partner,
            address=invoice,
            type=invoice.get("type"),
        )

        # create delivery address
        delivery = data.get("deliveryAddress")
        delivery_address = self.create_child_address(
            data=data,
            customer=customer_partner,
            address=delivery,
            type=delivery.get("type"),
        )

        # create private address
        private = data.get("privateAddress")
        private_address = self.create_child_address(
            data=data,
            customer=customer_partner,
            address=private,
            type=private.get("type"),
        )

        # create other address
        other = data.get("otherAddress")
        other_address = self.create_child_address(
            data=data,
            customer=customer_partner,
            address=other,
            type=other.get("type"),
        )

        # create contact address
        contact = data.get("contact")
        contact_address = self.create_child_address(
            data=data,
            customer=customer_partner,
            address=contact,
            type=contact.get("type"),
        )

        # Create account move (invoice)
        move = self.env["account.move"].create(
            {
                "partner_id": customer_partner.id,
                "move_type": "out_invoice",  # or 'in_invoice' for vendor bills
            }
        )

        items = data.get("items", [])
        for item in items:

            for key, item_ref in item.items():
                price_unit = item_ref.get("unitPrice")
                print(f"price_unit: {price_unit}")
                product = self.env["product.product"].create(
                    {
                        "name": item_ref.get("description"),
                    }
                )
                product._get_tax_included_unit_price(
                    company=move.company_id,
                    currency=move.currency_id,
                    document_date=move.date,
                    document_type="purchase",
                    product_price_unit=price_unit,
                )
                self.env["account.move.line"].create(
                    {
                        "move_id": move.id,
                        "name": item_ref.get("description"),
                        "product_id": product.id,
                        "quantity": item_ref.get("quantity"),
                        "discount": item_ref.get("discount"),
                        "price_unit": item_ref.get("unitPrice"),
                    }
                )
        print(items)
        print(invoice_address)

    def create_child_address(self, data, customer, address, type="other"):
        child_address = self.env["res.partner"].create(
            {
                "name": address.get("name"),
                "phone": address.get("phone"),
                "mobile": address.get("mobile"),
                "email": address.get("email"),
                "website": address.get("website"),
                "title": address.get("title"),
                "street": address.get("street"),
                "street2": address.get("street2"),
                "city": address.get("city"),
                "zip": address.get("zip"),
                "country_id": self.env["res.country"]
                .search([("name", "=", address.get("country"))], limit=1)
                .id,
                "parent_id": customer.id,
                "type": type,
            }
        )

        return child_address
