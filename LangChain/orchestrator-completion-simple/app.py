import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify

from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain.llms import AzureOpenAI
from langchain.memory import ConversationBufferWindowMemory, CombinedMemory, ConversationSummaryMemory
from langchain.callbacks import get_openai_callback

import Prompts

# Load Environment Variables
load_dotenv()

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
    k=NUM_CONVERSATION_MEMORY
)
summary_memory = ConversationSummaryMemory(
    llm=llm,
    input_key="input"
)
memory = CombinedMemory(memories=[conv_memory, summary_memory])

# create conversation chain
prompt = PromptTemplate(
    input_variables=["history", "input", "chat_history_lines"],
    template=Prompts.DEFAULT_TEMPLATE
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