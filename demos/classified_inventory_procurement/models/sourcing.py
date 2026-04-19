"""Data models for external sourcing."""

from __future__ import annotations

import yera as yr

from .common import ProcurementItem


class SupplierQuote(yr.Struct):
    """A quote from an external supplier for a single item.

    Returned by the search_suppliers tool. Multiple quotes may be
    returned for the same item from different suppliers.

    Fields:
        supplier_name: The name of the supplier providing the quote.
        item_name: The name of the item being quoted, matching the
            name from the original ProcurementItem.
        unit_price_gbp: The price per unit in GBP.
        lead_time_days: The number of calendar days from order to delivery.
        quantity_available: The maximum number of units the supplier can
            fulfil at this price.
    """

    supplier_name: str
    item_name: str
    unit_price_gbp: float
    lead_time_days: int
    quantity_available: int


class ProcurementPlan(yr.Struct):
    """A complete procurement plan assembled by the agent for user approval.

    Each line in the plan specifies where a quantity of an item will be
    sourced from — either "internal" (from classified inventory) or from
    a named external supplier. A single ProcurementItem may result in
    two lines if it is partially fulfilled internally.

    Fields:
        lines: The list of plan lines, one per source per item.
        total_cost_gbp: The total cost of all externally sourced lines.
            Internal lines have no cost. This must equal the sum of
            (unit_price_gbp * quantity) across all external lines.
    """

    class PlanLine(yr.Struct):
        """A single line in the procurement plan.

        Fields:
            item: The ProcurementItem being sourced on this line.
            source: Either "internal" for stock fulfilled from classified
                inventory, or the supplier name for externally sourced items.
            quantity: The number of units sourced on this line.
            unit_price_gbp: The price per unit in GBP. None for internal lines.
            lead_time_days: The number of calendar days to delivery.
                None for internal lines (assumed immediate).
        """

        item: ProcurementItem
        source: str
        quantity: int
        unit_price_gbp: float | None
        lead_time_days: int | None

    lines: list[PlanLine]
    total_cost_gbp: float
