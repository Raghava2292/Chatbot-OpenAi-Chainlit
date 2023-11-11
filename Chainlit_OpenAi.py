from openai import AsyncOpenAI
import chainlit as cl
from api_keys import openai_apikey
from chainlit.input_widget import TextInput

client = AsyncOpenAI(api_key=openai_apikey)


settings = {
    "model": "gpt-3.5-turbo",
    "temperature": 0.7,
    "max_tokens": 500,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
}


@cl.on_chat_start
async def start_chat():
    start_msg = "Hello. I am your AI Assistant. How can I help you today?"
    start = cl.Message(content=start_msg)
    await start.send()
    cl.user_session.set(
        "message_history",
        [{"role": "system", "content": f"You are a helpful assistant."}],
    )


@cl.on_message
async def main(message: cl.Message):
    message_history = cl.user_session.get("message_history")
    message_history.append({"role": "user", "content": message.content})

    msg = cl.Message(content="")
    await msg.send()

    stream = await client.chat.completions.create(
        messages=message_history, stream=True, **settings
    )

    async for part in stream:
        if token := part.choices[0].delta.content or "":
            await msg.stream_token(token)

    message_history.append({"role": "assistant", "content": msg.content})
    await msg.update()