import { ActivityHandler, BotState, ConversationState, StatePropertyAccessor, UserState, MessageFactory } from 'botbuilder';
import { Dialog, DialogState } from 'botbuilder-dialogs';
//import { QueryDialog } from '../dialogs/queryDialog';

export class GptBot extends ActivityHandler {
    private conversationState: BotState;
    private userState: BotState;
    private dialog: Dialog;
    private dialogState: StatePropertyAccessor<DialogState>;

    /**
     *
     * @param {ConversationState} conversationState
     * @param {UserState} userState
     * @param {Dialog} dialog
     */
    constructor(conversationState: BotState, userState: BotState, dialog: Dialog) {
        super();

        if (!conversationState) throw new Error('[DialogBot]: Missing parameter. conversationState is required');
        if (!userState) throw new Error('[DialogBot]: Missing parameter. userState is required');
        //if (!dialog) throw new Error('[DialogBot]: Missing parameter. dialog is required');

        this.conversationState = conversationState as ConversationState;
        this.userState = userState as UserState;
        //this.dialog = dialog;
        //this.dialogState = this.conversationState.createProperty('DialogState');

        // See https://aka.ms/about-bot-activity-message to learn more about the message and other activity types.
        this.onMessage(async (context, next) => {
            const replyText = `Echo: ${ context.activity.text }`;
            await context.sendActivity(MessageFactory.text(replyText, replyText));
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
