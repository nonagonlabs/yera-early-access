"""Tools for interacting with external suppliers."""

from __future__ import annotations

import yera as yr

from models.common import ProcurementItem
from models.orders import PurchaseOrder
from models.sourcing import SupplierQuote


@yr.tool
def search_suppliers(item_name: str, specification: str) -> list[SupplierQuote]:
    """Search external supplier catalogues for quotes on an item.

    Args:
        item_name: Name of the item to source.
        specification: Technical specification the item must meet.

    Returns:
        A list of supplier quotes matching the search criteria.
    """
    # Stub — in production this would call supplier APIs.
    raise NotImplementedError("Stub: replace with supplier catalogue search.")


@yr.tool
def place_order(
    supplier_name: str, items: list[ProcurementItem], total_gbp: float
) -> PurchaseOrder:
    """Place a purchase order with an external supplier.

    Args:
        supplier_name: Name of the supplier to order from.
        items: Items and quantities to order.
        total_gbp: Agreed total price in GBP.

    Returns:
        The confirmed purchase order with reference number.
    """
    # Stub — in production this would call a supplier ordering API.
    raise NotImplementedError("Stub: replace with supplier order placement.")
