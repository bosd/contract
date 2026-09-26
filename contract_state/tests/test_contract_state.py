# Copyright 2026 bosd
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.contract.tests.test_contract import TestContractBase


class TestContractState(TestContractBase):
    def test_new_contract_starts_in_draft(self):
        contract = self.env["contract.contract"].create(
            {"name": "Fresh", "partner_id": self.partner.id}
        )
        self.assertEqual(contract.state, "draft")

    def test_draft_hides_the_invoicing_button(self):
        """`create_invoice_visibility` drives the button, so it carries the gate."""
        self.contract.state = "active"
        self.contract.invalidate_recordset(["create_invoice_visibility"])
        active_visibility = self.contract.create_invoice_visibility
        self.contract.state = "draft"
        self.contract.invalidate_recordset(["create_invoice_visibility"])
        self.assertFalse(
            self.contract.create_invoice_visibility,
            "A draft contract must not offer the invoicing button",
        )
        self.assertTrue(
            active_visibility,
            "The fixture must be invoiceable while active, or this proves nothing",
        )

    def test_cancelled_hides_the_invoicing_button(self):
        self.contract.state = "cancel"
        self.contract.invalidate_recordset(["create_invoice_visibility"])
        self.assertFalse(self.contract.create_invoice_visibility)

    def test_cron_skips_contracts_that_are_not_invoiceable(self):
        model = self.env["contract.contract"]
        domain = model._get_contracts_to_invoice_domain()
        self.contract.state = "active"
        self.assertIn(self.contract, model.search(domain))
        self.contract.state = "draft"
        self.assertNotIn(self.contract, model.search(domain))

    def test_invoiceable_states_is_the_extension_point(self):
        """A module adding an invoiceable state overrides one method."""
        self.assertEqual(
            self.env["contract.contract"]._get_invoiceable_states(), ["active"]
        )

    def test_actions_move_between_states(self):
        self.contract.action_activate()
        self.assertEqual(self.contract.state, "active")
        self.contract.action_cancel()
        self.assertEqual(self.contract.state, "cancel")
        self.contract.action_draft()
        self.assertEqual(self.contract.state, "draft")
