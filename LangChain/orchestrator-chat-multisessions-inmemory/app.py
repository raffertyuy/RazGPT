import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify

from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
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
    headers={"Ocp-Apim-Subscription-Key": os.environ["OPENAI_API_KEY"]}, # add this if endpoint authorization is not the default "api-key".
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
    headers={"Ocp-Apim-Subscription-Key": os.environ["OPENAI_API_KEY"]}, # add this if endpoint authorization is not the default "api-key".
    model_name=COMPLETION_MODEL,
    deployment_name=COMPLETION_DEPLOYMENT,
    max_tokens=SUMMARY_MAX_TOKENS,
    temperature=SUMMARY_TEMPERATURE,
    verbose=True
)

conversation = ConversationChain(
        llm=chat,
        prompt=prompt,
        verbose=True)

memories = {}

# Create the Flask app
app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    request_data = request.get_json()
    sessionid = request_data['sessionid']
    message = request_data['message']
    
    if not sessionid:
        return jsonify({"error": "sessionid is required"}), 400
    
    if not message:
        return jsonify({"error": "message is required"}), 400
    
    memory = memories.get(sessionid, None)
    if memory is None:
        memory = ConversationSummaryBufferMemory(
            llm=llm,
            max_token_limit=CHAT_MEMORY_MAX_TOKENS,
            return_messages=True
        )
        memories[sessionid] = memory
    
    conversation.memory = memory
    
    with get_openai_callback() as cb:
        response = conversation.predict(input=message)
        total_tokens = cb.total_tokens

        return jsonify({
            "response": response,
            "total_tokens": total_tokens
        })

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8000)