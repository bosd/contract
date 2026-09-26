# Copyright 2026 bosd
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

_logger = logging.getLogger(__name__)


def post_init_hook(env):
    """Put the contracts that already exist in the active state.

    The field defaults to draft, and a draft contract does not invoice. An
    installation that already runs contracts must not have its invoicing stop
    the moment this module is installed, so everything that predates it is
    considered active.
    """
    env.cr.execute("UPDATE contract_contract SET state = 'active'")
    _logger.info("contract_state: %s existing contracts set to active", env.cr.rowcount)
