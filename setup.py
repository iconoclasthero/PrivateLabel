#
# Copyright (C) 2008 Martijn Voncken <mvoncken@gmail.com>
#
# This file is part of Deluge and is licensed under GNU General Public License 3.0, or later, with
# the additional special exception to link portions of this program with the OpenSSL library.
# See LICENSE for more details.
#

from setuptools import find_packages, setup

__plugin_name__ = 'PrivateLabel'
__author__ = 'Iconoclasthero'
__author_email__ = 'privatelabel@iconoclasthero.com'
__version__ = '0.5'
__url__ = 'https://github.com/iconoclasthero/PrivateLabel'
__license__ = 'GPLv3'
__description__ = "Label plugin that auto-applies labels by a torrent's private flag"
__long_description__ = (
    "Fork of Deluge's Label plugin that auto-applies a label to torrents with or without the private flag, "
    "with an apply-to-existing button and a Seed Until ratio column. Replaces the built-in Label plugin; do not enable both."
)
__pkg_data__ = {'deluge_' + __plugin_name__.lower(): ['data/*']}

setup(
    name=__plugin_name__,
    version=__version__,
    description=__description__,
    author=__author__,
    author_email=__author_email__,
    url=__url__,
    license=__license__,
    long_description=__long_description__,
    packages=find_packages(),
    package_data=__pkg_data__,
    entry_points="""
    [deluge.plugin.core]
    %s = deluge_%s:CorePlugin
    [deluge.plugin.gtk3ui]
    %s = deluge_%s:GtkUIPlugin
    """
    % ((__plugin_name__, __plugin_name__.lower()) * 2),
)
