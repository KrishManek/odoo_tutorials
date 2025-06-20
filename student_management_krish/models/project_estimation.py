# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import ValidationError


class ProjectEstimation(models.Model):
    _name = 'project.estimation'
    _description = 'Project Estimation'
    _inherit = ["mail.thread", 'mail.activity.mixin']

    name = fields.Char(string='ID',readonly=True, default="New", copy=False, help="Id of project")
    customer_id = fields.Many2one('res.partner', string='Customer', required=True, help="Customer Name")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('cancelled', 'Cancelled')], string="Status", tracking=True, default='draft', help="Current State of project")
    validity_date = fields.Date(string='Validity', tracking=True, required=True, default=fields.Date.today(), help="Validity Date of the project")
    assignee_id = fields.Many2one('res.users', tracking=True, string='Assignee', help="Assigned User Id")
    project_description = fields.Text(string="Description", help="Description for the project")
    use_as_template = fields.Boolean(string="Use as Template", help="want to use this as a template")
    template_id = fields.Many2one('project.estimation', string="Template", domain="[('use_as_template', '=', True)]", help="previsouly used template id")
    total_amount = fields.Monetary(string="Total Estimated Amount",  currency_field="company_currency_id", compute="_compute_amount_total", store=True, help="Total amount of current project")
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company.id)
    company_currency_id = fields.Many2one(related="company_id.currency_id", string="Company Currency")
    project_estimation_lines = fields.One2many('project.estimation.line', 'project_id', tracking=True)

    dup_product = fields.Many2many('product.product', string="duplicate_products", compute="_duplicate_products")

    @api.model_create_multi
    def create(self,vals_list):
        """create method used to create record this method update assignee id to self and assign sequence
        Args:
            vals_list: 
        Returns:
            recordset with updated data
        """
        res = super(ProjectEstimation, self).create(vals_list)
        for rec in res:
            if not rec.assignee_id:
                rec.assignee_id = self.env.uid
            rec.name = self.env['ir.sequence'].next_by_code('project.estimation')
        return res

    @api.onchange('template_id')
    def on_change_template_id(self):
        """
        onchange method used to update fields based on paticular change in value of field, this method assigns customer name and project description from template
        """
        if self.template_id:
            self.customer_id = self.template_id.customer_id
            self.project_description = self.template_id.project_description
            
    @api.constrains('validity_date')
    def check_validity_date(self):
        """used to validate values, this method validates validity date which can't be less than today 

        Raises:
            ValidationError: Validty date Should atleast be today or later
        """
        for record in self:
            if record.validity_date < fields.Date.today():
                raise ValidationError(f"Validty date Should atleast be today or later i.e. {fields.Datetime.today()}")
    
    @api.constrains('project_estimation_lines')
    def check_project_estimation_lines(self):
        """Atleast on line is required to save project estimation

        Raises:
            ValidationError: Atleast one line should be present in estimation lines
        """
        for record in self:
            if len(record.project_estimation_lines)< 1:
                raise ValidationError(f"Atleast one line should be present in estimation lines")
    
        
    @api.depends('project_estimation_lines.sub_total')
    def _compute_amount_total(self):
        """
        compute method computes the value of paticular field based on changes in values in dependent field
        here it calulates total amount based on subtotal of all project estimation lines 
        """
        
        #pass
        for record in self:
            #record.total_amount = 0
            record.total_amount = sum(record.project_estimation_lines.mapped('sub_total'))
        
            
    def action_confirm(self):
        """
        used to update the state of project to confirmed only if it's in draft state
        """
        for rec in self:
            rec.ensure_one()
            if rec.state == 'draft':
                rec.state = 'confirm'
                
    def action_cancel(self):
        """
        used to update the state of project to cancelled only if it's in confirmed state
        """
        for rec in self:
            rec.ensure_one()
            if rec.state == 'confirm':
                rec.state = 'cancelled'
                
    @api.depends('project_estimation_lines.product_id')
    def _duplicate_products(self):
        for rec in self:
            if rec.project_estimation_lines:
                rec.dup_product = [(5, 0, 0)]
                products = (self.env['project.estimation.line'].search([('project_id', '=', self.id)]).mapped('product_id').ids)
                for product in products:
                    rec.dup_product = [(4 , product)]
            else:
                rec.dup_product = [(5, 0, 0)]

