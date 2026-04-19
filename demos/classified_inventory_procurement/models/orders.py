"""Data models for purchase orders."""

from __future__ import annotations

import yera as yr

from .common import ProcurementItem


class PurchaseOrder(yr.Struct):
    """A confirmed purchase order placed with an external supplier.

    Returned by the place_order tool after an order has been submitted.

    Fields:
        supplier_name: The name of the supplier the order was placed with.
        items: The list of items and quantities ordered.
        total_gbp: The total price of the order in GBP.
        order_reference: A unique reference string for the order, assigned
            by the supplier's system.
    """

    supplier_name: str
    items: list[ProcurementItem]
    total_gbp: float
    order_reference: str
