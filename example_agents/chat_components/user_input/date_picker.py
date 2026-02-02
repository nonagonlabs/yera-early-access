import yera as yr


@yr.agent(
    name="Date Picker Agent",
    description="An agent that allows users to select a date from a calendar",
)
def date_picker_agent():
    yr.markdown("This date picker has a default date set to '2025-01-01':")
    date_1 = yr.date_picker(default_date="2025-01-01", label="Select another date")
    yr.markdown(f"You selected **{date_1}**!")

    yr.markdown("If not specificed, defaults to today's date:")
    date_2 = yr.date_picker(label="Select a date")
    yr.markdown(f"You selected **{date_2}**!")


if __name__ == "__main__":
    date_picker_agent()
