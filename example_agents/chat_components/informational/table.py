import pandas as pd

import yera as yr


@yr.agent(
    name="Table Agent",
    description="An agent that sends tabular data to the user",
)
def table_agent():
    yr.markdown("1. List of dicts - keys from first dict become columns")
    yr.table(
        {
            "Name": ["Item 1", "Item 2"],
            "Value": [100, 200],
            "Status": ["Active", "Inactive"],
        }
    )

    with yr.markdown("2. Dict with list values") as m2:
        m2.new_line("Keys are columns, values are lists of column data")
    yr.table(
        [
            {"Name": "Item 3", "Value": 300, "Status": "Active"},
            {"Name": "Item 4", "Value": 400, "Status": "Inactive"},
        ]
    )

    # 3. List of lists - all lists are rows
    with yr.markdown("3. List of lists - all lists are rows") as m3:
        m3.new_line(
            "Column names are auto-generated -> ['Column 1', 'Column 2', 'Column 3']"
        )
    yr.table(
        [
            ["Item 5", 500, "Active"],
            ["Item 6", 600, "Inactive"],
        ]
    )

    yr.markdown("4. Border options - No borders")
    yr.table(
        [["Widget", 10.99], ["Gadget", 20.99]],
        border=False,
    )
    yr.markdown("5. Border options - Horizontal borders")
    yr.table(
        [["Widget", 10.99], ["Gadget", 20.99]],
        border="horizontal",
    )

    yr.markdown("6. Pandas DataFrame")
    df = pd.DataFrame(
        {
            "Name": ["Item 7", "Item 8"],
            "Value": [700, 800],
            "Status": ["Active", "Inactive"],
        }
    )
    yr.table(df)


if __name__ == "__main__":
    table_agent()
