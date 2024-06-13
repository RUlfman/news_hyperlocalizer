import re
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urljoin


class WebsiteScraper(ABC):
    @abstractmethod
    def scrape_website(self, url):
        pass


# Class for scraping static websites
class StaticWebsiteScraper(WebsiteScraper):
    def scrape_website(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while trying to scrape {url}: {e}")
            return None

        soup = BeautifulSoup(response.content, 'html.parser')
        return str(soup)


# Class for scraping dynamic websites that use JavaScript to load content
class DynamicWebsiteScraper(WebsiteScraper):
    def scrape_website(self, url):
        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--log-level=3")

        try:
            webdriver_service = Service('/usr/bin/chromedriver')
            driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
            driver.get(url)
        except Exception as e:
            print(f"An error occurred while trying to scrape {url}: {e}")
            return None

        # This will ensure that the page is loaded before the html is retrieved
        WebDriverWait(driver, timeout=10).until(lambda d: d.execute_script('return document.readyState') == 'complete')

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        return str(soup)


# Class for scraping websites that use AJAX to load content
class AjaxWebsiteScraper(WebsiteScraper):
    def scrape_website(self, url):
        # Setup Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Ensure GUI is off
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--log-level=3")

        try:
            webdriver_service = Service('/usr/bin/chromedriver')
            driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
            driver.get(url)
        except Exception as e:
            print(f"An error occurred while trying to scrape {url}: {e}")
            return None

        try:
            # Wait for the AJAX content to load
            WebDriverWait(driver, 10).until(
                ec.presence_of_element_located((By.CSS_SELECTOR, "your_css_selector"))
            )
        except Exception as e:
            pass
        finally:
            # Get the page source and parse it with BeautifulSoup
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            driver.quit()

        return str(soup)


def get_scraper(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while trying to scrape {url}: {e}")
        return None

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Check if the HTML contains <script> tags
    is_dynamic = bool(soup.find('script'))

    # Check if the HTML contains AJAX calls
    is_ajax = bool(soup.find('script', text=re.compile('.*ajax.*')))

    if is_ajax:
        return AjaxWebsiteScraper()
    elif is_dynamic:
        return DynamicWebsiteScraper()
    else:
        return StaticWebsiteScraper()


def extract_all_urls(html_content, base_url):
    soup = BeautifulSoup(html_content, 'html.parser')
    urls = [urljoin(base_url, a['href']) for a in soup.find_all('a', href=True)]
    return urls


def extract_story_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract the text content
    text = soup.get_text()

    # Extract the meta properties
    meta_properties = {meta.get('name') or meta.get('property'): meta.get('content') for meta in soup.find_all('meta') if (meta.get('name') or meta.get('property')) and meta.get('content')}

    # Extract the images
    images = [img.get('src') for img in soup.find_all('img') if img.get('src')]

    # Unify the text content, meta properties, and images into a single format
    content = {
        'text': text,
        'meta_properties': meta_properties,
        'images': images
    }

    return content