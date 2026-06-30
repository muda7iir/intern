from odoo import models, fields


class NxInternConfigSettings(models.TransientModel):
    _name = 'nx.intern.config.settings'
    _inherit = 'res.config.settings'
    _description = 'NerithonX Internship Configuration'

    # Default program for new enrollments
    default_program_id = fields.Many2one(
        'nx.intern.program',
        string='Default Training Program',
        default_model='nx.intern.enrollment',
        help='Default program assigned to new intern enrollments.',
    )

    # Counts for the settings dashboard
    intern_count = fields.Integer(
        string='Total Interns',
        compute='_compute_counts',
    )
    program_count = fields.Integer(
        string='Total Programs',
        compute='_compute_counts',
    )
    enrollment_count = fields.Integer(
        string='Active Enrollments',
        compute='_compute_counts',
    )
    personality_report_count = fields.Integer(
        string='MBTI Reports Generated',
        compute='_compute_counts',
    )

    def _compute_counts(self):
        for rec in self:
            rec.intern_count = self.env['res.users'].search_count([
                ('group_ids', 'in', [self.env.ref('nx_intern_training.group_intern_training_intern').id])
            ])
            rec.program_count = self.env['nx.intern.program'].search_count([])
            rec.enrollment_count = self.env['nx.intern.enrollment'].search_count([
                ('state', '=', 'running')
            ])
            rec.personality_report_count = self.env['nx.intern.personality.report'].search_count([])

    def action_open_intern_users(self):
        """Open a list of all users in the Intern group."""
        intern_group = self.env.ref('nx_intern_training.group_intern_training_intern')
        return {
            'name': 'Intern Users',
            'type': 'ir.actions.act_window',
            'res_model': 'res.users',
            'view_mode': 'list,form',
            'domain': [('group_ids', 'in', [intern_group.id])],
            'context': {'default_group_ids': [(4, intern_group.id)]},
        }

    def action_create_intern_user(self):
        """Open a form to create a new intern user with the correct groups pre-set."""
        intern_group = self.env.ref('nx_intern_training.group_intern_training_intern')
        return {
            'name': 'Create New Intern',
            'type': 'ir.actions.act_window',
            'res_model': 'res.users',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_group_ids': [(4, intern_group.id)],
            },
        }

    def action_open_programs(self):
        """Open the list of programs."""
        return {
            'name': 'Training Programs',
            'type': 'ir.actions.act_window',
            'res_model': 'nx.intern.program',
            'view_mode': 'list,form',
        }

    def action_open_enrollments(self):
        """Open the list of enrollments."""
        return {
            'name': 'Enrollments',
            'type': 'ir.actions.act_window',
            'res_model': 'nx.intern.enrollment',
            'view_mode': 'list,form',
        }

    def action_open_personality_reports(self):
        """Open the personality reports."""
        return {
            'name': 'Personality Reports',
            'type': 'ir.actions.act_window',
            'res_model': 'nx.intern.personality.report',
            'view_mode': 'list,form,graph,pivot',
        }
