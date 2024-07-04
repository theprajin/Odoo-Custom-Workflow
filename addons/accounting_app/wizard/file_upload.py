from odoo import api, fields, models


class FileUploadWizard(models.TransientModel):
    _name = "accounting_app.file.upload.wizard"
    _description = "File Upload Wizard"

    document = fields.Binary(
        string="Single Invoice"
    )  # don't forget to make it required later
    document_filename = fields.Char("Document Filename", store=True)

    def action_upload(self):
        AccountMove = self.env[
            "account.move"
        ]  # name variable like this when doing model reference

        # print(self._context.get("params").get("model"))

        # if self._context.get("params").get("model") != "account.move":
        #     return False

        AccountMove.action_invoice_from_json(invoice_file=self.document)

        return True
