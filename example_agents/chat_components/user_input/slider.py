import yera as yr


@yr.agent(
    name="Slider Agent",
    description="An agent that allows users to select a float value from a slider",
)
def slider_agent():
    yr.markdown("This slider has a default value set to 20:")
    value_1 = yr.slider(
        min_value=0, max_value=100, default_value=20, label="Select a value"
    )
    yr.markdown(f"You selected **{value_1}**!")

    yr.markdown("If not specificed, defaults to midpoint:")
    value_2 = yr.slider(min_value=0, max_value=10, label="Select another value")
    yr.markdown(f"You selected **{value_2}**!")


if __name__ == "__main__":
    slider_agent()
