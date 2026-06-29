{
    'name': 'NerithonX Intern Training',
    'version': '19.0.1.0.0',
    'category': 'Human Resources/Training',
    'summary': 'Internship Training Automation System for NerithonX Technologies',
    'description': """
        NerithonX Internship Training Automation
        =========================================
        Manage internship training programs with day-by-day roadmaps,
        automated task generation, submission tracking, and manager reviews.
    """,
    'author': 'NerithonX Technologies',
    'website': 'https://www.nerithonx.com',
    'license': 'LGPL-3',
    'depends': ['base', 'mail'],
    'data': [
        # Security
        'security/nx_intern_training_groups.xml',
        'security/ir.model.access.csv',
        'security/nx_intern_training_rules.xml',
        # Data
        'data/nx_intern_data.xml',
        # Views
        'views/nx_intern_program_views.xml',
        'views/nx_intern_roadmap_day_views.xml',
        'views/nx_intern_enrollment_views.xml',
        'views/nx_intern_daily_task_views.xml',
        'views/nx_intern_submission_views.xml',
        'views/nx_intern_menus.xml',
        # Reports
        'reports/nx_intern_daily_task_report.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
