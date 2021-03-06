# -*- coding: utf-8 -*-
#
# Copyright 2012-2015 Spotify AB
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
The implementations of the hdfs clients. The hadoop cli client and the
snakebite client.
"""


from luigi.contrib.hdfs import config as hdfs_config
from luigi.contrib.hdfs import snakebite_client as hdfs_snakebite_client
from luigi.contrib.hdfs import hadoopcli_clients as hdfs_hadoopcli_clients
import luigi.contrib.target
import logging

logger = logging.getLogger('luigi-interface')


def get_autoconfig_client():
    """
    Creates the client as specified in the `luigi.cfg` configuration.
    """
    configured_client = hdfs_config.get_configured_hdfs_client()
    if configured_client == "snakebite":
        return hdfs_snakebite_client.SnakebiteHdfsClient()
    if configured_client == "snakebite_with_hadoopcli_fallback":
        return luigi.contrib.target.CascadingClient([hdfs_snakebite_client.SnakebiteHdfsClient(),
                                                     hdfs_hadoopcli_clients.create_hadoopcli_client()])
    if configured_client == "hadoopcli":
        return hdfs_hadoopcli_clients.create_hadoopcli_client()
    raise Exception("Unknown hdfs client " + hdfs_config.get_configured_hdfs_client())


def _with_ac(method_name):
    def result(*args, **kwargs):
        return getattr(get_autoconfig_client(), method_name)(*args, **kwargs)
    return result

exists = _with_ac('exists')
rename = _with_ac('rename')
remove = _with_ac('remove')
mkdir = _with_ac('mkdir')
listdir = _with_ac('listdir')
