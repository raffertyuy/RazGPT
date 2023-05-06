This folder contains my experimentations as I learn LangChain.

## How to Run
The apps in this folder generally requires Python 3.

To keep this repo simple, [venv](https://docs.python.org/3/library/venv.html) isn't configured.
So in order to run, the following python packages must be installed (i.e. `pip install <package_name>`):
- openai
- langchain
- python-dotenv
- Flask
- request
- jsonify
- and maybe more...

## Completed
- `/notebooks` contain LangChain quickstarts and my own experimentation.
- `/orchestrator-completion-simple` is an orchestrator service app using the Completion API of Azure OpenAI `text-davinci-003`. This is the latest model in GA as of 2023-05-01.
- `/orchestrator-chat-simple` is an orchestrator service using the Chat Completion API of Azure OpenAI `gpt-35-turbo` or `gpt-4`. These models are still in public preview and not recommended for production as of 2023-05-01.
- [ ] `/orchestrator-chat-multisessions-inmemory` - keep track of conversation history by `sessionid`. The _LangChain Memory_ is stored **in-memory.** Which means the conversation history will clear when the web server restarts (or the client session times-out).


## Work in Progress
- [ ] `/orchestrator-chat-multisessions` - have multiple memories by `sessionId`

## Not Started
- [ ] `/orchestrator-chat-search` - a version of [this sample](https://github.com/Azure-Samples/azure-search-openai-demo) that returns a simple response suitable for chat applications (like MS Teams)