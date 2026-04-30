from odoo import api, fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    access_role_ids = fields.Many2many(
        "access.role",
        "access_role_user_rel",
        "user_id",
        "role_id",
        string="Access Roles",
    )

    def _get_role_groups(self):
        self.ensure_one()
        return self.access_role_ids.mapped("group_ids")

    def _sync_groups_from_roles(self):
        for user in self:
            role_groups = user._get_role_groups()
            # Preserve non-role groups: only ensure role groups are present.
            if role_groups:
                user.groups_id = [(4, g.id) for g in role_groups]

    @api.model_create_multi
    def create(self, vals_list):
        users = super().create(vals_list)
        users._sync_groups_from_roles()
        return users

    def write(self, vals):
        res = super().write(vals)
        if "access_role_ids" in vals:
            self._sync_groups_from_roles()
        return res
