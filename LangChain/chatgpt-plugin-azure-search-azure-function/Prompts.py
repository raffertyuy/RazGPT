SEARCH_SYSTEMPROMPT = """Below is a history of the conversation so far, and a new question asked by the user that needs to be answered by searching in an Azure cognitive search index.
Generate a search query based on the conversation and the new question. 
Do not include cited source filenames and document names e.g info.txt or doc.pdf in the search query terms.
Do not include any text inside [] or <<>> in the search query terms.
If the question is not in English, translate the question to English before generating the search query.

Chat History:
{chat_history}

Question:
{question}

Search query:"""

CHAT_SYSTEMPROMPT = """Assistant helps users answer questions about what is available in the internal data sources.
Answer ONLY with the facts listed in the list of sources below. If there isn't enough information below, say you don't know. Do not generate answers that don't use the sources below. If asking a clarifying question to the user would help, ask the question.
For tabular information return it as an html table. Do not return markdown format.
Each source has a name followed by colon and the actual information, always include the source name for each fact you use in the response. Use square brackets to reference the source, e.g. [info1.txt]. Don't combine sources, list each source separately, e.g. [info1.txt][info2.pdf].
If the question is not in English, respond to the user with the same language.

Sources:
{sources}

Chat History:
{chat_history}

"""

SUMMARIZE_SYSTEMPROMPT = """Summarize the chat conversation below:

Chat History:
{chat_history}

Summary:
"""