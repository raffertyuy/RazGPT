import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import json

from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain.llms import AzureOpenAI
from langchain.memory import ConversationBufferWindowMemory, CombinedMemory, ConversationSummaryMemory
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
NUM_CONVERSATION_MEMORY = int(os.environ.get("NUM_CONVERSATION_MEMORY", "3"))

# Initialize LangChain with Azure OpenAI
llm = AzureOpenAI(
    model_name=COMPLETION_MODEL,
    deployment_name=COMPLETION_DEPLOYMENT,
    max_tokens=SUMMARY_MAX_TOKENS,
    temperature=SUMMARY_TEMPERATURE,
    verbose=True
)

# memory for chat history, use the completion model to summarize past conversations
conv_memory = ConversationBufferWindowMemory(
    memory_key="chat_history_lines",
    input_key="input",
    k=3
)
summary_memory = ConversationSummaryMemory(
    llm=llm,
    input_key="input"
)
memory = CombinedMemory(memories=[conv_memory, summary_memory])

# create conversation chain
prompt = PromptTemplate(
    input_variables=["history", "input", "chat_history_lines"],
    template=Prompts.COMPLETION_TEMPLATE
)

conversation = ConversationChain(
    llm=llm,
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