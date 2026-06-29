from odoo import http
from odoo.http import request

class AutoLoginController(http.Controller):
    @http.route('/autologin', type='http', auth='none', csrf=False)
    def autologin(self, **kw):
        # Find the admin user
        admin_user = request.env['res.users'].sudo().search([('login', '=', 'admin')], limit=1)
        if admin_user:
            # Set session parameters to log in the user
            request.session.uid = admin_user.id
            request.session.login = admin_user.login
            request.update_env(user=admin_user.id)
        return request.redirect('/web')
