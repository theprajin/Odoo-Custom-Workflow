from pathlib import Path
import os
import tempfile
import json
import requests
import base64

from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo import modules

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
    def action_invoice_from_json(self, invoice_file, filename):

        # data = json.loads(self.upload_json_to_api(invoice_file, filename=filename))
        data = self.upload_file_to_api(invoice_file, filename=filename)
        print(data)
        customer = data.get("customer")
        items = data.get("items", [])

        customer_with_email = self.env["res.partner"].search(
            [("email", "=", customer.get("email"))], limit=1
        )
        customer_with_name = self.env["res.partner"].search(
            [("name", "=", customer.get("name"))], limit=1
        )

        # if the customer has an email field not empty
        if customer_with_email.email:
            # Create account move (invoice)
            move = self.create_account_move(customer_partner=customer_with_email)

            # Create move lines (items)
            self.create_move_line_items(move=move, items=items)

            # create invoice address
            invoice = data.get("invoiceAddress")
            if invoice:
                invoice_address = self.create_child_address(
                    customer=customer_with_email,
                    address=invoice,
                    type=invoice.get("type"),
                )

            # create delivery address
            delivery = data.get("deliveryAddress")
            if delivery:
                delivery_address = self.create_child_address(
                    customer=customer_with_email,
                    address=delivery,
                    type=delivery.get("type"),
                )

            # create private address
            private = data.get("privateAddress")
            if private:
                private_address = self.create_child_address(
                    customer=customer_with_email,
                    address=private,
                    type=private.get("type"),
                )

            # create other address
            other = data.get("otherAddress")
            if other:
                other_address = self.create_child_address(
                    customer=customer_with_email,
                    address=other,
                    type=other.get("type"),
                )

            # create contact address
            contact = data.get("contact")
            if contact:
                contact_address = self.create_child_address(
                    customer=customer_with_email,
                    address=contact,
                    type=contact.get("type"),
                )

            return True
        elif (
            customer_with_name.name
        ):  # if customer has no email or customer with the email does not exist
            # Create account move (invoice)
            move = self.create_account_move(customer_partner=customer_with_name)

            # Create move lines (items)
            self.create_move_line_items(move=move, items=items)

            # create invoice address
            invoice = data.get("invoiceAddress")
            invoice_address = self.create_child_address(
                customer=customer_with_name,
                address=invoice,
                type=invoice.get("type"),
            )

            # create delivery address
            delivery = data.get("deliveryAddress")
            if delivery:
                delivery_address = self.create_child_address(
                    customer=customer_with_name,
                    address=delivery,
                    type=delivery.get("type"),
                )

            # create private address
            private = data.get("privateAddress")
            if private:
                private_address = self.create_child_address(
                    customer=customer_with_name,
                    address=private,
                    type=private.get("type"),
                )

            # create other address
            other = data.get("otherAddress")
            if other:
                other_address = self.create_child_address(
                    customer=customer_with_name,
                    address=other,
                    type=other.get("type"),
                )

            # create contact address
            contact = data.get("contact")
            if contact:
                contact_address = self.create_child_address(
                    customer=customer_with_name,
                    address=contact,
                    type=contact.get("type"),
                )

        else:
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
            if invoice:
                invoice_address = self.create_child_address(
                    customer=customer_partner,
                    address=invoice,
                    type=invoice.get("type"),
                )

            # create delivery address
            delivery = data.get("deliveryAddress")
            if delivery:
                delivery_address = self.create_child_address(
                    customer=customer_partner,
                    address=delivery,
                    type=delivery.get("type"),
                )

            # create private address
            private = data.get("privateAddress")
            if private:
                private_address = self.create_child_address(
                    customer=customer_partner,
                    address=private,
                    type=private.get("type"),
                )

            # create other address
            other = data.get("otherAddress")
            if other:
                other_address = self.create_child_address(
                    customer=customer_partner,
                    address=other,
                    type=other.get("type"),
                )

            # create contact address
            contact = data.get("contact")
            if contact:
                contact_address = self.create_child_address(
                    customer=customer_partner,
                    address=contact,
                    type=contact.get("type"),
                )

            # Create account move (invoice)
            move = self.create_account_move(customer_partner=customer_partner)

            # Create move lines (items)
            self.create_move_line_items(move=move, items=items)

    def create_child_address(self, customer, address, type="other"):
        child_add_with_email = self.env["res.partner"].search(
            [("email", "=", address.get("email")), ("parent_id", "=", customer.id)],
            limit=1,
        )

        # If no existing address is found, create a new one
        if not child_add_with_email.email:
            child_add_with_name = self.env["res.partner"].search(
                [("name", "=", address.get("name")), ("parent_id", "=", customer.id)],
                limit=1,
            )
            if not child_add_with_name.name:
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
            else:
                return child_add_with_name
        else:
            # If an address already exists, return the existing record
            return child_add_with_email

    # Sending JSON data to the API
    @api.model
    def upload_json_to_api(self, invoice_file, filename):
        # Decode the base64-encoded JSON string
        decoded_data = base64.b64decode(invoice_file)

        # For getting json reponse from own fastapi server
        try:
            url = "http://host.docker.internal:8000/json/upload"
            files = {"json_file": (filename, decoded_data, "application/octet-stream")}
            response = requests.post(url, files=files)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            return response.json()

        except requests.exceptions.RequestException as e:
            raise UserError(f"Error uploading JSON to API: {e}")

    # Sending file data to the API using temporary file
    @api.model
    def upload_file_to_api(self, invoice_file, filename):
        file_content = base64.b64decode(invoice_file)

        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(file_content)
            tmp_file_path = tmp_file.name

        try:
            url = "http://host.docker.internal:8000/file/upload"
            files = {
                "file": (filename, open(tmp_file_path, "rb"), "multipart/form-data")
            }

            response = requests.post(url, files=files)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            return response.json()

        except requests.exceptions.RequestException as e:
            raise UserError(f"Error uploading file to API: {e}")

        finally:
            # Ensure the temporary file is deleted after use
            os.remove(tmp_file_path)

    @api.model
    def create_customer_partner(self, customer, email):
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
        pass

    @api.model
    def create_account_move(self, customer_partner):
        # Create account move (invoice)
        move = self.env["account.move"].create(
            {
                "partner_id": customer_partner.id,
                "move_type": "out_invoice",  # or "in_invoice" for vendor bills
            }
        )

        return move

    @api.model
    def create_move_line_items(self, move, items):
        for item in items:

            for key, item_ref in item.items():
                # product_item = self.env["product.product"].search(
                #     [("name", "=", item_ref.get("name"))], limit=1
                # )

                # print(product_item)

                # if not product_item:
                product = self.env["product.product"].create(
                    {
                        "name": item_ref.get("description"),
                        "list_price": item_ref.get("unitPrice"),
                    }
                )

                # else:
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
