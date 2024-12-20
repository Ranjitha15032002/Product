from crewai import Crew, Process
from crewai.memory.long_term import EnhanceLongTermMemory, LTMSQLAlchemyStorage
from agents import ProductSearchAgent, WebScraperAgent, ProductAnalysisAgent
from tasks import create_search_task, create_scraping_task, create_analysis_task
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AutomatedProductResearchSystem:
    def __init__(self, db_url: str, serperdev_key: str):
        # Initialize agents with the SerperDev API key
        self.search_agent = ProductSearchAgent(serperdev_key=serperdev_key)
        self.scraper_agent = WebScraperAgent()
        self.analysis_agent = ProductAnalysisAgent()
        
        # Initialize long-term memory with MySQL
        self.long_term_memory = EnhanceLongTermMemory(
            storage=LTMSQLAlchemyStorage(db_url=db_url)
        )

    def process_query(self, query: str):
        try:
            # Create tasks
            search_task = create_search_task(query, self.search_agent)
            scrape_task = create_scraping_task([], self.scraper_agent)
            analysis_task = create_analysis_task({}, self.analysis_agent)

            # Create crew
            crew = Crew(
                agents=[self.search_agent, self.scraper_agent, self.analysis_agent],
                tasks=[search_task, scrape_task, analysis_task],
                process=Process.sequential,
                memory=True,
                long_term_memory=self.long_term_memory
            )

            return crew.kickoff()

        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            raise

def get_user_input():
    """Get product query from user."""
    print("\n=== Automated Product Research System ===")
    while True:
        query = input("\nEnter product to research (e.g., 'iPhone 15 Pro Max'): ").strip()
        if query:
            return query
        print("Query cannot be empty. Please try again.")

def main():
    try:
        # Securely fetch MySQL database connection details
        db_user = os.getenv("MYSQL_USER", "product_user")
        db_password = os.getenv("MYSQL_PASSWORD", "secure_password")
        db_host = os.getenv("MYSQL_HOST", "localhost")
        db_name = os.getenv("MYSQL_DB", "product_memory")
        db_url = f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}"
        
        # Fetch SerperDev API key securely
        serperdev_key = os.getenv("89baa9de3c1cc66e232da827a76aea24d3092a82")
        if not serperdev_key:
            raise ValueError("SerperDev API key is not set. Please set the SERPERDEV_API_KEY environment variable.")
        
        # Initialize system
        system = AutomatedProductResearchSystem(db_url=db_url, serperdev_key=serperdev_key)
        
        # Get user input
        query = get_user_input()
        
        print(f"\nResearching: {query}")
        print("This may take a few moments as we gather information from multiple sources...\n")
        
        # Process query and get results
        result = system.process_query(query)
        
        print("\n=== Product Analysis Results ===")
        print(result)
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        logger.error("Error in main execution", exc_info=True)
    finally:
        print("\nResearch complete!")

if __name__ == "__main__":
    main()
