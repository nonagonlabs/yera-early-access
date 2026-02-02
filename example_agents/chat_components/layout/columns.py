import yera as yr


@yr.agent(
    name="Columns Agent",
    description="An agent that sends content laid out in columns to the user",
)
def columns_agent():
    yr.markdown(
        "Here is a columns layout with a border, containing three markdown columns:"
    )
    with yr.columns(3, border=True):
        yr.markdown(content="Column 1")
        yr.markdown(content="Column 2")
        yr.markdown(content="Column 3")


if __name__ == "__main__":
    columns_agent()
