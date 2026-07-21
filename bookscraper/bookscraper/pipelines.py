# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import re
import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookscraperPipeline:
    def process_item(self, item, spider):
        adapter=ItemAdapter(item)
        # to remove white spaces
        fields=adapter.field_names()
        for field in fields:
            value=adapter.get(field)

            if field !='description' and value:
                adapter[field]=value.strip()
        # to lowercase character
        fields=['category','product_type']
        for field in fields:
            value=adapter.get(field)
            if value:
                adapter[field]=value.lower()
        # to convert $ to float
        price_field=['price_exc_tax','price_inc_tax','tax','price']
        for field in price_field:
            adapter[field]=float(adapter.get(field).replace('£','').strip())
            
        # to convert stock  avaialability value from str to float
        value=adapter.get('availability')
        if value:
            match=re.search(r"\d+",value)
            if match:
                adapter['availability']=int(match.group())

        # reviews to integer
        
        adapter['num_reviews']=int(adapter.get('num_reviews'))
        #start rating to int
        rating_map={
            'zero':0,
            'one':1,
            'two':2,
            'three':3,
            'four':4,
            'five':5
        }
        rating =adapter.get("rating")
        if rating:
            adapter["rating"]=rating_map[rating.lower()]
       




        return item

class SaveToMySQLPipeline:

    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME")
            )

            self.cursor = self.conn.cursor()

            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS book_info(
                    id INT NOT NULL AUTO_INCREMENT,
                    title VARCHAR(255),
                    prod_description TEXT,
                    category TEXT,
                    product_type VARCHAR(255),
                    price_exc_tax DECIMAL(10,2),
                    price_inc_tax DECIMAL(10,2),
                    tax DECIMAL(10,2),
                    availability INT,
                    num_reviews INT,
                    price DECIMAL(10,2),
                    rating DECIMAL(10,2),
                    PRIMARY KEY(id)
                )
            """)

            self.conn.commit() # ensure data is permanetely safe

            print(" Connected to MySQL successfully.")

        except Error as err:
            print(f"MySQL Connection Error: {err}")
            raise # stop the flow

    def process_item(self, item, spider):
        try:
            sql = """
                INSERT INTO book_info(
                    title,
                    prod_description,
                    category,
                    product_type,
                    price_exc_tax,
                    price_inc_tax,
                    tax,
                    availability,
                    num_reviews,
                    price,
                    rating
                )
                VALUES(
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
            """

            values = (
                item["title"],
                item["prod_description"],
                item["category"],
                item["product_type"],
                item["price_exc_tax"],
                item["price_inc_tax"],
                item["tax"],
                item["availability"],
                item["num_reviews"],
                item["price"],
                item["rating"]
            )

            self.cursor.execute(sql, values)
            self.conn.commit()

        except Error as err:
            print(f"MySQL Insert Error: {err}")
            self.conn.rollback()

        return item

    def close_spider(self, spider):
        try:
            if hasattr(self, "cursor"):
                self.cursor.close()

            if hasattr(self, "conn") and self.conn.is_connected():
                self.conn.close()

            print("MySQL connection closed.")

        except Error as err:
            print(f"MySQL Close Error: {err}")