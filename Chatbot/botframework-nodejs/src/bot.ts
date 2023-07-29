import { ActivityHandler, MessageFactory } from 'botbuilder';

export class GptBot extends ActivityHandler {
    constructor() {
        super();

        // Retrieve Configuration
        const config = require('config');
        let orchestratorBaseUrl = config.get('orchestrator.baseurl');
        let orchestratorSearchIndex = config.get('orchestrator.searchindex');
        console.log(`Orchestrator Base URL: ${orchestratorBaseUrl}`)
        console.log(`Orchestrator Search Index: ${orchestratorSearchIndex}`)

        // See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.
        this.onMessage(async (context, next) => {
            const replyText = `Echo: ${ context.activity.text }`;
            await context.sendActivity(MessageFactory.text(replyText, replyText));
            // By calling next() you ensure that the next BotHandler is run.
            await next();
        });

        this.onMembersAdded(async (context, next) => {
            const membersAdded = context.activity.membersAdded;
            const welcomeText = 'Hello and welcome!';
            for (const member of membersAdded) {
                if (member.id !== context.activity.recipient.id) {
                    await context.sendActivity(MessageFactory.text(welcomeText, welcomeText));
                }
            }
            // By calling next() you ensure that the next BotHandler is run.
            await next();
        });
    }
}
