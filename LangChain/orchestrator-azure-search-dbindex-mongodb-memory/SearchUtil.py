from langchain.chat_models import AzureChatOpenAI
from langchain.schema import HumanMessage

from azure.search.documents import SearchClient
import Prompts

def GenerateQuery(question: str, chat_history: dict, chatLLM: AzureChatOpenAI):
    searchprompt = Prompts.SEARCH_SYSTEMPROMPT.format(
        chat_history=chat_history,
        question=question)
    
    searchquery = chatLLM([HumanMessage(content=searchprompt)]).content
    if searchquery.startswith("search="):
        searchquery = searchquery[7:]
        
    return searchquery


def Search(query: str, top: int, client: SearchClient):
    results = client.search(query, top=top)

    resultslist = []
    for result in results:
        resultslist.append(str(result).replace("{", "{{").replace("}", "}}"))

    # Convert the list to a string
    resultscontent = "\n".join(resultslist)
    
    return resultscontent
