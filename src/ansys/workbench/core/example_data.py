import os
import logging
import shutil
import urllib.request

class ExampleData:
    """fetch data file from PyWorkbench example data repository."""

    def _get_file_url(filename, dirname):
        return f"https://github.com/pyansys/example-data/raw/master/pyworkbench/{dirname}/{filename}"

    def __retrieve_file(url, local_file_path):
        logging.info(f"Downloading {url} from example data repository ...")

        with urllib.request.urlopen(url) as in_stream:
            if (in_stream.code != 200):
                raise Exception("error getting the url, code " + str(in_stream.code))
            with open(local_file_path, "wb") as out_file:
                shutil.copyfileobj(in_stream, out_file)
        logging.info(f"Downloaded the file as {local_file_path}")

    def download(filename, dirname, local_dir_path):
        url = ExampleData._get_file_url(filename, dirname)
        local_file_path = os.path.join(local_dir_path, filename)
        return ExampleData.__retrieve_file(url, local_file_path)
