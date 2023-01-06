# -*- coding: utf-8 -*-
from odoo import fields, models

ACCOUNT_DOMAIN = "['&', '&', '&', ('deprecated', '=', False), ('internal_type','=','other'), ('company_id', '=', current_company_id), ('is_off_balance', '=', True)]"


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    pos_invoice_type = fields.Selection(
        string='Invoice Type',
        related='company_id.pos_invoice_type',
        readonly=False,
        help="")

    create_out_refund_as_payment = fields.Boolean(
        string='Create credit note as payment',
        related='company_id.create_out_refund_as_payment',
        readonly=False,
        help="If marked, the multi pos order invoice will be paid with a new credit note.")

    l10n_mx_edi_periodicity = fields.Selection([
            ('01', 'Daily'),
            ('02', 'Weekly'),
            ('03', 'Fortnight'),
            ('04', 'Monthly'),
            ('05', 'Bimonthly'),
        ],
        string='Periodicity',
        related='company_id.l10n_mx_edi_periodicity',
        required=True,
        readonly=False,
        help="Used on every global invoice on Global Information Node.")
    
        # CUENTAS PUENTE
    use_bridge_accounts = fields.Boolean(
        string='Use Bridge Accounts',
        related='company_id.use_bridge_accounts',
        readonly=False,
        help="If marked, the journal items of the global invoice will be create with the following bridge accounts instead the default invoice accounts.")
    
    # Cuenta de ingresos
    bridge_income_account_id = fields.Many2one(
        'account.account',
        string="Income Account",
        related='company_id.bridge_income_account_id',
        readonly=False,
        domain=ACCOUNT_DOMAIN,
        help=".")

    # Cuenta de gastos
    bridge_expense_account_id = fields.Many2one(
        'account.account',
        string="Expense Account",
        related='company_id.bridge_expense_account_id',
        readonly=False,
        domain=ACCOUNT_DOMAIN,
        help=".")