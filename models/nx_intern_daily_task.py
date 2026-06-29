from odoo import api, models, fields


class NxInternDailyTask(models.Model):
    _name = 'nx.intern.daily.task'
    _description = 'Intern Daily Task'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'day_number'

    enrollment_id = fields.Many2one(
        'nx.intern.enrollment',
        string='Enrollment',
        required=True,
        ondelete='cascade',
    )
    intern_user_id = fields.Many2one(
        'res.users',
        string='Intern',
        tracking=True,
    )
    manager_id = fields.Many2one(
        'res.users',
        string='Manager',
        tracking=True,
    )
    program_id = fields.Many2one(
        'nx.intern.program',
        string='Program',
        tracking=True,
    )
    day_number = fields.Integer(
        string='Day Number',
        tracking=True,
    )
    title = fields.Char(
        string='Task Title',
        required=True,
    )
    instructions = fields.Html(
        string='Instructions',
    )
    deliverables = fields.Html(
        string='Deliverables',
    )
    deadline = fields.Date(
        string='Deadline',
    )
    state = fields.Selection(
        [
            ('locked', 'Locked'),
            ('pending', 'Pending'),
            ('submitted', 'Submitted'),
            ('revision_required', 'Revision Required'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        string='Status',
        default='locked',
        tracking=True,
        required=True,
    )
    submission_ids = fields.One2many(
        'nx.intern.submission',
        'task_id',
        string='Submissions',
    )
    submission_count = fields.Integer(
        string='Submissions',
        compute='_compute_submission_count',
    )

    def _compute_submission_count(self):
        for rec in self:
            rec.submission_count = len(rec.submission_ids)

    @api.depends('day_number', 'title')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = (
                f"Day {rec.day_number} - {rec.title}"
                if rec.day_number and rec.title
                else rec.title or ''
            )
