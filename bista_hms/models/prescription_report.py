from odoo import models, api , fields


class ReportPrescription(models.AbstractModel):
    _name = 'report.bista_hms.prescription_template'

    def _get_report_values(self, docids, data=None):
        if data:
            pass

        prescription = self.env['hms.prescription'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': self.env['hms.prescription'],
            'data': data,
            'my_data': {'age': 25},
            'docs': prescription,
        }