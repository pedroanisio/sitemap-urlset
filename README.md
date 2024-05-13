# Sitemap urlset

## Overview
The Sitemap Processor is a Python tool designed to fetch and process XML sitemaps recursively. It leverages multithreading to enhance performance, particularly useful when dealing with large numbers of sitemaps or sitemaps that are deeply nested. This tool navigates through nested sitemap indices and extracts urlset sitemaps efficiently.

## Features
- **Recursive Processing**: Deeply navigate through sitemap indices to find and process all nested urlset sitemaps.
- **Multithreading Support**: Utilizes Python's `concurrent.futures` module to handle multiple sitemaps simultaneously, significantly speeding up the processing time.
- **Error Handling**: Robust error management to ensure stability even with faulty or inaccessible sitemap URLs.
- **Logging**: Detailed logging to trace the steps and errors during the sitemap processing.

## Installation
To use the Sitemap Processor, you need Python installed on your system along with some additional packages. Here's how you can set it up:

```bash
# Clone the repository
git clone https://github.com/yourusername/sitemap-urlset.git
cd sitemap-urlset

# Optionally, set up a virtual environment
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`

# Install required packages
pip install requests
