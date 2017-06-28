{
    'name': 'Debt Customer',
    'version': '10.0.0.0',
    'summary': 'Reporte de deudas de clientes',
    'description': """
        Genera un reporte de deudas de los clientes con diferentes filtros
    """,
    'category': '',
    'author': 'Raul Ovalle, raul@xmarts.do',
    'website': 'www.xmarts.com',
    'license': '',
    'depends': [
        'account',
        'account_accountant',

    ],
    'data': [
        'wizards/customer_debt_report_wizard_view.xml',
        'menuitems.xml',
        'reports/customer_debt_report.xml',
        'data/paperformats.xml',

    ],
    'installable': True,
    'auto_install': False,
}