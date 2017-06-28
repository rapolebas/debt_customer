# -*- encoding:utf-8 -*-
from odoo import models, fields, api, tools
import datetime

import locale

locale.setlocale(locale.LC_ALL, 'en_US')


class PosOrderLineWizardReport(models.TransientModel):
    """Model for wizard report"""
    _name = 'debt_customer.customer_debt_report_wizard'
    _description = 'Estado de cuenta de usuarios'

    str_partner_id = fields.Char()
    partner_id = fields.Many2one('res.partner', 'Cliente')
    date_start = fields.Date('Fecha de inicio')#, required=True)
    date_end = fields.Date('Fecha de fin')#, required=True)



    @api.model
    def _get_data(self):


        res_partner_obj = self.env['res.partner']

        if self.partner_id:
            res_partner_ids = res_partner_obj.search([('id', '=', self.partner_id.id)])
            partner_name = res_partner_ids.name
        else:
            res_partner_ids = res_partner_obj.search([])
            partner_name = 'Todos'



        result = [
            {
            'partner_name': partner_name,
            'start': self.date_start,
            'end': self.date_end,
            }
        ]

        currency_obj = self.env['res.currency']
        currencys_ids = currency_obj.search([('active', '=', True)])


        for currency in currency_obj.browse(currencys_ids.ids):

            if self.partner_id:

                invoices_obj = self.env['account.invoice']
                invoices_ids = invoices_obj.search([
                    ('currency_id', '=', currency.id),
                    ('state', '=', 'open'),
                    ('partner_id', '=', self.partner_id.id),
                    ('date_invoice', '>=', self.date_start + ' 00:00:00'),
                    ('date_invoice', '<=', self.date_end + ' 23:59:59'),
                ], order='date_invoice')
            else:
                invoices_obj = self.env['account.invoice']
                invoices_ids = invoices_obj.search([
                    ('currency_id', '=', currency.id),
                    ('state', '=', 'open'),
                    ('date_invoice', '>=', self.date_start + ' 00:00:00'),
                    ('date_invoice', '<=', self.date_end + ' 23:59:59'),
                ], order='date_invoice')




            if invoices_ids:
                report_lines = []

                residual_total = 0.00
                monto_vencido_total = 0.00
                monto_30_total = 0.00
                monto_60_total = 0.00
                monto_90_total = 0.00
                monto_120_total = 0.00
                monto_150_total = 0.00
                monto_aplic_total = 0.00

                for invoice in invoices_ids:

                    residual_total += invoice.residual

                    monto_vencido = 0.00
                    monto_30 = 0.00
                    monto_60 = 0.00
                    monto_90 = 0.00
                    monto_120 = 0.00
                    monto_150 = 0.00
                    monto_aplic = 0.00
                    if invoice.date_due:
                        if (datetime.datetime.strptime(invoice.date_due,
                                                       "%Y-%m-%d")- datetime.datetime.now()).days < 0:
                            monto_vencido = invoice.residual
                            monto_vencido_total += monto_vencido

                        if (datetime.datetime.strptime(invoice.date_due,
                                                       "%Y-%m-%d") - datetime.datetime.now()).days > 0 and (
                                    datetime.datetime.strptime(invoice.date_due,
                                                        "%Y-%m-%d") - datetime.datetime.now()).days <= 30:
                            monto_30 = invoice.residual
                            monto_30_total += monto_30

                        if (datetime.datetime.strptime(invoice.date_due,
                                                        "%Y-%m-%d") - datetime.datetime.now()).days > 30 and (
                                datetime.datetime.strptime(invoice.date_due,
                                                        "%Y-%m-%d") - datetime.datetime.now()).days <= 60:
                            monto_60 = invoice.residual
                            monto_60_total += monto_60

                        if (datetime.datetime.strptime(invoice.date_due,
                                                       "%Y-%m-%d") - datetime.datetime.now()).days > 60 and (
                                    datetime.datetime.strptime(invoice.date_due,
                                                        "%Y-%m-%d") - datetime.datetime.now()).days <= 90:
                            monto_90 = invoice.residual
                            monto_90_total += monto_90

                        if (datetime.datetime.strptime(invoice.date_due,
                                                        "%Y-%m-%d") - datetime.datetime.now()).days > 90 and (
                                datetime.datetime.strptime(invoice.date_due,
                                                        "%Y-%m-%d") - datetime.datetime.now()).days <= 120:
                            monto_120 = invoice.residual
                            monto_120_total += monto_120

                        if (datetime.datetime.strptime(invoice.date_due,
                                                        "%Y-%m-%d") - datetime.datetime.now()).days > 120:
                            monto_150 = invoice.residual
                            monto_150_total += monto_150

                    else:
                        monto_vencido = invoice.residual
                        monto_vencido_total += monto_vencido







                    vals = {
                        'partner_ref':invoice.partner_id.ref,
                        'partner_name': invoice.partner_id.name,
                        'date': invoice.date_invoice,
                        'journal_name': invoice.journal_id.name,
                        'folio': invoice.number,
                        'folio_digital': invoice.number,
                        'date_due': invoice.date_due,
                        'currency_id' : invoice.currency_id.name,
                        'residual' : locale.currency(invoice.residual, grouping=True ),
                        'monto_vencido': locale.currency(monto_vencido, grouping=True ),
                        'monto_30': locale.currency(monto_30, grouping=True ),
                        'monto_60': locale.currency(monto_60, grouping=True ),
                        'monto_90': locale.currency(monto_90, grouping=True ),
                        'monto_120': locale.currency(monto_120, grouping=True ),
                        'monto_150': locale.currency(monto_150, grouping=True ),
                        'monto_aplic': locale.currency(monto_aplic, grouping=True ),
                    }
                    report_lines.append(vals)

                sorted_report_lines = sorted(report_lines, key=lambda invoice: invoice['date'])

                report_currency = {
                    'currency': currency.name,
                    'report_lines':sorted_report_lines,
                    'residual_total': locale.currency(residual_total, grouping=True ),
                    'monto_vencido_total': locale.currency(monto_vencido_total, grouping=True ),
                    'monto_30_total': locale.currency(monto_30_total, grouping=True ),
                    'monto_60_total': locale.currency(monto_60_total, grouping=True ),
                    'monto_90_total': locale.currency(monto_90_total, grouping=True ),
                    'monto_120_total': locale.currency(monto_120_total, grouping=True ),
                    'monto_150_total': locale.currency(monto_150_total, grouping=True ),
                    'monto_aplic_total': locale.currency(monto_aplic_total, grouping=True ),
                }
                result.append(report_currency)

        return result

    def _build_contexts(self):
        result = {}
        data = self._get_data()
        result['data'] = data

        return result

    def _print_report(self, data):

        return self.env['report'].get_action(self,'debt_customer.customer_debt_report', data=data)

    @api.multi
    def check_report(self):
        self.ensure_one()
        datas = {}
        values = self._build_contexts()

        datas['dates'] = values.get('data').pop(0)
        datas['form'] = values.get('data')

        return self._print_report(datas)




