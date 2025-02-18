import requests
import litellm
import panel as pn
from PyPDF2 import PdfReader
from datetime import datetime
from dotenv import load_dotenv
from crewai.tools import BaseTool
from elasticsearch import Elasticsearch
from crewai.tasks.task_output import TaskOutput
from crewai import Agent, Crew, Process, Task, LLM
from crewai_tools import SerperDevTool, NL2SQLTool
from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff

litellm._turn_on_debug()

load_dotenv()

llama_vision_llm = LLM(model="watsonx/meta-llama/llama-3-2-90b-vision-instruct",
                       max_tokens=5000,
                       temperature=0
)

llama_instruct_llm = LLM(model="watsonx/meta-llama/llama-3-3-70b-instruct",
                                max_tokens=5000,
                                temperature=0.7
)

nl2sql = NL2SQLTool(
    db_uri="postgresql://salesuser:salesuserpassword@localhost:5432/sales"
)

elasticsearch_client = Elasticsearch("http://localhost:9200/")
#identifier = 1

chat_interface = pn.chat.ChatInterface()

def print_output(output: TaskOutput):
    #global identifier
    current = 1
    try:
        index_search = client.search(index="agentic-ai-chats", query={"match_all": {}})
        current = index_search["hits"]["total"]["value"] + 1
    except:
        print("Index not created yet...")
    message = output.raw
    bot_response = {"author": "bot", "text": message, "timestamp": datetime.now()}
    elasticsearch_client.index(index="agentic-ai-chats", id=current, document=bot_response)
    #identifer = identifer + 1
    chat_interface.send(message, user=output.agent, respond=False)

class FileDownloaderTool(BaseTool):
    name: str = "File Downloader"
    description: str = "Downloads file(s) belonging to the seller containing critical account(s) info"
    
    def _run(self, url: str) -> str:
       # Note the string "marwan" was hardcoded below, there should be a way to pass the name obtained
       # from the database analyser task to pass it here as a variable, dynamically.
       # I'm sure a construct for this exists
       file_download_response = requests.get(url)
       return file_download_response.content.decode('utf-8').strip()

file_downloader_tool = FileDownloaderTool()

@CrewBase
class SalesOnboarding:
    """Sales Onboarding crew"""

    @before_kickoff
    def before_kickoff_function(self, inputs):
        print(f"Before kickoff function with inputs: {inputs}")
        current = 1
        try:
            index_search = client.search(index="agentic-ai-chats", query={"match_all": {}})
            current = index_search["hits"]["total"]["value"] + 1
        except:
            print("Index not created yet...")
        human_query = {"author": "human", "text": inputs["query"], "timestamp": datetime.now()}
        elasticsearch_client.index(index="agentic-ai-chats", id=current, document=human_query)
        return inputs  # You can return the inputs or modify them as needed

    @after_kickoff
    def after_kickoff_function(self, result):
        print(f"After kickoff function with result: {result}")
        return result  # You can return the result or modify it as needed

    @agent
    def database_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["database_analyst"],
            allow_delegation=False,
            tools=[nl2sql],
            cache=True,
            max_execution_time=60,
            memory=True,
            max_iter=5,
            step_callback=lambda step_output: print(f"HELLOHELLOHELLO Step output: {step_output}"),
            llm=llama_vision_llm
        )


    @agent
    def file_downloader_agent(self) -> Agent:
        return Agent(
            role='Downloader',
            goal='Download specific files from a remote HTTP repository.',
            verbose=True,
            memory=True,
            max_iter=3,
            max_execution_time=20,
            backstory='You have a knack for downloading media from the internet.',
            tools=[file_downloader_tool],
            allow_delegation=False,
            llm=llama_vision_llm
        )

    @agent
    def summariser_agent(self) -> Agent:
        return Agent(
            role='Summariser',
            goal='Summarise the content of documents and return the salient points.',
            verbose=True,
            max_iter=3,
            max_execution_time=20,
            backstory='You are skilled at summarising long documents into concise short,brief summaries.',
            allow_delegation=False,
            llm=llama_instruct_llm
        )


    @task
    def database_task(self) -> Task:
        return Task(
            config=self.tasks_config["database_task"],
            callback=print_output
        )


    @task
    def downloader_task(self) -> Task:
        return Task(
            config=self.tasks_config["downloader_task"]
        )


    @task
    def summarise_task(self) -> Task:
        return Task(
            config=self.tasks_config["summariser_task"],
            callback=print_output,
            human_input=True
        )


    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents, # agents=self.agents 
            tasks=self.tasks,  # agents=self.tasks 
            process=Process.sequential,
            verbose=True
        )

