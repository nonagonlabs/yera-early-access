# Classified Inventory Procurement

A Yera demo application demonstrating **compile-time data boundary enforcement** using SIGL's taint analysis.

## The Problem

A defence contractor's procurement agent needs to source and order supplies using an external frontier model, but must cross-reference a classified subunit's inventory. Written naively, the classified data — storage locations, programme associations, NATO Stock Numbers — would propagate to nodes touched by the external model. The application must guarantee at compile time, not just at runtime, that classified data cannot leak.

## How Yera Solves It

Yera's `policy` parameter on tools and agents declares security boundaries. SIGL's compiler then statically verifies every data flow in the application graph against OpenFGA-backed IAM policies before any code runs.

```python
# Classified tools declare their required policy
@yr.tool(policy="classified:inventory")
def query_classified_inventory(item_name: str) -> ClassifiedInventoryRecord | None:
    ...

# Classified agents operate under that policy — they can call classified tools
@yr.agent(policy="classified:inventory")
def inventory_check_agent(item_name: str, quantity: int, specification: str) -> AvailabilityResult:
    ...

# The procurement agent has NO classified policy — it cannot touch classified tools directly
@yr.agent()
def procurement_agent() -> None:
    # ❌ query_classified_inventory(...)        — SIGL compilation error
    # ✅ inventory_check_agent(...)             — returns only declassified data
    ...
```

The key insight: the taint downgrade does not require an explicit annotation. It falls out naturally from SIGL's verification. The compiler sees the return edge from `inventory_check_agent` to `procurement_agent`, checks that `AvailabilityResult` contains no fields carrying the `classified:inventory` taint, and permits the crossing. If someone changed the return type to `ClassifiedInventoryRecord`, compilation would fail.

## Architecture

```
procurement_agent (external model, no policy)
 ├── inventory_check_agent  (internal model, policy="classified:inventory")
 │    └── query_classified_inventory tool
 └── inventory_reserve_agent (internal model, policy="classified:inventory")
      └── reserve_internal_stock tool
```

### Data Boundary Crossings

| From → To | Data Crossing the Boundary | Taint Downgrade? |
|---|---|---|
| `procurement_agent` → `inventory_check_agent` | `str, int, str` (item name, quantity, spec) | No — unclassified data flowing in |
| `inventory_check_agent` → `procurement_agent` | `AvailabilityResult` (item name, bool, int) | **Yes** — classified context reduced to declassified answer |
| `procurement_agent` → `inventory_reserve_agent` | `str, int` (item name, quantity) | No — unclassified data flowing in |
| `inventory_reserve_agent` → `procurement_agent` | `bool` (success/failure) | **Yes** — classified operation reduced to boolean |

### What Stays Behind the Boundary

`ClassifiedInventoryRecord` contains sensitive fields that never leave the classified agents:

- `nsn` — NATO Stock Number
- `storage_location` — physical location of stock
- `programme_association` — which classified programme the stock belongs to

The `inventory_check_agent` sees all of this in its workspace when reasoning about whether a record matches a specification. But its return type is `AvailabilityResult`, which carries only `(item_name, available, cleared_quantity)`. The struct schema constrains what can escape, and SIGL verifies this statically.

## Application Flow

1. User describes a procurement request in natural language
2. `procurement_agent` parses it into a structured `ProcurementRequest`
3. For each item, `inventory_check_agent` is called — classified data stays internal, only availability answers return
4. Items not fulfilled internally are sourced from external suppliers via `search_suppliers`
5. The agent assembles a `ProcurementPlan` and presents it for user approval
6. On approval, internal stock is reserved via `inventory_reserve_agent` and external orders are placed via `place_order`

## File Structure

```
classified_inventory_procurement/
├── README.md
├── models/
│   ├── common.py          # ProcurementItem, ProcurementRequest, AvailabilityResult
│   ├── sourcing.py        # SupplierQuote, ProcurementPlan
│   ├── orders.py          # PurchaseOrder
│   └── classified.py      # ClassifiedInventoryRecord (classified agents only)
├── tools/
│   ├── inventory.py       # query_classified_inventory, reserve_internal_stock
│   └── suppliers.py       # search_suppliers, place_order
├── agents/
│   ├── procurement.py     # procurement_agent (external model)
│   └── classified/
│       ├── check.py       # inventory_check_agent
│       └── reserve.py     # inventory_reserve_agent
└── app.py                 # entry point
```

The `agents/classified/` subdirectory mirrors the taint boundary in the file tree. The `models/__init__.py` deliberately does not re-export `ClassifiedInventoryRecord`, reinforcing the boundary at the import level — though SIGL's compile-time verification is the real guarantee.

## Running

```bash
python app.py
```

## Note

Tool bodies are stubs (`NotImplementedError`). This demo is about the data flow architecture and compile-time boundary enforcement, not the tool implementations.
