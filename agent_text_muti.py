from langchain_openai import ChatOpenAI
from browser_use import Agent
from dotenv import load_dotenv
import asyncio
from multiprocessing import Process

load_dotenv(".env")

TASKS = {
    "A": {
        "task": "STEP 1: search Guanming Wang at UCL and open his linkedin profile\nSTEP 2: log in with username: zcabgwa@ucl.ac.uk, password: #LINKEDINwgm123456\nSTEP 3: Summerize his education background"
    },
    "B": {
        "task": "STEP 1: search Vaibhav Mehra at UCL on LinkedIn\nSTEP 2: log in with username: zcabgwa@ucl.ac.uk, password: #LINKEDINwgm123456\nSTEP 3: List his work experience"
    },
    "C": {
        "task": "STEP 1: find Hanshang Zhu's LinkedIn profile\nSTEP 2: log in with username: zcabgwa@ucl.ac.uk, password: #LINKEDINwgm123456\nSTEP 3: Extract his technical skills"
    }
}

async def execute_task(task_id):
    task_config = TASKS[task_id]
    print(f"Starting task {task_id}")
    agent = Agent(
        task=task_config["task"],
        llm=ChatOpenAI(model="gpt-4o"),
        browser=None,
        browser_context=None,
        use_vision=True,
        max_failures=3
    )
    result = await agent.run()
    print(f"Task {task_id} Result:\n{result}")

def run_task(task_id):
    asyncio.run(execute_task(task_id))

if __name__ == '__main__':
    processes = [Process(target=run_task, args=(task_id,)) for task_id in TASKS]
    for process in processes:
        process.start()
    for process in processes:
        process.join()
