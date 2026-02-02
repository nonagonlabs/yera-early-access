import yera as yr


@yr.agent(
    name="Text Input Agent",
    description="An agent that requests free-form textual input from users",
)
def text_input_agent():
    name = yr.text_input("What is your name?")
    yr.markdown(f"Hello, {name}!")


if __name__ == "__main__":
    text_input_agent()
