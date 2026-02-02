import yera as yr


@yr.agent(
    name="Markdown Agent",
    description="An agent that sends markdown formatted content to the user",
)
def markdown_agent():
    @yr.agent
    def markdown_subagent_1():
        yr.markdown("Can send with initial content and new lines")
        with yr.markdown("**1...**") as m1:
            m1.new_line("**2...**")
            m1.new_line("**3...**")

    @yr.agent
    def markdown_subagent_2():
        yr.markdown("... or append without initial content")
        with yr.markdown() as m2:
            m2.append("**Foo ")
            m2.append("Bar ")
            m2.append("FooBar!**")

    yr.markdown("Direct call syntax - creates a single markdown block")
    yr.markdown("**Hello, world!**")

    yr.markdown(
        "Context manager syntax - allows creating multiple chunks of the same block"
    )

    markdown_subagent_1()
    markdown_subagent_2()


if __name__ == "__main__":
    markdown_agent()
