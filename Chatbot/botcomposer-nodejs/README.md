This code is for deploying a simple chatbot to [Azure AI Bot Service](https://azure.microsoft.com/en-us/products/ai-services/ai-bot-service) using the [Microsoft Bot Framework Composer](https://learn.microsoft.com/en-us/composer/introduction?tabs=v2x) (v2.1.2).

### Running the App
1. Have an orchestrator service deployed. See [samples](/LangChain/).
2. Update the `chatUrl` and `feedbackUrl` values in the [./settings/appsettings.json](./settings/appsettings.json).
3. Open this folder using the [Microsoft Bot Framework Composer](https://learn.microsoft.com/en-us/composer/introduction?tabs=v2x)
4. Run locally or deploy to your Azure subscription using the tool (see [documentation](https://learn.microsoft.com/en-us/composer/))

### Bot Composer Creation Settings
- Language: **NodeJS (Preview)**
- Template: **Empty Bot**
- Runtime Type: **Azure Web App**