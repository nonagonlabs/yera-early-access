import yera as yr


@yr.agent(name="Chatbot", description="The most basic chatbot")
def chatbot():
    while True:
        prompt = yr.text_input()

        if prompt == "/quit":
            yr.quit()
            return

        yr.chat(prompt)
