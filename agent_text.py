from langchain_openai import ChatOpenAI
from browser_use import Agent
from dotenv import load_dotenv
load_dotenv(".env")

import asyncio

llm = ChatOpenAI(model="gpt-4o")

async def main():
    agent = Agent(
        task='''STEP 1: search Guanming Wang at UCL and open his linkedin profile, if you see google pop-up, close it
        STEP 2: click his linkeidn profile if log in is required, log in with the following credentials: username: zcabgwa@ucl.ac.uk, password: #LINKEDINwgm123456
        STEP 3: Summerize his profile
        STEP 4: Click messaging and find CHI PUI (MARTIN) CHAN
        STEP 5: Use the name of Guanming Wang to write a coffee invite message to Martin Chan
        ''',
        llm=llm,
    )
    result = await agent.run()
    print(result)

asyncio.run(main())