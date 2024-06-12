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

"""Module for downloading example data from the ``example-data`` repository."""

import logging
import os
import shutil
import urllib.request


class ExampleData:
    """Provides for downloading example data from the ``example-data`` repository."""

    def _get_file_url(relative_file_path):  # noqa: N805
        """Get the URL of the file in the ``example-data`` repository.

        Parameters
        ----------
        filename : str
            Name of the file.
        dirname : str
            Name of the directory containing the file.

        Returns
        -------
        str
            URL of the file in the ``example-data`` repository.
        """
        return f"https://github.com/ansys/example-data/tree/master/pyworkbench/{relative_file_path}"

    def __retrieve_file(url, local_file_path):  # noqa: N805
        """Download the file from the URL.

        Parameters
        ----------
        url : str
            URL of the file.
        local_file_path : str
            Local path to save the file to.

        Raises
        ------
        Exception
            If the URL is not accessible.
        """
        logging.info(f"Downloading {url} from ``example-data`` repository ...")

        with urllib.request.urlopen(url) as in_stream:
            if in_stream.code != 200:
                raise Exception("error getting the url, code " + str(in_stream.code))
            with open(local_file_path, "wb") as out_file:
                shutil.copyfileobj(in_stream, out_file)
        logging.info(f"Downloaded the file as {local_file_path}.")

    def download(relative_file_path, local_dir_path):  # noqa: N805
        """Download the file from the ``example-data`` repository.

        Parameters
        ----------
        relative_file_path : str
            File path relative to the ``pyworkbench`` folder in the ``example-data`` repository.
        local_dir_path : str
           Local path to the directory to save the file to.

        Returns
        -------
        str
            Name of the downloaded file.
        """
        url = ExampleData._get_file_url(relative_file_path)
        downloaded_file_name = os.path.basename(relative_file_path)
        local_file_path = os.path.join(local_dir_path, downloaded_file_name)
        ExampleData.__retrieve_file(url, local_file_path)
        return downloaded_file_name


__all__ = []
