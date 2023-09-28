import os
from dotenv import load_dotenv

import streamlit as st
import pandas as pd
import json
import re

from langchain.llms import AzureOpenAI

from SqlDbUtility import SqlDbUtility
from SqlAgent import SqlAgent

st.set_page_config(page_title="DB Copilot | RazType")

##########################################################################################
# Functions
##########################################################################################
def DecodeResponse(response: str) -> dict:
    """This function converts the string response from the model to a dictionary object.

    Args:
        response (str): response from the model

    Returns:
        dict: dictionary with response data
    """
    for i in range(5): # try 5 times
        try:
            result = json.loads(response)   # try to parse...
            return result
        except Exception as e:
            # "Expecting , delimiter: line 34 column 54 (char 1158)"
            # position of unexpected character after '"'
            unexp = int(re.findall(r'\(char (\d+)\)', str(e))[0])
            # position of unescaped '"' before that
            unesc = response.rfind(r'"', 0, unexp)
            response = response[:unesc] + r'\"' + response[unesc+1:]
            # position of correspondig closing '"' (+2 for inserted '\')
            closg = response.find(r'"', unesc + 2)
            response = response[:closg] + r'\"' + response[closg+1:]

    raise Exception("Failed to decode response after 5 attempts.")


def WriteResponse(response_dict: dict):
    """
    Write a response from an agent to a Streamlit app.

    Args:
        response_dict: The response from the agent.

    Returns:
        None.
    """

    # Check if the response is an answer.
    if "answer" in response_dict:
        st.write(response_dict["answer"])

    # Check if the response is a bar chart.
    if "bar" in response_dict:
        data = response_dict["bar"]
        df = pd.DataFrame(data)
        df.set_index("columns", inplace=True)
        st.bar_chart(df)

    # Check if the response is a line chart.
    if "line" in response_dict:
        data = response_dict["line"]
        df = pd.DataFrame(data)
        df.set_index("columns", inplace=True)
        st.line_chart(df)

    # Check if the response is a table.
    if "table" in response_dict:
        data = response_dict["table"]
        df = pd.DataFrame(data["data"], columns=data["columns"])
        st.table(df)


##########################################################################################
# App
##########################################################################################

load_dotenv()

COMPLETION_MODEL = os.environ["OPENAI_COMPLETION_MODEL"]
COMPLETION_DEPLOYMENT = os.environ["OPENAI_COMPLETION_DEPLOYMENT"]
OPENAI_API_VERSION = os.environ["OPENAI_API_VERSION"]
OPENAI_TEMPERATURE = float(os.environ["OPENAI_TEMPERATURE"])

llm = AzureOpenAI(
    model_name=COMPLETION_MODEL,
    deployment_name=COMPLETION_DEPLOYMENT,
    temperature=OPENAI_TEMPERATURE,
    verbose=True
)

dbutility = SqlDbUtility()
dbagent = SqlAgent(llm=llm, db=dbutility.db, verbose=True)

# Streamlit App
st.title("👨‍💻 Chat with your Database")
st.write("This is a app that allows you to query your database using natural language.")

query = st.text_area("What do you want to ask?")

if st.button("Submit Query", type="primary"):
    response = dbagent.Query(query=query)

    decoded_response = DecodeResponse(response)
    WriteResponse(decoded_response)