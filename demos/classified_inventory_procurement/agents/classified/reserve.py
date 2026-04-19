"""Inventory Reserve Agent — classified boundary.

This agent operates under the classified:inventory policy. It wraps the
reserve_internal_stock tool so that the procurement agent never needs
direct access to classified inventory tools. Returns only a boolean.
"""

from __future__ import annotations

import yera as yr

from tools.inventory import reserve_internal_stock


@yr.agent(
    name="Inventory Reserve Agent",
    description=(
        "Reserves stock in the classified internal inventory. "
        "Returns only a success/failure boolean."
    ),
    policy="classified:inventory",
)
def inventory_reserve_agent(item_name: str, quantity: int) -> bool:
    """Reserve a quantity of an item in the classified internal inventory.

    Calls the reserve tool and returns a simple boolean. No classified
    detail leaves this agent. This agent exists purely for the taint
    boundary — it contains no LLM reasoning.

    Args:
        item_name: Name of the item to reserve.
        quantity: Number of units to reserve.

    Returns:
        True if reservation succeeded, False otherwise.
    """
    return reserve_internal_stock(item_name, quantity)
