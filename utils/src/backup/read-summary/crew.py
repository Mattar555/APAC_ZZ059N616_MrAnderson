import litellm
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from crewai.tools import BaseTool
from crewai import Agent, Crew, Process, Task, LLM
from crewai_tools import SerperDevTool, NL2SQLTool
from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff

litellm._turn_on_debug()

load_dotenv()

llm = LLM(model="watsonx/meta-llama/llama-3-2-90b-vision-instruct",
          max_tokens=5000,
          temperature=0
)


nl2sql = NL2SQLTool(
    db_uri="postgresql://salesuser:salesuserpassword@localhost:5432/sales"
)


class PDFReaderTool(BaseTool):
    name: str = "PDF Reader"
    description: str = "Read the content of the PDF file in question and returns the text enclosed"


    def _run(self, pdf_path: str) -> str:
        pdf_reader = PdfReader(pdf_path)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text

pdf_reader_tool = PDFReaderTool()


@CrewBase
class SalesOnboarding:
    """Sales Onboarding crew"""

    @before_kickoff
    def before_kickoff_function(self, inputs):
        print(f"Before kickoff function with inputs: {inputs}")
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
            memory=True,
            llm=llm
        )


    @agent
    def reader_agent(self) -> Agent:
        return Agent(
            role='Reader',
            goal='Extract text from PDF Documents.',
            verbose=True,
            memory=True,
            backstory='You are an expert in extracting text from PDF documents.',
            tools=[pdf_reader_tool],
            allow_delegation=True,
            llm=llm
        )



    @agent
    def summariser_agent(self) -> Agent:
        return Agent(
            role='Summariser',
            goal='Summarise the content of documents.',
            verbose=True,
            backstory='You are skilled at summarising long documents into concise summaries.',
            allow_delegation=False,
            llm=llm
        )


    @task
    def database_task(self) -> Task:
        return Task(
            config=self.tasks_config["database_task"],
        )



    @task
    def read_task(self) -> Task:
        return Task(
            config=self.tasks_config["reader_task"],
        )


    @task
    def summarise_task(self) -> Task:
        return Task(
            config=self.tasks_config["summariser_task"],
        )


    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents, # agents=self.agents 
            tasks=self.tasks,  # agents=self.tasks 
            process=Process.sequential,
            verbose=True
        )

