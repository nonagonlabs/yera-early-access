from time import sleep

import yera as yr


def process_data():
    sleep(1)


def validate_results():
    sleep(1)


def fetch_resources():
    sleep(1)


def fold_laundry():
    sleep(1)


def finalise_operations():
    sleep(1)


def put_away_clothes():
    sleep(1)


@yr.agent(
    name="Action Agent",
    description="An agent that keeps the user updated on the progress of tasks",
)
def action_agent():
    @yr.agent
    def action_subagent():
        yr.markdown("This agent interleaves actions from two ongoing processes:")
        # Multiple action blocks can run concurrently with concurrent actions
        with (
            yr.action(message="Starting task 2") as a2,
            yr.action(message="Starting task 3") as a3,
        ):
            a2.update(message="Fetching resources")
            fetch_resources()
            a3.update(message="Folding laundry")
            fold_laundry()

            a2.update(message="Finalising operations")
            finalise_operations()
            a3.update(message="Putting away clothes")
            put_away_clothes()

            a2.update(message="Task 2 complete")
            a3.update(message="Task 3 complete")
            # Both blocks complete when their contexts exit (LIFO order)

    # Context manager syntax - creates an action block with lifecycle management
    yr.markdown("This agent processes and validates data:")
    with yr.action(message="Starting task 1") as a1:
        # Each update call adds a new action to the list
        a1.update(message="Processing data")
        # Agent performs some time consuming action (e.g. tool use)...
        process_data()

        a1.update(message="Validating results")
        validate_results()

        a1.update(message="Task 1 complete")

    action_subagent()


if __name__ == "__main__":
    action_agent()
