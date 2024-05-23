# Copyright (C) 2023 - 2024 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Module for downloading example data from the example-data repository."""

import logging
import os
import shutil
import urllib.request


class ExampleData:
    def _get_file_url(filename, dirname):  # noqa: N805
        return f"https://github.com/ansys/example-data/tree/master/pyworkbench/{dirname}/{filename}"

    def __retrieve_file(url, local_file_path):  # noqa: N805
        logging.info(f"Downloading {url} from example data repository ...")

        with urllib.request.urlopen(url) as in_stream:
            if in_stream.code != 200:
                raise Exception("error getting the url, code " + str(in_stream.code))
            with open(local_file_path, "wb") as out_file:
                shutil.copyfileobj(in_stream, out_file)
        logging.info(f"Downloaded the file as {local_file_path}")

    def download(filename, dirname, local_dir_path):  # noqa: N805
        url = ExampleData._get_file_url(filename, dirname)
        local_file_path = os.path.join(local_dir_path, filename)
        return ExampleData.__retrieve_file(url, local_file_path)


__all__ = []
