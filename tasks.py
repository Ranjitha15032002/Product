from crewai import Task

def create_search_task(query: str, agent) -> Task:
    return Task(
        description=f"Find reliable sources for: {query}",
        agent=agent,
        expected_output="List of relevant URLs for product information",
        context={"query": query}
    )

def create_scraping_task(urls: list, agent) -> Task:
    return Task(
        description="Extract product information from provided URLs",
        agent=agent,
        expected_output="Consolidated product information from all sources",
        context={"urls": urls}
    )

def create_analysis_task(product_data: dict, agent) -> Task:
    return Task(
        description="Analyze and summarize product information",
        agent=agent,
        expected_output="Comprehensive product analysis and summary",
        context={"product_data": product_data}
    )
