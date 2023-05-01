This folder contains my experimentations as I learn LangChain.

- `/notebooks` contain LangChain quickstarts and my own experimentation.
- `/orchestrator-completion-simple` is an orchestrator service app using the Completion API of Azure OpenAI `text-davinci-003`. This is the latest model in GA as of 2023-05-01.
- `/orchestrator-chat-simple` is an orchestrator service using the Chat Completion API of Azure OpenAI `gpt-35-turbo` or `gpt-4`. These models are still in public preview and not recommended for production as of 2023-05-01.

## Known Issues / TODO
- The orchestrator services keep a single memory session for all API callers. Figure out how it can have a **separate memory per `sessionId`**
- Create another sample app that integrates with cognitive search