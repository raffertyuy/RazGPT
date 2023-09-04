This folder contains my experimentations as I learn LangChain.

## How to Run
The apps in this folder generally requires Python 3.
Where `azure-identity` / `DefaultAzureCredential` is used, the [Azure Developer CLI](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/install-azd) is required. Authenticate `azd auth login` before running locally.

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
- `/orchestrator-azure-search-inmemory` - is an orchestrator service based on [azure-search-openai-demo](https://github.com/Azure-Samples/azure-search-openai-demo). This allows you to that for using OpenAI to answer questions about your own data. This is a service suitable for chat applications (like MS Teams). The conversation history is stored in memory using [ConversationSummaryBufferMemory](https://python.langchain.com/docs/modules/memory/types/summary_buffer).
- `/orchestrator-azure-search-redis-memory` - This is a version of the above using Redis as a persistent memory storage. But due to [this issue](https://github.com/langchain-ai/langchain/issues/3072), we are using [ConversationBufferWindowMemory](https://python.langchain.com/docs/modules/memory/types/buffer_window) instead.
- `/orchestrator-azure-search-mongodb-memory` - a version of `/orchestrator-azure-search-redis-memory`, for long-term storage of chat messages. _(Observation: MongoDB is slower than Redis, but but I'm not certain if it's simply because of differences in pricing tier.)_
- `/orchestrator-azure-search-chatmodelonly-mongodb-memory` - this version uses chat models only (`gpt-35-turbo`) because new Azure subscriptions can no longer get the older `text-davinci-003`.
- `/orchestrator-azure-search-dbindex-mongodb-memory` - this version users a search index based on an Azure SQL table/view data source.

## Not Started / Work in Progress
- No backlog for this folder at the moment.