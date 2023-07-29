This code is for deploying a simple chatbot to [Azure AI Bot Service](https://azure.microsoft.com/en-us/products/ai-services/ai-bot-service) using the [Microsoft Bot Framework SDK](https://learn.microsoft.com/en-us/azure/bot-service/index-bf-sdk?view=azure-bot-service-4.0).

The starter code used is the Echo Bot from the [documentation quickstart](https://learn.microsoft.com/en-us/azure/bot-service/bot-service-quickstart-create-bot?view=azure-bot-service-4.0&tabs=javascript%2Cvs), which requires NodeJS v16 to run properly.

## Running the App
1. Create a folder `./config` and copy the files from `./config-sample`
2. Populate the configuration values in `./config`
3. `npm install`
4. `npm start`
5. Use the [Microsoft Bot Framework Emulator](https://learn.microsoft.com/en-us/azure/bot-service/bot-service-debug-emulator?view=azure-bot-service-4.0&tabs=javascript) for debugging