from markupsafe import Markup, escape

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class CrmLeadShareLinkWizard(models.TransientModel):
    _name = "crm.lead.share.link.wizard"
    _description = "CRM Lead Share Link"

    lead_id = fields.Many2one("crm.lead", string="Lead", required=True, readonly=True)
    share_link = fields.Char(string="Hiperligação", compute="_compute_share_link", readonly=True)
    partner_ids = fields.Many2many("res.partner", string="Destinatários")
    note = fields.Text(string="Nota")

    @api.depends("lead_id")
    def _compute_share_link(self):
        base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url", "").rstrip("/")
        for wizard in self:
            wizard.share_link = (
                f"{base_url}/web#id={wizard.lead_id.id}&model=crm.lead&view_type=form"
                if wizard.lead_id else False
            )

    def action_send_mail(self):
        self.ensure_one()
        if not self.partner_ids:
            raise UserError(_("Selecione pelo menos um destinatário."))
        missing = self.partner_ids.filtered(lambda p: not p.email)
        if missing:
            raise UserError(_("Os seguintes destinatários não têm endereço de email: %s") % ", ".join(missing.mapped("display_name")))

        lead = self.lead_id
        note_html = Markup("")
        if self.note:
            note_html = Markup("<p>%s</p>") % escape(self.note)
        body = Markup(
            "<p>%s</p>%s<p><a href='%s'>%s</a></p>"
            "<p><small>%s</small></p>"
        ) % (
            _("Foi partilhada consigo uma ligação direta para a Lead/Oportunidade ‘%s’.", lead.display_name),
            note_html,
            self.share_link,
            _("Abrir Lead/Oportunidade"),
            _("Esta é uma ligação interna do Odoo. É necessário iniciar sessão e ter permissões de acesso ao CRM."),
        )
        sender = self.env.user.email_formatted or self.env.company.email
        if not sender:
            raise UserError(_("Não foi possível determinar o endereço de email do remetente."))
        mails = self.env["mail.mail"]
        for partner in self.partner_ids:
            mails |= self.env["mail.mail"].create({
                "subject": _("Lead/Oportunidade: %s", lead.display_name),
                "body_html": body,
                "email_from": sender,
                "email_to": partner.email_formatted,
                "auto_delete": True,
            })
        mails.send()
        return {"type": "ir.actions.act_window_close"}
