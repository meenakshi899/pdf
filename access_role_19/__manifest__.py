{
    "name": "Access Role Management",
    "version": "19.0.1.0.0",
    "summary": "Create reusable business roles and assign security groups in one place",
    "description": """
Access Role Management
======================

This module adds a simple role layer on top of Odoo groups:
- Define a role with multiple security groups
- Assign one or more roles on users
- Auto-apply/remove groups when roles change
""",
    "author": "Custom",
    "license": "LGPL-3",
    "category": "Tools",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/access_role_views.xml",
        "views/res_users_views.xml"
    ],
    "installable": True,
    "application": True,
}
