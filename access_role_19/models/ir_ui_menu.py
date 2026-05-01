from odoo import api, models


class IrUiMenu(models.Model):
    _inherit = "ir.ui.menu"

    @api.model
    def _hidden_menu_ids_for_current_user(self):
        user = self.env.user
        if user._is_admin():
            return set()
        return set(user.access_role_ids.mapped("hide_menu_line_ids.menu_id").ids)

    def search(self, domain=None, offset=0, limit=None, order=None, count=False):
        records = super().search(domain=domain, offset=offset, limit=limit, order=order, count=False)
        hidden_ids = self._hidden_menu_ids_for_current_user()
        if hidden_ids:
            records = records.filtered(lambda m: m.id not in hidden_ids)
        if count:
            return len(records)
        return records
