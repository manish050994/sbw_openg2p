from odoo import _, fields, models
from odoo.exceptions import ValidationError


class G2PProgramMembership(models.Model):
    _inherit = 'g2p.program_membership'

    state = fields.Selection(
        selection=[
            ('draft', 'Application Received'),
            ('officer_assigned', 'Officer Assigned'),
            ('visit_office', 'Visit Office'),
            ('awaiting_site_visit', 'Awaiting Site Visit'),
            ('enrolled', 'Approved'),
            ('rejected', 'Rejected'),
        ],
            # ('preparing_funds', 'Preparing Funds'),
        default='draft',
        copy=False,
        string='Status',
    )

    visit_office_reason_ids = fields.Many2many(
        'g2p.visit.office.reason', 
        string="Visit Office Reasons"
    )

    def assign_to_officer(self):
        self.state = 'officer_assigned'

    def pending_office_visit(self):
        # Use only the reasons already set via the wizard
        if not self.visit_office_reason_ids:
            raise ValueError("No Visit Office reasons are set!")

        # Update state to 'visit_office' after setting reasons
        self.state = 'visit_office'

    def pending_site_visit(self):
        self.state = 'awaiting_site_visit'

    def prepare_funds(self):
        self.state = 'preparing_funds'

    def create_manual_inkind_entitlement(self):
        cycle = self.env['g2p.cycle'].search([('state','=','draft'),('program_id','=',self.program_id.id)],order='create_date desc',limit=1)
        if not cycle:
            raise ValidationError('No cycle found, create a cycle for this benefit!')
        cycle = cycle[0]
        return {
            "name": _("Create Entitlement"),
            "type": "ir.actions.act_window",
            "res_model": "g2p.manual.entitlement.inkind.wizard",
            "view_mode": "form",
            "view_type": "form",
            "context": {
                "default_cycle_id": cycle.id,
                "default_program_membership_id": self.id,
            },
            "target": "new",
        }

    def _compute_show_prepare_assessment(self):
        for rec in self:
            rec.show_prepare_assessment_button = True

    def _compute_show_create_entitlement(self):
        for rec in self:
            rec.show_create_entitlement_button = False

    def _compute_reject_application_assessment(self):
        for rec in self:
            if rec.state in ['officer_assigned','visit_office','awaiting_site_visit']:
                rec.show_reject_application_assessment_button = True
            else:
                rec.show_reject_application_assessment_button = False

    def reject_application_assessment(self):
        res = super().reject_application_assessment()
        self.state = 'rejected'
        return res
    
    