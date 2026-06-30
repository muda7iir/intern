import json
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class NxInternMbtiWizard(models.TransientModel):
    _name = 'nx.intern.mbti.wizard'
    _description = 'MBTI Personality Onboarding Wizard'

    user_id = fields.Many2one(
        'res.users',
        string='User',
        required=True,
        default=lambda self: self.env.user,
    )
    mbti_type = fields.Char(
        string='MBTI Type',
        required=True,
        help='Enter your 4-letter MBTI Type (e.g., INTJ, ENFP)',
    )
    i_e = fields.Selection(
        [('I', 'Introvert'), ('E', 'Extrovert')],
        string='Energy Style (I/E)',
        compute='_compute_dimensions',
        store=True,
    )
    s_n = fields.Selection(
        [('S', 'Sensing'), ('N', 'Intuition')],
        string='Thinking Style (S/N)',
        compute='_compute_dimensions',
        store=True,
    )
    t_f = fields.Selection(
        [('T', 'Thinking'), ('F', 'Feeling')],
        string='Decision Style (T/F)',
        compute='_compute_dimensions',
        store=True,
    )
    j_p = fields.Selection(
        [('J', 'Judging'), ('P', 'Perceiving')],
        string='Structure Style (J/P)',
        compute='_compute_dimensions',
        store=True,
    )
    result_json = fields.Text(
        string='Result JSON',
    )
    state = fields.Selection(
        [('draft', 'Draft'), ('done', 'Done')],
        string='State',
        default='draft',
    )

    @api.depends('mbti_type')
    def _compute_dimensions(self):
        for rec in self:
            if rec.mbti_type and len(rec.mbti_type) == 4:
                t = rec.mbti_type.upper()
                rec.i_e = 'I' if t[0] == 'I' else 'E'
                rec.s_n = 'S' if t[1] == 'S' else 'N'
                rec.t_f = 'T' if t[2] == 'T' else 'F'
                rec.j_p = 'J' if t[3] == 'J' else 'P'
            else:
                rec.i_e = False
                rec.s_n = False
                rec.t_f = False
                rec.j_p = False

    @api.constrains('mbti_type')
    def _check_mbti_type(self):
        for rec in self:
            if not rec.mbti_type:
                continue
            mbti_upper = rec.mbti_type.upper().strip()
            if len(mbti_upper) != 4:
                raise ValidationError(_("MBTI Type must be exactly 4 characters long."))
            
            valid_types = self.env['nx.intern.personality.report'].MBTI_DATA.keys()
            if mbti_upper not in valid_types:
                raise ValidationError(_(
                    "Invalid MBTI Type: '%s'. It must be one of the 16 valid types (e.g., INTJ, ENFP, INFJ, ISTJ)."
                ) % rec.mbti_type)

    def action_submit(self):
        self.ensure_one()
        mbti_upper = self.mbti_type.upper().strip()
        
        # 1. Get MBTI configuration details
        mbti_data = self.env['nx.intern.personality.report'].MBTI_DATA.get(mbti_upper)
        if not mbti_data:
            raise ValidationError(_("Failed to retrieve details for MBTI type: %s") % mbti_upper)

        # 2. Create the Personality Report
        report_vals = {
            'user_id': self.user_id.id,
            'mbti_type': mbti_upper,
            'strengths': mbti_data['strengths'],
            'weaknesses': mbti_data['weaknesses'],
            'communication_style': mbti_data['communication_style'],
            'recommended_role': mbti_data['recommended_role'],
            'internship_track': mbti_data['internship_track'],
            'risk_level': mbti_data['risk_level'],
        }
        report = self.env['nx.intern.personality.report'].create(report_vals)

        # Update wizard state
        self.write({
            'state': 'done',
            'result_json': json.dumps(report_vals),
        })

        # 3. Find active enrollment for the current user and update it
        enrollment = self.env['nx.intern.enrollment'].search([
            ('intern_user_id', '=', self.user_id.id),
            ('state', 'in', ['draft', 'running']),
        ], limit=1)

        if enrollment:
            enrollment.write({
                'personality_id': report.id,
                'mbti_type': mbti_upper,
                'recommended_track': mbti_data['internship_track'],
            })

        # 4. Send Odoo 19 Chatter Notifications
        self._send_chatter_notifications(report, enrollment, mbti_data)

        # 5. Return success action (e.g., reload client or show dashboard)
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    def _send_chatter_notifications(self, report, enrollment, mbti_data):
        # We will post messages to the enrollment's chatter if it exists, otherwise to the report's chatter.
        # This keeps everything centralized on the enrollment if possible.
        target_record = enrollment if enrollment else report

        # Find managers and admins to notify
        group_manager = self.env.ref('nx_intern_training.group_intern_training_manager')
        group_admin = self.env.ref('nx_intern_training.group_intern_training_admin')
        
        managers = group_manager.users
        admins = group_admin.users

        # A) Message to Manager
        manager_msg = _(
            "<h3>MBTI Personality Assessment Completed</h3>"
            "<p><strong>Intern:</strong> %s</p>"
            "<p><strong>MBTI Type:</strong> <span class='badge bg-primary'>%s</span></p>"
            "<p><strong>Recommended Track:</strong> %s</p>"
            "<p><strong>Risk Level:</strong> <span class='badge bg-warning'>%s</span></p>"
            "<br/>"
            "<h4>Full Personality Insights:</h4>"
            "<ul>"
            "<li><strong>Strengths:</strong> %s</li>"
            "<li><strong>Weaknesses:</strong> %s</li>"
            "<li><strong>Communication Style:</strong> %s</li>"
            "<li><strong>Recommended Role:</strong> %s</li>"
            "</ul>"
        ) % (
            self.user_id.name,
            report.mbti_type,
            report.internship_track,
            report.risk_level.capitalize(),
            report.strengths,
            report.weaknesses,
            report.communication_style,
            report.recommended_role,
        )
        
        # B) Message to Admin (Analytics / Classification)
        admin_msg = _(
            "<h3>Admin Onboarding Analytics Update</h3>"
            "<p><strong>New Intern Classification:</strong></p>"
            "<ul>"
            "<li><strong>User:</strong> %s</li>"
            "<li><strong>MBTI Type:</strong> %s</li>"
            "<li><strong>Assigned Track:</strong> %s</li>"
            "<li><strong>Risk Profiling:</strong> %s</li>"
            "</ul>"
            "<p><em>This data has been registered in the MBTI Distribution Analytics.</em></p>"
        ) % (
            self.user_id.name,
            report.mbti_type,
            report.internship_track,
            report.risk_level.upper(),
        )

        # C) Message to Intern (Simplified Report)
        intern_msg = _(
            "<h3>Your Personality Report</h3>"
            "<p>Congratulations on completing your onboarding assessment! Here is your MBTI profile:</p>"
            "<p><strong>Your Personality Type:</strong> %s</p>"
            "<p><strong>Your Recommended Track:</strong> %s</p>"
            "<p><strong>Your Strengths:</strong> %s</p>"
            "<p><strong>How You Communicate:</strong> %s</p>"
        ) % (
            report.mbti_type,
            report.internship_track,
            report.strengths,
            report.communication_style,
        )

        # Post messages to the chatter
        # In Odoo, we can specify partners/channels or post directly to the thread.
        # We will post to the chatter thread and notify specific user groups.
        if target_record:
            # Post to manager
            target_record.message_post(
                body=manager_msg,
                partner_ids=managers.partner_id.ids,
                message_type='notification',
                subtype_xmlid='mail.mt_note',
            )
            # Post to admin
            target_record.message_post(
                body=admin_msg,
                partner_ids=admins.partner_id.ids,
                message_type='notification',
                subtype_xmlid='mail.mt_note',
            )
            # Post to intern (private note or message)
            target_record.message_post(
                body=intern_msg,
                partner_ids=self.user_id.partner_id.ids,
                message_type='notification',
                subtype_xmlid='mail.mt_note',
            )
