from datetime import datetime

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class ProjectTask(models.Model):
    _inherit = "project.task"

    customer_name = fields.Char()
    license_plate = fields.Char()
    date_off_view = fields.Datetime()
    place_offview = fields.Char()

    agent = fields.Char()
    report_number = fields.Char()
    day_offcrash = fields.Datetime()
    place_offcrash = fields.Char()

    course_park = fields.Boolean()
    park_out = fields.Boolean()
    course_change_lane = fields.Boolean()
    rear_end_collision = fields.Boolean()

    vorfahrt = fields.Boolean()
    ast_park = fields.Boolean()
    ast_standing = fields.Boolean()

    others = fields.Boolean()
    other_text = fields.Text()

    client_fam_name = fields.Char()
    client_first_name = fields.Char()
    client_post_code = fields.Char()
    client_local = fields.Char()
    client_post_code = fields.Char()
    client_e_mail = fields.Char()
    client_phone = fields.Char()

    client_lawyer = fields.Boolean()
    client_name_lawyer = fields.Char()
    client_insurance = fields.Boolean()
    name_insurance = fields.Char()
    client_service_book = fields.Boolean()
    dekra = fields.Selection(
        selection=[("Dekra", "Dekra"), ("PLZ Fahrzeugschein", "PLZ Fahrzeugschein")]
    )

    policy_holder_fam_name = fields.Char()
    policy_holder_first_name = fields.Char()
    policy_holder_post_code = fields.Char()
    policy_holder_local = fields.Char()
    policy_holder_streat = fields.Char()

    policy_name = fields.Char()
    policy_number = fields.Char()

    selection_dismantle = fields.Selection(
        selection=[("unzerlegt", "unzerlegt"), ("teilzerlegt", "teilzerlegt")]
    )
    selection_driveable = fields.Selection(
        selection=[
            ("fahrbereit", "fahrbereit"),
            ("nicht fahrbereit", "nicht fahrbereit"),
            (
                "bedingt fahrfähig bis zur Werkstatt",
                "bedingt fahrfähig bis zur Werkstatt",
            ),
        ]
    )
    selection_driving_safety = fields.Selection(
        selection=[
            ("verkehrsicher", "verkehrsicher"),
            ("nicht verkehrsicher", "nicht verkehrsicher"),
        ]
    )

    inspection_note = fields.Text()

    selection_good = fields.Selection(
        selection=[("sehr gut", "sehr gut"), ("gut", "gut")]
    )
    selection_average = fields.Selection(
        selection=[
            ("durchschnittlich", "durchschnittlich"),
            ("überdurchschnittlich", "überdurchschnittlich"),
        ]
    )
    sehr_gepflegt = fields.Selection(
        selection=[("gepflegt", "gepflegt"), ("sehr gepflegt", "sehr gepflegt")]
    )
    selection_age_performance = fields.Selection(
        selection=[("Alter und Laufl. entsprechend", "Alter und Laufl. entsprechend")]
    )

    selection_car_good = fields.Selection(
        selection=[("sehr gut", " sehr gut"), ("gut", "gut")]
    )
    selection_car_average = fields.Selection(
        selection=[
            ("überdurchschnittlich", "überdurchschnittlich"),
            ("durchschnittlich", "durchschnittlich"),
        ]
    )
    selection_car_condition = fields.Selection(
        selection=[("sehr gepflegt", "sehr gepflegt"), ("gepflegt", "gepflegt")]
    )
    selection_car_usable_dirty = fields.Selection(
        selection=[
            ("Fahrzeug einsatzbereit verschmutzt", "Fahrzeug einsatzbereit verschmutzt")
        ]
    )

    front_dimension = fields.Char()
    front_index = fields.Char()
    front_manufacturer = fields.Char()
    front_wheel_type = fields.Selection(
        selection=[("Sommer", "Sommer"), ("Winter", "Winter")]
    )
    front_tread_depth = fields.Float()

    back_dimension = fields.Char()
    back_index = fields.Char()
    back_manufacturer = fields.Char()
    back_wheel_type = fields.Selection(
        selection=[("Sommer", "Sommer"), ("Winter", "Winter")]
    )
    back_tread_depth = fields.Float()

    pre_damage = fields.Text()

    unrepaired_damage = fields.Text()

    signature = fields.Binary()

    def _get_document_folder(self):
        current_month = str(datetime.now().month)
        current_year = str(datetime.now().year)
        folder_year_id = self.env["documents.folder"].search(
            [("name", "=", current_year)]
        )
        if not folder_year_id:
            folder_year_id = self.env["documents.folder"].create({"name": current_year})
        folder_month_id = self.env["documents.folder"].search(
            [("name", "=", current_month), ("parent_folder_id", "=", folder_year_id.id)]
        )
        if not folder_month_id:
            folder_month_id = self.env["documents.folder"].create(
                {"name": current_month, "parent_folder_id": folder_year_id.id}
            )
        folder_partner_id = self.env["documents.folder"].search(
            [
                ("name", "=", self.partner_id.name),
                ("parent_folder_id", "=", folder_month_id.id),
            ]
        )
        if not folder_partner_id:
            folder_partner_id = self.env["documents.folder"].create(
                {"name": self.partner_id.name, "parent_folder_id": folder_month_id.id}
            )
        return folder_partner_id

    @api.onchange("stage_id")
    def _check_attachment(self):
        attachment_ids = self.env["ir.attachment"].search(
            [("res_id", "=", self._origin.id), ("res_model", "=", "project.task")]
        )
        if (
            self.name
            and self.stage_id
            and self.stage_id.name != "New"
            and not attachment_ids
        ):
            message = _("Anhang von %s und Kunde %s fehlt") % (
                self.name,
                self.partner_id.name,
            )
            raise UserError(message)
