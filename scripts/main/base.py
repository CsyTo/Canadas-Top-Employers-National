from datetime import date
import urllib.request
import json
import datetime
import logging
import csv
import pytz
from scripts.helpers import *

MAX_RETRIES = 5

class Base:
    def __init__(self, prefix, alias):
        self.prefix = prefix
        self.retrieved_at()
        self.records = FileHelper.local_scratch_dir('downloads', 'records.csv')
        self.init_logger()

    def retrieved_at(self):
        self.retrieved_at = str(date.today())

    def init_logger(self):
        self.log = logging.getLogger(__name__)

    def copy_files_to_latest(self):
        self.log.info("Copying files to latest....")
        FileHelper.copy_to_data_out_latest(self.retrieved_at)

    def copy_parsed_files_to_latest(self):
        self.log.info("Copying files to latest....")
        FileHelper.copy_to_parsed_files_latest(self.retrieved_at)

    def copy_scratch_files_to_latest(self):
        self.log.info("Copying files to latest....")
        FileHelper.copy_scratch_to_latest('downloads')

    def download_data_out_last(self):
        self.log.info("Downloading data out last....")
        prefix = f"{self.prefix}/data-out/"
        return ObjectStorage().download_data_out_last(prefix)

    def download_latest_merged_dir(self):
        self.log.info("Downloading data out last....")
        prefix = f"{self.prefix}/merged/"
        return ObjectStorage().download_data_out_last(prefix)

    def download_scratch(self,dir_name):
        self.log.info("Downloading scratch....")
        return ObjectStorage().download_scratch(self.prefix,dir_name)

    def upload_data(self):
        self.log.info("Uploading files...")
        ObjectStorage().upload_data_out(self.prefix,self.retrieved_at)
        ObjectStorage().upload_data_out(self.prefix,'latest')
        self.log.info("Done uploading files...")
