from odoo import api, models, fields, _
from odoo.exceptions import UserError


class NxInternEnrollment(models.Model):
    _name = 'nx.intern.enrollment'
    _description = 'Intern Enrollment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char(
        string='Reference',
        readonly=True,
        default='New',
        copy=False,
        help='Auto-generated enrollment reference.',
    )
    intern_name = fields.Char(
        string='Intern Name',
        required=True,
        tracking=True,
    )
    intern_email = fields.Char(
        string='Intern Email',
        tracking=True,
    )
    intern_user_id = fields.Many2one(
        'res.users',
        string='Intern User',
        tracking=True,
        help='Odoo user account linked to this intern.',
    )
    program_id = fields.Many2one(
        'nx.intern.program',
        string='Program',
        required=True,
        tracking=True,
    )
    joining_date = fields.Date(
        string='Joining Date',
        default=fields.Date.today,
        tracking=True,
    )
    manager_id = fields.Many2one(
        'res.users',
        string='Manager',
        tracking=True,
        help='Manager responsible for reviewing this intern.',
    )
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('running', 'Running'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
        ],
        string='Status',
        default='draft',
        tracking=True,
        required=True,
    )
    current_day = fields.Integer(
        string='Current Day',
        default=0,
        tracking=True,
    )
    progress_percentage = fields.Float(
        string='Progress (%)',
        compute='_compute_progress_percentage',
        store=True,
    )
    task_ids = fields.One2many(
        'nx.intern.daily.task',
        'enrollment_id',
        string='Daily Tasks',
    )
    task_count = fields.Integer(
        string='Tasks',
        compute='_compute_task_count',
    )
    mbti_type = fields.Char(
        string='MBTI Type',
        related='personality_id.mbti_type',
        store=True,
    )
    personality_id = fields.Many2one(
        'nx.intern.personality.report',
        string='Personality Report',
        tracking=True,
    )
    recommended_track = fields.Char(
        string='Recommended Track',
        tracking=True,
    )

    # ---- Computed -------------------------------------------------------

    @api.depends('task_ids', 'task_ids.state')
    def _compute_progress_percentage(self):
        for rec in self:
            total = len(rec.task_ids)
            if total:
                approved = len(rec.task_ids.filtered(lambda t: t.state == 'approved'))
                rec.progress_percentage = (approved / total) * 100.0
            else:
                rec.progress_percentage = 0.0

    def _compute_task_count(self):
        for rec in self:
            rec.task_count = len(rec.task_ids)

    # ---- CRUD -----------------------------------------------------------

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'nx.intern.enrollment'
                ) or 'New'
        return super().create(vals_list)

    # ---- Actions --------------------------------------------------------

    def action_start_internship(self):
        """Generate daily tasks from the program roadmap and start."""
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Internship can only be started from Draft state.'))
        if not self.program_id.roadmap_day_ids:
            raise UserError(
                _('The selected program has no roadmap days defined.')
            )

        roadmap_days = self.program_id.roadmap_day_ids.sorted('day_number')
        task_vals_list = []
        for idx, day in enumerate(roadmap_days):
            task_vals_list.append({
                'enrollment_id': self.id,
                'intern_user_id': self.intern_user_id.id if self.intern_user_id else False,
                'manager_id': self.manager_id.id if self.manager_id else False,
                'program_id': self.program_id.id,
                'day_number': day.day_number,
                'title': day.title,
                'instructions': day.instructions,
                'deliverables': day.deliverables,
                'deadline': (
                    fields.Date.add(self.joining_date, days=day.day_number - 1)
                    if self.joining_date
                    else False
                ),
                'state': 'pending' if idx == 0 else 'locked',
            })
        self.env['nx.intern.daily.task'].create(task_vals_list)
        self.write({'state': 'running', 'current_day': 1})

    def action_cancel(self):
        self.ensure_one()
        self.write({'state': 'cancelled'})

    def action_view_tasks(self):
        """Smart-button action to open related tasks."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Daily Tasks'),
            'res_model': 'nx.intern.daily.task',
            'view_mode': 'list,form,kanban',
            'domain': [('enrollment_id', '=', self.id)],
            'context': {'default_enrollment_id': self.id},
        }
