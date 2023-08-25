# For self-learning, this notebook is using VS Code Interactive notebooks (https://code.visualstudio.com/docs/python/jupyter-support-py) 

#%% Load Variables
import os
from dotenv import load_dotenv

# Set environment variables in the .env file.
load_dotenv()

OPENAI_API_BASE = os.environ["OPENAI_API_BASE"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
OPENAI_API_VERSION = os.environ["OPENAI_API_VERSION"]

#COMPLETION_MODEL = os.environ["OPENAI_COMPLETION_MODEL"]
#COMPLETION_DEPLOYMENT = os.environ["OPENAI_COMPLETION_DEPLOYMENT"]
#CHAT_MODEL = os.environ["OPENAI_CHAT_MODEL"]
CHAT_DEPLOYMENT = os.environ["OPENAI_CHAT_DEPLOYMENT"]

#%% Initialize Semantic Kernel
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

kernel = sk.Kernel()
service = AzureChatCompletion(CHAT_DEPLOYMENT, OPENAI_API_BASE, OPENAI_API_KEY)
kernel.add_chat_service(
    service_id="chat_completion",
    service=service
    )

#%% Run a Semantic Function (from the skills folder)
skill = kernel.import_semantic_skill_from_directory("./skills", "FunSkill")

joke_function = skill["Joke"]
print(joke_function("time travel to dinosaur age"))

excuses_function = skill["Excuses"]
print(excuses_function("I forgot about the meeting"))

#%% Run a Semantic Function (inline)
prompt = """Summarize the content below into at most 3 sentences.
{{$input}}"""

input_text = """
Demo (ancient Greek poet)
From Wikipedia, the free encyclopedia
Demo or Damo (Greek: Δεμώ, Δαμώ; fl. c. AD 200) was a Greek woman of the Roman period, known for a single epigram, engraved upon the Colossus of Memnon, which bears her name. She speaks of herself therein as a lyric poetess dedicated to the Muses, but nothing is known of her life.[1]
Identity
Demo was evidently Greek, as her name, a traditional epithet of Demeter, signifies. The name was relatively common in the Hellenistic world, in Egypt and elsewhere, and she cannot be further identified. The date of her visit to the Colossus of Memnon cannot be established with certainty, but internal evidence on the left leg suggests her poem was inscribed there at some point in or after AD 196.[2]
Epigram
There are a number of graffiti inscriptions on the Colossus of Memnon. Following three epigrams by Julia Balbilla, a fourth epigram, in elegiac couplets, entitled and presumably authored by "Demo" or "Damo" (the Greek inscription is difficult to read), is a dedication to the Muses.[2] The poem is traditionally published with the works of Balbilla, though the internal evidence suggests a different author.[1]
In the poem, Demo explains that Memnon has shown her special respect. In return, Demo offers the gift for poetry, as a gift to the hero. At the end of this epigram, she addresses Memnon, highlighting his divine status by recalling his strength and holiness.[2]
Demo, like Julia Balbilla, writes in the artificial and poetic Aeolic dialect. The language indicates she was knowledgeable in Homeric poetry—'bearing a pleasant gift', for example, alludes to the use of that phrase throughout the Iliad and Odyssey.[a][2] 
"""

summarize_function = kernel.create_semantic_function(prompt, max_tokens=100, temperature=0.2, top_p=0.5)
print(summarize_function(input_text))