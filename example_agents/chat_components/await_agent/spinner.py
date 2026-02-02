from time import sleep

import yera as yr


def process_data():
    sleep(1)


def validate_results():
    sleep(1)


@yr.agent(
    name="Spinner Agent",
    description="An agent that provides a visual indication of ongoing processing",
)
def spinner_agent():
    yr.markdown("This agent processes and validates data:")

    # Context manager syntax - creates an action block with lifecycle management
    with yr.spinner(message="Loading...") as s1:
        # Each update call overwrites the previous message
        s1.update(message="Processing data...")
        # Agent performs some time consuming action (e.g. tool use)...
        process_data()

        s1.update(message="Validating results...")
        validate_results()

    yr.markdown("Process completed successfully!")


if __name__ == "__main__":
    spinner_agent()
