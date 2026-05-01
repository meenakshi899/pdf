{
    "name": "Access Role Management",
    "version": "19.0.1.1.0",
    "summary": "Role-based access configuration for groups, menus, buttons, filters, fields and domains",
    "description": """
Access Role Management (Odoo 19)
================================

This module provides an access-role layer on top of Odoo users/groups:

- Create business roles and map security groups
- Assign one or many roles to users
- Configure role lines for:
  - Hide Menu
  - Hide Any Button or Tab
  - Hide Any Filter or GroupBy
  - Edit Fields Access
  - Edit Model Access
  - Edit Domain Access
- Optional flags:
  - Disable chatter
  - Disable debug mode
  - Make system readonly
""",
    "author": "Custom",
    "website": "https://example.com",
    "license": "LGPL-3",
    "category": "Tools",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/access_role_views.xml",
        "views/res_users_views.xml",
    ],
    "installable": True,
    "application": True,
}
