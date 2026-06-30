from odoo import models, fields, api

class ResUsers(models.Model):
    _inherit = 'res.users'

    personality_report_ids = fields.One2many(
        'nx.intern.personality.report',
        'user_id',
        string='Personality Reports',
    )
    mbti_completed = fields.Boolean(
        string='MBTI Onboarding Completed',
        compute='_compute_mbti_completed',
        store=True,
    )

    @api.depends('personality_report_ids')
    def _compute_mbti_completed(self):
        for user in self:
            user.mbti_completed = bool(user.personality_report_ids)
