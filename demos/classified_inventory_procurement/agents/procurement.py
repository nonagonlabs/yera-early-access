"""Procurement Agent — top-level agent using an external frontier model.

This agent has NO classified policy. It cannot call classified tools
directly. It interacts with classified inventory exclusively through
the classified subagents, which return only declassified data.
"""

from __future__ import annotations

import yera as yr

from models.common import AvailabilityResult, ProcurementRequest
from models.orders import PurchaseOrder
from models.sourcing import ProcurementPlan, SupplierQuote
from tools.suppliers import place_order, search_suppliers

from .classified import inventory_check_agent, inventory_reserve_agent


@yr.agent(
    name="Procurement Agent",
    description=(
        "Handles end-to-end procurement: parses requests, checks internal "
        "stock via authorised subagents, sources externally, and places orders."
    ),
)
def procurement_agent() -> None:
    """Top-level procurement agent using an external frontier model.

    Interacts with the user via chat to receive procurement requests,
    checks classified internal inventory via authorised subagents,
    sources remaining items externally, presents a plan for approval,
    and executes it.

    Returns:
        None — communicates results to user via chat blocks.
    """
    # ── 1. PARSE REQUEST ────────────────────────────────────────────────
    yr.markdown(content="**Procurement Agent** — ready to process a request.")
    user_input = yr.text_input(label="Describe what you need to procure:")
    yr.workspace.set("user_request", user_input)
    request = ProcurementRequest.fill()
    yr.markdown(content="**Parsed procurement request:**")
    yr.table(
        [
            {
                "Item": item.name,
                "Qty": item.quantity,
                "Spec": item.specification,
            }
            for item in request.items
        ]
    )

    # ── 2. CHECK INTERNAL AVAILABILITY ──────────────────────────────────
    # Each call crosses the taint boundary — we send plain strings in,
    # and receive only AvailabilityResult (declassified) back.
    availability_results: list[AvailabilityResult] = []
    with yr.action(message="Checking classified inventory...") as action:
        for item in request.items:
            action.update(message=f"Checking: {item.name}")
            result = inventory_check_agent(
                item_name=item.name,
                quantity=item.quantity,
                specification=item.specification,
            )
            availability_results.append(result)
            yr.workspace.set(f"availability:{item.name}", result)

    yr.markdown(content="**Internal availability results:**")
    yr.table(
        [
            {
                "Item": r.item_name,
                "Available": r.available,
                "Cleared Qty": r.cleared_quantity,
            }
            for r in availability_results
        ]
    )

    # ── 3. EXTERNAL SOURCING ────────────────────────────────────────────
    # For items (or remaining quantities) not fulfilled internally,
    # search external suppliers.
    items_to_source = []
    for item, avail in zip(request.items, availability_results, strict=True):
        remaining = item.quantity - avail.cleared_quantity
        if remaining > 0:
            items_to_source.append((item, remaining))

    all_quotes: list[SupplierQuote] = []
    if items_to_source:
        with yr.action(message="Searching external suppliers...") as action:
            for item, remaining_qty in items_to_source:
                action.update(message=f"Sourcing: {item.name} (qty: {remaining_qty})")
                quotes = search_suppliers(
                    item_name=item.name, specification=item.specification
                )
                all_quotes.extend(quotes)
                yr.workspace.set(f"quotes:{item.name}", quotes)

    yr.workspace.set("priority", request.priority)

    # ── 4. ASSEMBLE PLAN ────────────────────────────────────────────────
    # The LLM builds a ProcurementPlan from all availability results and
    # quotes now present in the workspace, factoring in priority.
    plan = ProcurementPlan.fill()

    # ── 5. PRESENT PLAN TO USER ─────────────────────────────────────────
    yr.markdown(content="**Proposed procurement plan:**")
    yr.table(
        [
            {
                "Item": line.item.name,
                "Source": line.source,
                "Qty": line.quantity,
                "Unit Price (GBP)": line.unit_price_gbp or "—",
                "Lead Time (days)": line.lead_time_days or "—",
            }
            for line in plan.lines
        ]
    )
    yr.markdown(content=f"**Total cost: £{plan.total_cost_gbp:,.2f}**")

    from yera.events import request_input_buttons

    decision = request_input_buttons(
        options=["Approve", "Revise", "Cancel"],
        label="How would you like to proceed?",
    )

    # ── 6. HANDLE DECISION ──────────────────────────────────────────────
    if decision == "Cancel":
        yr.markdown(content="Procurement request cancelled.")
        return

    if decision == "Revise":
        yr.markdown(content="Revision flow not implemented in this demo.")
        return

    # ── 7. EXECUTE PLAN ─────────────────────────────────────────────────
    yr.markdown(content="**Executing procurement plan...**")
    orders: list[PurchaseOrder] = []
    reservation_failures: list[str] = []

    # 7a. Reserve internal stock — each call crosses the taint boundary,
    #     returning only a boolean.
    internal_lines = [line for line in plan.lines if line.source == "internal"]
    if internal_lines:
        with yr.action(message="Reserving internal stock...") as action:
            for line in internal_lines:
                action.update(message=f"Reserving: {line.item.name}")
                success = inventory_reserve_agent(
                    item_name=line.item.name, quantity=line.quantity
                )
                if not success:
                    reservation_failures.append(line.item.name)

    # 7b. Place external orders
    external_lines = [line for line in plan.lines if line.source != "internal"]
    if external_lines:
        with yr.action(message="Placing external orders...") as action:
            for line in external_lines:
                action.update(message=f"Ordering: {line.item.name} from {line.source}")
                order = place_order(
                    supplier_name=line.source,
                    items=[line.item],
                    total_gbp=line.unit_price_gbp * line.quantity
                    if line.unit_price_gbp
                    else 0.0,
                )
                orders.append(order)

    # ── 8. CONFIRMATION ─────────────────────────────────────────────────
    if reservation_failures:
        yr.markdown(
            content=(
                "**Warning:** Failed to reserve internal stock for: "
                + ", ".join(reservation_failures)
            )
        )

    if orders:
        yr.markdown(content="**Purchase orders placed:**")
        yr.table(
            [
                {
                    "Supplier": o.supplier_name,
                    "Reference": o.order_reference,
                    "Total (GBP)": f"£{o.total_gbp:,.2f}",
                }
                for o in orders
            ]
        )

    yr.markdown(content="**Procurement complete.**")
