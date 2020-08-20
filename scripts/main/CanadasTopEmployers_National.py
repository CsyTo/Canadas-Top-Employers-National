import datetime
import csv
import logging
import re
import shutil
import pandas as pd
import requests
from bs4 import BeautifulSoup
import string
import time
from scripts.main.base import Base
from scripts.helpers import *

class CanadasTop100_National(Base):
    def __init__(self,prefix,alias):
        super().__init__(prefix,alias)

    def prepare_snapshot(self,data_out_last):
        if data_out_last:
            self.merged_records = FileHelper.local_data_out_dir(data_out_last,'merged_records.csv')
            FileHelper.unzip(f"{self.merged_records}.gz")

    def combine_files(self,data_out_last):
        self.log.info("Combining files....")
        self.merged = FileHelper.local_data_out_dir(self.retrieved_at, 'merged_records.csv')
        shutil.copy(self.records, self.merged)
        if data_out_last:
            FileHelper.append_files(FileHelper.local_data_out_dir(data_out_last,'merged_records.csv'), self.merged)

    def archive(self,file):
        FileHelper.compress(file)

    def archive_files(self):
        self.log.info("Archiving files....")
        self.archive(self.records)
        self.archive(self.merged)

    def scrape_records(self):
        url = 'https://www.canadastop100.com/national/'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find_all('div', class_='col-md-4')
        company_names = []
        for res in results:
            for tag in res.find_all("li"):
                company_names.append(tag.text)

        df = pd.DataFrame(company_names, columns = ['company_name'])
        df['country'] = 'CANADA'
        df['source_url'] = url
        df['retrieved_at'] = datetime.datetime.today().strftime("%Y-%m-%d")
        print(df)
        return df


    def call(self):
        # data_out_last = self.download_latest_merged_dir()
        # self.prepare_snapshot(data_out_last)
        self.scrape_records()
        # self.combine_files(data_out_last)
        # self.archive_files()
        # self.copy_files_to_latest()
        # self.upload_data()
