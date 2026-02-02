import yera as yr


# Define a struct for the widgets
# Agents can fill structs like this from unstructured text using the `.fill()` method
class Widgets(yr.Struct):
    class Widget(yr.Struct):
        mass: float
        volume: float
        name: str

        def density(self):
            return self.mass / self.volume

    widgets: list[Widget]

    def total_mass(self):
        return sum(w.mass for w in self.widgets)

    def mean_density(self):
        return sum(w.density() for w in self.widgets) / len(self.widgets)

    def summary_table(self):
        import pandas as pd

        return pd.DataFrame(w.model_dump() for w in self.widgets)

    def markdown_summary(self):
        with yr.markdown("# Widgets:") as m:
            m.new_line("## Aggregate stats")
            m.new_line(f"  densities: {[w.density() for w in self.widgets]}")
            m.new_line(f"  total mass: {self.total_mass()}")
            m.new_line(f"  mean density: {self.mean_density()}")

        yr.table(self.summary_table())


@yr.agent(name="Widget Builder", description="An agent that builds widgets")
def widget_builder() -> None:
    while True:
        prompt = yr.text_input()

        if prompt == "/quit":
            yr.quit()
            break

        if prompt.startswith("/create "):
            res = Widgets.fill(prompt[8:])
            res.markdown_summary()
        else:
            res = yr.chat(prompt)
            yr.markdown(f"response stats: {len(res)} chars long")
