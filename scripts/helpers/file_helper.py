from pathlib import Path
import os
import gzip
import shutil

class FileHelper:
    @classmethod
    def make_tmp(cls):
        Path('tmp/scratch').mkdir(parents=True, exist_ok = True)
        Path('tmp/data-out').mkdir(parents=True, exist_ok = True)

    @classmethod
    def local_scratch_dir(cls, dir_name, filename):
        dir_path = f'tmp/scratch/{dir_name}'
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        return os.path.join(dir_path, filename)

    @classmethod
    def data_in(cls, filename):
        return os.path.join('tmp/data-in', filename)

    @classmethod
    def local_data_out(cls, filename):
        return os.path.join('tmp/data-out', filename)

    @classmethod
    def local_data_out_dir(cls, dir_name, filename):
        dir_path = f'tmp/data-out/{dir_name}'
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        return os.path.join(dir_path, filename)

    @classmethod
    def compress(cls, origin_file):
        os.system('gzip %s' %origin_file)

    @classmethod
    def unzip(cls, origin_file):
        os.system('gzip -d %s' %origin_file)

    @classmethod
    def append_files(cls, input_file, output_file):
        os.system(f'tail -n +2 {input_file} >> {output_file}')

    @classmethod
    def copy_to_data_out_latest(cls, origin):
        data_out_path = f'tmp/data-out/{origin}'
        latest_dir_path = 'tmp/data-out/latest'
        shutil.copytree(os.path.join(data_out_path),os.path.join(latest_dir_path))

    @classmethod
    def copy_to_parsed_files_latest(cls,origin):
        data_out_path = f'tmp/scratch/downloads'
        latest_dir_path = 'tmp/final_parsed/latest'
        shutil.copytree(os.path.join(data_out_path),os.path.join(latest_dir_path))
        shutil.copytree(os.path.join(data_out_path),os.path.join(f"tmp/final_parsed/{origin}"))

    @classmethod
    def copy_scratch_to_latest(cls, origin):
        data_out_path = f'tmp/scratch/{origin}/'
        latest_dir_path = 'tmp/data-out/latest'
        shutil.move(os.path.join(data_out_path),os.path.join(latest_dir_path),copy_function=copy2)
