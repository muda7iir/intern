from odoo import models, fields


class NxInternProgram(models.Model):
    _name = 'nx.intern.program'
    _description = 'Internship Training Program'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    name = fields.Char(
        string='Program Name',
        required=True,
        tracking=True,
        help='Name of the internship training program.',
    )
    code = fields.Char(
        string='Program Code',
        tracking=True,
        help='Short unique code for the program.',
    )
    duration_days = fields.Integer(
        string='Duration (Days)',
        tracking=True,
        help='Total number of days in this program.',
    )
    description = fields.Html(
        string='Description',
        help='Detailed description of the program.',
    )
    active = fields.Boolean(
        string='Active',
        default=True,
    )
    roadmap_day_ids = fields.One2many(
        'nx.intern.roadmap.day',
        'program_id',
        string='Roadmap Days',
        help='Day-by-day roadmap for this program.',
    )
    roadmap_day_count = fields.Integer(
        string='Roadmap Days',
        compute='_compute_roadmap_day_count',
    )

    def _compute_roadmap_day_count(self):
        for rec in self:
            rec.roadmap_day_count = len(rec.roadmap_day_ids)
