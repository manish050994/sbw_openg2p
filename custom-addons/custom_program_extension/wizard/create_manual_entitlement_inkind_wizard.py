# Part of OpenG2P Registry. See LICENSE file for full copyright and licensing details.
import logging

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class G2PManualEntitlementInKindWizard(models.TransientModel):
    _name = "g2p.manual.entitlement.inkind.wizard"
    _description = "Manual In-Kind Entitlement Wizard"

    @api.model
    def _default_warehouse_id(self):
        return self.env["stock.warehouse"].search([("company_id", "=", self.env.company.id)], limit=1)

    products_item_ids = fields.One2many(
        "g2p.manual.entitlement.inkind.item.wizard", "inkind_ent_id", required=True
    )

    cycle_id = fields.Many2one("g2p.cycle")

    program_membership_id = fields.Many2one(
        "g2p.program_membership"
    )

    evaluate_single_item = fields.Boolean("Evaluate one item", default=False)

    manage_inventory = fields.Boolean(default=False)
    warehouse_id = fields.Many2one(
        "stock.warehouse",
        string="Warehouse",
        required=True,
        default=_default_warehouse_id,
        check_company=True,
    )
    company_id = fields.Many2one("res.company", string="Company", default=lambda self: self.env.company)

    def create_entitlement(self):
        entitlement = self.prepare_entitlements(self.cycle_id, self.program_membership_id)
        if entitlement:
            kind = "success"
            message = _("Entitlements are created successfully.")
        else:
            kind = "danger"
            message = _("Duplicate entitlements detected for these beneficiaries.")
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("Entitlement"),
                "message": message,
                "sticky": True,
                "type": kind,
                "next": {
                    "type": "ir.actions.act_window_close",
                },
            },
        }

    def prepare_entitlements(self, cycle, beneficiary):
        partner = beneficiary.partner_id
        entitlement_start_validity = cycle.start_date
        entitlement_end_validity = cycle.end_date
        entitlements = []
        for rec in self.products_item_ids:
            multiplier = 1
            if rec.multiplier_field:
                # Get the multiplier value from multiplier_field else return the default multiplier=1
                multiplier = partner.mapped(rec.multiplier_field.name)
                if multiplier:
                    multiplier = multiplier[0] or 1
            if rec.max_multiplier > 0 and multiplier > rec.max_multiplier:
                multiplier = rec.max_multiplier
            qty = multiplier * rec.qty

            entitlement_fields = {
                "cycle_id": cycle.id,
                "partner_id": partner.id,
                "total_amount": rec.product_id.list_price * qty,
                "product_id": rec.product_id.id,
                "qty": qty,
                "unit_price": rec.product_id.list_price,
                "uom_id": rec.uom_id.id,
                "manage_inventory": self.manage_inventory,
                "warehouse_id": self.warehouse_id and self.warehouse_id.id or None,
                "state": "draft",
                "valid_from": entitlement_start_validity,
                "valid_until": entitlement_end_validity,
            }
            entitlements.append(entitlement_fields)

        if entitlements:
            self.env["g2p.entitlement.inkind"].sudo().create(entitlements)
            return True
        return None


class G2PManualEntitlementInKindItemWizard(models.TransientModel):
    _name = "g2p.manual.entitlement.inkind.item.wizard"
    _description = "Manual In-Kind Entitlement Item Wizard"

    inkind_ent_id = fields.Many2one("g2p.manual.entitlement.inkind.wizard", "New Program", required=True)

    product_id = fields.Many2one(
        "product.product", "Product", domain=[("type", "=", "product")], required=True
    )

    condition = fields.Char("Condition Domain")
    multiplier_field = fields.Many2one(
        "ir.model.fields",
        "Multiplier",
        domain=[("model_id.model", "=", "res.partner"), ("ttype", "=", "integer")],
    )
    max_multiplier = fields.Integer(
        default=0,
        string="Maximum number",
        help="0 means no limit",
    )

    qty = fields.Integer("QTY", default=1, required=True)
    uom_id = fields.Many2one("uom.uom", "Unit of Measure", related="product_id.uom_id")