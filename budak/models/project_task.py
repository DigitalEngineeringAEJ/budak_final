from datetime import datetime

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class ProjectTask(models.Model):
    _inherit = "project.task"

    partner_id = fields.Many2one(string="Kunde")
    license_plate = fields.Char(string="Kennzeichen")
    date_off_view = fields.Datetime(string="Besichtigunsdatum")
    place_offview = fields.Char(string="Besichtigunsort")
    agent = fields.Char(string="Vermittler")
    report_number = fields.Char(string="GA-Nr.:")
    day_offcrash = fields.Datetime(string="Schadenstag")
    place_offcrash = fields.Char(string="Schadensort")
    course_park = fields.Boolean(string="Einparken")
    park_out = fields.Boolean(string="Ausparken")
    course_change_lane = fields.Boolean(string="Spurwechsel")
    rear_end_collision = fields.Boolean(string="Auffahrunfall")
    vorfahrt = fields.Boolean(string="Vorfahrt")
    ast_park = fields.Boolean(string="AST Geparkt")
    ast_standing = fields.Boolean(string="AST Stand")
    others = fields.Boolean(string="Sonstiges")
    other_text = fields.Text(string=" ")
    client_fam_name = fields.Char(string="Nachname")
    client_first_name = fields.Char()
    client_post_code = fields.Char(string="PLZ")
    client_local = fields.Char(string="Ort")
    client_e_mail = fields.Char(string="E-Mail")
    client_phone = fields.Char(string="Telefon")
    client_lawyer = fields.Boolean(string="Rechtsanwalt")
    client_name_lawyer = fields.Char(string="Name Rechtsanwalt")
    client_insurance = fields.Boolean(string="Rechtchutzversicherung")
    name_insurance = fields.Char(string="Rechtschutzversicherung")
    client_service_book = fields.Boolean(string="Service- Scheckheft")
    dekra = fields.Selection(
        selection=[("Dekra", "Dekra"), ("PLZ Fahrzeugschein", "PLZ Fahrzeugschein")], string="  "
    )
    policy_holder_fam_name = fields.Char()
    policy_holder_first_name = fields.Char(string="Vorname")
    policy_holder_post_code = fields.Char()
    policy_holder_local = fields.Char()
    policy_holder_streat = fields.Char()
    policy_name = fields.Char(string="Versicherung")
    policy_number = fields.Char(string="Versicherungsnummer")
    selection_dismantle = fields.Selection(
        selection=[("unzerlegt", "unzerlegt"), ("teilzerlegt", "teilzerlegt")], string="Auswahl Demontage")
    selection_driveable = fields.Selection(
        selection=[
            ("fahrbereit", "fahrbereit"),
            ("nicht fahrbereit", "nicht fahrbereit"),
            (
                "bedingt fahrfähig bis zur Werkstatt",
                "bedingt fahrfähig bis zur Werkstatt",
            ),
        ],string="Auswahl Fahrbar")
    selection_driving_safety = fields.Selection(
        selection=[
            ("verkehrsicher", "verkehrsicher"),
            ("nicht verkehrsicher", "nicht verkehrsicher"),
        ], string="Verkehrssicher?"
    )
    inspection_note = fields.Text(string="Notiz Besichtigungszustand")
    selection_good = fields.Selection(
        selection=[("sehr gut", "sehr gut"), ("gut", "gut")], string="sehr gut/gut"
    )
    selection_average = fields.Selection(
        selection=[
            ("durchschnittlich", "durchschnittlich"),
            ("überdurchschnittlich", "überdurchschnittlich"),
        ], string="über/durchschnittlich"
    )
    sehr_gepflegt = fields.Selection(
        selection=[("gepflegt", "gepflegt"), ("sehr gepflegt", "sehr gepflegt")], string="sehr gepflegt/gepflegt"
    )
    selection_age_performance = fields.Selection(
        selection=[("Alter und Laufl. entsprechend", "Alter und Laufl. entsprechend")]
        , string="Alter und Laufl. entsprechend"
    )
    selection_car_good = fields.Selection(
        selection=[("sehr gut", " sehr gut"), ("gut", "gut")])
    selection_car_average = fields.Selection(
        selection=[
            ("überdurchschnittlich", "überdurchschnittlich"),
            ("durchschnittlich", "durchschnittlich")])
    selection_car_condition = fields.Selection(
        selection=[("sehr gepflegt", "sehr gepflegt"), ("gepflegt", "gepflegt")],

    )
    selection_car_usable_dirty = fields.Selection(
        selection=[
            ("Fahrzeug einsatzbereit verschmutzt", "Fahrzeug einsatzbereit verschmutzt")
        ], string="Fahrzeug einsatzb. verschmutzt"
    )
    front_dimension = fields.Char(string="Dimension")
    front_index = fields.Char(string="Index")
    front_manufacturer = fields.Char(string="Fabrikant")
    front_wheel_type = fields.Selection(
        selection=[("Sommer", "Sommer"), ("Winter", "Winter")], string="Reifenart"
    )
    front_tread_depth_left = fields.Float(string="Profiltiefe links")
    front_tread_depth_right = fields.Float(string="Profiltiefe rechts")
    back_dimension = fields.Char()
    back_index = fields.Char()
    back_manufacturer = fields.Char()
    back_wheel_type = fields.Selection(selection=[("Sommer", "Sommer"), ("Winter", "Winter")], string="Reifenart")
    back_tread_depth_left = fields.Float()
    back_tread_depth_right = fields.Float()
    pre_damage = fields.Text(string="Vorschäden")
    unrepaired_damage = fields.Text(string="Unreparierte Schäden (Altschäden)")
    signature = fields.Binary(string="Unterschrift")

    @api.onchange("stage_id")
    def _check_attachment(self):
        ''' Check if there are attachment before changing the state '''
        attachment_ids = self.env["ir.attachment"].search(
            [("res_id", "=", self._origin.id), ("res_model", "=", "project.task")]
        )
        if (
                self.name
                and self.partner_id
                and self.stage_id
                and self.stage_id.name != "New"
                and not attachment_ids
        ):
            message = _("Anhang von %s und Kunde %s fehlt") % (
                self.name,
                self.partner_id.name,
            )
            raise UserError(message)

    def _get_document_folder(self):
        ''' Add folder with the following schema (CurrentYear/CurrentMonth/PartnerName) to store the attachment '''
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
