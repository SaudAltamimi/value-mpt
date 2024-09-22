from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from operator import itemgetter
import chainlit as cl
from langchain_anthropic import ChatAnthropic
from crewai import Agent, Task, Crew


@cl.on_chat_start
async def on_chat_start():
    model = ChatAnthropic(
        model="claude-3-5-sonnet-20240620",
        streaming=True
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])

    memory = ConversationBufferMemory(return_messages=True)

    runnable = (
        RunnablePassthrough.assign(
            history=RunnableLambda(memory.load_memory_variables) | itemgetter("history")
        )
        | prompt
        | model
        | StrOutputParser()
    )

    cl.user_session.set("runnable", runnable)
    cl.user_session.set("memory", memory)


@cl.on_message
async def on_message(message: cl.Message):
    runnable = cl.user_session.get("runnable")
    memory = cl.user_session.get("memory")
    crew = cl.user_session.get("crew")

    msg = cl.Message(content="", author="Assistant")
    await msg.send()

    async for chunk in runnable.astream({"input": message.content}):
        await msg.stream_token(chunk)

    memory.save_context({"input": message.content}, {"output": msg.content})

    await msg.update()