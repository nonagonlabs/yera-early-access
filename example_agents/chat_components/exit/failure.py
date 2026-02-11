import yera as yr


@yr.agent(
    name="Failure Agent", description="An agent that demonstrates failure handling"
)
def failure_agent():
    yr.markdown("This agent raises an exception to demonstrate failure handling.")
    raise Exception("This is a test failure")  # noqa: TRY002


if __name__ == "__main__":
    failure_agent()
