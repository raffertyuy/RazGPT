There are multiple ways to implement a chatbot. For example, see [here](https://learn.microsoft.com/en-us/azure/bot-service/bot-overview?view=azure-bot-service-4.0) for the different options from Microsoft.

This folder contains code for deploying bots to the [Azure AI Bot Service](https://azure.microsoft.com/en-us/products/ai-services/ai-bot-service). Each code is written using one of these tools:
- Pro-code (C#, NodeJS, Python) using the [Bot Framework SDK](https://learn.microsoft.com/en-us/azure/bot-service/index-bf-sdk?view=azure-bot-service-4.0)
- Low-code/No-code to C#/NodeJS code generation using the [Bot Framework Composer](https://learn.microsoft.com/en-us/composer/introduction?tabs=v2x)


## Available Bots
1. `/botcomposer-nodejs`: created using Bot Framework Composer (scrapped for now, with deployment issues).
2. `/botframework-nodejs-simple`: Simple bot created using the Bot Framework SDK. No dialogs implemented.
3. `/teamstoolkit-typescript-simple`: Discovered this handy [Teams Toolkit for VS Code](https://learn.microsoft.com/en-us/microsoftteams/platform/toolkit/install-teams-toolkit?tabs=vscode) to implement bots for teams, with adaptive cards.


## Azure Deployment
- There are two Azure services to provision, an _Azure Bot Service_ and the bot "app server".
- The code is deployed to the "app server", this is usually an _Azure App Service_ or _Azure Functions_.
- The messaging endpoint is then configured in the _Azure Bot Service_, in the format of `https://APPSERVICENAME.azurewebsites.net/api/messages`.
- The _Azure Bot Service_ is also configured to identify the channels you want this bot to be available to.
- See [official documentation](https://learn.microsoft.com/en-us/azure/bot-service/provision-and-publish-a-bot?view=azure-bot-service-4.0&tabs=multitenant%2Cjavascript)

At this time, I have successfully deployed to a Windows Azure App Service.
When deploying to Windows, run the following to generate a `web.config` file.
```
az bot prepare-deploy --lang <language> --code-dir "."
```

It should, in theory, also work with Linux. But I have not yet been successful in doing so.


## Useful Links for Adaptive Card Templating
- Samples: https://adaptivecards.io/samples/
- Designer: https://adaptivecards.io/designer/


## Limitations
At the time of this writing, both the Bot Framework SDK and Composer are last updated 2022 or earlier. Therefore I hit a few limitations before arriving to the created sample codes:

### Microsoft Bot Framework SDK
- Works with C# and NodeJS.
- Java and Python are to be retired from November 2023.
- NodeJS v16 is required, later versions do not work.

### Microsoft Bot Framework Composer
- Generates code with a `web.config` file which indicates Windows/IIS deployment.
- NodeJS support is still in preview
- Ability to publish to Azure App Services and Functions (Windows and Linux)
- No container support
- Have yet to deploy successfully...