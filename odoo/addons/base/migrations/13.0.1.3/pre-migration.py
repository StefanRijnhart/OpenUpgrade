# Copyright 2020 Opener B.V. (stefan@opener.amsterdam)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.addons.openupgrade_records.lib import apriori
from openupgradelib import openupgrade

column_renames = [
    ('ir_attachment', [('datas_fname', None)])]


@openupgrade.migrate(use_env=True)
def migrate(env, version):
    openupgrade.rename_columns(env.cr, column_renames)
    openupgrade.update_module_names(
        env.cr, apriori.renamed_modules.items())
    openupgrade.update_module_names(
        env.cr, apriori.merged_modules.items(), merge_modules=True)

    openupgrade.set_xml_ids_noupdate_value(
        env, 'base', [
            'default_template_user_config',
            'view_menu',
            'lang_km',
        ], False)
    openupgrade.logged_query(
        """ UPDATE ir_model_constraint
        SET create_date = date_init
        WHERE create_date IS NULL AND date_init IS NOT NULL """)
    openupgrade.logged_query(
        """ UPDATE ir_model_constraint
        SET write_date = date_update
        WHERE write_date IS NULL AND date_update IS NOT NULL """)
