from odoo import models, fields, _
from odoo.exceptions import UserError


class NxInternSubmission(models.Model):
    _name = 'nx.intern.submission'
    _description = 'Intern Submission'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    task_id = fields.Many2one(
        'nx.intern.daily.task',
        string='Daily Task',
        required=True,
        ondelete='cascade',
    )
    intern_user_id = fields.Many2one(
        'res.users',
        string='Intern',
        default=lambda self: self.env.user,
        tracking=True,
    )
    submission_notes = fields.Html(
        string='Submission Notes',
    )
    attachment_ids = fields.Many2many(
        'ir.attachment',
        'nx_intern_submission_attachment_rel',
        'submission_id',
        'attachment_id',
        string='Attachments',
    )
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('submitted', 'Submitted'),
            ('approved', 'Approved'),
            ('revision_required', 'Revision Required'),
            ('rejected', 'Rejected'),
        ],
        string='Status',
        default='draft',
        tracking=True,
        required=True,
    )
    manager_feedback = fields.Html(
        string='Manager Feedback',
    )
    score = fields.Float(
        string='Score',
    )

    # ---- Workflow buttons -----------------------------------------------

    def action_submit(self):
        """Intern submits their work."""
        self.ensure_one()
        if self.state != 'draft' and self.state != 'revision_required':
            raise UserError(_('Only draft or revision-required submissions can be submitted.'))
        self.write({'state': 'submitted'})
        self.task_id.write({'state': 'submitted'})

    def action_approve(self):
        """Manager approves the submission."""
        self.ensure_one()
        self.write({'state': 'approved'})
        task = self.task_id
        task.write({'state': 'approved'})

        # Unlock the next day's task
        enrollment = task.enrollment_id
        next_tasks = enrollment.task_ids.filtered(
            lambda t: t.day_number == task.day_number + 1 and t.state == 'locked'
        )
        if next_tasks:
            next_tasks[0].write({'state': 'pending'})

        # Update enrollment progress
        approved_count = len(
            enrollment.task_ids.filtered(lambda t: t.state == 'approved')
        )
        total_count = len(enrollment.task_ids)
        current_max = max(
            enrollment.task_ids.filtered(
                lambda t: t.state == 'approved'
            ).mapped('day_number'),
            default=0,
        )
        vals = {'current_day': current_max + 1}
        if approved_count == total_count:
            vals['state'] = 'completed'
            vals['current_day'] = current_max
        enrollment.write(vals)

    def action_request_revision(self):
        """Manager requests revision."""
        self.ensure_one()
        self.write({'state': 'revision_required'})
        self.task_id.write({'state': 'revision_required'})

    def action_reject(self):
        """Manager rejects the submission."""
        self.ensure_one()
        self.write({'state': 'rejected'})
        self.task_id.write({'state': 'rejected'})
