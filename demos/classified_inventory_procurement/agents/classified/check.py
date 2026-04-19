"""Inventory Check Agent — classified boundary.

This agent operates under the classified:inventory policy. It has access
to the full ClassifiedInventoryRecord, but only returns a declassified
AvailabilityResult. SIGL verifies at compile time that no classified
data escapes through the return type.
"""

from __future__ import annotations

import yera as yr

from models.common import AvailabilityResult
from tools.inventory import query_classified_inventory


@yr.agent(
    name="Inventory Check Agent",
    description=(
        "Checks classified internal inventory for item availability. "
        "Returns only declassified availability answers."
    ),
    policy="classified:inventory",
)
def inventory_check_agent(
    item_name: str, quantity: int, specification: str
) -> AvailabilityResult:
    """Check whether the classified internal inventory can fulfil a request.

    Queries the classified inventory, uses LLM reasoning to determine
    whether the record matches the specification, and returns a declassified
    availability answer. No classified detail leaves this agent.

    Args:
        item_name: Name of the item to check.
        quantity: Number of units requested.
        specification: Technical specification the item must meet.

    Returns:
        A declassified AvailabilityResult with availability and cleared quantity.
    """
    record = query_classified_inventory(item_name)

    if record is None:
        return AvailabilityResult(
            item_name=item_name, available=False, cleared_quantity=0
        )

    # Add classified data to this agent's workspace so the LLM can reason
    # about whether the record matches the specification. This data never
    # leaves this agent's context.
    yr.workspace.set("inventory_record", record)
    yr.workspace.set("specification", specification)
    yr.workspace.set("quantity_requested", quantity)

    # The LLM fills the declassified struct from workspace context.
    # It sees the classified record internally, but the only output is
    # AvailabilityResult — SIGL marks this return as a taint downgrade.
    return AvailabilityResult.fill()
