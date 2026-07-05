# 📚 BookScraper

An end-to-end web scraping project built with **Scrapy** that crawls book information, cleans and processes the extracted data, and stores it in **both a JSON file and a MySQL database** using custom item pipelines.

## Demo

<p align="center">
  <img src="assets/demo.gif" alt="BookScraper Demo" width="850">
</p>

## Features

* Crawl book information using Scrapy
* Extract product details using XPath selectors
* Clean and preprocess scraped data
* Export scraped data to a JSON file
* Store cleaned data automatically in MySQL
* Modular Scrapy project structure
* Environment variables managed with `.env`
* Configurable Scrapy pipelines and feed exports

## Tech Stack

* Python
* Scrapy
* MySQL
* mysql-connector-python
* python-dotenv

## Project Structure

```text
BookScraper/
├── assets/
│   └── demo.gif
├── bookscraper/
│   ├── spiders/
│   ├── items.py
│   ├── pipelines.py
│   ├── settings.py
│   └── middlewares.py
├── scrapy.cfg
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd BookScraper
```

Create and activate a virtual environment:

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
DB_HOST=localhost
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=bookscraper
```

## Output Configuration

This project supports two output formats:

* **JSON export** using Scrapy's `FEEDS` setting.
* **MySQL database storage** using a custom Scrapy pipeline.

Configure `settings.py` as shown below.

### Export data to JSON

```python
FEEDS = {
    "cleaned_book_infos.json": {
        "format": "json",
        "overwrite": True,
    }
}
```

### Store data in MySQL

Enable the MySQL pipeline:

```python
ITEM_PIPELINES = {
    "bookscraper.pipelines.BookscraperPipeline": 300,
    "bookscraper.pipelines.SaveToMySQLPipeline": 400,
}
```

You can enable or disable these settings depending on whether you want to export to JSON, save to MySQL, or use both simultaneously.

## Run the Spider

```bash
scrapy crawl books_info
```

## Database

The project automatically creates the required MySQL table (if it does not already exist) and inserts each cleaned item into the database through a custom Scrapy pipeline.

## Future Improvements

* Incremental crawling
* Duplicate record detection
* Docker support
* Logging and monitoring
* Export to CSV/Excel
* Scheduling with Scrapy Cloud or cron

## License

This project is intended for educational and portfolio purposes.
