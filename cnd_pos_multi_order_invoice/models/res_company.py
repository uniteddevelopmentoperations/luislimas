# -*- coding: utf-8 -*-
from odoo import models, fields

ACCOUNT_DOMAIN = "['&', '&', '&', ('deprecated', '=', False), ('internal_type','=','other'), ('company_id', '=', current_company_id), ('is_off_balance', '=', True)]"


class ResCompany(models.Model):
    _inherit = 'res.company'

    pos_invoice_type = fields.Selection(
        [('single', 'Single'), ('mass', 'Mass')],
        string='Invoice Type',
        default='mass',
        help="Select \"Mass\" for create one invoice of several POS orders, select \"Single\" for create one invoice for each POS order.")

    create_out_refund_as_payment = fields.Boolean(
        string='Create credit note as payment',
        default=True,
        help="If marked, the multi pos order invoice will be paid with a new credit note.")

    l10n_mx_edi_periodicity = fields.Selection([
        ('01', 'Daily'),
        ('02', 'Weekly'),
        ('03', 'Fortnight'),
        ('04', 'Monthly'),
        ('05', 'Bimonthly'),
    ],
        string='Periodicity',
        default='04',
        required=True,
        help="Used on every global invoice on Global Information Node.")
    # CUENTAS PUENTE
    use_bridge_accounts = fields.Boolean(
        string='Use Bridge Accounts',
        default=False,
        help="If marked, the journal items of the global invoice will be create with the following bridge accounts instead the default invoice accounts.")
    
    # Cuenta de ingresos
    bridge_income_account_id = fields.Many2one(
        'account.account',
        string="Income Account",
        domain=ACCOUNT_DOMAIN,
        help=".")

    # Cuenta de gastos
    bridge_expense_account_id = fields.Many2one(
        'account.account',
        string="Expense Account",
        domain=ACCOUNT_DOMAIN,
        help=".")