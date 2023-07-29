There are multiple ways to implement a chatbot, depending on the channel.

Microsoft offers **two** solutions:
1. [Power Virtual Agents](https://powervirtualagents.microsoft.com/): Hosted Low-code/no-code solution
2. [Azure AI Bot Service](https://azure.microsoft.com/en-us/products/ai-services/ai-bot-service)
    - Pro-code (C#, NodeJS, Python) using the [Bot Framework SDK](https://learn.microsoft.com/en-us/azure/bot-service/index-bf-sdk?view=azure-bot-service-4.0)
    - Low-code/No-code to C#/NodeJS code generation using the [Bot Framework Composer](https://learn.microsoft.com/en-us/composer/introduction?tabs=v2x)

## Bots Available
This folder is planned to contain multiple chatbot code samples that integrate with LLMs. At the moment it contains one:
- [ ] [botcomposer-nodejs](./botcomposer-nodejs/): created using Bot Framework Composer. Still with deployment issues)
- [ ] [botframework-nodejs](./botframework-nodejs/): created using Bot Framework SDK.


### Limitations
At the time of this writing, both the Bot Framework SDK and Composer are last updated 2022 or earlier. Therefore I hit a few limitations before arriving to the created sample codes:

**Microsoft Bot Framework SDK**
- NodeJS quickstart does not run
- Python quickstart requires v3.10 or earlier
- Haven't tried the C# quickstart yet...

**Microsoft Bot Framework Composer**
- Generates code with a `web.config` file which indicates Windows/IIS deployment.
- NodeJS support is still in preview
- Ability to publish to Azure App Services and Functions (Windows and Linux)
- No container support