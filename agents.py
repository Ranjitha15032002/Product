from crewai import Agent
from crewai.tools import ScrapeWebsiteTool, SerperDevTool
import logging

logger = logging.getLogger(__name__)

class ProductSearchAgent(Agent):
    def __init__(self):
        super().__init__(
            role='Product Search Specialist',
            goal='Find relevant and authoritative sources for product information',
            backstory='''Expert at finding reliable product information sources including 
                        official product pages, major retailers, and trusted review sites''',
            tools=[SerperDevTool()],
            verbose=True
        )

    async def execute(self, task):
        try:
            # Search for product using SerperDevTool
            search_query = f"{task.context['query']} product specifications reviews"
            search_results = await self.tools[0]._arun(search_query)
            
            # Extract relevant URLs (first 3 most relevant)
            relevant_urls = []
            for result in search_results['organic'][:3]:
                relevant_urls.append(result['link'])
                
            return relevant_urls
        except Exception as e:
            logger.error(f"Error in search execution: {str(e)}")
            raise

class WebScraperAgent(Agent):
    def __init__(self):
        super().__init__(
            role='Web Scraping Specialist',
            goal='Extract comprehensive product information from websites',
            backstory='''Expert at extracting and consolidating product information 
                        from multiple sources into a coherent format''',
            tools=[ScrapeWebsiteTool()],
            verbose=True
        )

class ProductAnalysisAgent(Agent):
    def __init__(self):
        super().__init__(
            role='Product Analysis Expert',
            goal='Analyze and summarize product information from multiple sources',
            backstory='''Expert at analyzing product features, specifications, 
                        prices, and reviews to provide comprehensive insights''',
            tools=[SerperDevTool()],
            verbose=True
        )
