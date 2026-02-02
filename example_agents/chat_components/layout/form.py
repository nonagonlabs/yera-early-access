import datetime

import yera as yr


@yr.agent(
    name="Form Agent",
    description="An agent that sends an interactive data-collection form to the user",
)
def form_agent():
    yr.markdown("Here is a form with buttons, a slider, and a date picker:")
    
    with yr.form(border=True) as f:
        yr.markdown(content="Form Header")
        yr.buttons(
            options=["Option 1", "Option 2", "Option 3"],
            label="Choose an option",
        )
        yr.slider(min_value=0, max_value=100, label="Select a value", default_value=30)
        yr.date_picker(label="Select a date", default_date=datetime.date(2025, 1, 15))
    
    button_value, slider_value, date_picker_value = f.result()
    
    yr.markdown(f"Button value: {button_value}")
    yr.markdown(f"Slider value: {slider_value}")
    yr.markdown(f"Date picker value: {date_picker_value}")


if __name__ == "__main__":
    form_agent()
