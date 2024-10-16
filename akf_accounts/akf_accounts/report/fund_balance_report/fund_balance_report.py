# Copyright (c) 2024, Nabeel Saleem and contributors
# For license information, please see license.txt

import frappe
from frappe import _


@frappe.whitelist(allow_guest=True)
def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    columns = [
        _("Account") + ":Link/Account:140",
        _("Branch") + ":Link/Cost Center:140",
        _("Service Area") + ":Link/Program:140",
        _("Subservice Area") + ":Link/Subservice Area:140",
        _("Funds / Projects") + ":Link/Project:140",
        _("Funds Code") + ":Link/Project:140",
        _("Balance") + ":Data:140",
    ]
    return columns


def get_data(filters):
    result = get_query_result(filters)
    return result


def get_conditions(filters):
    conditions = ""

    # if filters.get("company"):
    #     conditions += " AND company = %(company)s"
    # if filters.get("applicant"):
    #     conditions += " AND applicant = %(applicant)s"
    # if filters.get("branch"):
    #     conditions += " AND branch = %(branch)s"
    # if filters.get("loan_type"):
    #     conditions += " AND loan_type = %(loan_category)s"
    # if filters.get("repayment_start_date"):
    #     conditions += " AND repayment_start_date = %(repayment_start_date)s"

    return conditions


def get_query_result(filters):
    conditions = get_conditions(filters)
    result = frappe.db.sql(
        """
        SELECT 
			gle.account,gle.cost_center,gle.program,gle.subservice_area,proj.project_name, gle.project, SUM(gle.debit)-SUM(gle.credit) 
        FROM 
            `tabGL Entry` gle
        LEFT JOIN 
            `tabAccount` acc ON gle.account = acc.name
        RIGHT JOIN 
            `tabProject` proj ON gle.project = proj.name
        WHERE
            acc.root_type = 'Equity'
        {0}""".format(conditions if conditions else ""
        ),
        filters,
        as_dict=0,
    )
    return result
