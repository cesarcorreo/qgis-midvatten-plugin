# -*- coding: utf-8 -*-
"""
/***************************************************************************
 This part of the Midvatten plugin tests the module that handles importing of
  measurements.
 
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
from collections import OrderedDict

import db_utils
import mock
import nose
from import_data_to_db import MidvDataImporterError
from mock import call
from nose.plugins.attrib import attr

import utils_for_tests


@attr(status='on')
class TestGeneralImport(utils_for_tests.MidvattenTestPostgisDbSvImportInstance):
    """ Test to make sure wlvllogg_import goes all the way to the end without errors
    """

    @mock.patch('midvatten_utils.MessagebarAndLog')
    @mock.patch('db_utils.QgsProject.instance', utils_for_tests.MidvattenTestPostgisNotCreated.mock_instance_settings_database)
    @mock.patch('db_utils.get_postgis_connections', utils_for_tests.MidvattenTestPostgisNotCreated.mock_postgis_connections)
    @mock.patch('import_data_to_db.utils.Askuser', mock.MagicMock())
    def test_general_import_wlvllogg(self, mock_messagebar):
        file = [(u'obsid',u'date_time',u'head_cm'),
                (u'rb1',u'2016-03-15 10:30:00',u'1')]
        db_utils.sql_alter_db(u'''INSERT INTO obs_points (obsid) VALUES ('rb1')''')
        self.importinstance.general_import(goal_table=u'w_levels_logger', file_data=file)

        test_string = utils_for_tests.create_test_string(
            db_utils.sql_load_fr_db(u'''select obsid, date_time, head_cm, temp_degc, cond_mscm, level_masl, comment from w_levels_logger'''))
        reference_string = ur'''(True, [(rb1, 2016-03-15 10:30:00, 1.0, None, None, None, None)])'''
        print(str(mock_messagebar.mock_calls))
        print(test_string)
        assert test_string == reference_string

    @mock.patch('midvatten_utils.MessagebarAndLog')
    @mock.patch('db_utils.QgsProject.instance', utils_for_tests.MidvattenTestPostgisNotCreated.mock_instance_settings_database)
    @mock.patch('db_utils.get_postgis_connections', utils_for_tests.MidvattenTestPostgisNotCreated.mock_postgis_connections)
    @mock.patch('import_data_to_db.utils.Askuser', mock.MagicMock())
    @mock.patch('qgis.utils.iface', autospec=True)
    def test_general_import_wlvllogg_missing_not_null_column(self, mock_iface, mock_messagebar):
        file = [(u'obsids',u'date_time',u'test'),
                (u'rb1',u'2016-03-15 10:30:00',u'1')]

        db_utils.sql_alter_db(u'''INSERT INTO obs_points (obsid) VALUES ('rb1')''')

        nose.tools.assert_raises(MidvDataImporterError, self.importinstance.general_import, goal_table=u'w_levels_logger', file_data=file)
        mock_iface.messageBar.return_value.createMessage.createMessage(u'Import error, see log message panel')
        test_string = utils_for_tests.create_test_string(
            db_utils.sql_load_fr_db(u'''select obsid, date_time, head_cm, temp_degc, cond_mscm, level_masl, comment from w_levels_logger'''))
        reference_string = ur'''(True, [])'''
        assert test_string == reference_string

    @mock.patch('db_utils.QgsProject.instance', utils_for_tests.MidvattenTestPostgisNotCreated.mock_instance_settings_database)
    @mock.patch('db_utils.get_postgis_connections', utils_for_tests.MidvattenTestPostgisNotCreated.mock_postgis_connections)
    @mock.patch('import_data_to_db.utils.Askuser', mock.MagicMock())
    def test_general_import_wlvllogg_with_comment(self):
        file = [(u'obsid', u'date_time' ,u'head_cm',u'comment'),
                (u'rb1', u'2016-03-15 10:30:00', u'1', u'testcomment')]

        db_utils.sql_alter_db(u'''INSERT INTO obs_points (obsid) VALUES ('rb1')''')
        self.importinstance.general_import(goal_table=u'w_levels_logger', file_data=file)
        test_string = utils_for_tests.create_test_string(
            db_utils.sql_load_fr_db(u'''select obsid, date_time, head_cm, temp_degc, cond_mscm, level_masl, comment from w_levels_logger'''))
        reference_string = ur'''(True, [(rb1, 2016-03-15 10:30:00, 1.0, None, None, None, testcomment)])'''
        assert test_string == reference_string

    @mock.patch('db_utils.QgsProject.instance', utils_for_tests.MidvattenTestPostgisNotCreated.mock_instance_settings_database)
    @mock.patch('db_utils.get_postgis_connections', utils_for_tests.MidvattenTestPostgisNotCreated.mock_postgis_connections)
    @mock.patch('import_data_to_db.utils.Askuser', mock.MagicMock())
    def test_general_import_wlvllogg_with_temp(self):
        file = [(u'obsid', u'date_time', u'head_cm', u'temp_degc'),
                (u'rb1', u'2016-03-15 10:30:00', u'1', u'5')]
        db_utils.sql_alter_db(u'''INSERT INTO obs_points (obsid) VALUES ('rb1')''')
        self.importinstance.general_import(goal_table=u'w_levels_logger', file_data=file)

        test_string = utils_for_tests.create_test_string(
            db_utils.sql_load_fr_db(u'''select obsid, date_time, head_cm, temp_degc, cond_mscm, level_masl, comment from w_levels_logger'''))
        reference_string = ur'''(True, [(rb1, 2016-03-15 10:30:00, 1.0, 5.0, None, None, None)])'''
        assert test_string == reference_string

    @mock.patch('db_utils.QgsProject.instance', utils_for_tests.MidvattenTestPostgisNotCreated.mock_instance_settings_database)
    @mock.patch('db_utils.get_postgis_connections', utils_for_tests.MidvattenTestPostgisNotCreated.mock_postgis_connections)
    @mock.patch('import_data_to_db.utils.Askuser', mock.MagicMock())
    def test_general_import_wlvllogg_with_temp_comment(self):
        file = [(u'obsid', u'date_time', u'head_cm', u'temp_degc', u'cond_mscm'),
                (u'rb1', u'2016-03-15 10:30:00', u'1', u'5', u'10')]

        db_utils.sql_alter_db(u'''INSERT INTO obs_points (obsid) VALUES ('rb1')''')
        self.importinstance.general_import(goal_table=u'w_levels_logger', file_data=file)
        test_string = utils_for_tests.create_test_string(
            db_utils.sql_load_fr_db(u'''select obsid, date_time, head_cm, temp_degc, cond_mscm, level_masl, comment from w_levels_logger'''))
        reference_string = ur'''(True, [(rb1, 2016-03-15 10:30:00, 1.0, 5.0, 10.0, None, None)])'''
        assert test_string == reference_string

    @mock.patch('db_utils.QgsProject.instance', utils_for_tests.MidvattenTestPostgisNotCreated.mock_instance_settings_database)
    @mock.patch('db_utils.get_postgis_connections', utils_for_tests.MidvattenTestPostgisNotCreated.mock_postgis_connections)
    @mock.patch('import_data_to_db.utils.Askuser', mock.MagicMock())
    def test_general_import_wlvllogg_different_order(self):
        file = [(u'obsid', u'cond_mscm', u'date_time', u'head_cm', u'temp_degc'),
                 (u'rb1', u'10', u'2016-03-15 10:30:00', u'1', u'5')]

        db_utils.sql_alter_db(u'''INSERT INTO obs_points (obsid) VALUES ('rb1')''')
        self.importinstance.general_import(goal_table=u'w_levels_logger', file_data=file)

        test_string = utils_for_tests.create_test_string(
            db_utils.sql_load_fr_db(u'''select obsid, date_time, head_cm, temp_degc, cond_mscm, level_masl, comment from w_levels_logger'''))
        reference_string = ur'''(True, [(rb1, 2016-03-15 10:30:00, 1.0, 5.0, 10.0, None, None)])'''
        assert test_string == reference_string

    @mock.patch('db_utils.QgsProject.instance', utils_for_tests.MidvattenTestPostgisNotCreated.mock_instance_settings_database)
    @mock.patch('db_utils.get_postgis_connections', utils_for_tests.MidvattenTestPostgisNotCreated.mock_postgis_connections)
    @mock.patch('import_data_to_db.utils.Askuser', mock.MagicMock())
    def test_general_import_wlvllogg_only_level_masl(self):
        file = [(u'obsid', u'date_time', u'level_masl'),
                (u'rb1', u'2016-03-15 10:30:00', u'1')]

        db_utils.sql_alter_db(u'''INSERT INTO obs_points (obsid) VALUES ('rb1')''')
        self.importinstance.general_import(goal_table=u'w_levels_logger', file_data=file)

        test_string = utils_for_tests.create_test_string(
            db_utils.sql_load_fr_db(u'''select obsid, date_time, head_cm, temp_degc, cond_mscm, level_masl, comment from w_levels_logger'''))
        reference_string = ur'''(True, [(rb1, 2016-03-15 10:30:00, None, None, None, 1.0, None)])'''
        assert test_string == reference_string

    @mock.patch('db_utils.QgsProject.instance', utils_for_tests.MidvattenTestPostgisNotCreated.mock_instance_settings_database)
    @mock.patch('db_utils.get_postgis_connections', utils_for_tests.MidvattenTestPostgisNotCreated.mock_postgis_connections)
    @mock.patch('import_data_to_db.utils.Askuser', mock.MagicMock())
    def test_general_import_wlvllogg_only_temp_degc(self):
        file = [(u'obsid', u'date_time', u'temp_degc'),
                 (u'rb1', u'2016-03-15 10:30:00', u'1')]

        db_utils.sql_alter_db(u'''INSERT INTO obs_points (obsid) VALUES ('rb1')''')
        self.importinstance.general_import(goal_table=u'w_levels_logger', file_data=file)

        test_string = utils_for_tests.create_test_string(
            db_utils.sql_load_fr_db(u'''select obsid, date_time, head_cm, temp_degc, cond_mscm, level_masl, comment from w_levels_logger'''))
        reference_string = ur'''(True, [(rb1, 2016-03-15 10:30:00, None, 1.0, None, None, None)])'''
        assert test_string == reference_string

    @mock.patch('db_utils.QgsProject.instance', utils_for_tests.MidvattenTestPostgisNotCreated.mock_instance_settings_database)
    @mock.patch('db_utils.get_postgis_connections', utils_for_tests.MidvattenTestPostgisNotCreated.mock_postgis_connections)
    @mock.patch('import_data_to_db.utils.Askuser', mock.MagicMock())
    def test_general_import_wlvllogg_only_cond_mscm(self):
        file = [(u'obsid', u'date_time', u'cond_mscm'),
                 (u'rb1', u'2016-03-15 10:30:00', u'1')]

        db_utils.sql_alter_db(u'''INSERT INTO obs_points (obsid) VALUES ('rb1')''')
        self.importinstance.general_import(goal_table=u'w_levels_logger', file_data=file)

        test_string = utils_for_tests.create_test_string(
            db_utils.sql_load_fr_db(u'''select obsid, date_time, head_cm, temp_degc, cond_mscm, level_masl, comment from w_levels_logger'''))
        reference_string = ur'''(True, [(rb1, 2016-03-15 10:30:00, None, None, 1.0, None, None)])'''
        assert test_string == reference_string

    @mock.patch('midvatten_utils.MessagebarAndLog')
    @mock.patch('db_utils.QgsProject.instance', utils_for_tests.MidvattenTestPostgisNotCreated.mock_instance_settings_database)
    @mock.patch('db_utils.get_postgis_connections', utils_for_tests.MidvattenTestPostgisNotCreated.mock_postgis_connections)
    @mock.patch('import_data_to_db.utils.Askuser', mock.MagicMock())
    def test_general_import_import_null(self, mock_messagebar):
        file = [(u'obsid',u'date_time',u'head_cm'),
                (u'rb1',u'2016-03-15 10:30:00',u'')]

        db_utils.sql_alter_db(u'''INSERT INTO obs_points (obsid) VALUES ('rb1')''')

        self.importinstance.general_import(goal_table=u'w_levels_logger', file_data=file)

        test_string = utils_for_tests.create_test_string(
            db_utils.sql_load_fr_db(u'''select obsid, date_time, head_cm, temp_degc, cond_mscm, level_masl, comment from w_levels_logger'''))
        reference_string = ur'''(True, [(rb1, 2016-03-15 10:30:00, None, None, None, None, None)])'''
        print(str(mock_messagebar.mock_calls))
        print(test_string)
        assert test_string == reference_string


@attr(status='on')
class TestImportObsPointsObsLines(utils_for_tests.MidvattenTestPostgisDbSvImportInstance):
    @mock.patch('db_utils.QgsProject.instance', utils_for_tests.MidvattenTestPostgisNotCreated.mock_instance_settings_database)
    @mock.patch('db_utils.get_postgis_connections', utils_for_tests.MidvattenTestPostgisNotCreated.mock_postgis_connections)
    @mock.patch('import_data_to_db.utils.Askuser', mock.MagicMock())
    def test_import_obsids_directly(self):
        db_utils.sql_alter_db(u"INSERT INTO obs_points (obsid) VALUES ('obsid1')")
        db_utils.sql_alter_db(u"INSERT INTO obs_points (obsid) VALUES ('obsid2')")
        result = db_utils.sql_load_fr_db(u'select * from obs_points')
        assert result == (True, [(u'obsid1', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None), (u'obsid2', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)])

    @mock.patch('db_utils.QgsProject.instance', utils_for_tests.MidvattenTestPostgisNotCreated.mock_instance_settings_database)
    @mock.patch('db_utils.get_postgis_connections', utils_for_tests.MidvattenTestPostgisNotCreated.mock_postgis_connections)
    @mock.patch('import_data_to_db.utils.Askuser', mock.MagicMock())
    def test_import_obs_points(self):
        f = [[u'obsid', u'name', u'place', u'type', u'length', u'drillstop', u'diam', u'material', u'screen', u'capacity', u'drilldate', u'wmeas_yn', u'wlogg_yn', u'east', u'north', u'ne_accur', u'ne_source', u'h_toc', u'h_tocags', u'h_gs', u'h_accur', u'h_syst', u'h_source', u'source', u'com_onerow', u'com_html'],
             [u'rb1', u'rb1', u'a', u'pipe', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'421484', u'6542696', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1']]

        self.importinstance.general_import(file_data=f, goal_table=u'obs_points')

        test_string = utils_for_tests.create_test_string(
            db_utils.sql_load_fr_db(u'''select obsid, name, place, type, length, drillstop, diam, material, screen, capacity, drilldate, wmeas_yn, wlogg_yn, east, north, ne_accur, ne_source, h_toc, h_tocags, h_gs, h_accur, h_syst, h_source, source, com_onerow, com_html, ST_AsText(geometry) from obs_points'''))

        reference_string = ur'''(True, [(rb1, rb1, a, pipe, 1.0, 1, 1.0, 1, 1, 1, 1, 1, 1, 421484.0, 6542696.0, 1.0, 1, 1.0, 1.0, 1.0, 1.0, 1, 1, 1, 1, 1, POINT(421484 6542696))])'''
        assert test_string == reference_string

    @mock.patch('qgis.utils.iface')
    @mock.patch('db_utils.QgsProject.instance', utils_for_tests.MidvattenTestPostgisNotCreated.mock_instance_settings_database)
    @mock.patch('db_utils.get_postgis_connections', utils_for_tests.MidvattenTestPostgisNotCreated.mock_postgis_connections)
    @mock.patch('import_data_to_db.utils.Askuser', mock.MagicMock())
    def test_import_obs_points_already_exist(self, mock_iface):
        db_utils.sql_alter_db(u'''insert into obs_points (obsid) values ('rb1')''')
        self.importinstance.charsetchoosen = [u'utf-8']

        f = [[u'obsid', u'name', u'place', u'type', u'length', u'drillstop', u'diam', u'material', u'screen', u'capacity', u'drilldate', u'wmeas_yn', u'wlogg_yn', u'east', u'north', u'ne_accur', u'ne_source', u'h_toc', u'h_tocags', u'h_gs', u'h_accur', u'h_syst', u'h_source', u'source', u'com_onerow', u'com_html'],
             [u'rb1', u'rb1', u'a', u'pipe', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'421484', u'6542696', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1']]

        self.importinstance.general_import(file_data=f, goal_table=u'obs_points')
        assert call.messageBar().createMessage(u'0 rows imported and 1 excluded for table obs_points. See log message panel for details') in mock_iface.mock_calls

        test_string = utils_for_tests.create_test_string(
            db_utils.sql_load_fr_db(u'''select obsid, name, place, type, length, drillstop, diam, material, screen, capacity, drilldate, wmeas_yn, wlogg_yn, east, north, ne_accur, ne_source, h_toc, h_tocags, h_gs, h_accur, h_syst, h_source, source, com_onerow, com_html, ST_AsText(geometry) from obs_points'''))

        reference_string = ur'''(True, [(rb1, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)])'''
        assert test_string == reference_string

    @mock.patch('db_utils.QgsProject.instance', utils_for_tests.MidvattenTestPostgisNotCreated.mock_instance_settings_database)
    @mock.patch('db_utils.get_postgis_connections', utils_for_tests.MidvattenTestPostgisNotCreated.mock_postgis_connections)
    @mock.patch('import_data_to_db.utils.Askuser', mock.MagicMock())
    @mock.patch('midvatten_utils.MessagebarAndLog')
    def test_import_obs_points_duplicates(self, mock_messagebar):
        f = [[u'obsid', u'name', u'place', u'type', u'length', u'drillstop', u'diam', u'material', u'screen', u'capacity', u'drilldate', u'wmeas_yn', u'wlogg_yn', u'east', u'north', u'ne_accur', u'ne_source', u'h_toc', u'h_tocags', u'h_gs', u'h_accur', u'h_syst', u'h_source', u'source', u'com_onerow', u'com_html'],
         [u'rb1', u'rb1', u'a', u'pipe', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'421484', u'6542696', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1'],
         [u'rb1', u'rb2', u'a', u'pipe', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'421485', u'6542697', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1'],
         [u'rb1', u'rb3', u'a', u'pipe', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'421484', u'6542696', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1']]

        self.importinstance.general_import(file_data=f, goal_table=u'obs_points')

        call.info(bar_msg=u'1 rows imported and 2 excluded for table obs_points. See log message panel for details', log_msg=u'2 nr of duplicate rows in file was skipped while importing.\n--------------------') in mock_messagebar.mock_calls
        test_string = utils_for_tests.create_test_string(
            db_utils.sql_load_fr_db(u'''select obsid, name, place, type, length, drillstop, diam, material, screen, capacity, drilldate, wmeas_yn, wlogg_yn, east, north, ne_accur, ne_source, h_toc, h_tocags, h_gs, h_accur, h_syst, h_source, source, com_onerow, com_html, ST_AsText(geometry) from obs_points'''))

        reference_string = ur'''(True, [(rb1, rb1, a, pipe, 1.0, 1, 1.0, 1, 1, 1, 1, 1, 1, 421484.0, 6542696.0, 1.0, 1, 1.0, 1.0, 1.0, 1.0, 1, 1, 1, 1, 1, POINT(421484 6542696))])'''
        assert test_string == reference_string

    @mock.patch('db_utils.QgsProject.instance', utils_for_tests.MidvattenTestPostgisNotCreated.mock_instance_settings_database)
    @mock.patch('db_utils.get_postgis_connections', utils_for_tests.MidvattenTestPostgisNotCreated.mock_postgis_connections)
    @mock.patch('import_data_to_db.utils.Askuser', mock.MagicMock())
    def test_import_obs_points_no_east_north(self):
        f = [[u'obsid', u'name', u'place', u'type', u'length', u'drillstop', u'diam', u'material', u'screen', u'capacity', u'drilldate', u'wmeas_yn', u'wlogg_yn', u'east', u'north', u'ne_accur', u'ne_source', u'h_toc', u'h_tocags', u'h_gs', u'h_accur', u'h_syst', u'h_source', u'source', u'com_onerow', u'com_html'],
             [u'rb1', u'rb1', u'a', u'pipe', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'', u'', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1']]

        self.importinstance.general_import(file_data=f,
                                           goal_table=u'obs_points')

        test_string = utils_for_tests.create_test_string(
            db_utils.sql_load_fr_db(u'''select obsid, name, place, type, length, drillstop, diam, material, screen, capacity, drilldate, wmeas_yn, wlogg_yn, east, north, ne_accur, ne_source, h_toc, h_tocags, h_gs, h_accur, h_syst, h_source, source, com_onerow, com_html, ST_AsText(geometry) from obs_points'''))

        reference_string = ur'''(True, [(rb1, rb1, a, pipe, 1.0, 1, 1.0, 1, 1, 1, 1, 1, 1, None, None, 1.0, 1, 1.0, 1.0, 1.0, 1.0, 1, 1, 1, 1, 1, None)])'''
        assert test_string == reference_string

    @mock.patch('db_utils.QgsProject.instance', utils_for_tests.MidvattenTestPostgisNotCreated.mock_instance_settings_database)
    @mock.patch('db_utils.get_postgis_connections', utils_for_tests.MidvattenTestPostgisNotCreated.mock_postgis_connections)
    @mock.patch('import_data_to_db.utils.Askuser', mock.MagicMock())
    def test_import_obs_points_geometry_as_wkt(self):
        f = [[u'obsid', u'name', u'place', u'type', u'length', u'drillstop', u'diam', u'material', u'screen', u'capacity', u'drilldate', u'wmeas_yn', u'wlogg_yn', u'east', u'north', u'ne_accur', u'ne_source', u'h_toc', u'h_tocags', u'h_gs', u'h_accur', u'h_syst', u'h_source', u'source', u'com_onerow', u'com_html', u'geometry'],
             [u'rb1', u'rb1', u'a', u'pipe', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'', u'', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'POINT(45 55)']]

        self.importinstance.general_import(file_data=f, goal_table=u'obs_points')

        test_string = utils_for_tests.create_test_string(
            db_utils.sql_load_fr_db(u'''select obsid, name, place, type, length, drillstop, diam, material, screen, capacity, drilldate, wmeas_yn, wlogg_yn, east, north, ne_accur, ne_source, h_toc, h_tocags, h_gs, h_accur, h_syst, h_source, source, com_onerow, com_html, ST_AsText(geometry) from obs_points'''))

        reference_string = ur'''(True, [(rb1, rb1, a, pipe, 1.0, 1, 1.0, 1, 1, 1, 1, 1, 1, 45.0, 55.0, 1.0, 1, 1.0, 1.0, 1.0, 1.0, 1, 1, 1, 1, 1, POINT(45 55))])'''
        assert test_string == reference_string


    @mock.patch('db_utils.QgsProject.instance', utils_for_tests.MidvattenTestPostgisNotCreated.mock_instance_settings_database)
    @mock.patch('db_utils.get_postgis_connections', utils_for_tests.MidvattenTestPostgisNotCreated.mock_postgis_connections)
    @mock.patch('import_data_to_db.utils.Askuser', mock.MagicMock())
    def test_import_obs_lines_geometry_as_wkt(self):
        f = [[u'obsid', u'geometry'],
             [u'line1', u'LINESTRING(1 2, 3 4, 5 6, 7 8)']]

        self.importinstance.general_import(file_data=f, goal_table=u'obs_lines')
        test_string = utils_for_tests.create_test_string(db_utils.sql_load_fr_db(u'''select obsid, ST_AsText(geometry) from obs_lines'''))

        reference_string = ur'''(True, [(line1, LINESTRING(1 2,3 4,5 6,7 8))])'''
        assert test_string == reference_string


@attr(status='on')
class TestWquallabImport(utils_for_tests.MidvattenTestPostgisDbSvImportInstance):
    @mock.patch('db_utils.QgsProject.instance', utils_for_tests.MidvattenTestPostgisNotCreated.mock_instance_settings_database)
    @mock.patch('db_utils.get_postgis_connections', utils_for_tests.MidvattenTestPostgisNotCreated.mock_postgis_connections)
    @mock.patch('import_data_to_db.utils.Askuser', mock.MagicMock())
    def test_wquallab_import_from_csvlayer(self):
        db_utils.sql_alter_db(u'''INSERT INTO zz_staff (staff) VALUES ('teststaff')''')

        db_utils.sql_alter_db(u"INSERT INTO obs_points (obsid) VALUES ('obsid1')")
        f = [[u'obsid', u'depth', u'report', u'project', u'staff', u'date_time', u'anameth', u'parameter', u'reading_num', u'reading_txt', u'unit', u'comment'],
             [u'obsid1', u'2', u'testreport', u'testproject', u'teststaff', u'2011-10-19 12:30:00', u'testmethod', u'1,2-Dikloretan', u'1.5', u'<1.5', u'µg/l', u'testcomment']]

        self.importinstance.general_import(goal_table=u'w_qual_lab', file_data=f)

        test_string = utils_for_tests.create_test_string(
            db_utils.sql_load_fr_db(u'''select * from w_qual_lab'''))

        reference_string = ur'''(True, [(obsid1, 2.0, testreport, testproject, teststaff, 2011-10-19 12:30:00, testmethod, 1,2-Dikloretan, 1.5, <1.5, µg/l, testcomment)])'''
        assert test_string == reference_string

    @mock.patch('db_utils.QgsProject.instance', utils_for_tests.MidvattenTestPostgisNotCreated.mock_instance_settings_database)
    @mock.patch('db_utils.get_postgis_connections', utils_for_tests.MidvattenTestPostgisNotCreated.mock_postgis_connections)
    @mock.patch('import_data_to_db.utils.Askuser', mock.MagicMock())
    def test_wquallab_import_from_csvlayer_depth_empty_string(self):
        db_utils.sql_alter_db(u'''INSERT INTO zz_staff (staff) VALUES ('teststaff')''')

        db_utils.sql_alter_db(u"INSERT INTO obs_points (obsid) VALUES ('obsid1')")
        f = [[u'obsid', u'depth', u'report', u'project', u'staff', u'date_time', u'anameth', u'parameter', u'reading_num', u'reading_txt', u'unit', u'comment'],
             [u'obsid1', u'', u'testreport', u'testproject', u'teststaff', u'2011-10-19 12:30:00', u'testmethod', u'1,2-Dikloretan', u'1.5', u'<1.5', u'µg/l', u'testcomment']]

        self.importinstance.general_import(goal_table=u'w_qual_lab', file_data=f)

        test_string = utils_for_tests.create_test_string(
            db_utils.sql_load_fr_db(u'''select * from w_qual_lab'''))

        reference_string = ur'''(True, [(obsid1, None, testreport, testproject, teststaff, 2011-10-19 12:30:00, testmethod, 1,2-Dikloretan, 1.5, <1.5, µg/l, testcomment)])'''
        assert test_string == reference_string

    @mock.patch('db_utils.QgsProject.instance', utils_for_tests.MidvattenTestPostgisNotCreated.mock_instance_settings_database)
    @mock.patch('db_utils.get_postgis_connections', utils_for_tests.MidvattenTestPostgisNotCreated.mock_postgis_connections)
    @mock.patch('import_data_to_db.utils.Askuser', mock.MagicMock())
    def test_wquallab_import_from_csvlayer_no_staff(self):
        db_utils.sql_alter_db(u'''INSERT INTO zz_staff (staff) VALUES ('teststaff')''')
        db_utils.sql_alter_db(u"INSERT INTO obs_points (obsid) VALUES ('obsid1')")

        f = [[u'obsid', u'depth', u'report', u'project', u'date_time', u'anameth', u'parameter', u'reading_num', u'reading_txt', u'unit', u'comment'],
             [u'obsid1', u'2', u'testreport', u'testproject', u'2011-10-19 12:30:00', u'testmethod', u'1,2-Dikloretan', u'1.5', u'<1.5', u'µg/l', u'testcomment']]

        self.importinstance.general_import(goal_table=u'w_qual_lab', file_data=f)

        test_string = utils_for_tests.create_test_string(
            db_utils.sql_load_fr_db(u'''select * from w_qual_lab'''))
        reference_string = ur'''(True, [(obsid1, 2.0, testreport, testproject, None, 2011-10-19 12:30:00, testmethod, 1,2-Dikloretan, 1.5, <1.5, µg/l, testcomment)])'''
        assert test_string == reference_string


@attr(status='on')
class TestWflowImport(utils_for_tests.MidvattenTestPostgisDbSvImportInstance):
    @mock.patch('db_utils.QgsProject.instance', utils_for_tests.MidvattenTestPostgisNotCreated.mock_instance_settings_database)
    @mock.patch('db_utils.get_postgis_connections', utils_for_tests.MidvattenTestPostgisNotCreated.mock_postgis_connections)
    @mock.patch('import_data_to_db.utils.Askuser', mock.MagicMock())
    def test_wflow_import_from_csvlayer(self):
        db_utils.sql_alter_db(u"""INSERT INTO obs_points (obsid) VALUES ('obsid1')""")
        f = [[u'obsid', u'instrumentid', u'flowtype', u'date_time', u'reading', u'unit', u'comment'],
             [u'obsid1', u'testid', u'Momflow', u'2011-10-19 12:30:00', u'2', u'l/s', u'testcomment']]

        self.importinstance.general_import(goal_table=u'w_flow', file_data=f)

        test_string = utils_for_tests.create_test_string(
            db_utils.sql_load_fr_db(u'''select * from w_flow'''))
        reference_string = ur'''(True, [(obsid1, testid, Momflow, 2011-10-19 12:30:00, 2.0, l/s, testcomment)])'''
        assert test_string == reference_string

    @mock.patch('db_utils.QgsProject.instance', utils_for_tests.MidvattenTestPostgisNotCreated.mock_instance_settings_database)
    @mock.patch('db_utils.get_postgis_connections', utils_for_tests.MidvattenTestPostgisNotCreated.mock_postgis_connections)
    @mock.patch('import_data_to_db.utils.Askuser', mock.MagicMock())
    def test_wflow_import_from_csvlayer_type_missing(self):
        db_utils.sql_alter_db(u"""INSERT INTO obs_points (obsid) VALUES ('obsid1')""")
        f = [[u'obsid', u'instrumentid', u'flowtype', u'date_time', u'reading', u'unit', u'comment'],
             [u'obsid1', u'testid', u'Testtype', u'2011-10-19 12:30:00', u'2', u'l/s', u'testcomment']]

        self.importinstance.general_import(goal_table=u'w_flow', file_data=f)

        test_string = utils_for_tests.create_test_string(
            db_utils.sql_load_fr_db(u'''select * from w_flow'''))
        reference_string = ur'''(True, [(obsid1, testid, Testtype, 2011-10-19 12:30:00, 2.0, l/s, testcomment)])'''
        assert test_string == reference_string

    @mock.patch('db_utils.QgsProject.instance', utils_for_tests.MidvattenTestPostgisNotCreated.mock_instance_settings_database)
    @mock.patch('db_utils.get_postgis_connections', utils_for_tests.MidvattenTestPostgisNotCreated.mock_postgis_connections)
    @mock.patch('import_data_to_db.utils.Askuser', mock.MagicMock())
    def test_wflow_new_param_into_zz_flowtype(self):
        db_utils.sql_alter_db(u"""INSERT INTO obs_points (obsid) VALUES ('obsid1')""")
        f = [[u'obsid', u'instrumentid', u'flowtype', u'date_time', u'reading', u'unit', u'comment'],
             [u'obsid1', u'testid', u'Momflow2', u'2011-10-19 12:30:00', u'2', u'l/s', u'testcomment']]

        self.importinstance.general_import(goal_table=u'w_flow', file_data=f)

        test_string = utils_for_tests.create_test_string(
            db_utils.sql_load_fr_db(u'''select * from w_flow'''))
        reference_string = ur'''(True, [(obsid1, testid, Momflow2, 2011-10-19 12:30:00, 2.0, l/s, testcomment)])'''
        assert test_string == reference_string
        test_string = utils_for_tests.create_test_string(
            db_utils.sql_load_fr_db(u'''select * from zz_flowtype'''))
        reference_string = ur'''(True, [(Accvol, Accumulated volume), (Momflow, Momentary flow rate), (Aveflow, Average flow since last reading), (Momflow2, None)])'''
        assert test_string == reference_string


@attr(status='on')
class TestWqualfieldImport(utils_for_tests.MidvattenTestPostgisDbSvImportInstance):
    @mock.patch('db_utils.QgsProject.instance', utils_for_tests.MidvattenTestPostgisNotCreated.mock_instance_settings_database)
    @mock.patch('db_utils.get_postgis_connections', utils_for_tests.MidvattenTestPostgisNotCreated.mock_postgis_connections)
    @mock.patch('import_data_to_db.utils.Askuser', mock.MagicMock())
    def test_w_qual_field_import_from_csvlayer(self):
        db_utils.sql_alter_db(u"""INSERT INTO obs_points (obsid) VALUES ('obsid1')""")
        f = [[u'obsid', u'staff', u'date_time', u'instrument', u'parameter', u'reading_num', u'reading_txt', u'unit', u'depth', u'comment'],
             [u'obsid1', u'teststaff', u'2011-10-19 12:30:00', u'testinstrument', u'DO', u'12', u'<12', u'%', u'22', u'testcomment']]

        self.importinstance.general_import(goal_table=u'w_qual_field', file_data=f)

        test_string = utils_for_tests.create_test_string(
            db_utils.sql_load_fr_db(u'''select * from w_qual_field'''))
        reference_string = ur'''(True, [(obsid1, teststaff, 2011-10-19 12:30:00, testinstrument, DO, 12.0, <12, %, 22.0, testcomment)])'''
        assert test_string == reference_string

    @mock.patch('db_utils.QgsProject.instance', utils_for_tests.MidvattenTestPostgisNotCreated.mock_instance_settings_database)
    @mock.patch('db_utils.get_postgis_connections', utils_for_tests.MidvattenTestPostgisNotCreated.mock_postgis_connections)
    @mock.patch('import_data_to_db.utils.Askuser', mock.MagicMock())
    def test_w_qual_field_import_from_csvlayer_no_depth(self):
        db_utils.sql_alter_db(u"""INSERT INTO obs_points (obsid) VALUES ('obsid1')""")
        f = [[u'obsid', u'staff', u'date_time', u'instrument', u'parameter', u'reading_num', u'reading_txt', u'unit', u'depth', u'comment'],
             [u'obsid1', u'teststaff', u'2011-10-19 12:30:00', u'testinstrument', u'DO', u'12', u'<12', u'%', u'', u'testcomment']]

        self.importinstance.general_import(goal_table=u'w_qual_field', file_data=f)

        test_string = utils_for_tests.create_test_string(
            db_utils.sql_load_fr_db(u'''select * from w_qual_field'''))
        reference_string = ur'''(True, [(obsid1, teststaff, 2011-10-19 12:30:00, testinstrument, DO, 12.0, <12, %, None, testcomment)])'''
        assert test_string == reference_string

    @mock.patch('db_utils.QgsProject.instance', utils_for_tests.MidvattenTestPostgisNotCreated.mock_instance_settings_database)
    @mock.patch('db_utils.get_postgis_connections', utils_for_tests.MidvattenTestPostgisNotCreated.mock_postgis_connections)
    @mock.patch('import_data_to_db.utils.Askuser', mock.MagicMock())
    @mock.patch('midvatten_utils.MessagebarAndLog')
    def test_w_qual_field_no_parameter(self, mock_messagebar):
        db_utils.sql_alter_db(u"""INSERT INTO obs_points (obsid) VALUES ('obsid1')""")
        f = [[u'obsid', u'staff', u'date_time', u'instrument',
              u'reading_num', u'reading_txt', u'unit', u'depth', u'comment'],
             [u'obsid1', u'teststaff', u'2011-10-19 12:30:00', u'testinstrument',
              u'12', u'<12', u'%', u'22', u'testcomment']]

        with nose.tools.assert_raises(MidvDataImporterError) as err:
            self.importinstance.general_import(goal_table = u'w_qual_field', file_data = f)
        ex = err.exception
        assert ex.message == u'Required columns parameter are missing for table w_qual_field'

        test_string = utils_for_tests.create_test_string(
            db_utils.sql_load_fr_db(u'''select * from w_qual_field'''))
        reference_string = ur'''(True, [])'''
        assert test_string == reference_string

    @mock.patch('db_utils.QgsProject.instance', utils_for_tests.MidvattenTestPostgisNotCreated.mock_instance_settings_database)
    @mock.patch('db_utils.get_postgis_connections', utils_for_tests.MidvattenTestPostgisNotCreated.mock_postgis_connections)
    @mock.patch('import_data_to_db.utils.Askuser', mock.MagicMock())
    @mock.patch('midvatten_utils.MessagebarAndLog')
    def test_w_qual_field_parameter_empty_string(self, mock_messagebar):
        db_utils.sql_alter_db(u"""INSERT INTO obs_points (obsid) VALUES ('obsid1')""")
        f = [[u'obsid', u'staff', u'date_time', u'instrument', u'parameter', u'reading_num', u'reading_txt', u'unit', u'depth', u'comment'],
             [u'obsid1', u'teststaff', u'2011-10-19 12:30:00', u'testinstrument', u'DO', u'12', u'<12', u'%', u'22', u'testcomment'],
             [u'obsid2', u'teststaff', u'2011-10-19 12:30:00', u'testinstrument', u'', u'12', u'<12', u'%', u'22', u'testcomment']]

        self.importinstance.general_import(goal_table=u'w_qual_field', file_data=f)

        test_calls_list = [call.info(log_msg=u'In total 1 rows were imported to foreign key table zz_staff while importing to w_qual_field.'),
                         call.info(log_msg=u'In total "0" rows were deleted due to foreign keys restrictions and "2" rows remain.'),
                         call.info(bar_msg=u'1 rows imported and 1 excluded for table w_qual_field. See log message panel for details')]
        for test_call in test_calls_list:
            assert test_call in mock_messagebar.mock_calls

        test_string = utils_for_tests.create_test_string(
            db_utils.sql_load_fr_db(u'''select * from w_qual_field'''))
        reference_string = ur'''(True, [(obsid1, teststaff, 2011-10-19 12:30:00, testinstrument, DO, 12.0, <12, %, 22.0, testcomment)])'''
        assert test_string == reference_string

    @mock.patch('db_utils.QgsProject.instance', utils_for_tests.MidvattenTestPostgisNotCreated.mock_instance_settings_database)
    @mock.patch('db_utils.get_postgis_connections', utils_for_tests.MidvattenTestPostgisNotCreated.mock_postgis_connections)
    @mock.patch('import_data_to_db.utils.Askuser', mock.MagicMock())
    @mock.patch('midvatten_utils.MessagebarAndLog')
    def test_w_qual_field_staff_null(self, mock_messagebar):
        self.importinstance.charsetchoosen = [u'utf-8']

        db_utils.sql_alter_db(u"""INSERT INTO obs_points (obsid) VALUES ('obsid1')""")
        db_utils.sql_alter_db(u"""INSERT INTO obs_points (obsid) VALUES ('obsid2')""")
        db_utils.sql_alter_db(u"""INSERT INTO obs_points (obsid) VALUES ('obsid3')""")
        db_utils.sql_alter_db(u"""INSERT INTO obs_points (obsid) VALUES ('obsid4')""")
        f = [[u'obsid', u'staff', u'date_time', u'instrument', u'parameter', u'reading_num', u'reading_txt', u'unit', u'depth', u'comment'],
             [u'obsid1', u'', u'2011-10-19 12:30:00', u'testinstrument', u'DO', u'12', u'<12', u'%', u'22', u'testcomment'],
             [u'obsid2', u'', u'2011-10-19 12:30:00', u'testinstrument', u'DO', u'12', u'<12', u'%', u'22', u'testcomment']]

        self.importinstance.general_import(goal_table=u'w_qual_field', file_data=f)

        test_calls_list = [call.info(log_msg=u'In total "0" rows were deleted due to foreign keys restrictions and "2" rows remain.'),
                            call.info(bar_msg=u'2 rows imported and 0 excluded for table w_qual_field. See log message panel for details')]
        for test_call in test_calls_list:
            assert test_call in mock_messagebar.mock_calls

        test_string = utils_for_tests.create_test_string(
            db_utils.sql_load_fr_db(u'''select * from w_qual_field'''))
        reference_string = ur'''(True, [(obsid1, None, 2011-10-19 12:30:00, testinstrument, DO, 12.0, <12, %, 22.0, testcomment), (obsid2, None, 2011-10-19 12:30:00, testinstrument, DO, 12.0, <12, %, 22.0, testcomment)])'''
        assert test_string == reference_string

        test_string = utils_for_tests.create_test_string(
            db_utils.sql_load_fr_db(u'''select * from zz_staff'''))
        reference_string = ur'''(True, [])'''
        print(str(test_string))
        assert test_string == reference_string

        #Import another null and check that there is not two nulls now.
        f = [[u'obsid', u'staff', u'date_time', u'instrument', u'parameter', u'reading_num', u'reading_txt', u'unit', u'depth', u'comment'],
             [u'obsid3', u'', u'2011-10-19 12:30:00', u'testinstrument', u'DO', u'12', u'<12', u'%', u'22', u'testcomment'],
             [u'obsid4', u'', u'2011-10-19 12:30:00', u'testinstrument', u'DO', u'12', u'<12', u'%', u'22', u'testcomment']]
        self.importinstance.general_import(goal_table=u'w_qual_field', file_data=f)
        test_string = utils_for_tests.create_test_string(
            db_utils.sql_load_fr_db(u'''select * from zz_staff'''))
        reference_string = ur'''(True, [])'''
        assert test_string == reference_string


@attr(status='on')
class TestWlevelsImport(utils_for_tests.MidvattenTestPostgisDbSvImportInstance):
    @mock.patch('db_utils.QgsProject.instance', utils_for_tests.MidvattenTestPostgisNotCreated.mock_instance_settings_database)
    @mock.patch('db_utils.get_postgis_connections', utils_for_tests.MidvattenTestPostgisNotCreated.mock_postgis_connections)
    @mock.patch('import_data_to_db.utils.Askuser', mock.MagicMock())
    def test_w_level_import_from_csvlayer(self):
        db_utils.sql_alter_db(u"""INSERT INTO obs_points (obsid) VALUES ('obsid1')""")
        f = [[u'obsid', u'date_time', u'meas', u'comment'],
             [u'obsid1', u'2011-10-19 12:30:00', u'2', u'testcomment']]

        self.importinstance.general_import(goal_table=u'w_levels', file_data=f)

        test_string = utils_for_tests.create_test_string(
            db_utils.sql_load_fr_db(u'''select * from w_levels'''))
        reference_string = ur'''(True, [(obsid1, 2011-10-19 12:30:00, 2.0, None, None, testcomment)])'''
        assert test_string == reference_string

    @mock.patch('db_utils.QgsProject.instance', utils_for_tests.MidvattenTestPostgisNotCreated.mock_instance_settings_database)
    @mock.patch('db_utils.get_postgis_connections', utils_for_tests.MidvattenTestPostgisNotCreated.mock_postgis_connections)
    @mock.patch('import_data_to_db.utils.Askuser', mock.MagicMock())
    def _test_w_level_import_from_csvlayer_missing_columns(self):
        db_utils.sql_alter_db(u"""INSERT INTO obs_points (obsid) VALUES ('obsid1')""")
        #f = [[u'obsid', u'date_time', u'meas', u'comment'],
        #     [u'obsid1', u'2011-10-19 12:30:00', u'2', u'testcomment']]
        f = [[u'obsid', u'date_time', u'meas'],
             [u'obsid1', u'2011-10-19 12:30:00', u'2']]

        self.importinstance.general_import(goal_table=u'w_levels', file_data=f)

        test_string = utils_for_tests.create_test_string(db_utils.sql_load_fr_db(u'''SELECT * FROM w_levels'''))
        reference_string = ur'''(True, [])'''
        assert test_string == reference_string


@attr(status='on')
class TestSeismicImport(utils_for_tests.MidvattenTestPostgisDbSvImportInstance):
    @mock.patch('db_utils.QgsProject.instance', utils_for_tests.MidvattenTestPostgisNotCreated.mock_instance_settings_database)
    @mock.patch('db_utils.get_postgis_connections', utils_for_tests.MidvattenTestPostgisNotCreated.mock_postgis_connections)
    @mock.patch('import_data_to_db.utils.Askuser', mock.MagicMock())
    def test_seismic_import_from_csvlayer(self):
        db_utils.sql_alter_db(u"""INSERT INTO obs_lines (obsid) VALUES ('obsid1')""")
        f = [[u'obsid', u'length', u'ground', u'bedrock', u'gw_table', u'comment'],
             [u'obsid1', u'500', u'2', u'4', u'3', u'acomment']]

        self.importinstance.general_import(goal_table=u'seismic_data', file_data=f)

        test_string = utils_for_tests.create_test_string(
            db_utils.sql_load_fr_db(u'''select * from seismic_data'''))
        reference_string = ur'''(True, [(obsid1, 500.0, 2.0, 4.0, 3.0, acomment)])'''
        assert test_string == reference_string


@attr(status='on')
class TestCommentsImport(utils_for_tests.MidvattenTestPostgisDbSvImportInstance):
    @mock.patch('db_utils.QgsProject.instance', utils_for_tests.MidvattenTestPostgisNotCreated.mock_instance_settings_database)
    @mock.patch('db_utils.get_postgis_connections', utils_for_tests.MidvattenTestPostgisNotCreated.mock_postgis_connections)
    @mock.patch('import_data_to_db.utils.Askuser', mock.MagicMock())
    def test_comments_import_from_csvlayer(self):
        db_utils.sql_alter_db(u"""INSERT INTO obs_points (obsid) VALUES ('obsid1')""")
        f = [[u'obsid', u'date_time', u'comment', u'staff'],
             [u'obsid1', u'2011-10-19 12:30:00', u'testcomment', u'teststaff']]

        self.importinstance.general_import(goal_table=u'comments', file_data=f)

        test_string = utils_for_tests.create_test_string(
            db_utils.sql_load_fr_db(u'''select * from comments'''))
        reference_string = ur'''(True, [(obsid1, 2011-10-19 12:30:00, testcomment, teststaff)])'''
        assert test_string == reference_string


@attr(status='on')
class TestStratImport(utils_for_tests.MidvattenTestPostgisDbSvImportInstance):
    @mock.patch('db_utils.QgsProject.instance', utils_for_tests.MidvattenTestPostgisNotCreated.mock_instance_settings_database)
    @mock.patch('db_utils.get_postgis_connections', utils_for_tests.MidvattenTestPostgisNotCreated.mock_postgis_connections)
    @mock.patch('import_data_to_db.utils.Askuser', mock.MagicMock())
    def test_strat_import_from_csvlayer(self):
        db_utils.sql_alter_db(u"""INSERT INTO obs_points (obsid) VALUES ('obsid1')""")
        f = [[u'obsid', u'stratid', u'depthtop', u'depthbot', u'geology', u'geoshort', u'capacity', u'development', u'comment'],
             [u'obsid1', u'1', u'0', u'1', u'grusig sand', u'sand', u'5', u'(j)', u'acomment'],
             [u'obsid1', u'2', u'1', u'4', u'siltigt sandigt grus', u'grus', u'4+', u'(j)', u'acomment2']]

        self.importinstance.general_import(goal_table=u'stratigraphy', file_data=f) #goal_table=u'stratigraphy')

        test_string = utils_for_tests.create_test_string(
            db_utils.sql_load_fr_db(u'''select * from stratigraphy'''))
        reference_string = u'''(True, [(obsid1, 1, 0.0, 1.0, grusig sand, sand, 5, (j), acomment), (obsid1, 2, 1.0, 4.0, siltigt sandigt grus, grus, 4+, (j), acomment2)])'''
        assert test_string == reference_string

    @mock.patch('db_utils.QgsProject.instance', utils_for_tests.MidvattenTestPostgisNotCreated.mock_instance_settings_database)
    @mock.patch('db_utils.get_postgis_connections', utils_for_tests.MidvattenTestPostgisNotCreated.mock_postgis_connections)
    @mock.patch('import_data_to_db.utils.Askuser', mock.MagicMock())
    def test_strat_import_from_csvlayer_eleven_layers(self):
        db_utils.sql_alter_db(u"""INSERT INTO obs_points (obsid) VALUES ('obsid1')""")
        f = [[u'obsid', u'stratid', u'depthtop', u'depthbot', u'geology', u'geoshort', u'capacity', u'development', u'comment'],
             [u'obsid1', u'1', u'0', u'1', u's', u's', u'1', u'(j)', u'acomment'],
             [u'obsid1', u'2', u'1', u'2', u's', u's', u'1', u'(j)', u'acomment'],
             [u'obsid1', u'3', u'2', u'3', u's', u's', u'1', u'(j)', u'acomment'],
             [u'obsid1', u'4', u'3', u'4', u's', u's', u'1', u'(j)', u'acomment'],
             [u'obsid1', u'5', u'4', u'5', u's', u's', u'1', u'(j)', u'acomment'],
             [u'obsid1', u'6', u'5', u'6', u's', u's', u'1', u'(j)', u'acomment'],
             [u'obsid1', u'7', u'6', u'7', u's', u's', u'1', u'(j)', u'acomment'],
             [u'obsid1', u'8', u'7', u'8', u's', u's', u'1', u'(j)', u'acomment'],
             [u'obsid1', u'9', u'8', u'9', u's', u's', u'1', u'(j)', u'acomment'],
             [u'obsid1', u'10', u'9', u'12.1', u's', u's', u'1', u'(j)', u'acomment'],
             [u'obsid1', u'11', u'12.1', u'13', u's', u's', u'1', u'(j)', u'acomment']]

        self.importinstance.general_import(goal_table=u'stratigraphy', file_data=f) #goal_table=u'stratigraphy')

        test_string = utils_for_tests.create_test_string(
            db_utils.sql_load_fr_db(u'''select * from stratigraphy'''))
        reference_string = u'''(True, [(obsid1, 1, 0.0, 1.0, s, s, 1, (j), acomment), (obsid1, 2, 1.0, 2.0, s, s, 1, (j), acomment), (obsid1, 3, 2.0, 3.0, s, s, 1, (j), acomment), (obsid1, 4, 3.0, 4.0, s, s, 1, (j), acomment), (obsid1, 5, 4.0, 5.0, s, s, 1, (j), acomment), (obsid1, 6, 5.0, 6.0, s, s, 1, (j), acomment), (obsid1, 7, 6.0, 7.0, s, s, 1, (j), acomment), (obsid1, 8, 7.0, 8.0, s, s, 1, (j), acomment), (obsid1, 9, 8.0, 9.0, s, s, 1, (j), acomment), (obsid1, 10, 9.0, 12.1, s, s, 1, (j), acomment), (obsid1, 11, 12.1, 13.0, s, s, 1, (j), acomment)])'''
        assert test_string == reference_string

    @mock.patch('db_utils.QgsProject.instance', utils_for_tests.MidvattenTestPostgisNotCreated.mock_instance_settings_database)
    @mock.patch('db_utils.get_postgis_connections', utils_for_tests.MidvattenTestPostgisNotCreated.mock_postgis_connections)
    @mock.patch('import_data_to_db.utils.Askuser', mock.MagicMock())
    def test_strat_import_one_obs_fail_stratid_gaps(self):
        db_utils.sql_alter_db(u"""INSERT INTO obs_points (obsid) VALUES ('obsid1')""")
        f = [[u'obsid', u'stratid', u'depthtop', u'depthbot', u'geology', u'geoshort', u'capacity', u'development', u'comment'],
             [u'obsid1', u'1', u'0', u'1', u'grusig sand', u'sand', u'5', u'(j)', u'acomment'],
             [u'obsid1', u'2', u'1', u'4', u'siltigt sandigt grus', u'grus', u'4+', u'(j)', u'acomment2'],
             [u'obsid2', u'1', u'0', u'1', u'grusig sand', u'sand', u'5', u'(j)', u'acomment'],
             [u'obsid2', u'3', u'1', u'4', u'siltigt sandigt grus', u'grus', u'4+', u'(j)', u'acomment2']]

        self.importinstance.general_import(goal_table=u'stratigraphy', file_data=f) #goal_table=u'stratigraphy')

        test_string = utils_for_tests.create_test_string(
            db_utils.sql_load_fr_db(u'''select * from stratigraphy'''))
        reference_string = u'''(True, [(obsid1, 1, 0.0, 1.0, grusig sand, sand, 5, (j), acomment), (obsid1, 2, 1.0, 4.0, siltigt sandigt grus, grus, 4+, (j), acomment2)])'''
        assert test_string == reference_string

    @mock.patch('db_utils.QgsProject.instance', utils_for_tests.MidvattenTestPostgisNotCreated.mock_instance_settings_database)
    @mock.patch('db_utils.get_postgis_connections', utils_for_tests.MidvattenTestPostgisNotCreated.mock_postgis_connections)
    @mock.patch('import_data_to_db.utils.Askuser', mock.MagicMock())
    def test_strat_import_one_obs_fail_depthbot_gaps(self):
        db_utils.sql_alter_db(u"""INSERT INTO obs_points (obsid) VALUES ('obsid1')""")
        f = [[u'obsid', u'stratid', u'depthtop', u'depthbot', u'geology', u'geoshort', u'capacity', u'development', u'comment'],
             [u'obsid1', u'1', u'0', u'1', u'grusig sand', u'sand', u'5', u'(j)', u'acomment'],
             [u'obsid1', u'2', u'1', u'4', u'siltigt sandigt grus', u'grus', u'4+', u'(j)', u'acomment2'],
             [u'obsid2', u'1', u'0', u'1', u'grusig sand', u'sand', u'5', u'(j)', u'acomment'],
             [u'obsid2', u'2', u'3', u'4', u'siltigt sandigt grus', u'grus', u'4+', u'(j)', u'acomment2']]

        self.importinstance.general_import(goal_table=u'stratigraphy', file_data=f) #goal_table=u'stratigraphy')

        test_string = utils_for_tests.create_test_string(
            db_utils.sql_load_fr_db(u'''select * from stratigraphy'''))
        reference_string = u'''(True, [(obsid1, 1, 0.0, 1.0, grusig sand, sand, 5, (j), acomment), (obsid1, 2, 1.0, 4.0, siltigt sandigt grus, grus, 4+, (j), acomment2)])'''
        assert test_string == reference_string


@attr(status='on')
class TestMeteoImport(utils_for_tests.MidvattenTestPostgisDbSvImportInstance):
    @mock.patch('db_utils.QgsProject.instance', utils_for_tests.MidvattenTestPostgisNotCreated.mock_instance_settings_database)
    @mock.patch('db_utils.get_postgis_connections', utils_for_tests.MidvattenTestPostgisNotCreated.mock_postgis_connections)
    @mock.patch('import_data_to_db.utils.Askuser', mock.MagicMock())
    def test_meteo_import_from_csvlayer(self):
        db_utils.sql_alter_db(u"""INSERT INTO obs_points (obsid) VALUES ('obsid1')""")
        f = [[u'obsid', u'instrumentid', u'parameter', u'date_time', u'reading_num', u'reading_txt', u'unit', u'comment'],
             [u'obsid1', u'ints1', u'pressure', u'2016-01-01 00:00:00', u'1100', u'1100', u'aunit', u'acomment']]

        self.importinstance.general_import(goal_table=u'meteo', file_data=f)

        test_string = utils_for_tests.create_test_string(
            db_utils.sql_load_fr_db(u'''select * from meteo'''))
        reference_string = u'''(True, [(obsid1, ints1, pressure, 2016-01-01 00:00:00, 1100.0, 1100, aunit, acomment)])'''
        assert test_string == reference_string


@attr(status='on')
class TestVlfImport(utils_for_tests.MidvattenTestPostgisDbSvImportInstance):
    @mock.patch('db_utils.QgsProject.instance', utils_for_tests.MidvattenTestPostgisNotCreated.mock_instance_settings_database)
    @mock.patch('db_utils.get_postgis_connections', utils_for_tests.MidvattenTestPostgisNotCreated.mock_postgis_connections)
    @mock.patch('import_data_to_db.utils.Askuser', mock.MagicMock())
    def test_vlf_import_from_csvlayer(self):
        db_utils.sql_alter_db(u"""INSERT INTO obs_lines (obsid) VALUES ('obsid1')""")
        f = [[u'obsid', u'length', u'real_comp', u'imag_comp', u'comment'],
             [u'obsid1', u'500', u'2', u'10', u'acomment']]

        self.importinstance.general_import(goal_table=u'vlf_data', file_data=f)

        test_string = utils_for_tests.create_test_string(
            db_utils.sql_load_fr_db(u'''select * from vlf_data'''))
        reference_string = u'''(True, [(obsid1, 500.0, 2.0, 10.0, acomment)])'''
        assert test_string == reference_string

    @mock.patch('midvatten_utils.MessagebarAndLog')
    @mock.patch('db_utils.QgsProject.instance', utils_for_tests.MidvattenTestPostgisNotCreated.mock_instance_settings_database)
    @mock.patch('db_utils.get_postgis_connections', utils_for_tests.MidvattenTestPostgisNotCreated.mock_postgis_connections)
    @mock.patch('import_data_to_db.utils.Askuser', mock.MagicMock())
    def test_vlf_import_from_csvlayer_no_obs_line(self, mock_messagebar):
        f = [[u'obsid', u'length', u'real_comp', u'imag_comp', u'comment'],
             [u'obsid1', u'500', u'2', u'10', u'acomment']]

        try:
            self.importinstance.general_import(goal_table=u'vlf_data', file_data=f)
        except Exception as e:
            assert utils_for_tests.foreign_key_test_from_exception(e, u'postgis')

        test_string = utils_for_tests.create_test_string(
            db_utils.sql_load_fr_db(u'''select * from vlf_data'''))
        reference_string = u'''(True, [])'''
        assert test_string == reference_string


@attr(status='on')
class TestObsLinesImport(utils_for_tests.MidvattenTestPostgisDbSvImportInstance):
    @mock.patch('db_utils.QgsProject.instance', utils_for_tests.MidvattenTestPostgisNotCreated.mock_instance_settings_database)
    @mock.patch('db_utils.get_postgis_connections', utils_for_tests.MidvattenTestPostgisNotCreated.mock_postgis_connections)
    @mock.patch('import_data_to_db.utils.Askuser', mock.MagicMock())
    @mock.patch('midvatten_utils.MessagebarAndLog')
    def test_obs_lines_import_from_csvlayer(self, mock_messagebar):
        f = [[u'obsid', u'name', u'place', u'type', u'source'],
             [u'obsid1', u'aname', u'aplace', u'atype', u'asource']]

        self.importinstance.general_import(goal_table=u'obs_lines', file_data=f)

        test_string = utils_for_tests.create_test_string(
            db_utils.sql_load_fr_db(u'''select * from obs_lines'''))
        reference_string = u'''(True, [(obsid1, aname, aplace, atype, asource, None)])'''
        assert test_string == reference_string


@attr(status='on')
class TestGetForeignKeys(utils_for_tests.MidvattenTestPostgisDbSvImportInstance):
    @mock.patch('db_utils.QgsProject.instance', utils_for_tests.MidvattenTestPostgisNotCreated.mock_instance_settings_database)
    @mock.patch('db_utils.get_postgis_connections', utils_for_tests.MidvattenTestPostgisNotCreated.mock_postgis_connections)
    @mock.patch('import_data_to_db.utils.Askuser', mock.MagicMock())
    def test_get_foreign_columns(self):
        test = db_utils.get_foreign_keys(u'w_levels')
        assert len(test) > 0
        assert isinstance(test, (dict, OrderedDict))
        for k, v in test.iteritems():
            assert isinstance(v, (list, tuple))


@attr(status='on')
class TestDeleteExistingDateTimesFromTemptable(utils_for_tests.MidvattenTestPostgisDbSvImportInstance):
    @mock.patch('db_utils.QgsProject.instance', utils_for_tests.MidvattenTestPostgisNotCreated.mock_instance_settings_database)
    @mock.patch('db_utils.get_postgis_connections', utils_for_tests.MidvattenTestPostgisNotCreated.mock_postgis_connections)
    @mock.patch('import_data_to_db.utils.Askuser', mock.MagicMock())
    def test_delete_existing_date_times_from_temptable_00_already_exists(self):
        db_utils.sql_alter_db(u"""INSERT INTO obs_points (obsid) VALUES ('obsid1')""")
        db_utils.sql_alter_db(u"""INSERT INTO w_levels (obsid, date_time, level_masl) VALUES ('obsid1', '2016-01-01 00:00:00', '123.0')""")

        f = [[u'obsid', u'date_time', u'level_masl'],
             [u'obsid1', u'2016-01-01 00:00', u'345']]

        self.importinstance.general_import(goal_table=u'w_levels', file_data=f)

        test_string = utils_for_tests.create_test_string(
            db_utils.sql_load_fr_db(u'''select * from w_levels'''))
        reference_string = ur'''(True, [(obsid1, 2016-01-01 00:00:00, None, None, 123.0, None)])'''
        assert test_string == reference_string

    @mock.patch('db_utils.QgsProject.instance', utils_for_tests.MidvattenTestPostgisNotCreated.mock_instance_settings_database)
    @mock.patch('db_utils.get_postgis_connections', utils_for_tests.MidvattenTestPostgisNotCreated.mock_postgis_connections)
    @mock.patch('import_data_to_db.utils.Askuser', mock.MagicMock())
    def test_delete_existing_date_times_from_temptable_00_already_exists(self):
        db_utils.sql_alter_db(u"""INSERT INTO obs_points (obsid) VALUES ('obsid1')""")
        db_utils.sql_alter_db(u"""INSERT INTO w_levels (obsid, date_time, level_masl) VALUES ('obsid1', '2016-01-01 00:00:00', '123.0')""")

        f = [[u'obsid', u'date_time', u'level_masl'],
             [u'obsid1', u'2016-01-01 00:00', u'345']]

        self.importinstance.general_import(goal_table=u'w_levels', file_data=f)

        test_string = utils_for_tests.create_test_string(
            db_utils.sql_load_fr_db(u'''select * from w_levels'''))
        reference_string = ur'''(True, [(obsid1, 2016-01-01 00:00:00, None, None, 123.0, None)])'''
        assert test_string == reference_string

    @mock.patch('db_utils.QgsProject.instance', utils_for_tests.MidvattenTestPostgisNotCreated.mock_instance_settings_database)
    @mock.patch('db_utils.get_postgis_connections', utils_for_tests.MidvattenTestPostgisNotCreated.mock_postgis_connections)
    @mock.patch('import_data_to_db.utils.Askuser', mock.MagicMock())
    def test_delete_existing_date_times_from_temptable_minute_already_exists(self):
        self.importinstance.charsetchoosen = [u'utf-8']

        db_utils.sql_alter_db(u"""INSERT INTO obs_points (obsid) VALUES ('obsid1')""")
        db_utils.sql_alter_db(u"""INSERT INTO w_levels (obsid, date_time, level_masl) VALUES ('obsid1', '2016-01-01 00:00', '123.0')""")

        f = [[u'obsid', u'date_time', u'level_masl'],
             [u'obsid1', u'2016-01-01 00:00:00', u'345'],
             [u'obsid1', u'2016-01-01 00:00:01', u'456'],
             [u'obsid1', u'2016-01-01 00:02:00', u'789']]

        self.importinstance.general_import(goal_table=u'w_levels', file_data=f)

        test_string = utils_for_tests.create_test_string(
            db_utils.sql_load_fr_db(u'''select * from w_levels'''))
        reference_string = ur'''(True, [(obsid1, 2016-01-01 00:00, None, None, 123.0, None), (obsid1, 2016-01-01 00:02:00, None, None, 789.0, None)])'''
        assert test_string == reference_string

