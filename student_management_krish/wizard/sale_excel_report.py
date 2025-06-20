# -*- coding: utf-8 -*-

from odoo import models, fields,api
from odoo.exceptions import UserError
import xlsxwriter
import io
import base64


class SalesReportWizard(models.TransientModel):
    _name = 'sale.report.wizard'
    _description = 'Sale Report Wizard'

    customer_id = fields.Many2one('res.partner',string="Customer")
    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)
    
    excel_file = fields.Binary("Download Excel file", filename="Sales Excel Report.xlsx", readonly=True)
    filename = fields.Char('Excel File', size=64)

    @api.constrains('end_date')
    def _validate_end_date(self):
        if self.end_date <= self.start_date:
            raise UserError("End Date should be Greater than Start Date: ")
    
    def download_report(self):
        """code for downloading excel report

        Returns:
            excel report save 
        """
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Sale Orders')
        row = 2
        
        worksheet.write(0, 0, 'Start Date')
        worksheet.write(0, 1, str(self.start_date))
        worksheet.write(1, 0, 'End Date')
        worksheet.write(1, 1, str(self.end_date))
        
        worksheet.write(row, 0, 'No')
        worksheet.write(row, 1, 'Order No')
        worksheet.write(row, 2, 'Order Date')
        worksheet.write(row, 3, 'Customer')
        worksheet.write(row, 4, 'Sales Person')
        worksheet.write(row, 5, 'No of Lines')
        worksheet.write(row, 6, 'Total Amount ')

        row += 1
        mo_no = 1
        start_date = self.start_date.strftime("%Y-%m-%d %H:%M:%S")
        end_date = self.end_date.strftime("%Y-%m-%d %H:%M:%S")
        if not self.customer_id:
            so_records = self.env['sale.order'].search([('date_order', '>=', start_date),
                                                        ('date_order','<=', end_date)])
        else:
            so_records = self.env['sale.order'].search([('partner_id', '=', self.customer_id.id),
                                                        ('date_order', '>=', start_date),
                                                        ('date_order','<=', end_date)])

        for record in so_records:
            total_lines = len(record.order_line)
            worksheet.write(row, 0, mo_no)
            worksheet.write(row, 1, record.name or '')
            worksheet.write(row, 2, str(record.date_order or ''))
            worksheet.write(row, 3, record.partner_id.name or 0.0)
            worksheet.write(row, 4, record.user_id.name or '')
            worksheet.write(row, 5, total_lines or '')
            worksheet.write(row, 6, record.amount_total or '')

            mo_no += 1
            row += 1

        workbook.close()
        output.seek(0)

        file_data = base64.b64encode(output.read())
        file_name = 'Sales Excel Report.xlsx'
        attachment = self.env['ir.attachment'].create({
            'name': file_name,
            'type': 'binary',
            'datas': file_data,
            'res_model': self._name,
            'res_id': self.id,
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        })

        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'new',
        }