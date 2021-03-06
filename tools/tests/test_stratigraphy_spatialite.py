# -*- coding: utf-8 -*-
"""
/***************************************************************************
 This part of the Midvatten plugin tests the stratigraphy plot.

 This part is to a big extent based on QSpatialite plugin.
                             -------------------
        begin                : 2017-10-17
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
import midvatten_utils as utils
import mock
from nose.plugins.attrib import attr
from stratigraphy import Stratigraphy

import utils_for_tests


@attr(status='on')
class TestStratigraphy(utils_for_tests.MidvattenTestSpatialiteDbSv):
    @mock.patch('db_utils.QgsProject.instance', utils_for_tests.MidvattenTestSpatialiteNotCreated.mock_instance_settings_database)
    def create_and_select_vlayer(self):
        self.qgs = QgsApplication([], True)
        self.qgs.initQgis()

        self.midvatten.ms.settingsdict['secplotdrillstop'] = u"%berg%"

        dbconnection = db_utils.DbConnectionManager()
        uri = dbconnection.uri
        uri.setDataSource('', 'obs_points', 'geometry', '', 'obsid')
        dbtype = db_utils.get_dbtype(dbconnection.dbtype)
        self.vlayer = QgsVectorLayer(uri.uri(), 'TestLayer', dbtype)
        features = self.vlayer.getFeatures()
        feature_ids = [feature.id() for feature in features]
        self.vlayer.setSelectedFeatures(feature_ids)

    @mock.patch('midvatten_utils.MessagebarAndLog')
    @mock.patch('stratigraphy.utils.pop_up_info', autospec=True)
    @mock.patch('db_utils.QgsProject.instance', utils_for_tests.MidvattenTestSpatialiteNotCreated.mock_instance_settings_database)
    def test_stratigraphy(self, mock_skippopup, mock_messagebar):
        """
        
        :param mock_skippopup:
        :param mock_messagebar:
        :return:
        """
        db_utils.sql_alter_db(u'''INSERT INTO obs_points (obsid, h_gs, geometry) VALUES ('P1', 5, ST_GeomFromText('POINT(633466 711659)', 3006))''')
        db_utils.sql_alter_db(u'''INSERT INTO obs_points (obsid, h_gs, geometry) VALUES ('P2', 10, ST_GeomFromText('POINT(6720727 016568)', 3006))''')
        db_utils.sql_alter_db(u'''INSERT INTO obs_points (obsid, h_gs, geometry) VALUES ('P3', 20, ST_GeomFromText('POINT(6720728 016569)', 3006))''')
        db_utils.sql_alter_db(u'''INSERT INTO stratigraphy (obsid, stratid, depthtop, depthbot, geology, geoshort, capacity, development) VALUES ('P1', 1, 0, 1, 'sand', 'sand', '3', 'j')''')
        db_utils.sql_alter_db(u'''INSERT INTO stratigraphy (obsid, stratid, depthtop, depthbot, geology, geoshort, capacity, development) VALUES ('P1', 2, 1, 4.5, 'morän', 'morän', '3', 'j')''')

        self.create_and_select_vlayer()

        dlg = Stratigraphy(self.iface, self.vlayer, self.ms.settingsdict)

        dlg.showSurvey()
        test = utils.anything_to_string_representation(dlg.data)
        test_survey = utils.anything_to_string_representation(repr(dlg.data[u'P1']))
        test_strata = utils.anything_to_string_representation(utils.returnunicode(dlg.data[u'P1'].strata, keep_containers=True))

        assert len(mock_skippopup.mock_calls) == 0
        assert len(mock_messagebar.mock_calls) == 0
        assert test == u"""{u"P1": SURVEY('P1', 5.000000, '(633466,711659)')}"""
        assert test_survey == u'''"SURVEY('P1', 5.000000, '(633466,711659)')"'''
        print("Test strata " + test_strata)
        assert test_strata == u'''[u"strata(1, '3', 'sand', 'sand', 0.000000-1.000000)", u"strata(2, '3', 'morän', 'moran', 1.000000-4.500000)"]'''

    @mock.patch('midvatten_utils.MessagebarAndLog')
    @mock.patch('stratigraphy.utils.pop_up_info', autospec=True)
    @mock.patch('db_utils.QgsProject.instance', utils_for_tests.MidvattenTestSpatialiteNotCreated.mock_instance_settings_database)
    def test_stratigraphy_gap(self, mock_skippopup, mock_messagebar):
        """
        
        :param mock_skippopup:
        :param mock_messagebar:
        :return:
        """
        db_utils.sql_alter_db(u'''INSERT INTO obs_points (obsid, h_gs, geometry) VALUES ('P1', 5, ST_GeomFromText('POINT(633466 711659)', 3006))''')
        db_utils.sql_alter_db(u'''INSERT INTO obs_points (obsid, h_gs, geometry) VALUES ('P2', 10, ST_GeomFromText('POINT(6720727 016568)', 3006))''')
        db_utils.sql_alter_db(u'''INSERT INTO obs_points (obsid, h_gs, geometry) VALUES ('P3', 20, ST_GeomFromText('POINT(6720728 016569)', 3006))''')
        db_utils.sql_alter_db(u'''INSERT INTO stratigraphy (obsid, stratid, depthtop, depthbot, geology, geoshort, capacity, development) VALUES ('P1', 1, 0, 1, 'sand', 'sand', '3', 'j')''')
        db_utils.sql_alter_db(u'''INSERT INTO stratigraphy (obsid, stratid, depthtop, depthbot, geology, geoshort, capacity, development) VALUES ('P1', 2, 2, 4.5, 'morän', 'morän', '3', 'j')''')

        self.create_and_select_vlayer()

        dlg = Stratigraphy(self.iface, self.vlayer, self.ms.settingsdict)

        dlg.showSurvey()
        test = utils.anything_to_string_representation(dlg.data)
        test_survey = utils.anything_to_string_representation(repr(dlg.data[u'P1']))
        test_strata = utils.anything_to_string_representation(utils.returnunicode(dlg.data[u'P1'].strata, keep_containers=True))

        assert len(mock_skippopup.mock_calls) == 0
        assert len(mock_messagebar.mock_calls) == 0
        assert test == u"""{u"P1": SURVEY('P1', 5.000000, '(633466,711659)')}"""
        assert test_survey == u'''"SURVEY('P1', 5.000000, '(633466,711659)')"'''
        print("Test strata " + test_strata)
        assert test_strata == u'''[u"strata(1, '3', 'sand', 'sand', 0.000000-1.000000)", u"strata(2, '', '', '', 1.000000-2.000000)", u"strata(3, '3', 'morän', 'moran', 2.000000-4.500000)"]'''

    @mock.patch('midvatten_utils.MessagebarAndLog')
    @mock.patch('stratigraphy.utils.pop_up_info', autospec=True)
    @mock.patch('db_utils.QgsProject.instance', utils_for_tests.MidvattenTestSpatialiteNotCreated.mock_instance_settings_database)
    def test_stratigraphy_missing_h_gs_use_h_toc(self, mock_skippopup, mock_messagebar):
        """
        
        :param mock_skippopup:
        :param mock_messagebar:
        :return:
        """
        db_utils.sql_alter_db(u'''INSERT INTO obs_points (obsid, h_gs, geometry) VALUES ('P1', 5, ST_GeomFromText('POINT(633466 711659)', 3006))''')
        db_utils.sql_alter_db(u'''INSERT INTO obs_points (obsid, h_gs, h_toc, geometry) VALUES ('P2', NULL, 10, ST_GeomFromText('POINT(6720727 016568)', 3006))''')
        db_utils.sql_alter_db(u'''INSERT INTO obs_points (obsid, geometry) VALUES ('P3', ST_GeomFromText('POINT(6720728 016569)', 3006))''')
        db_utils.sql_alter_db(u'''INSERT INTO stratigraphy (obsid, stratid, depthtop, depthbot, geology, geoshort, capacity, development) VALUES ('P1', 1, 0, 1, 'sand', 'sand', '3', 'j')''')
        db_utils.sql_alter_db(u'''INSERT INTO stratigraphy (obsid, stratid, depthtop, depthbot, geology, geoshort, capacity, development) VALUES ('P1', 2, 1, 4.5, 'morän', 'morän', '3', 'j')''')
        db_utils.sql_alter_db(u'''INSERT INTO stratigraphy (obsid, stratid, depthtop, depthbot, geology, geoshort, capacity, development) VALUES ('P2', 1, 0, 1, 'sand', 'sand', '3', 'j')''')
        db_utils.sql_alter_db(u'''INSERT INTO stratigraphy (obsid, stratid, depthtop, depthbot, geology, geoshort, capacity, development) VALUES ('P2', 2, 1, 4.5, 'morän', 'morän', '3', 'j')''')
        db_utils.sql_alter_db(u'''INSERT INTO stratigraphy (obsid, stratid, depthtop, depthbot, geology, geoshort, capacity, development) VALUES ('P3', 1, 0, 2, 'sand', 'sand', '3', 'j')''')
        db_utils.sql_alter_db(u'''INSERT INTO stratigraphy (obsid, stratid, depthtop, depthbot, geology, geoshort, capacity, development) VALUES ('P3', 2, 2, 6, 'morän', 'morän', '3', 'j')''')
        self.create_and_select_vlayer()

        dlg = Stratigraphy(self.iface, self.vlayer, self.ms.settingsdict)

        dlg.showSurvey()
        test = utils.anything_to_string_representation(dlg.data)
        test_survey = utils.anything_to_string_representation(repr(dlg.data[u'P1']))
        test_strata = utils.anything_to_string_representation(utils.returnunicode(dlg.data[u'P1'].strata, keep_containers=True))

        assert len(mock_skippopup.mock_calls) == 1
        print(str(mock_skippopup.mock_calls))
        print(str(mock_messagebar.mock_calls))
        assert mock_skippopup.mock_calls == [mock.call(u'Warning, h_gs is missing. See messagebar.')]
        assert mock_messagebar.mock_calls == [mock.call.warning(bar_msg=u"Obsid P2: using h_gs '' failed, using 'h_toc' instead.", duration=90, log_msg=u'False'),
                                              mock.call.warning(bar_msg=u"Obsid P3: using h_gs '' failed, using '-1' instead.", duration=90, log_msg=u'False')]
        print(test)
        assert test == u"""{u"P1": SURVEY('P1', 5.000000, '(633466,711659)'), u"P2": SURVEY('P2', 10.000000, '(6.72073e+06,16568)'), u"P3": SURVEY('P3', -1.000000, '(6.72073e+06,16569)')}"""
        assert test_survey == u'''"SURVEY('P1', 5.000000, '(633466,711659)')"'''
        print("Test strata " + test_strata)
        assert test_strata == u'''[u"strata(1, '3', 'sand', 'sand', 0.000000-1.000000)", u"strata(2, '3', 'morän', 'moran', 1.000000-4.500000)"]'''

    def tearDown(self):
        QgsMapLayerRegistry.instance().addMapLayer(self.vlayer)
        QgsMapLayerRegistry.instance().removeMapLayer(self.vlayer.id())
        super(self.__class__, self).tearDown()
