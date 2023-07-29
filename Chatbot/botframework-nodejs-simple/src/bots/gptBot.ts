import { ActivityHandler, MessageFactory } from 'botbuilder';

export class GptBot extends ActivityHandler {
    constructor() {
        super();

        // See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.
        this.onMessage(async (context, next) => {
            const replyText = `Echo: ${ context.activity.text }`;

            const axios = require('axios');
            let response = await axios.post(`${process.env.ORCHESTRATOR_URL}/chat`, {
                sessionid: context.activity.conversation.id,
                message: context.activity.text,
                searchindex: process.env.SEARCH_INDEX
            });
            
            if (response.status != 200)
                console.log(`ERROR: ${response.status} ${response.statusText}`);
            else {
                await context.sendActivity(MessageFactory.text(`${response.data.response} (Total Tokens: ${response.data.total_tokens})`));
            }
            
            // By calling next() you ensure that the next BotHandler is run.
            await next();
        });

        this.onMembersAdded(async (context, next) => {
            const membersAdded = context.activity.membersAdded;
            const welcomeText = 'Hi, I\'m Raynor! Your GPT-powered AI assistant. How can I help you today?';
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
