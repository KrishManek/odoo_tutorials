from odoo import models, fields,api
from odoo.exceptions import UserError, ValidationError
import xlsxwriter
import io
import base64

class ManufacturingOrder(models.TransientModel):
    _name = 'manufacturing.wizard'
    _description = 'Manufacturing Report Wizard'
    
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    
    excel_file = fields.Binary("Download Excel file", filename="Manufacturing Report", readonly=True)
    filename = fields.Char('Excel File', size=64)

    @api.constrains('end_date')
    def _validate_end_date(self):
        if self.end_date <= self.start_date:
            raise UserError("End Date should be Greater than Start Date: ")
    
    def download_report(self):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Manufacturing Orders')
        row = 3

        merge_format = workbook.add_format({
            'bold': 1,
            'border': 1,
            'bg_color': "#D3D3D3",
            'align': 'center',
            'valign': 'vcenter',
        })

        content_format = workbook.add_format({
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
        })

        """ worksheet.set_column('A:A', 7)
        worksheet.set_column('B:B', 15)
        worksheet.set_column('C:C', 25)
        worksheet.set_column('D:D', 15)
        worksheet.set_column('E:E', 25)
        worksheet.set_column('F:F', 20)
        worksheet.set_column('G:G', 25) """

        worksheet.merge_range('A1:G2', 'Manufacturing Report', merge_format)

        worksheet.write(row, 0, 'MO No', merge_format)
        worksheet.write(row, 1, 'Product', merge_format)
        worksheet.write(row, 2, 'Quantity', merge_format)
        worksheet.write(row, 3, 'Bill of Material', merge_format)
        worksheet.write(row, 4, 'Scheduled Date', merge_format)
        worksheet.write(row, 5, 'Component Status', merge_format)
        worksheet.write(row, 6, 'Responsible', merge_format)

        row += 1
        mo_no = 1

        mo_records = self.env['mrp.production'].search([('date_start', '>=', self.start_date),
                                                        ('date_start','<=', self.end_date)])

        for record in mo_records:
            worksheet.write(row, 0, mo_no, content_format)
            worksheet.write(row, 1, record.product_id.display_name or '', content_format)
            worksheet.write(row, 2, record.product_qty or 0.0, content_format)
            worksheet.write(row, 3, record.bom_id.display_name or '', content_format)
            worksheet.write(row, 4, str(record.date_start or ''), content_format)
            worksheet.write(row, 5, record.components_availability or '', content_format)
            worksheet.write(row, 6, record.user_id.name or '', content_format)

            mo_no += 1
            row += 1

        workbook.close()
        output.seek(0)

        file_data = base64.b64encode(output.read())
        file_name = 'demoReport.xlsx'
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
        
        """ manufacturing_data = self.env['mrp.production'].search([('date_start', '>=', self.start_date), ('date_start', '<=', self.end_date)])
        
        headers = ['ID', 'Product']
        no_of_headers = len(headers)
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Sheet 1')

        row = 1
        col = 0
        
        header_format = workbook.add_format({'bold': True, 'font_size': 16, 'align': 'center', 'valign': 'vcenter', 'border': 1})
        sub_header_format = workbook.add_format({'bold': True, 'font_size': 14, 'align': 'center', 'valign': 'vcenter', 'border': 1})
        data_format = workbook.add_format({'font_size': 12, 'align': 'center', 'valign': 'vcenter', 'border': 1})
        worksheet.merge_range(0, 0, no_of_headers, 0, 'Merged Range', header_format)
        worksheet.write(0, 0, "Manufacturing Report")
        worksheet.write_row(1, 0, headers)
        for item, val in (data):
            worksheet.write(row, col, item)
            worksheet.write(row, col + 1, val)
            row += 1

        workbook.close()
        output.seek(0)

        file_data = base64.b64encode(output.read())
        file_name = 'ManuFaturing_Report.xlsx'
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
     """