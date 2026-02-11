import yera as yr


@yr.agent(
    name="Success Agent", description="An agent that demonstrates successful completion"
)
def success_agent():
    yr.markdown("This agent demonstrates successful completion.")


if __name__ == "__main__":
    success_agent()
