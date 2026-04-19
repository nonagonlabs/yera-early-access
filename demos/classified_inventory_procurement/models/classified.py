"""Classified data models — internal to classified agents only."""

from __future__ import annotations

import yera as yr


class ClassifiedInventoryRecord(yr.Struct):
    """CLASSIFIED — a record from the classified subunit's inventory.

    Contains sensitive information about the internal stock holdings of a
    classified subunit. Fields marked as classified below must never leave
    the classified agent boundary.

    This model is used by the inventory_check_agent to determine whether
    internal stock matches a procurement request's specification. The agent
    sees all fields when reasoning, but can only return an AvailabilityResult
    containing the item name, a boolean, and a quantity.

    Fields:
        item_name: The common name of the item in the inventory.
        nsn: The NATO Stock Number assigned to the item. CLASSIFIED.
        quantity_on_hand: The number of units currently in stock.
        storage_location: The physical storage location of the stock,
            e.g. a warehouse code or facility name. CLASSIFIED.
        programme_association: The classified programme or project this
            stock is allocated to. CLASSIFIED.
        specification_notes: Internal notes describing the item's technical
            specifications, used to determine whether the item matches a
            procurement request's specification.
    """

    item_name: str
    nsn: str
    quantity_on_hand: int
    storage_location: str
    programme_association: str
    specification_notes: str
