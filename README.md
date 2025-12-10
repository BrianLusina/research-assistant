# Research Assistant

An AI-powered research assistant capable of performing iterative, deep research on any topic. It combines search engines, 
web scraping via Firecrawl, and large language models (OpenAI's GPT) orchestrated by CrewAI multi-agent workflows. The 
goal of this project is to provide the simplest implementation of a deep research agent, an autonomous system that can 
refine its research direction over time and deep dive into any subject.

## Requirements

### [Python 3.1x+](https://www.python.org/)

Have at least Python 3.1x+ installed on your development machine to use this project and contribute to it. More information
on setting this up can be found in the link.

### [UV](https://docs.astral.sh/uv/)

UV is used as the package manager of choice. To download it follow the instructions outlined in the link provided.

### [OpenAI API Key](https://openai.com/)

Ensure you have an OpenAI account and can get an API key to use for this project. More details on setting that up can be
found in the link. Once you have the key, set that in the `.env` file like below:

```dotenv
OPENAI_API_KEY="<your_openai_api_key>"
```

> Note that this file is not checked into version control

### [FireCrawl API Key](https://www.firecrawl.dev/)

You will also need a Firecrawl API key. Follow the instructions in the link and once you have set up your account, get the
API key and add it to the `.env` file like below:

```dotenv
FIRECRAWL_KEY="<your_firecrawl_api_key>"
```

> Note: While Firecrawl is powerful and easy to use, it may not always return complete or highly relevant results 
> depending on the topic. In such cases, or for more customized control, you may consider alternatives such as:
> SerpAPI: Structured Google search results
> Tavily API: Clean summaries and metadata for queries
 
