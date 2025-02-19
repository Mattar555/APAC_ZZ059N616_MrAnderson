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

# Feel free to comment this out if you don't want granular logs
litellm._turn_on_debug()

load_dotenv()

# I am no LLM expert, but my rudimentary experimentation yielded more accurate results for meta-llama, as opposed to
# WatsonX
llama_vision_llm = LLM(model="watsonx/meta-llama/llama-3-2-90b-vision-instruct",
                       max_tokens=5000,
                       temperature=0
)

# Re-iterating above comment, feel free to use WatsonX Granite models. I didn't have time to investigate much.
llama_instruct_llm = LLM(model="watsonx/meta-llama/llama-3-3-70b-instruct",
                                max_tokens=5000,
                                temperature=0.7
)

# Refer to the Compose file, the username and password are salesuser and salesuerpassword respectively.
# Needless to say, they ought to be injected by other means. For instance, environment variables.
# This is the agent responsible for translating natural language to SQL and querying the database given below.
nl2sql = NL2SQLTool(
    db_uri="postgresql://salesuser:salesuserpassword@localhost:5432/sales"
)

# Our Elasticsearch client. Although it runs on its network it is port mapped to the local workstation hence 
# accessible via Localhost. I've disabled security, so no need to provide credentials.
elasticsearch_client = Elasticsearch("http://localhost:9200/")

chat_interface = pn.chat.ChatInterface()


# This is the callback which is called after task execution, bot input/output is pushed to Elasticsearch.
def print_output(output: TaskOutput):
    current = 1
    try:
        index_search = client.search(index="agentic-ai-chats", query={"match_all": {}})
        current = index_search["hits"]["total"]["value"] + 1
    except:
        print("Index not created yet...")
    message = output.raw
    bot_response = {"author": "bot", "text": message, "timestamp": datetime.now()}
    # Querying the length of the index just to find out the next position isn't the best way to do this at scale..
    elasticsearch_client.index(index="agentic-ai-chats", id=current, document=bot_response)
    # This is how we render output back to the user
    chat_interface.send(message, user=output.agent, respond=False)

# Remember, you can create your own tooling. This one downloads the document from Nginx.
class FileDownloaderTool(BaseTool):
    name: str = "File Downloader"
    description: str = "Downloads file(s) belonging to the seller containing critical account(s) info"
    
    def _run(self, url: str) -> str:
       # Note the string "marwan" was hardcoded below, there should be a way to pass the name obtained
       # from the database analyser task to pass it here as a variable, dynamically.
       # I'm sure a construct for this exists, but I got lazy.
       # Remember, the "url" parameter was passed to the inputs in the main.py function, it is referenced here.
       file_download_response = requests.get(url)
       return file_download_response.content.decode('utf-8').strip()

file_downloader_tool = FileDownloaderTool()

@CrewBase
class SalesOnboarding:
    """Sales Onboarding crew"""

    @before_kickoff
    # We initialise the index here, if it does not exist.
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

    # Remember, this agent is referencing our NL2SQL tool using one of the models defined above.
    # We don't delegate, as this is self contained. The configuration provided can be found in the
    # config directory with the stanza "database_analyst"
    # Ignore the step_callback function, I was just testing things...
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


    # Unlike the above, configuration is hardcoded here, as opposed to inserting into the config file.
    # Why did I do this? No reason, just to show both ways work...
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

    # If you reference the downloader_task stanza in the tasks.yaml file in the config directory, we can see the 
    # association between the task and the agent.
    # Note, we don't callback in the above because we don't want to dump the entire account info to the user,
    # just the summary, as done in the summarise_task below.
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

