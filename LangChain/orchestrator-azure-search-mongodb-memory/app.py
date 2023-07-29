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
from langchain.callbacks import get_openai_callback
from langchain.memory import ConversationBufferWindowMemory
from langchain.memory.chat_message_histories import MongoDBChatMessageHistory

from azure.identity import DefaultAzureCredential
#from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

import Prompts
import SearchUtil

# Load Environment Variables
load_dotenv()

OPENAI_API_VERSION = os.environ.get("OPENAI_API_VERSION", "2023-05-15")
CHAT_DEPLOYMENT = os.environ.get("OPENAI_CHAT_DEPLOYMENT", "gpt35")
CHAT_TEMPERATURE = float(os.environ.get("OPENAI_CHAT_TEMPERATURE", "0.0"))
CHAT_RESPONSE_MAX_TOKENS = int(os.environ.get("OPENAI_CHAT_RESPONSE_MAX_TOKENS", "100"))
CHAT_MEMORY_WINDOW = int(os.environ.get("OPENAI_CHAT_MEMORY_WINDOW", "3"))

COMPLETION_MODEL = os.environ.get("OPENAI_COMPLETION_MODEL", "text-davinci-003")
COMPLETION_DEPLOYMENT = os.environ.get("OPENAI_COMPLETION_DEPLOYMENT", "davinci")
COMPLETION_TEMPERATURE = float(os.environ.get("OPENAI_COMPLETION_TEMPERATURE", "0.0"))
COMPLETION_MAX_TOKENS = os.environ.get("OPENAI_COMPLETION_MAX_TOKENS", "300")

AZURE_SEARCH_SERVICE_ENDPOINT = os.environ["AZURE_SEARCH_SERVICE_ENDPOINT"]
AZURE_SEARCH_INDEX_NAME = os.environ["AZURE_SEARCH_INDEX_NAME"]
SEARCH_MAX_RESULTS = int(os.environ.get("SEARCH_MAX_RESULTS", "3"))

MONGODB_CONNECTIONSTRING = os.environ["MONGODB_CONNECTIONSTRING"]

# Use the current user identity to authenticate with Azure OpenAI, Cognitive Search and Blob Storage (no secrets needed, 
# just use 'az login' locally, and managed identity when deployed on Azure). If you need to use keys, use separate AzureKeyCredential instances with the 
# keys for each service
# If you encounter a blocking error during a DefaultAzureCredntial resolution, you can exclude the problematic credential by using a parameter (ex. exclude_shared_token_cache_credential=True)
azure_credential = DefaultAzureCredential()

# Initialize LangChain with Azure OpenAI
chat = AzureChatOpenAI(
    deployment_name=CHAT_DEPLOYMENT,
    openai_api_version=OPENAI_API_VERSION,
    max_tokens=CHAT_RESPONSE_MAX_TOKENS,
    temperature=CHAT_TEMPERATURE,
    verbose=True
)

# memory for chat history, use the completion model to summarize past conversations
llm = AzureOpenAI(
    model_name=COMPLETION_MODEL,
    deployment_name=COMPLETION_DEPLOYMENT,
    max_tokens=COMPLETION_MAX_TOKENS,
    temperature=COMPLETION_TEMPERATURE,
    verbose=True
)

conversation = ConversationChain(
    llm=chat,
    verbose=True)

memories = {}

# Create the Flask app
app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    request_data = request.get_json()
    sessionid = request_data['sessionid']
    message = request_data['message']
    searchindex = request_data.get('searchindex', AZURE_SEARCH_INDEX_NAME)
    
    searchclient = SearchClient(
        endpoint=AZURE_SEARCH_SERVICE_ENDPOINT,
        index_name=searchindex,
        credential=azure_credential)
        #credential=AzureKeyCredential(os.environ["AZURE_SEARCH_SERVICE_KEY"]))        
    
    if not sessionid:
        return jsonify({"error": "sessionid is required"}), 400
    
    if not message:
        return jsonify({"error": "message is required"}), 400

    memory = memories.get(sessionid, None)
    if memory is None:
        history = MongoDBChatMessageHistory(
            connection_string=MONGODB_CONNECTIONSTRING,
            session_id=sessionid
        )
        memory = ConversationBufferWindowMemory(
            k = CHAT_MEMORY_WINDOW,
            chat_memory=history,
            return_messages=True
        )
        memories[sessionid] = memory
    
    conversation.memory = memory

    # STEP 1: Rephrase Search Query
    memory_variables = memory.load_memory_variables({})
    chat_history = memory_variables["history"]

    searchquery = SearchUtil.RephraseQuery(
        message,
        chat_history,
        llm)
    
    # STEP 2: Do the Search
    searchresults, sources = SearchUtil.Search(
        searchquery,
        SEARCH_MAX_RESULTS,
        searchclient)
    
    del searchclient
    
    # STEP 3: Answer the Question
    systemprompt = Prompts.CHAT_SYSTEMPROMPT.format(sources=searchresults)
    chatprompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(systemprompt),
        MessagesPlaceholder(variable_name="history"),
        HumanMessagePromptTemplate.from_template("{input}")
    ])
    conversation.prompt = chatprompt

    with get_openai_callback() as cb:
        response = conversation.predict(input=message)
        total_tokens = cb.total_tokens

        return jsonify({
            "response": response,
            "sources": sources,
            "total_tokens": total_tokens
        })

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8000)

