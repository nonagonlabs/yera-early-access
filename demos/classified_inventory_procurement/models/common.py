"""Data models shared across the taint boundary."""

from __future__ import annotations

import yera as yr


class ProcurementItem(yr.Struct):
    """A single item in a procurement request.

    Represents one line item that a requester needs to procure, including
    the quantity required and any technical specification the item must meet.

    Fields:
        name: The common name of the item, e.g. "Ruggedised GPS Module".
        quantity: The number of units required.
        specification: A free-text technical specification the item must
            satisfy, e.g. "MIL-STD-810 rated, 12V DC input, IP67".
    """

    name: str
    quantity: int
    specification: str


class ProcurementRequest(yr.Struct):
    """A batch procurement request submitted by a user.

    Contains one or more items to procure, along with the priority level
    and the name of the person making the request. Parsed from a
    natural-language user input.

    Fields:
        items: The list of items to procure.
        priority: The urgency of the request. One of "routine", "urgent",
            or "critical". Use "routine" if the user does not specify.
        requester: The name or identifier of the person making the request.
            Use "unspecified" if the user does not provide this.
    """

    items: list[ProcurementItem]
    priority: str
    requester: str


class AvailabilityResult(yr.Struct):
    """The declassified result of checking a single item against the
    classified internal inventory.

    This model is the taint downgrade boundary. It must contain no
    classified information — only whether the item is available and
    how many units can be fulfilled internally.

    Fields:
        item_name: The name of the item that was checked, matching the
            name from the original ProcurementItem.
        available: True if the classified inventory holds stock that
            matches the requested specification. False if no matching
            record was found, or the record does not satisfy the spec.
        cleared_quantity: The number of units that can be fulfilled from
            internal stock. Must be 0 if available is False. Must not
            exceed the quantity originally requested. Must not exceed the
            quantity on hand in the inventory.
    """

    item_name: str
    available: bool
    cleared_quantity: int
