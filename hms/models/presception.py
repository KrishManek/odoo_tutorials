from odoo import models, fields, api


class HmsPrescription(models.Model):
    _name = "hms.prescription"
    _description = "Prescription"
    _res_name = "patient_id.name"

    patient_id = fields.Many2one('patient.details', string="Patient", required=True)
    date = fields.Date(string="Date", default=fields.Date.today, required=True)
    state = fields.Selection([('draft', 'Draft'),
                              ('confirmed', 'Confirmed'),
                              ('canceled', 'Canceled')], string="Status", default='draft', required=True )
    prescription_lines = fields.One2many('hms.prescription.line', 'prescription_id', string="Prescription Lines")
    prescription_count = fields.Integer(compute="_compute_prescription_count", string="Prescription Count", store=True)
    total = fields.Integer(string='Total',compute="_compute_prescription_total", store=True)

    @api.depends('prescription_lines.sub_total')
    def _compute_prescription_total(self):
        for rec in self:
            rec.total = sum(rec.prescription_lines.mapped('sub_total'))
    
    @api.depends('prescription_lines')
    def _compute_prescription_count(self):
        for patient in self:
            patient.total = self.env['hms.prescription.line'].search_count([('prescription_id','=', patient.id)])


    def action_confirm_prescription(self):
        self.state = 'confirmed'
        
    def action_cancel_prescription(self):
        self.state = 'canceled'

    def action_open_prescriptions(self):
        form_view_id = self.env.ref('hms.view_hms_prescription_line_form').id
        list_view_id = self.env.ref('hms.view_hms_prescription_line_list').id
        
        res = {
            'name' : 'Prescriptions',
            'type' : 'ir.actions.act_window',
            'view_mode' : 'form',
            'res_model' : 'hms.prescription.line',
            'view_id' : form_view_id,
            'target' : 'current',
            'context' : {'default_patient_id' : self.id }
        }
        if self.prescription_count >= 1:
            res['view_mode'] = 'list,form'
            res['views'] = [(list_view_id,'list'),(form_view_id,'form')]
            res['domain'] = [('prescription_id', '=', self.id)]
            res['view_id'] = False
        return res
