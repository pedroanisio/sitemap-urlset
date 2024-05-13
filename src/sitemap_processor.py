import requests
import xml.etree.ElementTree as ET
from typing import List
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SitemapProcessor:
    """
    Class responsible for processing XML sitemaps recursively, designed
    to navigate through nested sitemap indices and extract urlset sitemaps,
    now enhanced with multithreading to improve performance.
    """

    def __init__(self):
        """
        Initializes the SitemapProcessor instance.
        """
        pass

    def fetch_sitemap(self, url: str) -> ET.Element:
        """
        Fetches a sitemap from a given URL and parses it into an XML element.

        Args:
            url (str): URL of the sitemap to fetch.

        Returns:
            ET.Element: Parsed XML element of the sitemap.

        Raises:
            ValueError: If the sitemap cannot be fetched or parsed.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()  # Will raise an HTTPError for bad responses
            return ET.fromstring(response.content)
        except requests.RequestException as e:
            logging.error(f"Failed to fetch sitemap at {url}: {e}")
            raise ValueError(f"Failed to fetch sitemap at {url}") from e

    def process_sitemap(self, sitemap: str, namespace: dict) -> List[str]:
        """
        Process a single sitemap URL, either fetching its child sitemaps or returning it if it's a urlset.

        Args:
            sitemap (str): URL of the sitemap to process.
            namespace (dict): XML namespace dictionary.

        Returns:
            List[str]: List of urlset sitemaps or recursive results.
        """
        try:
            xml_root = self.fetch_sitemap(sitemap)
            if xml_root.tag.endswith('sitemapindex'):
                child_sitemaps = [elem.find('sitemap:loc', namespace).text for elem in xml_root.findall('sitemap:sitemap', namespace) if elem.find('sitemap:loc', namespace) is not None]
                return self.process_sitemaps(child_sitemaps)
            elif xml_root.tag.endswith('urlset'):
                return [sitemap]
        except Exception as e:
            logging.error(f"Error processing {sitemap}: {e}")
            return []

    def process_sitemaps(self, sitemaps: List[str]) -> List[str]:
        """
        Recursively processes a list of sitemap URLs using multithreading, extracting and accumulating
        urlset sitemaps until no further nested sitemap indices are found.

        Args:
            sitemaps (List[str]): A list of URLs to sitemap files, which can be
                                  either sitemap indices or urlset sitemaps.

        Returns:
            List[str]: A list of urls pointing to urlset sitemaps, representing
                       the leaf nodes in the sitemap hierarchy.
        """
        urlsets = []
        namespace = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(self.process_sitemap, sitemap, namespace): sitemap for sitemap in sitemaps}
            for future in as_completed(futures):
                urlsets.extend(future.result())
        return urlsets