# -*- coding: utf-8 -*-
"""
/***************************************************************************
 This part of the Midvatten plugin tests the db_utils for postgis.

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

import db_utils
import mock
from nose.plugins.attrib import attr

import utils_for_tests


@attr(status='on')
class TestDbTablesColumnsInfo(utils_for_tests.MidvattenTestPostgisDbSv):
    @mock.patch('db_utils.get_postgis_connections', utils_for_tests.MidvattenTestPostgisNotCreated.mock_postgis_connections)
    @mock.patch('midvatten_utils.QgsProject.instance', utils_for_tests.MidvattenTestPostgisNotCreated.mock_instance_settings_database)
    def test_tables_columns_info_all_tables(self):
        """  """
        #Assert that obsid is primary key and not null in obs_points
        #{u'tablename': (ordernumber, name, type, notnull, defaultvalue, primarykey)}
        tables_columns_info = db_utils.db_tables_columns_info()
        col_obsid = [col for col in tables_columns_info[u'obs_points'] if col[1] == u'obsid'][0]
        assert len(tables_columns_info) > 1
        assert int(col_obsid[0]) == 1
        assert col_obsid[1] == u'obsid'
        assert col_obsid[2].lower() == u'text'
        assert int(col_obsid[3]) == 1
        assert col_obsid[4] is None
        assert int(col_obsid[5]) == 1

    @mock.patch('db_utils.get_postgis_connections', utils_for_tests.MidvattenTestPostgisNotCreated.mock_postgis_connections)
    @mock.patch('midvatten_utils.QgsProject.instance', utils_for_tests.MidvattenTestPostgisNotCreated.mock_instance_settings_database)
    def test_tables_columns_info_only_obs_points(self):
        """  """
        # Assert that obsid is primary key and not null in obs_points
        # {u'tablename': (ordernumber, name, type, notnull, defaultvalue, primarykey)}
        tables_columns_info = db_utils.db_tables_columns_info(u'obs_points')
        col_obsid = [col for col in tables_columns_info[u'obs_points'] if col[1] == u'obsid'][0]
        assert len(tables_columns_info) == 1
        assert int(col_obsid[0]) == 1
        assert col_obsid[1] == u'obsid'
        assert col_obsid[2].lower() == u'text'
        assert int(col_obsid[3]) == 1
        assert col_obsid[4] is None
        assert int(col_obsid[5]) == 1


@attr(status='on')
class TestTablesColumns(utils_for_tests.MidvattenTestPostgisDbSv):
    @mock.patch('db_utils.get_postgis_connections', utils_for_tests.MidvattenTestPostgisNotCreated.mock_postgis_connections)
    @mock.patch('midvatten_utils.QgsProject.instance', utils_for_tests.MidvattenTestPostgisNotCreated.mock_instance_settings_database)
    def test_tables_columns_no_dbconnection_supplied(self):
        """  """
        tables_columns = db_utils.tables_columns()
        for tablename in [u'obs_points', u'w_levels', u'w_qual_lab', u'w_lvls_last_geom']:
            assert tablename in tables_columns
            assert u'obsid' in tables_columns[tablename]

        for tablename in [u'geometry_columns', u'spatial_ref_sys']:
            assert tablename not in tables_columns

    @mock.patch('db_utils.get_postgis_connections', utils_for_tests.MidvattenTestPostgisNotCreated.mock_postgis_connections)
    @mock.patch('midvatten_utils.QgsProject.instance', utils_for_tests.MidvattenTestPostgisNotCreated.mock_instance_settings_database)
    def test_tables_columns_dbconnection_supplied(self):
        """  """
        dbconnection = db_utils.DbConnectionManager()
        tables_columns = db_utils.tables_columns(dbconnection=dbconnection)
        for tablename in [u'obs_points', u'w_levels', u'w_qual_lab', u'w_lvls_last_geom']:
            assert tablename in tables_columns
            assert u'obsid' in tables_columns[tablename]

        for tablename in [u'geometry_columns', u'spatial_ref_sys']:
            assert tablename not in tables_columns


@attr(status='on')
class TestGetForeignKeys(utils_for_tests.MidvattenTestPostgisDbSv):
    @mock.patch('db_utils.get_postgis_connections', utils_for_tests.MidvattenTestPostgisNotCreated.mock_postgis_connections)
    @mock.patch('midvatten_utils.QgsProject.instance', utils_for_tests.MidvattenTestPostgisNotCreated.mock_instance_settings_database)
    def test_get_foreign_keys(self):
        """  """
        foreign_keys = db_utils.get_foreign_keys(u'w_levels')
        test_string = utils_for_tests.create_test_string(foreign_keys)
        reference = u'{obs_points: [(obsid, obsid)]}'
        assert test_string == reference

    @mock.patch('db_utils.get_postgis_connections', utils_for_tests.MidvattenTestPostgisNotCreated.mock_postgis_connections)
    @mock.patch('midvatten_utils.QgsProject.instance', utils_for_tests.MidvattenTestPostgisNotCreated.mock_instance_settings_database)
    def test_get_foreign_keys_no_keys(self):
        """  """
        foreign_keys = db_utils.get_foreign_keys(u'obs_points')
        test_string = utils_for_tests.create_test_string(foreign_keys)
        reference = u'{}'
        assert test_string == reference


@attr(status='on')
class TestVerifyTableExist(utils_for_tests.MidvattenTestPostgisDbSv):
    @mock.patch('db_utils.get_postgis_connections', utils_for_tests.MidvattenTestPostgisNotCreated.mock_postgis_connections)
    @mock.patch('midvatten_utils.QgsProject.instance', utils_for_tests.MidvattenTestPostgisNotCreated.mock_instance_settings_database)
    def test_verify_table_exists(self):
        exists = db_utils.verify_table_exists(u'obs_points')
        assert exists


@attr(status='on')
class TestNonplotTables():
    def test_as_tuple(self):
        tables = db_utils.nonplot_tables(as_tuple=True)

        assert tables == ('about_db',
                        'comments',
                        'zz_flowtype',
                        'zz_meteoparam',
                        'zz_strat',
                        'zz_hydro')

    def test_as_string(self):
        tables = db_utils.nonplot_tables(as_tuple=False)

        assert tables == r"""('about_db', 'comments', 'zz_flowtype', 'zz_meteoparam', 'zz_strat', 'zz_hydro')"""

    def test_as_string_default(self):
        tables = db_utils.nonplot_tables()

        assert tables == r"""('about_db', 'comments', 'zz_flowtype', 'zz_meteoparam', 'zz_strat', 'zz_hydro')"""