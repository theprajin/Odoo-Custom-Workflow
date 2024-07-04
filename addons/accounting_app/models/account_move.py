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
        print(from_json_file())
