from odoo import models, fields, api

class NxInternPersonalityReport(models.Model):
    _name = 'nx.intern.personality.report'
    _description = 'Intern Personality Report'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'mbti_type'

    user_id = fields.Many2one(
        'res.users',
        string='Intern User',
        required=True,
        ondelete='cascade',
        tracking=True,
    )
    mbti_type = fields.Char(
        string='MBTI Type',
        required=True,
        tracking=True,
    )
    strengths = fields.Text(
        string='Strengths',
    )
    weaknesses = fields.Text(
        string='Weaknesses',
    )
    communication_style = fields.Text(
        string='Communication Style',
    )
    recommended_role = fields.Char(
        string='Recommended Role',
    )
    internship_track = fields.Char(
        string='Recommended Track',
    )
    risk_level = fields.Selection(
        [
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High'),
        ],
        string='Risk Level',
        default='low',
        tracking=True,
    )
    manager_notes = fields.Text(
        string='Manager Notes',
        tracking=True,
    )

    # Static MBTI data engine dictionary
    MBTI_DATA = {
        'INTJ': {
            'strengths': 'Strategic, logical, independent, determined, highly analytical.',
            'weaknesses': 'Can be analytical to a fault, reserved, impatient with inefficiency.',
            'communication_style': 'Direct, logical, focuses on big ideas and systems.',
            'recommended_role': 'Systems Architect, Backend Developer, Business Analyst',
            'internship_track': 'Technical / Backend Development',
            'risk_level': 'low',
        },
        'INTP': {
            'strengths': 'Analytical, original, open-minded, highly curious, objective.',
            'weaknesses': 'Prone to overthinking, detached, dislikes routine and structure.',
            'communication_style': 'Thoughtful, precise, prefers written communication.',
            'recommended_role': 'Research Scientist, Algorithm Engineer, Data Analyst',
            'internship_track': 'Research & Development',
            'risk_level': 'low',
        },
        'ENTJ': {
            'strengths': 'Natural leader, efficient, self-confident, strong-willed, decisive.',
            'weaknesses': 'Can be stubborn, dominant, intolerant of inefficiency.',
            'communication_style': 'Decisive, authoritative, goal-oriented, direct.',
            'recommended_role': 'Project Manager, Team Lead, Product Manager',
            'internship_track': 'Management & Leadership',
            'risk_level': 'low',
        },
        'ENTP': {
            'strengths': 'Innovative, intellectual, highly adaptable, enthusiastic, quick-witted.',
            'weaknesses': 'Dislikes routine, can be argumentative, easily distracted.',
            'communication_style': 'Debating, energetic, brainstorming-focused, engaging.',
            'recommended_role': 'Product Innovator, R&D Engineer, Consultant',
            'internship_track': 'Product & Innovation',
            'risk_level': 'medium',
        },
        'INFJ': {
            'strengths': 'Creative, dedicated, highly insightful, compassionate, principled.',
            'weaknesses': 'Sensitive to criticism, extremely private, prone to burnout.',
            'communication_style': 'Empathetic, inspiring, values-driven, quiet.',
            'recommended_role': 'UI/UX Designer, HR Specialist, Mentor',
            'internship_track': 'Design & Human Resources',
            'risk_level': 'low',
        },
        'INFP': {
            'strengths': 'Idealistic, empathetic, creative, loyal, open-minded.',
            'weaknesses': 'Too altruistic, dislikes conflict, takes things personally.',
            'communication_style': 'Gentle, supportive, prefers one-on-one discussions.',
            'recommended_role': 'Content Writer, UI Designer, HR Coordinator',
            'internship_track': 'Creative & Design',
            'risk_level': 'low',
        },
        'ENFJ': {
            'strengths': 'Charismatic, altruistic, highly reliable, natural leader, empathetic.',
            'weaknesses': 'Overly idealistic, sensitive, self-sacrificing.',
            'communication_style': 'Warm, persuasive, highly encouraging, collaborative.',
            'recommended_role': 'Intern Coordinator, Customer Success Manager',
            'internship_track': 'Operations & Customer Success',
            'risk_level': 'low',
        },
        'ENFP': {
            'strengths': 'Imaginative, enthusiastic, social, creative, highly adaptable.',
            'weaknesses': 'Poor administrative skills, easily stressed, overthinks.',
            'communication_style': 'Expressive, spontaneous, highly engaging and warm.',
            'recommended_role': 'Marketing Specialist, Developer Relations, UI/UX',
            'internship_track': 'Marketing & Creative',
            'risk_level': 'medium',
        },
        'ISTJ': {
            'strengths': 'Responsible, organized, practical, dutiful, highly detail-oriented.',
            'weaknesses': 'Stubborn, judgmental, respects rules to a fault.',
            'communication_style': 'Fact-based, structured, clear and concise.',
            'recommended_role': 'Quality Assurance Engineer, Database Admin, Accountant',
            'internship_track': 'Quality Assurance & Operations',
            'risk_level': 'low',
        },
        'ISFJ': {
            'strengths': 'Supportive, reliable, highly observant, hardworking, loyal.',
            'weaknesses': 'Humble to a fault, takes on too much, dislikes change.',
            'communication_style': 'Helpful, patient, detail-oriented, quiet.',
            'recommended_role': 'Support Specialist, HR Assistant, Document Writer',
            'internship_track': 'Support & Operations',
            'risk_level': 'low',
        },
        'ESTJ': {
            'strengths': 'Organized, dedicated, direct, highly reliable, systematic.',
            'weaknesses': 'Inflexible, uncomfortable with unconventional situations.',
            'communication_style': 'Direct, systematic, focuses on order and tasks.',
            'recommended_role': 'Operations Manager, Quality Control Lead',
            'internship_track': 'Operations & Quality Control',
            'risk_level': 'low',
        },
        'ESFJ': {
            'strengths': 'Outgoing, loyal, warm, helpful, highly organized.',
            'weaknesses': 'Worries about social status, inflexible, sensitive to criticism.',
            'communication_style': 'Friendly, collaborative, focuses on harmony and community.',
            'recommended_role': 'Event Organizer, HR Assistant, Customer Relations',
            'internship_track': 'Human Resources & Support',
            'risk_level': 'low',
        },
        'ISTP': {
            'strengths': 'Bold, practical, highly analytical, adaptable, troubleshooter.',
            'weaknesses': 'Reserved, easily bored, dislikes commitment and rules.',
            'communication_style': 'Action-oriented, quiet, solves problems on the fly.',
            'recommended_role': 'DevOps Engineer, Troubleshooter, Systems Admin',
            'internship_track': 'DevOps & Infrastructure',
            'risk_level': 'medium',
        },
        'ISFP': {
            'strengths': 'Artistic, sensitive, imaginative, passionate, open-minded.',
            'weaknesses': 'Fiercely independent, easily stressed, unpredictable.',
            'communication_style': 'Quiet, observant, shows care through actions.',
            'recommended_role': 'Graphic Designer, UI/UX Designer, Front-End Developer',
            'internship_track': 'Design & Front-End',
            'risk_level': 'low',
        },
        'ESTP': {
            'strengths': 'Energetic, practical, action-oriented, highly sociable, bold.',
            'weaknesses': 'Insensitive, impatient, prone to risky behavior.',
            'communication_style': 'Direct, humorous, focuses on immediate results.',
            'recommended_role': 'Sales Representative, Business Development Intern',
            'internship_track': 'Sales & Business Development',
            'risk_level': 'high',
        },
        'ESFP': {
            'strengths': 'Bold, original, practical, excellent people skills, fun-loving.',
            'weaknesses': 'Easily bored, poor long-term planner, unfocused.',
            'communication_style': 'Fun, enthusiastic, highly interactive, spontaneous.',
            'recommended_role': 'Event Specialist, Public Relations Intern',
            'internship_track': 'Public Relations & Marketing',
            'risk_level': 'medium',
        }
    }
