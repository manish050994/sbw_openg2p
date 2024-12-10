from odoo import models, fields, api

class G2PVisitOfficeReason(models.Model):
    _name = 'g2p.visit.office.reason'
    _description = 'Visit Office Reason'

    name = fields.Char("Reason", required=True)

class VisitOfficeWizard(models.TransientModel):
    _name = 'visit.office.wizard'
    _description = 'Visit Office Wizard'
    visit_office_reason_ids = fields.Many2many(
        'g2p.visit.office.reason', 
        string="Visit Office Reasons", 
        required=True
    )

    def confirm_visit_office(self):
        active_id = self.env.context.get('active_id')
        if not active_id:
            return

        # Update selected reasons in the related program membership record
        record = self.env['g2p.program_membership'].browse(active_id)
        if record:
            record.visit_office_reason_ids = [(6, 0, self.visit_office_reason_ids.ids)]
            record.pending_office_visit()  # Transition to 'visit_office' state
