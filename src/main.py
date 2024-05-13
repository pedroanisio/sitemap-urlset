from flask import Flask, request, jsonify
import logging
from sitemap_processor import SitemapProcessor

# Set up basic configuration for logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

@app.route('/process_sitemaps', methods=['POST'])
def process_sitemaps():
    """
    Receives a POST request with JSON content containing a list of sitemap URLs,
    processes them using the SitemapProcessor, and returns a list of urlset sitemaps.
    """
    try:
        # Expecting JSON data with a 'sitemaps' key
        sitemap_urls = request.json['sitemaps']
        if not isinstance(sitemap_urls, list):
            raise ValueError("Invalid input: 'sitemaps' must be a list of URLs.")
        
        logging.info(f"Received sitemaps to process: {sitemap_urls}")
        processor = SitemapProcessor()
        result = processor.process_sitemaps(sitemap_urls)
        logging.info(f"Processed sitemaps successfully: {result}")
        return jsonify({"urlsets": result}), 200
    except KeyError:
        logging.error("JSON body must include 'sitemaps' key.")
        return jsonify({"error": "JSON body must include 'sitemaps' key."}), 400
    except ValueError as e:
        logging.error(f"Error processing sitemaps: {e}")
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        logging.error(f"Unexpected error occurred: {e}")
        return jsonify({"error": "An error occurred during processing."}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
