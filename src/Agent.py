# !pip install -U "langchain[openai]"

import os
from langchain.chat_models import init_chat_model

#setup you openai api key
os.environ["OPENAI_API_KEY"] = "<API-KEY>"


model = init_chat_model("gpt-4.1")
response = model.invoke("What is Agentic AI?")


