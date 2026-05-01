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

    disable_chatter = fields.Boolean()
    disable_debug_mode = fields.Boolean()
    make_system_readonly = fields.Boolean(string="Make System Readonly")

    hide_menu_line_ids = fields.One2many("access.role.hide.menu", "role_id", string="Hide Menu")
    hide_button_line_ids = fields.One2many("access.role.hide.button", "role_id", string="Hide Any Button or Tab")
    hide_filter_line_ids = fields.One2many("access.role.hide.filter", "role_id", string="Hide Any Filter or GroupBy")
    edit_field_line_ids = fields.One2many("access.role.edit.field", "role_id", string="Edit Fields Access")
    model_access_line_ids = fields.One2many("access.role.model.access", "role_id", string="Edit Model Access")
    domain_access_line_ids = fields.One2many("access.role.domain.access", "role_id", string="Edit Domain Access")

    _sql_constraints = [
        ("access_role_name_uniq", "unique(name)", "Role name must be unique."),
    ]

    @api.onchange("group_ids")
    def _onchange_group_ids(self):
        return


class AccessRoleLineBase(models.AbstractModel):
    _name = "access.role.line.base"
    _description = "Access Role Line Base"

    role_id = fields.Many2one("access.role", required=True, ondelete="cascade")
    model_id = fields.Many2one("ir.model", string="Model", required=True)


class AccessRoleHideMenu(models.Model):
    _name = "access.role.hide.menu"
    _description = "Access Role Hide Menu"

    role_id = fields.Many2one("access.role", required=True, ondelete="cascade")
    menu_id = fields.Many2one("ir.ui.menu", string="Menu", required=True)


class AccessRoleHideButton(models.Model):
    _name = "access.role.hide.button"
    _description = "Access Role Hide Button"

    role_id = fields.Many2one("access.role", required=True, ondelete="cascade")
    model_id = fields.Many2one("ir.model", required=True)
    button_name = fields.Char(required=True, help="Technical button name (method)")
    tab_name = fields.Char(help="Notebook page string or technical name")


class AccessRoleHideFilter(models.Model):
    _name = "access.role.hide.filter"
    _description = "Access Role Hide Filter"

    role_id = fields.Many2one("access.role", required=True, ondelete="cascade")
    model_id = fields.Many2one("ir.model", required=True)
    filter_name = fields.Char(required=True)
    groupby_name = fields.Char()


class AccessRoleEditField(models.Model):
    _name = "access.role.edit.field"
    _description = "Access Role Edit Field"

    role_id = fields.Many2one("access.role", required=True, ondelete="cascade")
    model_id = fields.Many2one("ir.model", required=True)
    field_id = fields.Many2one("ir.model.fields", required=True, domain="[('model_id', '=', model_id)]")
    readonly = fields.Boolean()
    invisible = fields.Boolean()
    required = fields.Boolean()
    remove_external_link = fields.Boolean()


class AccessRoleModelAccess(models.Model):
    _name = "access.role.model.access"
    _description = "Access Role Model Access"

    role_id = fields.Many2one("access.role", required=True, ondelete="cascade")
    model_id = fields.Many2one("ir.model", required=True)
    readonly = fields.Boolean()
    hide_create = fields.Boolean()
    hide_delete = fields.Boolean()
    hide_archive = fields.Boolean()
    hide_export = fields.Boolean()
    hide_duplicate = fields.Boolean()
    hide_report = fields.Boolean()
    hide_actions = fields.Boolean()


class AccessRoleDomainAccess(models.Model):
    _name = "access.role.domain.access"
    _description = "Access Role Domain Access"

    role_id = fields.Many2one("access.role", required=True, ondelete="cascade")
    model_id = fields.Many2one("ir.model", required=True)
    domain = fields.Char(required=True, default="[]")
