import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import json

from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)
from langchain.schema import (
    BaseMessage,
    SystemMessage,
    AIMessage,
    HumanMessage
)
from langchain.chains import ConversationChain
from langchain.llms import AzureOpenAI
from langchain.chat_models import AzureChatOpenAI
from langchain.memory import ConversationSummaryBufferMemory
from langchain.callbacks import get_openai_callback

import Prompts

# Load Environment Variables
load_dotenv()

CHAT_API_VERSION = os.environ.get("OPENAI_CHAT_API_VERSION", "2023-03-15-preview")
CHAT_DEPLOYMENT = os.environ.get("OPENAI_CHAT_DEPLOYMENT", "gpt35")
CHAT_TEMPERATURE = float(os.environ.get("OPENAI_CHAT_TEMPERATURE", "0.3"))
CHAT_RESPONSE_MAX_TOKENS = int(os.environ.get("OPENAI_CHAT_RESPONSE_MAX_TOKENS", "300"))

COMPLETION_MODEL = os.environ.get("OPENAI_COMPLETION_MODEL", "text-davinci-003")
COMPLETION_DEPLOYMENT = os.environ.get("OPENAI_COMPLETION_DEPLOYMENT", "davinci")
SUMMARY_TEMPERATURE = float(os.environ.get("SUMMARY_TEMPERATURE", "0.3"))
SUMMARY_MAX_TOKENS = os.environ.get("SUMMARY_MAX_TOKENS", "100")
CHAT_MEMORY_MAX_TOKENS = int(os.environ.get("OPENAI_CHAT_MEMORY_MAX_TOKENS", "2000"))

# Initialize LangChain with Azure OpenAI
chat = AzureChatOpenAI(
    deployment_name=CHAT_DEPLOYMENT,
    openai_api_version=CHAT_API_VERSION,
    max_tokens=CHAT_RESPONSE_MAX_TOKENS,
    temperature=CHAT_TEMPERATURE,
    verbose=True
)

prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(Prompts.SYSTEM_METAPROMPT),
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template("{input}")
])

# memory for chat history, use the completion model to summarize past conversations
llm = AzureOpenAI(
    model_name=COMPLETION_MODEL,
    deployment_name=COMPLETION_DEPLOYMENT,
    max_tokens=SUMMARY_MAX_TOKENS,
    temperature=SUMMARY_TEMPERATURE,
    verbose=True
)
memory = ConversationSummaryBufferMemory(
    llm=llm,
    max_token_limit=CHAT_MEMORY_MAX_TOKENS,
    return_messages=True
)

conversation = ConversationChain(
    llm=chat,
    memory=memory,
    prompt=prompt,
    verbose=True)

# Create the Flask app
app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    request_data = request.get_json()
    message = request_data['message']
    if not message:
        return jsonify({"error": "Message is required"}), 400
    
    with get_openai_callback() as cb:
        response = conversation.predict(input=message)
        total_tokens = cb.total_tokens

        return jsonify({
            "response": response,
            "total_tokens": total_tokens
        })

if __name__ == '__main__':
    app.run()