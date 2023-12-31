import os
from langchain import PromptTemplate, OpenAI, LLMChain
import chainlit as cl
from api_keys import openai_apikey
from langchain.chat_models import ChatOpenAI

os.environ['OPENAI_API_KEY'] = openai_apikey

template = """Question: {question}
Answer: Let's think step by step."""

@cl.on_chat_start
def main():
  # Instantiate the chain for that user session
  prompt = PromptTemplate(template=template, input_variables=["question"])
  llm_chain = LLMChain(prompt=prompt, llm=OpenAI(temperature=0), verbose=False)  
  
  # Store the chain in the user session
  cl.user_session.set("llm_chain", llm_chain)

@cl.on_message
async def main(message: str):
   # Retrieve the chain from the user session
  llm_chain = cl.user_session.get("llm_chain") # type: LLMChain

  # Call the chain asynchronously
  res = await llm_chain.acall(message, callbacks=[cl.AsyncLangchainCallbackHandler()])

  # Do any post processing here

  # Send the response
  await cl.Message(content=res["text"]).send()
