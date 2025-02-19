# README


## TLDR

This section is dedicated to the lazy individuals who wish to simply run this application without necessarily reading the rest of the document.

### TLDR - Python Env Setup

Note, this guides assumes a MacOS.

At the time of writing, Python versions >= 3.10 and < 3.13 work. You may have, say, 3.13 installed locally and as such, may need to downgrade. There exists a few utilities out there in relation to Python version management. I'll be using "pyenv" in this case. Feel free to use your own version manager.

Install pyenv via Brew:

```
brew install pyenv
```

Init Pyenv:

```
pyenv init
source ~/.zshrc # change to ~/.bashrc if not using zsh
```

Set your desired Python version for the shell:

```
pyenv shell 3.12.7
source ~/.zshrc # change to ~/.bashrc if not using zsh
```

Install the necessary tools:

```
pip install 'crewai[tools]' # New Installs
pip install --upgrade crewai crewai-tools # Existing Installs
```

Install additional dependencies:

```
uv pip install psycopg2
uv pip install panel
uv pip install PyPDF2
uv pip install 'crewai[tools]'
uv pip install elasticsearch
pip install panel
pip install PyPDF2
pip install psycopg2
pip install python-dotenv
pip install litellm
pip install elasticsearch
```

Your resultant .env file should, as a result of completing the configurations above, resemble the following:

```
WATSONX_API_KEY=KEY_HERE
WATSONX_PROJECT_ID=ID_HERE
WATSONX_URL=URL_HERE
```

This file should be located at the directory titled "sales_onboarding"


### Upstream Provider Setup


A WatsonX.ai instance needs to be setup. Refer to the section titled "Setting up your watsonx project" within the following [link](https://developer.ibm.com/tutorials/awb-build-ai-agents-integrating-crewai-watsonx/).

The TechZone instance name was "watsonx ai plus Discovery". The collection URL is invalid hence the exclusion from this README. I used the Dallas region, it appears to be the most stable.

Not stated in the link provided, you need to, in addition to creating a project, associate said project with an instance of a WatsonX AI runtime. Navigate to your project, click on the "Services and Integrations" tab, select the "IBM Services" tab, then associate a "WatsonX AI Runtime" service with this project. One should already be created for you once the instance is provisioned successfully from Techzone.


### Containers/Services

Assuming you have Docker/Podman installed locally, run the following command:

```
[docker | podman] compose -f utils/compose/docker-compose.yml up --detach 
```

This should spin up 5 containers with the following names:

1) mailserver
2) web
3) elastic
4) kibana
5) sales-db


### Crew Program

Run the following command:

```
panel serve sales_onboarding/sales/sales_onboarding/main.py
```

See the video in the next section for a working example.

### Video





https://github.com/user-attachments/assets/8a9ffe4f-1572-4fc0-ac3a-2d0454461361




https://github.com/user-attachments/assets/c3d8dea4-b83e-40c9-beee-28959ffc28ba



## Detailed Notes


## Prerequisites

### WatsonX

A WatsonX.ai instance needs to be setup. Refer to the section titled "Setting up your watsonx project" within the following [link](https://developer.ibm.com/tutorials/awb-build-ai-agents-integrating-crewai-watsonx/).

The TechZone instance name was "watsonx ai plus Discovery". The collection URL is invalid hence the exclusion from this README. I used the Dallas region, it appears to be the most stable.

Not stated in the link provided, you need to, in addition to creating a project, associate said project with an instance of a WatsonX AI runtime. Navigate to your project, click on the "Services and Integrations" tab, select the "IBM Services" tab, then associate a "WatsonX AI Runtime" service with this project. One should already be created for you once the instance is provisioned successfully from Techzone.


### Env file

Create a .env file should, as a result of completing the configurations above, resemble the following:

```
WATSONX_API_KEY=KEY_HERE
WATSONX_PROJECT_ID=ID_HERE
WATSONX_URL=URL_HERE
```

Pleace this file in the "sales_onboarding" directory.

## Installation and Setup

Note, the following assumes a MacOS workstation.

It is important to note CrewAI requires, at the time of writing, Python >= 3.10 and < 3.13. See [here](https://docs.crewai.com/installation) for more information.

I had Python 3.13.1 and so was obtaining installation errors. You can use pyenv to simplify the Python version management process in your workstation, as described [here](https://dev.to/imkven/how-to-set-up-crewai-on-macos-a-step-by-step-guide-48d8). Note, you will need to install pyenv first:

```
brew install pyenv
```

Note, if using pyenv, you need not use a virtual environment as described in then steps [here](https://docs.crewai.com/installation#setting-up-your-environment). I suspect it uses a virtual environment behind the scenes anyhow. You may continue [here](https://docs.crewai.com/installation#installing-crewai):


```
pip install 'crewai[tools]' # New Installs
pip install --upgrade crewai crewai-tools # Existing Installs
```

Now, create your project as such:

```
crewai create crew <project_name>
```

Choose the Watson option when prompted, and input the API key, project ID and URL when required. You can leave them blank and manaully populate the dotenv file at a later stage if so desired.

Note, place the dotenv file at the projct root directory. A directory with name given by the <projct_name> directory upon successful execution of the command above. The dotenv file should be placed there.


Install additional tools as such:

```
uv add <tool-name>
```

Do note, UV is CrewAI's preferred package manager as it’s significantly faster than pip and provides better dependency resolution.


Run the following commands below. I am aware the presence of the "pip install" commands above are contradictory to the above statement, but I get ModuleNotFound errors otherwise. Perhaps my setup above was incomplete?

```
uv pip install psycopg2
uv pip install panel
uv pip install PyPDF2
uv pip install 'crewai[tools]'
uv pip install elasticsearch
pip install panel
pip install PyPDF2
pip install psycopg2
pip install python-dotenv
pip install litellm
pip install elasticsearch
```

### Aside - NL2SQL Bug Fix

This is important, do not skip this. If you get an error with the following output, then return to this section and complete the solution provided below. Depending on the time of reading, the issues raised against the NL2SQL module may have been resolved.

```
Field required [type=missing, input_value={'query': 
```

Part of this exercise involves the usage of the following NL2SQL module outlined [here](https://docs.crewai.com/tools/nl2sqltool). That said, it will fail when using it. There are active issues against this as raised [here](https://github.com/crewAIInc/crewAI/issues?q=is%3Aissue%20state%3Aopen%20nl2sql).

There is a workaround outlined [here](https://github.com/crewAIInc/crewAI/issues/1855#issuecomment-2638905545). It involves performing the following:

```
find ./.venv -name "structured_tool.py" 
vi /path/to/structured_tool.py
```

Add the following snippet to the _parse_args function:

```
if('query' in raw_args):
  raw_args['sql_query'] = raw_args.pop('query')
```


### Enable Granular Logs

Add the following lines, as stated [here](https://docs.litellm.ai/docs/debugging/local_debugging), to the crew.py file to enable granular logs:

```
import litellm

litellm._turn_on_debug()
```



### WatsonX Integration

Note, agents are associated with an upstream LLM Model. See below:

```
  @agent
  def researcher(self) -> Agent:
    return Agent(
      config=self.agents_config['researcher'],
      verbose=True,
      tools=[SerperDevTool()]
    )

  @agent
  def reporting_analyst(self) -> Agent:
    return Agent(
      config=self.agents_config['reporting_analyst'],
      verbose=True
    )
```

Each agent optionally accepts an LLM argument in the event one wants to supply a custom LLM model. See [here](https://docs.crewai.com/concepts/agents#agent-attributes) for more information.

The LLM can be supplied as such:

```
from crewai import LLM

llm = LLM(
    model=WATSONX_MODEL_ID,
    base_url=WATSONX_URL,
    project_id=WATSONX_PROJECT_ID,
    max_tokens=2000,
    temperature=0.7
)
```

In my case, the LLM was declared as such:

```
llm = LLM(model="watsonx/ibm/granite-3-8b-instruct", max_tokens=1000, temperature=0)
```

The base_url and project_id were loaded from the dotenv file, as given in the following line:

```
load_dotenv()
```

The value assigned to the model attribute can be obtained when launching the WatsonX.AI runtime studio interface. Select the model you wish to choose. Click the "code" button to determine the path variables. That is, model="watsonx/provider_path_variable/model_identifier_path_variable")

This LLM can then be referenced directly on agent declaration as such:

```
data_collector = Agent(
    role='Data Collector',
    goal='Collect accurate and up-to-date financial data',
    backstory='You are an expert in gathering financial data from various sources.',
    tools=[scrape_tool, search_tool],
    verbose=True,
    allow_delegation=True,
    llm=custom_llm
)

financial_analyst = Agent(
    role='Financial Analyst',
    goal='Analyze financial data and provide insights',
    backstory='You are a seasoned financial analyst with years of experience in interpreting market trends.',
    verbose=True,
    allow_delegation=True,
    tools=[scrape_tool, search_tool],
    llm=custom_llm
)

report_writer = Agent(
    role='Report Writer',
    goal='Compile findings into a comprehensive report',
    backstory='You are skilled at creating clear and concise financial reports.',
    llm=custom_llm
)
```

Note the llm parameter passed to the agents above, custom_llm is the llm object created above. Each LLM, depending on the provider, expects certain variables be passed in, either directly or supplied via a dotenv file. You will have to refer to your provider documentation for more information above. You may refer to the links provided in the references section, subsection "WatsonX-CrewAI Integration" for example implementations.


This begs the question, what is the default LLM, if no LLM is provided? The [getting started example](https://docs.crewai.com/quickstart#build-your-first-crewai-agent) requires, as given in Step 7, an OpenAI API Key, with environment variable "OPENAI_API_KEY". OpenAPI is the default assumed provider.



### Persistence

Execute the following:

```
./utils/persistence/run-db.sh
```

To ensure all is working, feel free to run the following commands:

```
podman exec -it sales-db psql -U salesuser -d sales
select * from accounts;
\q
exit
```

Ensure the following module is installed:

```
uv pip install psycopg2
pip install psycopg2
```

Remember, use uv to perform pip installs, as recommended.

Note, this SQL server will effectively mock IBM's instance of Salesforce.


### WebServer

Execute the following:

```
./utils/nginx/init-webserver.sh
```

This is a simple Nginx webserver serving static content. This will mock the cloud object storage provided by Box.


### Mailserver

Run the following command to spin up the mailserver:

```
./utils/mailhog/run-mailhog.sh
```

Mailhog is a Web and API based SMTP testing mailserver used to mock sending/receving of outbound/inbound emails.


### Elasticsearch & Kibana

Remember, both Elasticsearch and Kibana will effctively mock our analytics and query engines respectively.

Execute the following command:

```
./utils/elasticsearch-kibana/init.sh
./utils/elasticsearch-kibana/deploy-elastic.sh # Wait a minute or two before deploying Kibana. ES is a big boy.
./utils/elasticsearch-kibana/deploy-kibana.sh
```


### CrewAI Program

Reference video can be found [here](https://www.youtube.com/watch?v=Rp4xO0XLfzU&t=382s)

Run the following command:

```
uv pip install panel
pip install panel
```

Now, run the program:

```
panel serve sales_onboarding/src/sales_onboarding/main.py
```

Navigate to http://localhost:5006/main

## References


### WatsonX

0) [Setup WatsonX Environment](https://developer.ibm.com/tutorials/awb-build-ai-agents-integrating-crewai-watsonx/) - Section titled "Setting up your watsonx project"
1) [Adding Services to a Project](https://dataplatform.cloud.ibm.com/docs/content/wsj/getting-started/assoc-services.html?context=cpdaas)
2) [Creating a Project](https://www.ibm.com/docs/en/watsonx/saas?topic=projects-creating-project)


### CrewAI

0) [Pyenv](https://dev.to/imkven/how-to-set-up-crewai-on-macos-a-step-by-step-guide-48d8)
1) [Installation](https://docs.crewai.com/installation)
2) [Quick Start](https://docs.crewai.com/quickstart)
3) [Agent Attributes](https://docs.crewai.com/concepts/agents#agent-attributes)
3) [NL2SQL](https://docs.crewai.com/tools/nl2sqltool)
5) [NL2SQL Issues](https://github.com/crewAIInc/crewAI/issues?q=is%3Aissue%20state%3Aopen%20nl2sql)
6) [Enable Granular Logs](https://docs.litellm.ai/docs/debugging/local_debugging)
7) [Creating your own Tools](https://docs.crewai.com/concepts/tools#creating-your-own-tools)
8) [Using Panel to Serve CrewAI workflows](https://www.youtube.com/watch?v=Rp4xO0XLfzU&t=382s)
9) [Collaboration](https://docs.crewai.com/concepts/collaboration)
10) [Importing tools - error](https://community.crewai.com/t/importerror-cannot-import-name-basetool-from-crewai-tools/2488/5)
11) [Substack - Panel Example - Paywall](https://yeyu.substack.com/p/how-to-create-an-interactive-ui-for?utm_campaign=post&utm_medium=web)
12) [All about crews](https://docs.crewai.com/concepts/crews)
13) [All about tasks](https://docs.crewai.com/concepts/tasks)
14) [All about agents](https://docs.crewai.com/concepts/agents)
15) [Example BYO Tool](https://www.youtube.com/watch?v=adLwGpjYXTg)
16) [How to guides](https://docs.crewai.com/how-to/create-custom-tools) - See Nav Bar on LHS for an exhaustive list
17) [CrewAI - Introduction](https://docs.crewai.com/introduction)

### WatsonX - CrewAI Integration

0) [Example Integration - 1](https://developer.ibm.com/blogs/awb-leveraging-crewai-and-ibm-watsonx/)
1) [Example Integration - 2](https://developer.ibm.com/tutorials/awb-build-ai-agents-integrating-crewai-watsonx/)


Note, both of these links seem to be slightly outdated. The API Key environment variable is WATSONX_API_KEY, as opposed to WATSONX_APIKEY

Here is the relevant error thrown:

```
def generate_iam_token(api_key=None, **params) -> str:
    result: Optional[str] = iam_token_cache.get_cache(api_key)  # type: ignore

    if result is None:
        headers = {}
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        if api_key is None:
            api_key = get_secret_str("WX_API_KEY") or get_secret_str("WATSONX_API_KEY")
        if api_key is None:
            raise ValueError("API key is required")
```

### Persistence

0) [PostgreSQL Docs](https://www.tutorialsteacher.com/postgresql)
1) [PostgreSQL Docker Init Scripts](https://mkyong.com/docker/how-to-run-an-init-script-for-docker-postgres/)


### Nginx WebServer

0) [How to run Nginx](https://www.docker.com/blog/how-to-use-the-official-nginx-docker-image/)


### Mailhog

0) [Mailhog - Docker](https://hub.docker.com/r/mailhog/mailhog)
1) [Deploying Mailhog](https://akrabat.com/using-mailhog-via-docker-for-testing-email/)
2) [Send SMTP Email - Example](https://stackoverflow.com/questions/50695188/what-is-the-proper-way-to-actually-send-mail-from-python-code)
3) [Embed HTML - SMTP](https://stackoverflow.com/questions/31715138/how-to-add-href-link-in-email-content-when-sending-email-through-smtplib)


ELK

0) [Start a Single node cluster](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html#_start_a_single_node_cluster)
1) [Run Kibana](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html#run-kibana-docker)
2) [Python ES Client Example Usage](https://elasticsearch-py.readthedocs.io/en/v8.17.1/#example-usage)
3) [Default user and password for ES](https://stackoverflow.com/questions/46627979/what-is-the-default-user-and-password-for-elasticsearch)
4) [Disable ES security](https://stackoverflow.com/questions/47035056/how-to-disable-security-username-password-on-elasticsearch-docker-container)
5) [Disable Enrollment Security](https://stackoverflow.com/questions/78826286/configuring-elasticsearch-and-kibana-to-work-with-each-other-without-requiring-e)


### Hackathon

0) [Main Page](https://w3.ibm.com/w3publisher/apac-agentic-ai-hackathon)
1) [Sample Submission Proposal](https://ibm.ent.box.com/s/i79u4wus3yve6muafx76t29r5clqx8iu)
2) [Template Submission Proposal](https://ibm.ent.box.com/s/xmxtjba7x774w25nm8agwvoys5s9wljf)


