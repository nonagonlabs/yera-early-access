# Yera Early Access

Firstly we'd like to thank you so much for your time!

This is our very early access product where we learn and iterate. 
Please forgive the rough edges. 

We want to learn as much as possible while helping you with your AI use cases.
If you have any questions, concerns or just want some guidance we are always happy to
help.

The best way to get in touch is the Slack channel you should be in, or email us.
We're also getting a Discord lined up because we appear to be outgrowing the Slack channel 
already.

## Introduction

We're developing Yera as a better way to use AI in your workflows. It is designed to
have the great UX of Streamlit while having the safety and governance features that
enable use in enterprise.

In brief: for you, a developer

> seamlessly build end-to-end AI apps in Python - logic, UI, testing, deployment (like Streamlit).

and then for your management

> empower your devs to actually ship the AI stuﬀ you promised your boss.

## Getting Started

### Prerequisites

The minimum supported python version is 3.10. The library is tested in our cicd jobs on 
3.10, 3.11 and 3.12. Yera currently supports the following providers:

- OpenAI
- Anthropic
- Ollama (if installed)
- Llamacpp (if installed)
- Azure AI Foundry (OpenAI model deployments only)

In the next iteration we'll be adding
- AWS Bedrock
- The rest of Azure Foundry
- Mistral

Yera's setup will try to detect your creds and available models on setup. More on that
in the setup section.

This has not been tested on Windows yet. If any of you guys have trouble please let us 
know straight away. 

### Installation

We recommend using [uv](https://astral.sh/uv) to install to a project

```shell
uv add yera
```

or to install the yera CLI globally

```shell
uv tool install yera
```

but you can also pip install as normal.

```shell
pip install yera
```

By default, Yera has a lightweight set of model provider dependencies (openai, anthropic)
if you want `llama-cpp` or `ollama` there are extras under `yera[llama-cpp]` and
`yera[ollama]`.

### Setup

**N.B.** you may get a notification from your system
keychain asking for permission to use it. This is normal and is how Yera stores credentials safely.

You can kick off this whole process with

```
yera setup  # uv tool or pip install
```
or if you did `uv add`
```shell
uv run yera setup
```

an explanation of what it does is below. 

Yera has a command line setup helper that will automatically set up your config, credentials
and find your available models. For each provider the auto-discovery requires the following

- **OpenAI**: an `OPENAI_API_KEY` env variable
- **Anthropic**: an `ANTHROPIC_API_KEY` env variable
- **Azure**: you must be logged in with `az login`
- **Ollama**: ollama just has to be up and running
- **Llama-cpp**: it will look in `./model` then a user-level data directory determined 
by `platformdirs.user_data_dir` (OS-dependent: on macOS it's 
`/Users/<your name>/Library/Application Support`)

Your credentials will be added to your operating system keyring so Yera knows where
to find them. This is encrypted at rest and much more secure than env vars, .env files
and secrets.jsons. After this Yera will query each provider for available models and
add them to your `yera.toml`.

By default, this is user-level (`~/.config/yera/yera.toml`) rather than project-level
(`./yera.toml`).

For any provider yera doesn't find it'll ask you if you want to add it manually.

Finally, after all your models are added to config it'll ask you to enter which one you
want to use as default. We assume you've chosen a default model for the rest of our docs
unless stated otherwise.

### Your First App

Now you're all set up let's make a basic chatbot to test everything hangs together.
Create a py file called `chatbot.py` and write the following

```python
import yera as yr
@yr.agent
def chatbot():
    while True:
        prompt = yr.text_input()

        if prompt.startswith("/quit"):
            yr.quit()
            break

        yr.chat(prompt)
```

Once that's ready you can run it in the CLI.

```shell
yera run chatbot.py
```
or if you ran `uv add`
```shell
uv run yera run chatbot.py
```

You should see a browser window open running your first chatbot.
If that's all worked you're ready to start on our tutorial notebooks.

### Running notebooks

```shell
uv run jupyter lab
```

Interactive Yera agents can be invoked in a notebook to commence an in-line conversation, eg [Basic Chatbot](tutorials/Basic%20Chatbot.ipynb).

You can also invoke pipeline agents which run autonomously, without user interaction, eg [Entity Recognition Demo](tutorials/Entity%20Recognition%20Demo.ipynb).

### CLI Reference

The CLI has four commands:

- `yera run` runs a yera app from a single `.py` file.
- `yera dev` discovers the Yera apps you have available in the run directory and makes
  them available in the UI for you to try out.
- `yera setup` handles yera config and creds setup.
- `yera show` prints information on the specified objects to the terminal.

Use the `--help` flag with any of the above commands to learn more about their usage and parameters.

## Info Resources

The early access examples repo can be found
[here](https://github.com/nonagonlabs/yera-early-access)

### Tutorial Notebooks

#### Tutorial 1: Basic Chatbot

This tutorial introduces the basic features of the Yera library. It guides you through
the same chatbot example as above but goes into detail on each top-level function used,
and how to invoke an agent within jupyter.

#### Tutorial 2: Structured Generation

This tutorial demonstrates how to use Yera to do structured generation. It will guide
you through how to define a struct and then fill it. In this case it's knowledge graphs.
The interactive graphs in this example use `pyvis` which you might need to install.

#### In the Works

- **Tutorial 3**: Tool Usage - structured data extract in a cybersecurity context.
  Uses tools to get data and then add the inferred structs to a database.
- **Tutorial 4**: Workspaces - what are workspaces, how are they shared and segregated?
- **Tutorial 5**: Multi-agent Systems - easy orchestration via functions and decorators.

### Reference Examples

Many examples under `example_agents/chat_components`. Each of these shows how to use
a different UI element in your Yera app. This includes buttons, sliders, markdown,
tables and many more.

### Miscellaneous Demos

- Widget Builder
- Cyberscurity Report Log
