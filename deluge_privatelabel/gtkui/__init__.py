#
# Copyright (C) 2008 Martijn Voncken <mvoncken@gmail.com>
#
# This file is part of Deluge and is licensed under GNU General Public License 3.0, or later, with
# the additional special exception to link portions of this program with the OpenSSL library.
# See LICENSE for more details.
#

import logging

from deluge import component  # for systray
from deluge.plugins.pluginbase import Gtk3PluginBase

from . import label_config, sidebar_menu, submenu

log = logging.getLogger(__name__)

SEED_UNTIL_HEADER = 'Seed Until'


def cell_data_seed_until(column, cell, model, row, data):
    """Show a torrent's stop-at-ratio setting compactly.

    ``2.0⏸`` pauses at 2.0:1, ``2.0×`` removes at 2.0:1, and ``∞`` means the
    torrent has no ratio limit.
    """
    ratio, stop_at_ratio, remove_at_ratio = model.get(row, *data)
    if not stop_at_ratio:
        text = '∞'
    else:
        text = '%.2f' % ratio
        if text.endswith('0'):
            text = text[:-1]  # 2.00 -> 2.0, 1.25 stays 1.25
        text += '×' if remove_at_ratio else '⏸'
    cell.set_property('text', text)

NO_LABEL = 'No Label'


def cell_data_label(column, cell, model, row, data):
    cell.set_property('text', str(model.get_value(row, data)))


class GtkUI(Gtk3PluginBase):
    def start(self):
        if self.label_menu:
            self.label_menu.on_show()

    def enable(self):
        self.plugin = component.get('PluginManager')
        self.torrentmenu = component.get('MenuBar').torrentmenu
        self.label_menu = None
        self.labelcfg = None
        self.sidebar_menu = None
        self.load_interface()

    def disable(self):
        if self.label_menu in self.torrentmenu.get_children():
            self.torrentmenu.remove(self.label_menu)

        self.labelcfg.unload()
        self.sidebar_menu.unload()
        del self.sidebar_menu

        component.get('TorrentView').remove_column(_('Label'))
        component.get('TorrentView').remove_column(_(SEED_UNTIL_HEADER))

    def load_interface(self):
        # sidebar
        # disabled
        if not self.sidebar_menu:
            self.sidebar_menu = sidebar_menu.LabelSidebarMenu()
        # self.sidebar.load()

        # menu:
        log.debug('add items to torrentview-popup menu.')
        self.label_menu = submenu.LabelMenu()
        self.torrentmenu.append(self.label_menu)
        self.label_menu.show_all()

        # columns:
        self.load_columns()

        # config:
        if not self.labelcfg:
            self.labelcfg = label_config.LabelConfig(self.plugin)
        self.labelcfg.load()

        log.debug('Finished loading Label plugin')

    def load_columns(self):
        log.debug('add columns')

        component.get('TorrentView').add_text_column(_('Label'), status_field=['label'])
        component.get('TorrentView').add_func_column(
            _(SEED_UNTIL_HEADER),
            cell_data_seed_until,
            [float, bool, bool],
            status_field=['stop_ratio', 'stop_at_ratio', 'remove_at_ratio'],
            tooltip=_(
                'Ratio at which the torrent pauses (⏸) or is removed (×). '
                '∞ means no ratio limit.'
            ),
        )
