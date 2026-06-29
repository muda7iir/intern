from odoo import api, models, fields


class NxInternRoadmapDay(models.Model):
    _name = 'nx.intern.roadmap.day'
    _description = 'Internship Roadmap Day'
    _order = 'day_number'

    program_id = fields.Many2one(
        'nx.intern.program',
        string='Program',
        required=True,
        ondelete='cascade',
    )
    day_number = fields.Integer(
        string='Day Number',
        required=True,
    )
    title = fields.Char(
        string='Title',
        required=True,
    )
    learning_objectives = fields.Html(
        string='Learning Objectives',
    )
    instructions = fields.Html(
        string='Instructions',
    )
    deliverables = fields.Html(
        string='Deliverables',
    )
    estimated_hours = fields.Float(
        string='Estimated Hours',
    )
    difficulty = fields.Selection(
        [
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
        ],
        string='Difficulty',
        default='beginner',
    )
    attachment_ids = fields.Many2many(
        'ir.attachment',
        'nx_intern_roadmap_day_attachment_rel',
        'roadmap_day_id',
        'attachment_id',
        string='Attachments',
    )
    active = fields.Boolean(
        string='Active',
        default=True,
    )

    @api.depends('day_number', 'title')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f"Day {rec.day_number} - {rec.title}" if rec.day_number and rec.title else rec.title or ''
