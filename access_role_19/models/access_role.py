from odoo import api, fields, models


class AccessRole(models.Model):
    _name = "access.role"
    _description = "Access Role"
    _order = "name"

    name = fields.Char(required=True, translate=True)
    active = fields.Boolean(default=True)
    group_ids = fields.Many2many(
        "res.groups",
        "access_role_group_rel",
        "role_id",
        "group_id",
        string="Groups",
    )
    user_ids = fields.Many2many(
        "res.users",
        "access_role_user_rel",
        "role_id",
        "user_id",
        string="Users",
        readonly=True,
    )

    _sql_constraints = [
        ("access_role_name_uniq", "unique(name)", "Role name must be unique."),
    ]

    @api.onchange("group_ids")
    def _onchange_group_ids(self):
        # Kept intentionally light; group sync is handled on users write/create.
        return
