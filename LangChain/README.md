This folder contains my experimentations as I learn LangChain.

## How to Run
The apps in this folder generally requires Python 3.

To keep this repo simple, [venv](https://docs.python.org/3/library/venv.html) isn't configured.
The python package dependencies are found in the `requirements.txt` of each respective folder. To ensure that required dependencies are installed, run:
```
pip install -r requirements.txt
```

## Completed
- `/notebooks` contain LangChain quickstarts and my own experimentation.
- `/orchestrator-completion-simple` is an orchestrator service app using the Completion API of Azure OpenAI `text-davinci-003`. This is the latest model in GA as of 2023-05-01.
- `/orchestrator-chat-simple` is an orchestrator service using the Chat Completion API of Azure OpenAI `gpt-35-turbo` or `gpt-4`. These models are still in public preview and not recommended for production as of 2023-05-01.
- `/orchestrator-chat-multisessions-inmemory` - keep track of conversation history by `sessionid`. The _LangChain Memory_ is stored **in-memory.** Which means the conversation history will clear when the web server restarts (or the client session times-out). If this is deployed in Azure App Services, make sure that **ARR Affinity** is enabled.
- `/orchestrator-azure-search` - is an orchestrator service based on [azure-search-openai-demo](https://github.com/Azure-Samples/azure-search-openai-demo). This allows you to that for using OpenAI to answer questions about your own data. This is a service suitable for chat applications (like MS Teams)


## Work in Progress
- none at the moment

## Not Started
- [ ] `/orchestrator-chat-redis` - a version of `/orchestrator-chat-multisessions-inmemory` but store the memory in Redis instead of in-memory, making this a stateless orchestrator.