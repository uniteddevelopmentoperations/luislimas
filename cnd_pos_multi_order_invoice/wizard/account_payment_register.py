# -*- coding: utf-8 -*-
from odoo import models, api, _
from odoo.exceptions import UserError


class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    @api.model 
    def default_get(self, fields_list):
        # OVERRIDE
        print("EntrAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        print('fields_list: ', fields_list)

        if self._context.get('active_model') == 'account.move':
            lines = self.env['account.move'].browse(self._context.get('active_ids', [])).line_ids
        elif self._context.get('active_model') == 'account.move.line':
            lines = self.env['account.move.line'].browse(self._context.get('active_ids', []))

        # Publicar la factura por defecto
        use_bridge_accounts = lines[0].company_id.use_bridge_accounts
        if use_bridge_accounts:
            lines[0].company_id.bridge_income_account_id.write(
                {'user_type_id': lines[0].env.ref('account.data_account_type_revenue').id, 'reconcile': True})
            lines[0].company_id.bridge_expense_account_id.write(
                {'user_type_id': lines[0].env.ref('account.data_account_type_receivable').id, 'reconcile': True})

        res = super().default_get(fields_list)

        if use_bridge_accounts:
            pass
            # lines[0].company_id.bridge_income_account_id.write(
            #     {'user_type_id': lines[0].env.ref('account.data_account_off_sheet').id, 'reconcile': False})
            # lines[0].company_id.bridge_expense_account_id.write(
            #     {'user_type_id': lines[0].env.ref('account.data_account_off_sheet').id, 'reconcile': False})

        return res


    def action_create_payments(self):
        action = super().action_create_payments()

        use_bridge_accounts = self.journal_id.company_id.use_bridge_accounts
        if use_bridge_accounts:
            self.journal_id.company_id.bridge_income_account_id.write(
                {'user_type_id': self.journal_id.env.ref('account.data_account_off_sheet').id, 'reconcile': False})
            self.journal_id.company_id.bridge_expense_account_id.write(
                {'user_type_id': self.journal_id.env.ref('account.data_account_off_sheet').id, 'reconcile': False})
        return action

    # def action_create_payments(self):
    #     payments = self._create_payments()

    #     if self._context.get('dont_redirect_to_payments'):
    #         return True

    #     action = {
    #         'name': _('Payments'),
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'account.payment',
    #         'context': {'create': False},
    #     }
    #     if len(payments) == 1:
    #         action.update({
    #             'view_mode': 'form',
    #             'res_id': payments.id,
    #         })
    #     else:
    #         action.update({
    #             'view_mode': 'tree,form',
    #             'domain': [('id', 'in', payments.ids)],
    #         })
    #     return action

