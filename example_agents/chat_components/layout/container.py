import pandas as pd

import yera as yr

employee_data = pd.DataFrame(
    {
        "Name": ["Alice Smith", "Bob Johnson", "Carol Lee"],
        "Email": [
            "alice@example.com",
            "bob.johnson@company.com",
            "carol.lee@company.com",
        ],
    }
)


@yr.agent(
    name="Container Agent",
    description="An agent that sends content laid out in containers to the user",
)
def container_agent():
    yr.markdown("Here is a basic container with a border, some markdown, and a table:")
    with yr.container(border=True):
        yr.markdown(content="Outer Markdown 1")
        yr.markdown(content="Outer Markdown 2")
        yr.table(data=employee_data)

    yr.markdown(
        "Here is a container without a border, containing some markdown and a nested container with a border:"
    )
    with yr.container():
        yr.markdown(content="Outer Markdown 1")
        with yr.columns(3, border=True):
            yr.markdown(content="Column 1")
            yr.markdown(content="Column 2")
            yr.markdown(content="Column 3")
        yr.markdown(content="Outer Markdown 2")


if __name__ == "__main__":
    container_agent()
