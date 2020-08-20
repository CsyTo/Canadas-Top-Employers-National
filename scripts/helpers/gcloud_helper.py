import os
import datetime
import pytz
import sys
import re
from google.cloud import storage
import logging

class ObjectStorage(object):
    def __init__(self):
        client_secrets_path = os.path.abspath('gs_client_secrets.json')
        # os.system("echo %s | base64 -d > %s"
        #     % (os.environ['GS_CLIENT_SECRETS'], client_secrets_path))
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = client_secrets_path
        self.client = storage.Client(project = os.environ['GS_PROJECT'])
        self.bucket = self.client.get_bucket(os.environ['GS_BUCKET'])
        self.init_logger()

    def init_logger(self):
        self.log = logging.getLogger(__name__)

    def download_file(self, file, dest):
        blob = self.bucket.blob(file)
        blob.download_to_filename(dest)

    def upload_file(self, file, remote_path):
        remote_file = storage.Blob(remote_path, self.bucket)
        if '.gz' in file:
            remote_file.upload_from_filename(file, content_type = 'application/gzip')
        else:
            remote_file.upload_from_filename(file)

    def data_out_dir(self, prefix, alias):
        return f'{prefix}/data-out/{alias}'

    def upload_to_latest(self, file, alias):
        latest = os.path.join(self.data_out_dir(alias), 'latest', file.split('/')[-1])
        self.upload_file(file, latest)

    def upload_to_timestamp(self, file, alias):
        today = datetime.datetime.now(tz = pytz.timezone('US/Eastern')).strftime('%Y-%m-%d')
        gs_path = os.path.join(self.data_out_dir(alias), today, file.split('/')[-1])
        self.upload_file(file, gs_path)

    def upload_to_scratch(self, file, alias):
        gs_path =  os.path.join(self.scratch_dir(alias), file.split('/')[-1])
        self.upload_file(file, gs_path)

    def upload_dir(self, prefix, alias):
        all_files = os.listdir(os.path.join(f'tmp/{alias}'))
        for file_name in all_files:
            gs_path =  os.path.join(f"{prefix}/{alias}", file_name)
            file = os.path.join(f'tmp/{alias}/{file_name}')
            self.upload_file(file, gs_path)

    def upload_data_out(self, prefix, alias):
        all_files = os.listdir(os.path.join(f'tmp/data-out/{alias}'))
        for file_name in all_files:
            gs_path =  os.path.join(self.data_out_dir(prefix,alias), file_name)
            file = os.path.join(f'tmp/data-out/{alias}/{file_name}')
            self.upload_file(file, gs_path)

    def list_files(self,prefix,delimiter):
          return self.client.list_blobs(
            self.bucket, prefix=prefix, delimiter=delimiter
          )

    def download_scratch(self,prefix,dir_name,delimiter=None):
        prefix = f"{prefix}/scratch/{dir_name}"
        files = self.list_files(prefix,delimiter)
        file_names = [x.name for x in files]
        if not file_names:
            self.log.info("Folder Not found..")
            return None
        else:
          dest_path = f'tmp/scratch/{dir_name}/'
          if not os.path.exists(dest_path):
              os.mkdir(dest_path)
          for file in file_names:
              file_name = file.split("/")[-1]
              src = os.path.join(f'{prefix}',file_name)
              dest = os.path.join(dest_path,file_name)
              if not os.path.isdir(dest):
                  self.download_file(src,dest)


    def download_data_out_last(self, prefix, delimiter = None):
          date_regex = r'\d{4}-\d{2}-\d{2}'
          files = self.list_files(prefix,delimiter)
          file_names = [x.name for x in files if re.search(date_regex, x.name)]
          if not file_names:
              self.log.info("Folder Not found..")
              return None
          else:
              last_snapshot = sorted(file_names).pop()
              last_date = re.search(date_regex,last_snapshot)[0]
              last_snapshot_prefix = f"{prefix}{last_date}/"
              dest_path = f'tmp/data-out/{last_date}/'
              if not os.path.exists(dest_path):
                  os.mkdir(dest_path)
              ls_files = self.list_files(last_snapshot_prefix,delimiter)
              last_snapshot_files = [x.name for x in ls_files]
              for file in last_snapshot_files:
                 file_name = file.split("/")[-1]
                 src = os.path.join(f'{last_snapshot_prefix}',file_name)
                 dest = os.path.join(dest_path,file_name)
                 if not os.path.isdir(dest):
                    self.download_file(src,dest)
          return last_date
