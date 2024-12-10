from odoo import models, fields, http , api
import logging
import requests

_logger = logging.getLogger(__name__)

class InvoiceModel(models.Model):
    _name = 'invoice.model'
    _description = 'Invoice Model'

    id = fields.Char(string="ID", required=True)
    transaction_id=fields.Char(string="ID", required=True)
    vendor_id = fields.Char(string="Vendor ID")
    beneficiary_eid = fields.Char(string="Beneficiary EID")
    beneficiary_id = fields.Char(string="Beneficiary ID")
    business_name = fields.Char(string="Business Name")
    vendor_eid = fields.Char(string="Vendor EID")
    item_code = fields.Char(string="Item Code")
    item_category = fields.Char(string="Item Category")
    price = fields.Float(string="Price")
    program_id = fields.Char(string="Program ID")
    vendor_item_id = fields.Char(string="Vendor Item ID")
    vendor_image_id = fields.Char(string="Vendor Image ID")
    invoice_id = fields.Char(string="Invoice ID")
    beneficiary_image_id = fields.Char(string="Beneficiary Image ID")
    status = fields.Char( string="Status")
    created_date = fields.Datetime(string="Created Date")
    updated_date = fields.Datetime(string="Updated Date")
    redemption_status = fields.Char(string="Redemption Status", compute="_compute_redemption_status" , store=True)

    @api.depends('item_code', 'status')
    def _compute_redemption_status(self):
        for record in self:
            if record.status and record.item_code:  # Ensure both fields are set
                if record.status == '1':
                    record.redemption_status = 'Initiated'
                elif record.status == '2':
                    record.redemption_status = 'Redeemed'
                elif record.status == '3':
                    record.redemption_status = 'Delivered'
                else:
                    record.redemption_status = 'Unknown Status'
            else:
                record.redemption_status = 'Not Available'



   
    def action_view_doc_image(self):
        # API endpoint to view the document
        document_url = f"http://sbwdev.gov.tt/vendor/api/documents/redemption/view/{self.vendor_image_id}"
        
        # Optional: You can log the URL or handle API responses if needed
        _logger.info(f"Redirecting to document URL: {document_url}")

        # Return a window action to open the URL in a new tab
        return {
            'type': 'ir.actions.act_url',
            'url': document_url,
            'target': 'new',
        }


    def action_view_item_image(self):
        # API endpoint to view the document
        document_url = f"http://sbwdev.gov.tt/vendor/api/documents/redemption/view/{self.beneficiary_image_id}"
        
        # Optional: You can log the URL or handle API responses if needed
        _logger.info(f"Redirecting to document URL: {document_url}")

        # Return a window action to open the URL in a new tab
        return {
            'type': 'ir.actions.act_url',
            'url': document_url,
            'target': 'new',
        }

    def action_view_invoice(self):
        # API endpoint to view the document
        document_url = f"http://sbwdev.gov.tt/vendor/api/documents/redemption/view/{self.invoice_id}"
        
        # Optional: You can log the URL or handle API responses if needed
        _logger.info(f"Redirecting to document URL: {document_url}")

        # Return a window action to open the URL in a new tab
        return {
            'type': 'ir.actions.act_url',
            'url': document_url,
            'target': 'new',
        }
