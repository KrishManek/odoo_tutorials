from odoo import models, fields, api
from odoo.exceptions import UserError

BLOOD_GROUP = [('A+', 'A+ve'),
                ('B+', 'B+ve'),
                ('O+', 'O+ve'),
                ('AB+', 'AB+ve'),
                ('A-', 'A-ve'),
                ('B-', 'B-ve'),
                ('O-', 'O-ve'),
                ('AB-', 'AB-ve')]


class ResPatient(models.Model):
    _name = "res.patient"
    _description = "Patient"

    patient_code = fields.Char(string="Patient ID")
    name = fields.Char(string="Name", required=True)
    blood_group = fields.Selection(BLOOD_GROUP,
                                   string="Blood Group",  required=True)
    date_of_birth = fields.Date(string="Date of Birth", required=True)
    age = fields.Char(string="Age")
    previous_diseases = fields.Text(string="Previous Diseases")
    phone = fields.Char(string="Phone", copy=False)
    email = fields.Char(string="Email")
    mobile = fields.Char(string="Mobile", copy=False)
    appointment_count = fields.Integer(compute="_compute_appointment_count", string="Appointment Count", store=True)
    appointment_ids = fields.One2many("hms.appointment", "patient_id", string="Appointments", copy=False)

    def create_prescription(self):
        vals = {'patient_id': self.id,
                'date': fields.Datetime.now()}

        new_id = self.env['hms.prescription'].create(vals)
        new_id.state = 'confirm'

    @api.depends('appointment_ids.patient_id')
    def _compute_appointment_count(self):
        for patient in self:
            patient.appointment_count = self.env['hms.appointment'].search_count([('patient_id', '=', patient.id)])


    @api.model_create_multi
    def create(self, vals_list):
        res = super(ResPatient, self).create(vals_list)
        for record in res:
            record.patient_code = self.env['ir.sequence'].next_by_code('res.patient')
        return res

    def write(self, vals):
        res = super(ResPatient, self).write(vals)
        # if 'phone' in vals:
        #    if len(vals.get('phone')) < 10:
        #        raise UserError("Phone number should be minimum 10 digits")
        return res

    @api.constrains('phone')
    def check_phone(self):
        for record in self:
            if record.phone and len(record.phone) < 10:
                raise UserError("Phone number should be minimum 10 digits")

            # check no duplicate phone number
            if record.phone:
                patient_ids = self.env['res.patient'].search_count([('phone', '=', record.phone),('id', '!=', record.id)])
                if patient_ids:
                    raise UserError("Phone number already exists")

    def action_open_appointments(self):
        # action = self.env['ir.actions.actions']._for_xml_id('bista_hms.hms_appointment_form_action')
        # if self.appointment_count > 1:
        #     action['domain'] = [('patient_id', '=', self.id)]
        # elif self.appointment_count == 1:
        #     form_view = [(self.env.ref('bista_hms.hms_appointment_form_view').id, 'form')]
        #     if 'views' in action:
        #         action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
        #     else:
        #         action['views'] = form_view
        # else:
        #     action = {'type': 'ir.actions.act_window_close'}
        #
        # action['context'] = {'default_patient_id': self.id}
        # return action

        form_view_id = self.env.ref('bista_hms.hms_appointment_form_view').id
        list_view_id = self.env.ref('bista_hms.hms_appointment_tree_view').id

        res = {
            'name': 'Appointments',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'hms.appointment',
            'target': 'current',
            'view_id': form_view_id,
            'context': {'default_patient_id': self.id, 'child': True}
        }

        if self.appointment_count >= 1:
            res['view_mode'] = 'list,form'
            res['views'] = [(list_view_id, 'list'), (form_view_id, 'form')]
            res['domain'] = [('patient_id', '=', self.id)]
            res['view_id'] = False

        return res

    # def copy(self, default=None):
    #     if default is None:
    #         default = {}
    #     default['phone'] = False
    #     return super(ResPatient, self).copy(default)
    #

    def update_phone_to_null(self):
        active_ids = self._context.get('active_ids')
        patient_ids = self.env['res.patient'].browse(active_ids)
        patient_ids.write({'phone': False})
        # patient_ids.phone = False


    def action_prescription(self):
        form_view_id = self.env.ref('bista_hms.hms_prescription_form_view').id
        list_view_id = self.env.ref('bista_hms.hms_prescription_list_view').id

        res = {
            'name': 'Prescription',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'hms.prescription',
            'target': 'current',
            'view_id': form_view_id,
            'context': {'default_patient_id': self.id,}
        }

        res['view_mode'] = 'list,form'
        res['views'] = [(list_view_id, 'list'), (form_view_id, 'form')]
        res['domain'] = [('patient_id', '=', self.id)]
        res['view_id'] = False

        return res

