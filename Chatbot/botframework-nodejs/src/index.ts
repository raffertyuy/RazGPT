import { config } from 'dotenv';
import { INodeSocket } from 'botframework-streaming';
import * as path from 'path';
import * as restify from 'restify';

// Import required bot services.
// See https://aka.ms/bot-services to learn more about the different parts of a bot.
import {
    CloudAdapter,
    ConfigurationBotFrameworkAuthentication,
    ConfigurationBotFrameworkAuthenticationOptions,
    ConversationState,
    MemoryStorage,
    UserState
} from 'botbuilder';

// This bot's main dialog.
import { GptBot } from './bots/gptBot';
//import { QueryDialog } from './dialogs/queryDialog';

// Read environment variables from .env file
const ENV_FILE = path.join(__dirname, '.env');
config({ path: ENV_FILE });

console.log(`.env file path ${ENV_FILE}`)
console.log(`Orchestrator Base URL: ${process.env.ORCHESTRATOR_URL}`)

const botFrameworkAuthentication = new ConfigurationBotFrameworkAuthentication(process.env as ConfigurationBotFrameworkAuthenticationOptions);

// Create adapter.
// See https://aka.ms/about-bot-adapter to learn more about adapters.
const adapter = new CloudAdapter(botFrameworkAuthentication);

// Catch-all for errors.
const onTurnErrorHandler = async (context, error) => {
    // This check writes out errors to console log .vs. app insights.
    // NOTE: In production environment, you should consider logging this to Azure
    //       application insights.
    console.error(`\n [onTurnError] unhandled error: ${ error }`);

    // Send a trace activity, which will be displayed in Bot Framework Emulator
    await context.sendTraceActivity(
        'OnTurnError Trace',
        `${ error }`,
        'https://www.botframework.com/schemas/error',
        'TurnError'
    );

    // Send a message to the user
    await context.sendActivity('The bot encountered an error or bug.');
    await context.sendActivity('To continue to run this bot, please fix the bot source code.');

    // Clear out state
    await conversationState.delete(context);
};

// Set the onTurnError for the singleton CloudAdapter.
adapter.onTurnError = onTurnErrorHandler;

// Define the state store for your bot.
// See https://aka.ms/about-bot-state to learn more about using MemoryStorage.
// A bot requires a state storage system to persist the dialog and user state between messages.
const memoryStorage = new MemoryStorage();

// Create conversation state with in-memory storage provider.
const conversationState = new ConversationState(memoryStorage);
const userState = new UserState(memoryStorage);

// Create the main dialog.
//const dialog = new QueryDialog();
const bot = new GptBot(conversationState, userState, null);

// Create HTTP server.
const server = restify.createServer();
server.use(restify.plugins.bodyParser());

server.listen(process.env.port || process.env.PORT || 3978, () => {
    console.log(`\n${server.name} listening to ${server.url}`);
});

// Listen for incoming requests.
server.post('/api/messages', async (req, res) => {
    // Route received a request to adapter for processing
    await adapter.process(req, res, (context) => bot.run(context));
});

// Listen for Upgrade requests for Streaming.
server.on('upgrade', async (req, socket, head) => {
    // Create an adapter scoped to this WebSocket connection to allow storing session data.
    const streamingAdapter = new CloudAdapter(botFrameworkAuthentication);

    // Set onTurnError for the CloudAdapter created for each connection.
    streamingAdapter.onTurnError = onTurnErrorHandler;

    await streamingAdapter.process(req, socket as unknown as INodeSocket, head, (context) => bot.run(context));
});
