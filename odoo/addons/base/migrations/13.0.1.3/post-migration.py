# Copyright 2020 Opener B.V. (stefan@opener.amsterdam)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from psycopg2 import sql
from openupgradelib import openupgrade


@openupgrade.migrate(use_env=True)
def migrate(env, version):
    # Populate missing binding_model_id values in ir_act_window
    openupgrade.logged_query(
        env.cr,
        """ UPDATE ir_act_window iaw
        SET binding_model_id = im.id
        FROM ir_model im
        WHERE binding_model_id IS NULL
            AND src_model IS NOT NULL
            AND iaw.src_model = im.model; """)
    openupgrade.logged_query(
        env.cr,
        sql.SQL("""
        UPDATE ir_attachment
        SET name = {datas_fname}
        WHERE {datas_fname} IS NOT NULL
            AND {datas_fname} != name
        """.format({
            'datas_fname': sql.Identifier(
                openupgrade.get_legacy_name('datas_fname')),
        })))
