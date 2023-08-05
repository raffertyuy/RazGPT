import {
  TeamsActivityHandler,
  CardFactory,
  MessageFactory,
  TurnContext,
  AdaptiveCardInvokeValue,
  AdaptiveCardInvokeResponse,
} from "botbuilder";
import rawResponseCard from "./adaptiveCards/response.json";
import rawFeedbackCard from "./adaptiveCards/feedback.json";
import rawRestartCard from "./adaptiveCards/restart.json";
import { AdaptiveCards } from "@microsoft/adaptivecards-tools";

import { v4 as uuidv4 } from 'uuid';
import { invoke } from "lodash";

const ACData = require('adaptivecards-templating');
const sessionIds: { [key: string]: string } = {};
const welcomeText = 'Hi, I\'m Raynor! Your GPT-powered AI assistant. How can I help you today?';

export class TeamsBot extends TeamsActivityHandler {
  constructor() {
    super();

    this.onMessage(async (context, next) => {
      console.log("Running with Message Activity.");

      let txt = context.activity.text;
      const removedMentionText = TurnContext.removeRecipientMention(context.activity);
      if (removedMentionText) {
        // Remove the line break
        txt = removedMentionText.toLowerCase().replace(/\n|\r/g, "").trim();
      }

      console.log(`[MessageActivity] ${txt}}`);

      // Trigger command by IM text
      switch (txt) {
        case "feedback": {
          const card = AdaptiveCards.declareWithoutData(rawFeedbackCard).render();
          await context.sendActivity({ attachments: [CardFactory.adaptiveCard(card)] });
          break;
        }
        case "restart": {
          const template = new ACData.Template(rawRestartCard);
          const templateData = {
            areButtonsVisible: true
          };

          const adaptiveCard = template.expand({
            $root: templateData
          });

          await context.sendActivity({
            attachments: [CardFactory.adaptiveCard(adaptiveCard)]
          });

          break;
        }
        default: {
          console.log(`Sending POST to ${process.env.ORCHESTRATOR_URL}/chat`);

          let sessionid = sessionIds[context.activity.conversation.id] || (sessionIds[context.activity.conversation.id] = uuidv4());

          const axios = require('axios');
          let response = await axios.post(`${process.env.ORCHESTRATOR_URL}/chat`, {
            sessionid: sessionid,
            message: context.activity.text,
            searchindex: process.env.SEARCH_INDEX
          });

          let responseText = "";
          if (response.status != 200) {
            console.log(`ERROR: ${response.status} ${response.statusText}`);
            responseText = "Oops! Something went wrong. Please try again later.";
          }
          else {
            responseText = `${response.data.response} (Total Tokens: ${response.data.total_tokens})`;
          }

          const template = new ACData.Template(rawResponseCard);
          const templateData = {
            response: responseText,
            areButtonsVisible: true
          };

          const adaptiveCard = template.expand({
            $root: templateData
          });

          await context.sendActivity({
            attachments: [CardFactory.adaptiveCard(adaptiveCard)]
          });
        }
      }

      // By calling next() you ensure that the next BotHandler is run.
      await next();
    });

    this.onMembersAdded(async (context, next) => {
      const membersAdded = context.activity.membersAdded;

      for (let cnt = 0; cnt < membersAdded.length; cnt++) {
        if (membersAdded[cnt].id) {
          await context.sendActivity(MessageFactory.text(welcomeText, welcomeText));
          break;
        }
      }
      await next();
    });
  }

  // Invoked when an action is taken on an Adaptive Card. The Adaptive Card sends an event to the Bot and this
  // method handles that event.
  async onAdaptiveCardInvoke(
    context: TurnContext,
    invokeValue: AdaptiveCardInvokeValue
  ): Promise<AdaptiveCardInvokeResponse> {
    console.log("Running onAdaptiveCardInvoke with verb " + invokeValue.action.verb + ".")

    switch (invokeValue.action.verb) {
      case "thumbsup": {
        console.log("[Running onAdaptiveCardInvoke] Thumbs Up");

        // TODO: Send to Feedback to API


        // TODO: Disable buttons. The following doesn't work because context.activity.text is empty.
        // const template = new ACData.Template(rawResponseCard);
        // const templateData = {
        //   response: context.activity.text,
        //   areButtonsVisible: false
        // };

        // const adaptiveCard = template.expand({
        //   $root: templateData
        // });

        // await context.updateActivity({
        //   type: "message",
        //   id: context.activity.replyToId,
        //   attachments: [CardFactory.adaptiveCard(adaptiveCard)]
        // });

        // Send message
        let message = "Thank you for your feedback!";
        await context.sendActivity(MessageFactory.text(message, message));

        break;
      }
      case "thumbsdown": {
        console.log("[Running onAdaptiveCardInvoke] Thumbs Down");

        // TODO: Send to Feedback to API
        

        // TODO: Disable buttons

        
        // Send message
        let message = "Thank you for your feedback! I'm sorry that my response didn't help. If you would like to share more, please type 'feedback'";
        await context.sendActivity(MessageFactory.text(message, message));
        break;
      }
      case "restart-yes": {
        console.log("[Running onAdaptiveCardInvoke] Restart confirmed.");

        // Disable buttons
        const template = new ACData.Template(rawRestartCard);
        const templateData = {
          areButtonsVisible: false
        };

        const adaptiveCard = template.expand({
          $root: templateData
        });

        await context.updateActivity({
          type: "message",
          id: context.activity.replyToId,
          attachments: [CardFactory.adaptiveCard(adaptiveCard)]
        });

        // Generate new Session ID
        sessionIds[context.activity.conversation.id] = uuidv4();
        await context.sendActivity(MessageFactory.text(welcomeText, welcomeText));

        break;
      }
      case "restart-no": {
        console.log("[Running onAdaptiveCardInvoke] Restart cancelled.");

        // Disable buttons
        const template = new ACData.Template(rawRestartCard);
        const templateData = {
          areButtonsVisible: false
        };

        const adaptiveCard = template.expand({
          $root: templateData
        });

        await context.updateActivity({
          type: "message",
          id: context.activity.replyToId,
          attachments: [CardFactory.adaptiveCard(adaptiveCard)]
        });

        // Send message
        let message = "Okay then, let's continue.";
        await context.sendActivity(MessageFactory.text(message, message));

        break;
      }
      default: {
        console.log("[Running onAdaptiveCardInvoke] Unknown Verb");
        // do nothing
      }
    }

    return { statusCode: 200, type: undefined, value: undefined };
  }
}
