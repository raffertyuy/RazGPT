_Last updated: 2023-05-01_

There are two sample apps in this folder, both of which works.
1. `app-completion.py` shows the method for creating a chat app using Azure OpenAI GPT-3 (text-davinci-003). This is preferred for production purposes, as `text-davinci-003` is in GA.
2. `app-chat.py` shows the method for creating a chat app using Azure OpenAI GPT 3.5 or 4, which uses a new API called Chat Completions. Note that both of these models are in public preview as at this time.