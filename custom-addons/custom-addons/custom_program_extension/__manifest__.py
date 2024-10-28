{
    'name': 'Custom Program Extension',
    'version': '1.0',
    'summary': 'Customizations for extending Openg2p Program Module',
    'description': """
        This module extends the G2P Program Module  to handle customizations and other enhancements.
    """,
    'author': 'Kamal',
    'website': 'http://www.developer.com',
    'category': 'Custom',
    'depends': ['base', 'g2p_programs', 'g2p_program_assessment', 'g2p_entitlement_in_kind', 'g2p_program_registrant_info'],  # Include dependencies
    'data': [
        'security/ir.model.access.csv',
        'views/action_report.xml',
        'views/program_membership_view.xml',
        'wizard/create_manual_entitlement_inkind_wizard.xml',
        # List any XML files containing views, actions, or security rules if needed.
    ],
    "assets": {
        "web.assets_frontend": [
            "custom_program_extension/static/src/scss/new_login_page.scss",
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
}
