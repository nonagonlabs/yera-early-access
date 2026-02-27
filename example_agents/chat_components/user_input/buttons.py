import yera as yr


def list_portfolios() -> list[str]:
    return ["High Growth", "ETFs", "CryptoDerivatives", "Commodities"]


@yr.agent(
    name="Buttons Agent",
    description="An agent that only allows users to select from a finite set of options",
)
def buttons_agent():
    yr.markdown("This agent allows users to select from a finite set of options:")

    # Direct call syntax - creates a buttons block with options and label
    choice_1 = yr.buttons(
        options=["Option A", "Option B", "Option C"], label="Choose an option"
    )

    yr.markdown(f"You selected **{choice_1}**!")

    yr.markdown(
        "Only allowing users to select from a finite set of options enforces stricter conversation flow."
    )
    choice_2 = yr.buttons(
        options=list_portfolios(), label="Select the portfolio you would like to manage"
    )
    yr.markdown(f"You selected portfolio **{choice_2}**!")


if __name__ == "__main__":
    buttons_agent()
