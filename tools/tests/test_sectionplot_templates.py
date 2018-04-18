# -*- coding: utf-8 -*-
"""
/***************************************************************************
 This part of the Midvatten plugin tests the sectionplot templates.

 This part is to a big extent based on QSpatialite plugin.
                             -------------------
        begin                : 2016-03-08
        copyright            : (C) 2016 by joskal (HenrikSpa)
        email                : groundwatergis [at] gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from qgis.core import QgsMapLayerRegistry, QgsVectorLayer, QgsApplication

import db_utils
import gui_utils
import ast
import io
import os
import mock
from mock import call
from nose.plugins.attrib import attr
from utils import returnunicode as ru
import PyQt4

import utils_for_tests
import utils
import sectionplot
from definitions import midvatten_defs as defs

@attr(status='on')
class TestSecplotTemplates(utils_for_tests.MidvattenTestSpatialiteNotCreated):

    def setUp(self):
        super(self.__class__, self).setUp()
        self.template_list = PyQt4.QtGui.QListWidget()
        self.sectionplot = mock.MagicMock()

    @mock.patch('midvatten_utils.MessagebarAndLog')
    def test_load_from_msettings(self, mock_messagebar):
        test_str = '''{"test": 1}'''
        self.midvatten.ms.settingsdict['secplot_loaded_template'] = test_str
        self.midvatten.ms.settingsdict['secplot_templates'] = ''

        secplottemplates = sectionplot.SecplotTemplates(self.sectionplot, self.template_list, self.midvatten.ms)

        assert call.info(log_msg=u'Loaded template from midvatten settings secplot_loaded_template.') in mock_messagebar.mock_calls
        assert utils.anything_to_string_representation(secplottemplates.loaded_template) == test_str

    def test_load_default_file(self):
        default_file = u'''{'Axes_set_ylabel': {'fontsize': 10}, 'wlevels_Axes_plot': {'DEFAULT': {'marker': 'v', 'markersize': 6, 'linewidth': 1, 'linestyle': '-'}}, 'geology_Axes_bar': {'edgecolor': 'black'}, 'obsid_Axes_bar': {'edgecolor': 'black', 'linewidth': 0.5, 'fill': False}, 'dems_Axes_plot': {'DEFAULT': {'marker': 'None', 'linewidth': 1, 'linestyle': '-'}}, 'Axes_set_xlabel': {'fontsize': 10}, 'Axes_set_ylim': None, 'plot_width': None, 'grid_Axes_grid': {'color': '0.65', 'b': True, 'linestyle': '-', 'which': 'both'}, 'legend_Axes_legend': {'loc': 0, 'framealpha': 1, 'fontsize': 10}, 'legend_Frame_set_fill': False, 'plot_height': None, 'layer_Axes_annotate': {'va': 'center', 'xytext': (5, 0), 'fontsize': 9, 'bbox': {'alpha': 0.6, 'fc': 'white', 'boxstyle': 'square,pad=0.05', 'edgecolor': 'white'}, 'ha': 'left', 'textcoords': 'offset points'}, 'ticklabels_Text_set_fontsize': {'fontsize': 10}, 'legend_Text_set_fontsize': 10, 'Figure_subplots_adjust': {}, 'Axes_set_xlim': None, 'obsid_Axes_annotate': {'va': 'top', 'xytext': (0, 10), 'fontsize': 9, 'bbox': {'alpha': 0.4, 'fc': 'white', 'boxstyle': 'square,pad=0.05', 'edgecolor': 'white'}, 'rotation': 0, 'ha': 'center', 'textcoords': 'offset points'}, 'drillstop_Axes_plot': {'color': 'black', 'marker': '^', 'markersize': 8, 'linestyle': ''}, 'legend_Frame_set_facecolor': '1'}'''
        as_dict = ast.literal_eval(default_file)

        self.midvatten.ms.settingsdict['secplot_loaded_template'] = ''

        with utils.tempinput(default_file, u'utf-8') as f1:

            @mock.patch('midvatten_utils.MessagebarAndLog')
            @mock.patch('os.path.join')
            def _test(self, filename, mock_join, mock_messagebar):
                mock_join.return_value = filename
                self.midvatten.ms.settingsdict['secplot_templates'] = filename
                secplottemplates = sectionplot.SecplotTemplates(self.sectionplot, self.template_list, self.midvatten.ms)
                return secplottemplates, mock_messagebar

            secplottemplates, mock_messagebar = _test(self, f1)

        assert call.info(log_msg=u'Loaded template from default template file.') in mock_messagebar.mock_calls
        assert utils.anything_to_string_representation(secplottemplates.loaded_template) == utils.anything_to_string_representation(as_dict)

    def test_import_files_load(self):
        afile = u'''{"loaded_file": 2}'''
        as_dict = ast.literal_eval(afile)

        self.midvatten.ms.settingsdict['secplot_loaded_template'] = ''

        with utils.tempinput(afile, u'utf-8') as f1:

            @mock.patch('midvatten_utils.select_files')
            @mock.patch('midvatten_utils.MessagebarAndLog')
            @mock.patch('os.path.join')
            def _test(self, filename, mock_join, mock_messagebar, mock_select_files):
                mock_join.return_value = ''
                mock_select_files.return_value = [filename]
                self.midvatten.ms.settingsdict['secplot_templates'] = ''
                secplottemplates = sectionplot.SecplotTemplates(self.sectionplot, self.template_list, self.midvatten.ms)
                secplottemplates.import_templates()
                item = [self.template_list.item(idx) for idx in xrange(self.template_list.count())][0]
                item.setSelected(True)
                secplottemplates.load()

                return secplottemplates, mock_messagebar, filename

            secplottemplates, mock_messagebar, reference_filename = _test(self, f1)

        items = [self.template_list.item(idx) for idx in xrange(self.template_list.count())]
        filename = items[0].filename
        assert filename == reference_filename

        test = utils.anything_to_string_representation(secplottemplates.loaded_template)
        reference = utils.anything_to_string_representation(as_dict)
        assert test == reference

    def test_remove(self):
        default_file = u'''{'Axes_set_ylabel': {'fontsize': 10}, 'wlevels_Axes_plot': {'DEFAULT': {'marker': 'v', 'markersize': 6, 'linewidth': 1, 'linestyle': '-'}}, 'geology_Axes_bar': {'edgecolor': 'black'}, 'obsid_Axes_bar': {'edgecolor': 'black', 'linewidth': 0.5, 'fill': False}, 'dems_Axes_plot': {'DEFAULT': {'marker': 'None', 'linewidth': 1, 'linestyle': '-'}}, 'Axes_set_xlabel': {'fontsize': 10}, 'Axes_set_ylim': None, 'plot_width': None, 'grid_Axes_grid': {'color': '0.65', 'b': True, 'linestyle': '-', 'which': 'both'}, 'legend_Axes_legend': {'loc': 0, 'framealpha': 1, 'fontsize': 10}, 'legend_Frame_set_fill': False, 'plot_height': None, 'layer_Axes_annotate': {'va': 'center', 'xytext': (5, 0), 'fontsize': 9, 'bbox': {'alpha': 0.6, 'fc': 'white', 'boxstyle': 'square,pad=0.05', 'edgecolor': 'white'}, 'ha': 'left', 'textcoords': 'offset points'}, 'ticklabels_Text_set_fontsize': {'fontsize': 10}, 'legend_Text_set_fontsize': 10, 'Figure_subplots_adjust': {}, 'Axes_set_xlim': None, 'obsid_Axes_annotate': {'va': 'top', 'xytext': (0, 10), 'fontsize': 9, 'bbox': {'alpha': 0.4, 'fc': 'white', 'boxstyle': 'square,pad=0.05', 'edgecolor': 'white'}, 'rotation': 0, 'ha': 'center', 'textcoords': 'offset points'}, 'drillstop_Axes_plot': {'color': 'black', 'marker': '^', 'markersize': 8, 'linestyle': ''}, 'legend_Frame_set_facecolor': '1'}'''

        self.midvatten.ms.settingsdict['secplot_loaded_template'] = ''

        with utils.tempinput(default_file, u'utf-8') as f1:

            @mock.patch('midvatten_utils.MessagebarAndLog')
            @mock.patch('os.path.join')
            def _test(self, filename, mock_join, mock_messagebar):
                mock_join.return_value = filename
                self.midvatten.ms.settingsdict['secplot_templates'] = filename
                secplottemplates = sectionplot.SecplotTemplates(self.sectionplot, self.template_list, self.midvatten.ms)
                return secplottemplates, mock_messagebar

            secplottemplates, mock_messagebar = _test(self, f1)

        assert self.template_list.count() == 1

        item = [self.template_list.item(idx) for idx in xrange(self.template_list.count())][0]
        item.setSelected(True)
        secplottemplates.remove()

        assert self.template_list.count() == 0

    def test_save_as(self):
        afile = u'''{
    "file_to_save": 3}'''

        self.midvatten.ms.settingsdict['secplot_loaded_template'] = ''

        with utils.tempinput('', u'utf-8') as save_file:
            with utils.tempinput(afile, u'utf-8') as f1:
                @mock.patch('PyQt4.QtGui.QFileDialog.getSaveFileName')
                @mock.patch('midvatten_utils.select_files')
                @mock.patch('midvatten_utils.MessagebarAndLog')
                @mock.patch('os.path.join')
                def _test(self, filename, save_file, mock_join, mock_messagebar, mock_select_files, mock_save_filename):
                    mock_join.return_value = ''
                    mock_select_files.return_value = [filename]
                    mock_save_filename.return_value = save_file
                    self.midvatten.ms.settingsdict['secplot_templates'] = ''
                    secplottemplates = sectionplot.SecplotTemplates(self.sectionplot, self.template_list,
                                                                    self.midvatten.ms)
                    secplottemplates.import_templates()
                    item = [self.template_list.item(idx) for idx in xrange(self.template_list.count())][0]
                    item.setSelected(True)
                    secplottemplates.load()
                    secplottemplates.save_as()

                    return secplottemplates, mock_messagebar, filename

                secplottemplates, mock_messagebar, reference_filename = _test(self, f1, save_file)

        with io.open(save_file, encoding='utf-8') as f:
            lines = u''.join(f.readlines())

        assert lines == afile
        assert self.template_list.count() == 2

    @mock.patch('sectionplot.defs.secplot_default_template')
    @mock.patch('os.path.join')
    @mock.patch('midvatten_utils.MessagebarAndLog')
    def test_load_hard_coded_settings(self, mock_messagebar, mock_join, mock_hardcoded_template):
        self.midvatten.ms.settingsdict['secplot_loaded_template'] = ''
        self.midvatten.ms.settingsdict['secplot_templates'] = ''
        mock_join.return_value = ''
        test_dict = {"hardcoded": 1}
        mock_hardcoded_template.return_value = test_dict

        secplottemplates = sectionplot.SecplotTemplates(self.sectionplot, self.template_list, self.midvatten.ms)
        test = utils.anything_to_string_representation(secplottemplates.loaded_template)
        reference = utils.anything_to_string_representation(test_dict)

        assert call.warning(bar_msg=u'Default template not found, loading hard coded default template.') in mock_messagebar.mock_calls
        assert call.info(log_msg=u'Loaded template from default hard coded template.') in mock_messagebar.mock_calls
        assert test == reference

@attr(status='on')
class TestDefaultHardcodedTemplate(object):
    def test_secplot_default_template(self):
        adict = defs.secplot_default_template()
        assert isinstance(adict, dict)
        assert adict