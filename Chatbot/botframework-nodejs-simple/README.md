This code is for deploying a simple chatbot to [Azure AI Bot Service](https://azure.microsoft.com/en-us/products/ai-services/ai-bot-service) using the [Microsoft Bot Framework SDK](https://learn.microsoft.com/en-us/azure/bot-service/index-bf-sdk?view=azure-bot-service-4.0).

The starter code used is the Echo Bot from the [documentation quickstart](https://learn.microsoft.com/en-us/azure/bot-service/bot-service-quickstart-create-bot?view=azure-bot-service-4.0&tabs=javascript%2Cvs), which requires NodeJS v16 to run properly.

## Initial Configuration
1. In the root directory (same directory as this README.md), create a `.env` file
2. Copy the contents from `.env.example` and populate the values.

## Running the App Locally
1. `npm install`
2. `npm run start-dev`
3. Use the [Microsoft Bot Framework Emulator](https://learn.microsoft.com/en-us/azure/bot-service/bot-service-debug-emulator?view=azure-bot-service-4.0&tabs=javascript) for debugging