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
#

import utils_for_tests
import midvatten_utils as utils
from definitions import midvatten_defs as defs
from date_utils import datestring_to_date
import utils_for_tests as test_utils
from tools.midvatten_utils import get_foreign_keys
from utils_for_tests import init_test
from tools.tests.mocks_for_tests import DummyInterface
from nose.tools import raises
from mock import mock_open, patch, call
from mocks_for_tests import MockUsingReturnValue, MockReturnUsingDict, MockReturnUsingDictIn, MockQgisUtilsIface, MockNotFoundQuestion, MockQgsProjectInstance, DummyInterface2, mock_answer
import mock
import io
from midvatten.midvatten import midvatten
import os
import PyQt4
from collections import OrderedDict
from import_data_to_db import midv_data_importer

TEMP_DB_PATH = u'/tmp/tmp_midvatten_temp_db.sqlite'
MIDV_DICT = lambda x, y: {('Midvatten', 'database'): [TEMP_DB_PATH]}[(x, y)]

MOCK_DBPATH = MockUsingReturnValue(MockQgsProjectInstance([TEMP_DB_PATH]))
DBPATH_QUESTION = MockUsingReturnValue(TEMP_DB_PATH)


class _TestParseDiverofficeFile(object):
    utils_ask_user_about_stopping = MockReturnUsingDictIn({'Failure, delimiter did not match': 'cancel',
                                                           'Failure: The number of data columns in file': 'cancel',
                                                           'Failure, parsing failed for file': 'cancel'},
                                                          0)

    def setUp(self):
        self.importinstance = midv_data_importer()

    def test_parse_diveroffice_file_utf8(self):

        f = (u'Location=rb1',
             u'Date/time,Water head[cm],Temperature[°C]',
             u'2016/03/15 10:30:00,26.9,5.18',
             u'2016/03/15 11:00:00,157.7,0.6'
             )
        existing_obsids = [u'rb1']

        charset_of_diverofficefile = u'utf-8'
        with utils.tempinput(u'\n'.join(f), charset_of_diverofficefile) as path:
                ask_for_names = False
                file_data = self.importinstance.parse_diveroffice_file(path, charset_of_diverofficefile, existing_obsids, ask_for_names)

        test_string = utils_for_tests.create_test_string(file_data)
        reference_string = u'[[obsid, date_time, head_cm, temp_degc, cond_mscm], [rb1, 2016-03-15 10:30:00, 26.9, 5.18, ], [rb1, 2016-03-15 11:00:00, 157.7, 0.6, ]]'
        assert test_string == reference_string

    def test_parse_diveroffice_file_cp1252(self):

        f = (u'Location=rb1',
             u'Date/time,Water head[cm],Temperature[°C]',
             u'2016/03/15 10:30:00,26.9,5.18',
             u'2016/03/15 11:00:00,157.7,0.6'
             )
        existing_obsids = [u'rb1']

        charset_of_diverofficefile = u'cp1252'
        with utils.tempinput(u'\n'.join(f), charset_of_diverofficefile) as path:
                ask_for_names = False
                file_data = self.importinstance.parse_diveroffice_file(path, charset_of_diverofficefile, existing_obsids, ask_for_names)

        test_string = utils_for_tests.create_test_string(file_data)
        reference_string = u'[[obsid, date_time, head_cm, temp_degc, cond_mscm], [rb1, 2016-03-15 10:30:00, 26.9, 5.18, ], [rb1, 2016-03-15 11:00:00, 157.7, 0.6, ]]'
        assert test_string == reference_string

    def test_parse_diveroffice_file_semicolon_sep(self):

        f = (u'Location=rb1',
             u'Date/time;Water head[cm];Temperature[°C]',
             u'2016/03/15 10:30:00;26.9;5.18',
             u'2016/03/15 11:00:00;157.7;0.6'
             )
        existing_obsids = [u'rb1']

        charset_of_diverofficefile = u'cp1252'
        with utils.tempinput(u'\n'.join(f), charset_of_diverofficefile) as path:
                ask_for_names = False
                file_data = self.importinstance.parse_diveroffice_file(path, charset_of_diverofficefile, existing_obsids, ask_for_names)

        test_string = utils_for_tests.create_test_string(file_data)
        reference_string = u'[[obsid, date_time, head_cm, temp_degc, cond_mscm], [rb1, 2016-03-15 10:30:00, 26.9, 5.18, ], [rb1, 2016-03-15 11:00:00, 157.7, 0.6, ]]'
        assert test_string == reference_string

    def test_parse_diveroffice_file_comma_dec(self):

        f = (u'Location=rb1',
             u'Date/time;Water head[cm];Temperature[°C]',
             u'2016/03/15 10:30:00;26,9;5,18',
             u'2016/03/15 11:00:00;157,7;0,6'
             )
        existing_obsids = [u'rb1']

        charset_of_diverofficefile = u'cp1252'
        with utils.tempinput(u'\n'.join(f), charset_of_diverofficefile) as path:
                ask_for_names = False
                file_data = self.importinstance.parse_diveroffice_file(path, charset_of_diverofficefile, existing_obsids, ask_for_names)

        test_string = utils_for_tests.create_test_string(file_data)
        reference_string = ur'''[[obsid, date_time, head_cm, temp_degc, cond_mscm], [rb1, 2016-03-15 10:30:00, 26.9, 5.18, ], [rb1, 2016-03-15 11:00:00, 157.7, 0.6, ]]'''
        assert test_string == reference_string

    @mock.patch('import_data_to_db.utils.ask_user_about_stopping', utils_ask_user_about_stopping.get_v)
    def test_parse_diveroffice_file_comma_sep_comma_dec_failed(self):

        f = (u'Location=rb1',
             u'Date/time,Water head[cm],Temperature[°C]',
             u'2016/03/15 10:30:00,26,9,5,18',
             u'2016/03/15 11:00:00,157,7,0,6'
             )
        existing_obsids = [u'rb1']

        charset_of_diverofficefile = u'cp1252'
        with utils.tempinput(u'\n'.join(f), charset_of_diverofficefile) as path:
                ask_for_names = False
                file_data = self.importinstance.parse_diveroffice_file(path, charset_of_diverofficefile, existing_obsids, ask_for_names)

        test_string = utils_for_tests.create_test_string(file_data)
        reference_string = 'cancel'
        assert test_string == reference_string

    @mock.patch('import_data_to_db.utils.ask_user_about_stopping', utils_ask_user_about_stopping.get_v)
    def test_parse_diveroffice_file_different_separators_failed(self):

        f = (u'Location=rb1',
             u'Date/time,Water head[cm],Temperature[°C]',
             u'2016/03/15 10:30:00;26,9;5,18',
             u'2016/03/15 11:00:00;157,7;0,6'
             )
        existing_obsids = [u'rb1']

        charset_of_diverofficefile = u'cp1252'
        with utils.tempinput(u'\n'.join(f), charset_of_diverofficefile) as path:
                ask_for_names = False
                file_data = self.importinstance.parse_diveroffice_file(path, charset_of_diverofficefile, existing_obsids, ask_for_names)

        test_string = utils_for_tests.create_test_string(file_data)
        reference_string = 'cancel'
        assert test_string == reference_string

    def test_parse_diveroffice_file_try_capitalize(self):

        f = (u'Location=rb1',
             u'Date/time;Water head[cm];Temperature[°C]',
             u'2016/03/15 10:30:00;26,9;5,18',
             u'2016/03/15 11:00:00;157,7;0,6'
             )
        existing_obsids = [u'Rb1']

        charset_of_diverofficefile = u'cp1252'
        with utils.tempinput(u'\n'.join(f), charset_of_diverofficefile) as path:
                ask_for_names = False
                file_data = self.importinstance.parse_diveroffice_file(path, charset_of_diverofficefile, existing_obsids, ask_for_names)

        test_string = utils_for_tests.create_test_string(file_data)
        reference_string = u'[[obsid, date_time, head_cm, temp_degc, cond_mscm], [Rb1, 2016-03-15 10:30:00, 26.9, 5.18, ], [Rb1, 2016-03-15 11:00:00, 157.7, 0.6, ]]'
        assert test_string == reference_string

    @mock.patch('import_data_to_db.utils.NotFoundQuestion', autospec=True)
    def test_parse_diveroffice_file_cancel(self, mock_notfoundquestion):
        mock_notfoundquestion.return_value.answer = u'cancel'
        mock_notfoundquestion.return_value.value = u''

        f = (u'Location=rb1',
             u'Date/time,Water head[cm],Temperature[°C]',
             u'2016/03/15 10:30:00,26.9,5.18',
             u'2016/03/15 11:00:00,157.7,0.6'
             )
        existing_obsids = [u'rb2']

        charset_of_diverofficefile = u'utf-8'
        with utils.tempinput(u'\n'.join(f), charset_of_diverofficefile) as path:
                ask_for_names = False
                file_data = self.importinstance.parse_diveroffice_file(path, charset_of_diverofficefile, existing_obsids, ask_for_names)

        test_string = utils_for_tests.create_test_string(file_data)
        reference_string = u'cancel'
        assert test_string == reference_string


class _TestWlvllogImportFromDiverofficeFiles(object):
    """ Test to make sure wlvllogg_import goes all the way to the end without errors
    """
    answer_yes = mock_answer('yes')
    answer_no = mock_answer('no')
    CRS_question = MockUsingReturnValue([3006])
    dbpath_question = MockUsingReturnValue(TEMP_DB_PATH)
    mocked_iface = MockQgisUtilsIface()  #Used for not getting messageBar errors
    mock_dbpath = MockUsingReturnValue(MockQgsProjectInstance([TEMP_DB_PATH]))
    mock_askuser = MockReturnUsingDictIn({u'It is a strong': answer_no.get_v(), u'Please note!\nThere are ': answer_yes.get_v(), u'Please note!\nForeign keys will': answer_yes.get_v()}, 1)
    skip_popup = MockUsingReturnValue('')

    @mock.patch('create_db.utils.NotFoundQuestion')
    @mock.patch('midvatten_utils.askuser', answer_yes.get_v)
    @mock.patch('midvatten_utils.QgsProject.instance')
    @mock.patch('create_db.PyQt4.QtGui.QInputDialog.getInteger')
    @mock.patch('create_db.PyQt4.QtGui.QFileDialog.getSaveFileName')
    def setUp(self, mock_savefilename, mock_crsquestion, mock_qgsproject_instance, mock_locale):
        mock_crsquestion.return_value = [3006]
        mock_savefilename.return_value = TEMP_DB_PATH
        mock_qgsproject_instance.return_value.readEntry = MIDV_DICT

        self.dummy_iface = DummyInterface2()
        self.iface = self.dummy_iface.mock
        self.midvatten = midvatten(self.iface)

        try:
            os.remove(TEMP_DB_PATH)
        except OSError:
            pass
        mock_locale.return_value.answer = u'ok'
        mock_locale.return_value.value = u'sv_SE'
        self.midvatten.new_db()
        self.importinstance = midv_data_importer()

    def tearDown(self):
        #Delete database
        os.remove(TEMP_DB_PATH)

    @mock.patch('midvatten_utils.QgsProject.instance', mock_dbpath.get_v)
    def test_wlvllogg_import_from_diveroffice_files(self):
        files = [(u'Location=rb1',
                u'Date/time,Water head[cm],Temperature[°C]',
                u'2016/03/15 10:30:00,1,10',
                u'2016/03/15 11:00:00,11,101'),
                (u'Location=rb2',
                u'Date/time,Water head[cm],Temperature[°C]',
                u'2016/04/15 10:30:00,2,20',
                u'2016/04/15 11:00:00,21,201'),
                (u'Location=rb3',
                u'Date/time,Water head[cm],Temperature[°C],Conductivity[mS/cm]',
                u'2016/05/15 10:30:00,3,30,5',
                u'2016/05/15 11:00:00,31,301,6')
                 ]

        utils.sql_alter_db(u'''INSERT INTO obs_points ("obsid") VALUES ("rb1")''')
        utils.sql_alter_db(u'''INSERT INTO obs_points ("obsid") VALUES ("rb2")''')
        utils.sql_alter_db(u'''INSERT INTO obs_points ("obsid") VALUES ("rb3")''')

        self.importinstance.charsetchoosen = u'utf-8'
        with utils.tempinput(u'\n'.join(files[0]), self.importinstance.charsetchoosen) as f1:
            with utils.tempinput(u'\n'.join(files[1]), self.importinstance.charsetchoosen) as f2:
                with utils.tempinput(u'\n'.join(files[2]), self.importinstance.charsetchoosen) as f3:

                    filenames = [f1, f2, f3]
                    utils_askuser_answer_no_obj = MockUsingReturnValue(None)
                    utils_askuser_answer_no_obj.result = 0
                    utils_askuser_answer_no = MockUsingReturnValue(utils_askuser_answer_no_obj)

                    @mock.patch('midvatten_utils.QgsProject.instance', TestWlvllogImportFromDiverofficeFiles.mock_dbpath.get_v)
                    @mock.patch('import_data_to_db.utils.askuser')
                    @mock.patch('qgis.utils.iface', autospec=True)
                    @mock.patch('PyQt4.QtGui.QInputDialog.getText')
                    @mock.patch('import_data_to_db.utils.pop_up_info', autospec=True)
                    @mock.patch('import_data_to_db.utils.select_files')
                    def _test_wlvllogg_import_from_diveroffice_files(self, filenames, mock_filenames, mock_skippopup, mock_encoding, mock_iface, mock_askuser):
                        mock_filenames.return_value = filenames
                        mock_encoding.return_value = [u'utf-8']
                        self.importinstance.wlvllogg_import_from_diveroffice_files()

                    _test_wlvllogg_import_from_diveroffice_files(self, filenames)

                    test_string = utils_for_tests.create_test_string(utils.sql_load_fr_db(u'''select obsid, date_time, head_cm, temp_degc, cond_mscm, level_masl, comment from w_levels_logger'''))
                    reference_string = ur'''(True, [(rb1, 2016-03-15 10:30:00, 1.0, 10.0, None, None, None), (rb1, 2016-03-15 11:00:00, 11.0, 101.0, None, None, None), (rb2, 2016-04-15 10:30:00, 2.0, 20.0, None, None, None), (rb2, 2016-04-15 11:00:00, 21.0, 201.0, None, None, None), (rb3, 2016-05-15 10:30:00, 3.0, 30.0, 5.0, None, None), (rb3, 2016-05-15 11:00:00, 31.0, 301.0, 6.0, None, None)])'''
                    assert test_string == reference_string

    @mock.patch('midvatten_utils.QgsProject.instance', mock_dbpath.get_v)
    def test_wlvllogg_import_from_diveroffice_files_skip_duplicate_datetimes(self):
        files = [(u'Location=rb1',
                u'Date/time,Water head[cm],Temperature[°C]',
                u'2016/03/15 10:30:00,1,10',
                u'2016/03/15 11:00:00,11,101'),
                (u'Location=rb2',
                u'Date/time,Water head[cm],Temperature[°C]',
                u'2016/04/15 10:30:00,2,20',
                u'2016/04/15 11:00:00,21,201'),
                (u'Location=rb3',
                u'Date/time,Water head[cm],Temperature[°C],Conductivity[mS/cm]',
                u'2016/05/15 10:30:00,3,30,5',
                u'2016/05/15 11:00:00,31,301,6')
                 ]

        utils.sql_alter_db(u'''INSERT INTO obs_points ("obsid") VALUES ("rb1")''')
        utils.sql_alter_db(u'''INSERT INTO obs_points ("obsid") VALUES ("rb2")''')
        utils.sql_alter_db(u'''INSERT INTO obs_points ("obsid") VALUES ("rb3")''')
        utils.sql_alter_db(u'''INSERT INTO w_levels_logger ("obsid", "date_time", "head_cm") VALUES ('rb1', '2016-03-15 10:30', '5.0')''')

        self.importinstance.charsetchoosen = u'utf-8'
        with utils.tempinput(u'\n'.join(files[0]), self.importinstance.charsetchoosen) as f1:
            with utils.tempinput(u'\n'.join(files[1]), self.importinstance.charsetchoosen) as f2:
                with utils.tempinput(u'\n'.join(files[2]), self.importinstance.charsetchoosen) as f3:

                    filenames = [f1, f2, f3]

                    @mock.patch('midvatten_utils.QgsProject.instance', TestWlvllogImportFromDiverofficeFiles.mock_dbpath.get_v)
                    @mock.patch('import_data_to_db.utils.askuser')
                    @mock.patch('qgis.utils.iface', autospec=True)
                    @mock.patch('PyQt4.QtGui.QInputDialog.getText')
                    @mock.patch('import_data_to_db.utils.pop_up_info', autospec=True)
                    @mock.patch('import_data_to_db.utils.select_files')
                    def _test_wlvllogg_import_from_diveroffice_files(self, filenames, mock_filenames, mock_skippopup, mock_encoding, mock_iface, mock_askuser):
                        mock_filenames.return_value = filenames
                        mock_encoding.return_value = [u'utf-8']

                        def side_effect(*args, **kwargs):
                            mock_result = mock.MagicMock()
                            if args[1].startswith(u'Do you want to confirm'):
                                mock_result.result = 0
                                return mock_result
                                #mock_askuser.return_value.result.return_value = 0
                            elif args[1].startswith(u'Do you want to import all'):
                                mock_result.result = 0
                                return mock_result
                            elif args[1].startswith(u'Please note!\nForeign keys'):
                                mock_result.result = 1
                                return mock_result
                            elif args[1].startswith(u'Please note!\nThere are'):
                                mock_result.result = 1
                                return mock_result
                            elif args[1].startswith(u'It is a strong recommendation'):
                                mock_result.result = 0
                                return mock_result
                        mock_askuser.side_effect = side_effect

                        self.importinstance.wlvllogg_import_from_diveroffice_files()

                    _test_wlvllogg_import_from_diveroffice_files(self, filenames)

                    test_string = utils_for_tests.create_test_string(utils.sql_load_fr_db(u'''select obsid, date_time, head_cm, temp_degc, cond_mscm, level_masl, comment from w_levels_logger'''))
                    reference_string = ur'''(True, [(rb1, 2016-03-15 10:30, 5.0, None, None, None, None), (rb1, 2016-03-15 11:00:00, 11.0, 101.0, None, None, None), (rb2, 2016-04-15 10:30:00, 2.0, 20.0, None, None, None), (rb2, 2016-04-15 11:00:00, 21.0, 201.0, None, None, None), (rb3, 2016-05-15 10:30:00, 3.0, 30.0, 5.0, None, None), (rb3, 2016-05-15 11:00:00, 31.0, 301.0, 6.0, None, None)])'''
                    assert test_string == reference_string

    @mock.patch('midvatten_utils.QgsProject.instance', mock_dbpath.get_v)
    def test_wlvllogg_import_from_diveroffice_files_filter_dates(self):
        files = [(u'Location=rb1',
                u'Date/time,Water head[cm],Temperature[°C]',
                u'2016/03/15 10:30:00,1,10',
                u'2016/03/15 11:00:00,11,101'),
                (u'Location=rb2',
                u'Date/time,Water head[cm],Temperature[°C]',
                u'2016/04/15 10:30:00,2,20',
                u'2016/04/15 11:00:00,21,201'),
                (u'Location=rb3',
                u'Date/time,Water head[cm],Temperature[°C],Conductivity[mS/cm]',
                u'2016/05/15 10:30:00,3,30,5',
                u'2016/05/15 11:00:00,31,301,6')
                 ]

        utils.sql_alter_db(u'''INSERT INTO obs_points ("obsid") VALUES ("rb1")''')
        utils.sql_alter_db(u'''INSERT INTO obs_points ("obsid") VALUES ("rb2")''')
        utils.sql_alter_db(u'''INSERT INTO obs_points ("obsid") VALUES ("rb3")''')
        utils.sql_alter_db(u'''INSERT INTO w_levels_logger ("obsid", "date_time", "head_cm") VALUES ('rb1', '2016-03-15 10:31', '5.0')''')

        self.importinstance.charsetchoosen = u'utf-8'
        with utils.tempinput(u'\n'.join(files[0]), self.importinstance.charsetchoosen) as f1:
            with utils.tempinput(u'\n'.join(files[1]), self.importinstance.charsetchoosen) as f2:
                with utils.tempinput(u'\n'.join(files[2]), self.importinstance.charsetchoosen) as f3:

                    filenames = [f1, f2, f3]

                    @mock.patch('midvatten_utils.QgsProject.instance', TestWlvllogImportFromDiverofficeFiles.mock_dbpath.get_v)
                    @mock.patch('import_data_to_db.utils.askuser')
                    @mock.patch('qgis.utils.iface', autospec=True)
                    @mock.patch('PyQt4.QtGui.QInputDialog.getText')
                    @mock.patch('import_data_to_db.utils.pop_up_info', autospec=True)
                    @mock.patch('import_data_to_db.utils.select_files')
                    def _test_wlvllogg_import_from_diveroffice_files(self, filenames, mock_filenames, mock_skippopup, mock_encoding, mock_iface, mock_askuser):
                        mock_filenames.return_value = filenames
                        mock_encoding.return_value = [u'utf-8']

                        def side_effect(*args, **kwargs):
                            mock_result = mock.MagicMock()
                            if args[1].startswith(u'Do you want to confirm'):
                                mock_result.result = 0
                                return mock_result
                                #mock_askuser.return_value.result.return_value = 0
                            elif args[1].startswith(u'Do you want to import all'):
                                mock_result.result = 0
                                return mock_result
                            elif args[1].startswith(u'Please note!\nForeign keys'):
                                mock_result.result = 1
                                return mock_result
                            elif args[1].startswith(u'Please note!\nThere are'):
                                mock_result.result = 1
                                return mock_result
                            elif args[1].startswith(u'It is a strong recommendation'):
                                mock_result.result = 0
                                return mock_result

                        mock_askuser.side_effect = side_effect

                        self.importinstance.wlvllogg_import_from_diveroffice_files()

                    _test_wlvllogg_import_from_diveroffice_files(self, filenames)

                    test_string = utils_for_tests.create_test_string(utils.sql_load_fr_db(u'''select obsid, date_time, head_cm, temp_degc, cond_mscm, level_masl, comment from w_levels_logger'''))
                    reference_string = ur'''(True, [(rb1, 2016-03-15 10:31, 5.0, None, None, None, None), (rb1, 2016-03-15 11:00:00, 11.0, 101.0, None, None, None), (rb2, 2016-04-15 10:30:00, 2.0, 20.0, None, None, None), (rb2, 2016-04-15 11:00:00, 21.0, 201.0, None, None, None), (rb3, 2016-05-15 10:30:00, 3.0, 30.0, 5.0, None, None), (rb3, 2016-05-15 11:00:00, 31.0, 301.0, 6.0, None, None)])'''
                    assert test_string == reference_string

    @mock.patch('midvatten_utils.QgsProject.instance', mock_dbpath.get_v)
    def test_wlvllogg_import_from_diveroffice_files_all_dates(self):
        files = [(u'Location=rb1',
                u'Date/time,Water head[cm],Temperature[°C]',
                u'2016/03/15 10:30:00,1,10',
                u'2016/03/15 11:00:00,11,101'),
                (u'Location=rb2',
                u'Date/time,Water head[cm],Temperature[°C]',
                u'2016/04/15 10:30:00,2,20',
                u'2016/04/15 11:00:00,21,201'),
                (u'Location=rb3',
                u'Date/time,Water head[cm],Temperature[°C],Conductivity[mS/cm]',
                u'2016/05/15 10:30:00,3,30,5',
                u'2016/05/15 11:00:00,31,301,6')
                 ]

        utils.sql_alter_db(u'''INSERT INTO obs_points ("obsid") VALUES ("rb1")''')
        utils.sql_alter_db(u'''INSERT INTO obs_points ("obsid") VALUES ("rb2")''')
        utils.sql_alter_db(u'''INSERT INTO obs_points ("obsid") VALUES ("rb3")''')
        utils.sql_alter_db(u'''INSERT INTO w_levels_logger ("obsid", "date_time", "head_cm") VALUES ('rb1', '2016-03-15 10:31', '5.0')''')

        self.importinstance.charsetchoosen = u'utf-8'
        with utils.tempinput(u'\n'.join(files[0]), self.importinstance.charsetchoosen) as f1:
            with utils.tempinput(u'\n'.join(files[1]), self.importinstance.charsetchoosen) as f2:
                with utils.tempinput(u'\n'.join(files[2]), self.importinstance.charsetchoosen) as f3:

                    filenames = [f1, f2, f3]

                    @mock.patch('midvatten_utils.QgsProject.instance', TestWlvllogImportFromDiverofficeFiles.mock_dbpath.get_v)
                    @mock.patch('import_data_to_db.utils.askuser')
                    @mock.patch('qgis.utils.iface', autospec=True)
                    @mock.patch('PyQt4.QtGui.QInputDialog.getText')
                    @mock.patch('import_data_to_db.utils.pop_up_info', autospec=True)
                    @mock.patch('import_data_to_db.utils.select_files')
                    def _test_wlvllogg_import_from_diveroffice_files(self, filenames, mock_filenames, mock_skippopup, mock_encoding, mock_iface, mock_askuser):
                        mock_filenames.return_value = filenames
                        mock_encoding.return_value = [u'utf-8']

                        def side_effect(*args, **kwargs):
                            mock_result = mock.MagicMock()
                            if args[1].startswith(u'Do you want to confirm'):
                                mock_result.result = 0
                                return mock_result
                                #mock_askuser.return_value.result.return_value = 0
                            elif args[1].startswith(u'Do you want to import all'):
                                mock_result.result = 1
                                return mock_result
                            elif args[1].startswith(u'Please note!\nForeign keys'):
                                mock_result.result = 1
                                return mock_result
                            elif args[1].startswith(u'Please note!\nThere are'):
                                mock_result.result = 1
                                return mock_result
                            elif args[1].startswith(u'It is a strong recommendation'):
                                mock_result.result = 0
                                return mock_result

                        mock_askuser.side_effect = side_effect

                        self.importinstance.wlvllogg_import_from_diveroffice_files()

                    _test_wlvllogg_import_from_diveroffice_files(self, filenames)

                    test_string = utils_for_tests.create_test_string(utils.sql_load_fr_db(u'''select obsid, date_time, head_cm, temp_degc, cond_mscm, level_masl, comment from w_levels_logger'''))
                    reference_string = ur'''(True, [(rb1, 2016-03-15 10:31, 5.0, None, None, None, None), (rb1, 2016-03-15 10:30:00, 1.0, 10.0, None, None, None), (rb1, 2016-03-15 11:00:00, 11.0, 101.0, None, None, None), (rb2, 2016-04-15 10:30:00, 2.0, 20.0, None, None, None), (rb2, 2016-04-15 11:00:00, 21.0, 201.0, None, None, None), (rb3, 2016-05-15 10:30:00, 3.0, 30.0, 5.0, None, None), (rb3, 2016-05-15 11:00:00, 31.0, 301.0, 6.0, None, None)])'''
                    assert test_string == reference_string


class _TestGeneralCsvImport(object):
    """ Test to make sure wlvllogg_import goes all the way to the end without errors
    """
    answer_yes = mock_answer('yes')
    answer_no = mock_answer('no')
    CRS_question = MockUsingReturnValue([3006])
    mocked_iface = MockQgisUtilsIface()  #Used for not getting messageBar errors
    mock_askuser = MockReturnUsingDictIn({u'It is a strong': answer_no.get_v(), u'Please note!\nThere are ': answer_yes.get_v(), u'Please note!\nForeign keys will': answer_yes.get_v()}, 1)
    mock_encoding = MockUsingReturnValue([True, u'utf-8'])

    @mock.patch('create_db.utils.NotFoundQuestion')
    @mock.patch('midvatten_utils.askuser', answer_yes.get_v)
    @mock.patch('midvatten_utils.QgsProject.instance')
    @mock.patch('create_db.PyQt4.QtGui.QInputDialog.getInteger')
    @mock.patch('create_db.PyQt4.QtGui.QFileDialog.getSaveFileName')
    def setUp(self, mock_savefilename, mock_crsquestion, mock_qgsproject_instance, mock_locale):
        mock_crsquestion.return_value = [3006]
        mock_savefilename.return_value = TEMP_DB_PATH
        mock_qgsproject_instance.return_value.readEntry = MIDV_DICT

        self.dummy_iface = DummyInterface2()
        self.iface = self.dummy_iface.mock
        self.midvatten = midvatten(self.iface)

        try:
            os.remove(TEMP_DB_PATH)
        except OSError:
            pass
        mock_locale.return_value.answer = u'ok'
        mock_locale.return_value.value = u'sv_SE'
        self.midvatten.new_db()
        self.importinstance = midv_data_importer()

    def tearDown(self):
        #Delete database
        os.remove(TEMP_DB_PATH)

    @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
    def test_general_csv_import_wlvllogg(self):
        file = [u'obsid,date_time,head_cm',
                 u'rb1,2016-03-15 10:30:00,1']

        utils.sql_alter_db(u'''INSERT INTO obs_points ("obsid") VALUES ("rb1")''')

        self.importinstance.charsetchoosen = [u'utf-8']
        with utils.tempinput(u'\n'.join(file), self.importinstance.charsetchoosen[0]) as filename:
                    utils_askuser_answer_no_obj = MockUsingReturnValue(None)
                    utils_askuser_answer_no_obj.result = 0
                    utils_askuser_answer_no = MockUsingReturnValue(utils_askuser_answer_no_obj)

                    @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
                    @mock.patch('import_data_to_db.utils.askuser')
                    @mock.patch('qgis.utils.iface', autospec=True)
                    @mock.patch('PyQt4.QtGui.QInputDialog.getText')
                    @mock.patch('import_data_to_db.utils.pop_up_info', autospec=True)
                    @mock.patch.object(PyQt4.QtGui.QFileDialog, 'getOpenFileName')
                    def _test_general_csv_import_wlvllogg(self, filename, mock_filename, mock_skippopup, mock_encoding, mock_iface, mock_askuser):

                        mock_filename.return_value = filename
                        mock_encoding.return_value = [True, u'utf-8']
                        self.importinstance.general_csv_import(goal_table=u'w_levels_logger')

                    _test_general_csv_import_wlvllogg(self, filename)

                    test_string = utils_for_tests.create_test_string(utils.sql_load_fr_db(u'''select obsid, date_time, head_cm, temp_degc, cond_mscm, level_masl, comment from w_levels_logger'''))
                    reference_string = ur'''(True, [(rb1, 2016-03-15 10:30:00, 1.0, None, None, None, None)])'''
                    assert test_string == reference_string

    @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
    def test_general_csv_import_wlvllogg_missing_not_null_column(self):
        file = [u'obsids,date_time,test',
                 u'rb1,2016-03-15 10:30:00,1']

        utils.sql_alter_db(u'''INSERT INTO obs_points ("obsid") VALUES ("rb1")''')

        self.importinstance.charsetchoosen = [u'utf-8']
        with utils.tempinput(u'\n'.join(file), self.importinstance.charsetchoosen[0]) as filename:
                    utils_askuser_answer_no_obj = MockUsingReturnValue(None)
                    utils_askuser_answer_no_obj.result = 0
                    utils_askuser_answer_no = MockUsingReturnValue(utils_askuser_answer_no_obj)

                    @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
                    @mock.patch('import_data_to_db.utils.askuser')
                    @mock.patch('qgis.utils.iface', autospec=True)
                    @mock.patch('PyQt4.QtGui.QInputDialog.getText')
                    @mock.patch('import_data_to_db.utils.pop_up_info', autospec=True)
                    @mock.patch.object(PyQt4.QtGui.QFileDialog, 'getOpenFileName')
                    def _test_general_csv_import_wlvllogg(self, filename, mock_filename, mock_skippopup, mock_encoding, mock_iface, mock_askuser):
                        mock_filename.return_value = filename
                        mock_encoding.return_value = [True, u'utf-8']
                        self.importinstance.general_csv_import(goal_table=u'w_levels_logger')

                        mock_iface.messageBar.return_value.createMessage.assert_called_with(u'Error: Import failed, see log message panel')
                    _test_general_csv_import_wlvllogg(self, filename)

                    test_string = utils_for_tests.create_test_string(utils.sql_load_fr_db(u'''select obsid, date_time, head_cm, temp_degc, cond_mscm, level_masl, comment from w_levels_logger'''))
                    reference_string = ur'''(True, [])'''
                    assert test_string == reference_string

    @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
    def test_general_csv_import_wlvllogg_with_comment(self):
        file = [u'obsid,date_time,head_cm,comment',
                 u'rb1,2016-03-15 10:30:00,1,testcomment']

        utils.sql_alter_db(u'''INSERT INTO obs_points ("obsid") VALUES ("rb1")''')

        self.importinstance.charsetchoosen = [u'utf-8']
        with utils.tempinput(u'\n'.join(file), self.importinstance.charsetchoosen[0]) as filename:
                    utils_askuser_answer_no_obj = MockUsingReturnValue(None)
                    utils_askuser_answer_no_obj.result = 0
                    utils_askuser_answer_no = MockUsingReturnValue(utils_askuser_answer_no_obj)

                    @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
                    @mock.patch('import_data_to_db.utils.askuser')
                    @mock.patch('qgis.utils.iface', autospec=True)
                    @mock.patch('PyQt4.QtGui.QInputDialog.getText')
                    @mock.patch('import_data_to_db.utils.pop_up_info', autospec=True)
                    @mock.patch.object(PyQt4.QtGui.QFileDialog, 'getOpenFileName')
                    def _test_general_csv_import_wlvllogg(self, filename, mock_filename, mock_skippopup, mock_encoding, mock_iface, mock_askuser):
                        mock_filename.return_value = filename
                        mock_encoding.return_value = [True, u'utf-8']
                        self.importinstance.general_csv_import(goal_table=u'w_levels_logger')

                    _test_general_csv_import_wlvllogg(self, filename)

                    test_string = utils_for_tests.create_test_string(utils.sql_load_fr_db(u'''select obsid, date_time, head_cm, temp_degc, cond_mscm, level_masl, comment from w_levels_logger'''))
                    reference_string = ur'''(True, [(rb1, 2016-03-15 10:30:00, 1.0, None, None, None, testcomment)])'''
                    assert test_string == reference_string

    @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
    def test_general_csv_import_wlvllogg_with_temp(self):
        file = [u'obsid,date_time,head_cm,temp_degc',
                 u'rb1,2016-03-15 10:30:00,1, 5']

        utils.sql_alter_db(u'''INSERT INTO obs_points ("obsid") VALUES ("rb1")''')

        self.importinstance.charsetchoosen = [u'utf-8']
        with utils.tempinput(u'\n'.join(file), self.importinstance.charsetchoosen[0]) as filename:
                    utils_askuser_answer_no_obj = MockUsingReturnValue(None)
                    utils_askuser_answer_no_obj.result = 0
                    utils_askuser_answer_no = MockUsingReturnValue(utils_askuser_answer_no_obj)

                    @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
                    @mock.patch('import_data_to_db.utils.askuser')
                    @mock.patch('qgis.utils.iface', autospec=True)
                    @mock.patch('PyQt4.QtGui.QInputDialog.getText')
                    @mock.patch('import_data_to_db.utils.pop_up_info', autospec=True)
                    @mock.patch.object(PyQt4.QtGui.QFileDialog, 'getOpenFileName')
                    def _test_general_csv_import_wlvllogg(self, filename, mock_filename, mock_skippopup, mock_encoding, mock_iface, mock_askuser):
                        mock_filename.return_value = filename
                        mock_encoding.return_value = [True, u'utf-8']
                        self.importinstance.general_csv_import(goal_table=u'w_levels_logger')

                    _test_general_csv_import_wlvllogg(self, filename)

                    test_string = utils_for_tests.create_test_string(utils.sql_load_fr_db(u'''select obsid, date_time, head_cm, temp_degc, cond_mscm, level_masl, comment from w_levels_logger'''))
                    reference_string = ur'''(True, [(rb1, 2016-03-15 10:30:00, 1.0, 5.0, None, None, None)])'''
                    assert test_string == reference_string

    @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
    def test_general_csv_import_wlvllogg_with_temp_comment(self):
        file = [u'obsid,date_time,head_cm,temp_degc,cond_mscm',
                 u'rb1,2016-03-15 10:30:00,1,5,10']

        utils.sql_alter_db(u'''INSERT INTO obs_points ("obsid") VALUES ("rb1")''')

        self.importinstance.charsetchoosen = [u'utf-8']
        with utils.tempinput(u'\n'.join(file), self.importinstance.charsetchoosen[0]) as filename:
                    utils_askuser_answer_no_obj = MockUsingReturnValue(None)
                    utils_askuser_answer_no_obj.result = 0
                    utils_askuser_answer_no = MockUsingReturnValue(utils_askuser_answer_no_obj)

                    @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
                    @mock.patch('import_data_to_db.utils.askuser')
                    @mock.patch('qgis.utils.iface', autospec=True)
                    @mock.patch('PyQt4.QtGui.QInputDialog.getText')
                    @mock.patch('import_data_to_db.utils.pop_up_info', autospec=True)
                    @mock.patch.object(PyQt4.QtGui.QFileDialog, 'getOpenFileName')
                    def _test_general_csv_import_wlvllogg(self, filename, mock_filename, mock_skippopup, mock_encoding, mock_iface, mock_askuser):
                        mock_filename.return_value = filename
                        mock_encoding.return_value = [True, u'utf-8']
                        self.importinstance.general_csv_import(goal_table=u'w_levels_logger')

                    _test_general_csv_import_wlvllogg(self, filename)

                    test_string = utils_for_tests.create_test_string(utils.sql_load_fr_db(u'''select obsid, date_time, head_cm, temp_degc, cond_mscm, level_masl, comment from w_levels_logger'''))
                    reference_string = ur'''(True, [(rb1, 2016-03-15 10:30:00, 1.0, 5.0, 10.0, None, None)])'''
                    assert test_string == reference_string

    @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
    def test_general_csv_import_wlvllogg_different_order(self):
        file = [u'obsid,cond_mscm,date_time,head_cm,temp_degc',
                 u'rb1,10,2016-03-15 10:30:00,1,5']

        utils.sql_alter_db(u'''INSERT INTO obs_points ("obsid") VALUES ("rb1")''')

        self.importinstance.charsetchoosen = [u'utf-8']
        with utils.tempinput(u'\n'.join(file), self.importinstance.charsetchoosen[0]) as filename:
                    utils_askuser_answer_no_obj = MockUsingReturnValue(None)
                    utils_askuser_answer_no_obj.result = 0
                    utils_askuser_answer_no = MockUsingReturnValue(utils_askuser_answer_no_obj)

                    @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
                    @mock.patch('import_data_to_db.utils.askuser')
                    @mock.patch('qgis.utils.iface', autospec=True)
                    @mock.patch('PyQt4.QtGui.QInputDialog.getText')
                    @mock.patch('import_data_to_db.utils.pop_up_info', autospec=True)
                    @mock.patch.object(PyQt4.QtGui.QFileDialog, 'getOpenFileName')
                    def _test_general_csv_import_wlvllogg(self, filename, mock_filename, mock_skippopup, mock_encoding, mock_iface, mock_askuser):
                        mock_filename.return_value = filename
                        mock_encoding.return_value = [True, u'utf-8']
                        self.importinstance.general_csv_import(goal_table=u'w_levels_logger')

                    _test_general_csv_import_wlvllogg(self, filename)

                    test_string = utils_for_tests.create_test_string(utils.sql_load_fr_db(u'''select obsid, date_time, head_cm, temp_degc, cond_mscm, level_masl, comment from w_levels_logger'''))
                    reference_string = ur'''(True, [(rb1, 2016-03-15 10:30:00, 1.0, 5.0, 10.0, None, None)])'''
                    assert test_string == reference_string

    @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
    def test_general_csv_import_wlvllogg_only_level_masl(self):
        file = [u'obsid,date_time,level_masl',
                 u'rb1,2016-03-15 10:30:00,1']

        utils.sql_alter_db(u'''INSERT INTO obs_points ("obsid") VALUES ("rb1")''')

        self.importinstance.charsetchoosen = [u'utf-8']
        with utils.tempinput(u'\n'.join(file), self.importinstance.charsetchoosen[0]) as filename:
                    utils_askuser_answer_no_obj = MockUsingReturnValue(None)
                    utils_askuser_answer_no_obj.result = 0
                    utils_askuser_answer_no = MockUsingReturnValue(utils_askuser_answer_no_obj)

                    @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
                    @mock.patch('import_data_to_db.utils.askuser')
                    @mock.patch('qgis.utils.iface', autospec=True)
                    @mock.patch('PyQt4.QtGui.QInputDialog.getText')
                    @mock.patch('import_data_to_db.utils.pop_up_info', autospec=True)
                    @mock.patch.object(PyQt4.QtGui.QFileDialog, 'getOpenFileName')
                    def _test_general_csv_import_wlvllogg(self, filename, mock_filename, mock_skippopup, mock_encoding, mock_iface, mock_askuser):
                        mock_filename.return_value = filename
                        mock_encoding.return_value = [True, u'utf-8']
                        self.importinstance.general_csv_import(goal_table=u'w_levels_logger')

                    _test_general_csv_import_wlvllogg(self, filename)

                    test_string = utils_for_tests.create_test_string(utils.sql_load_fr_db(u'''select obsid, date_time, head_cm, temp_degc, cond_mscm, level_masl, comment from w_levels_logger'''))
                    reference_string = ur'''(True, [(rb1, 2016-03-15 10:30:00, None, None, None, 1.0, None)])'''
                    assert test_string == reference_string

    @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
    def test_general_csv_import_wlvllogg_only_temp_degc(self):
        file = [u'obsid,date_time,temp_degc',
                 u'rb1,2016-03-15 10:30:00,1']

        utils.sql_alter_db(u'''INSERT INTO obs_points ("obsid") VALUES ("rb1")''')

        self.importinstance.charsetchoosen = [u'utf-8']
        with utils.tempinput(u'\n'.join(file), self.importinstance.charsetchoosen[0]) as filename:
                    utils_askuser_answer_no_obj = MockUsingReturnValue(None)
                    utils_askuser_answer_no_obj.result = 0
                    utils_askuser_answer_no = MockUsingReturnValue(utils_askuser_answer_no_obj)

                    @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
                    @mock.patch('import_data_to_db.utils.askuser')
                    @mock.patch('qgis.utils.iface', autospec=True)
                    @mock.patch('PyQt4.QtGui.QInputDialog.getText')
                    @mock.patch('import_data_to_db.utils.pop_up_info', autospec=True)
                    @mock.patch.object(PyQt4.QtGui.QFileDialog, 'getOpenFileName')
                    def _test_general_csv_import_wlvllogg(self, filename, mock_filename, mock_skippopup, mock_encoding, mock_iface, mock_askuser):
                        mock_filename.return_value = filename
                        mock_encoding.return_value = [True, u'utf-8']
                        self.importinstance.general_csv_import(goal_table=u'w_levels_logger')

                    _test_general_csv_import_wlvllogg(self, filename)

                    test_string = utils_for_tests.create_test_string(utils.sql_load_fr_db(u'''select obsid, date_time, head_cm, temp_degc, cond_mscm, level_masl, comment from w_levels_logger'''))
                    reference_string = ur'''(True, [(rb1, 2016-03-15 10:30:00, None, 1.0, None, None, None)])'''
                    assert test_string == reference_string

    @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
    def test_general_csv_import_wlvllogg_only_cond_mscm(self):
        file = [u'obsid,date_time,cond_mscm',
                 u'rb1,2016-03-15 10:30:00,1']

        utils.sql_alter_db(u'''INSERT INTO obs_points ("obsid") VALUES ("rb1")''')

        self.importinstance.charsetchoosen = [u'utf-8']
        with utils.tempinput(u'\n'.join(file), self.importinstance.charsetchoosen[0]) as filename:
                    utils_askuser_answer_no_obj = MockUsingReturnValue(None)
                    utils_askuser_answer_no_obj.result = 0
                    utils_askuser_answer_no = MockUsingReturnValue(utils_askuser_answer_no_obj)

                    @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
                    @mock.patch('import_data_to_db.utils.askuser')
                    @mock.patch('qgis.utils.iface', autospec=True)
                    @mock.patch('PyQt4.QtGui.QInputDialog.getText')
                    @mock.patch('import_data_to_db.utils.pop_up_info', autospec=True)
                    @mock.patch.object(PyQt4.QtGui.QFileDialog, 'getOpenFileName')
                    def _test_general_csv_import_wlvllogg(self, filename, mock_filename, mock_skippopup, mock_encoding, mock_iface, mock_askuser):
                        mock_filename.return_value = filename
                        mock_encoding.return_value = [True, u'utf-8']
                        self.importinstance.general_csv_import(goal_table=u'w_levels_logger')

                    _test_general_csv_import_wlvllogg(self, filename)

                    test_string = utils_for_tests.create_test_string(utils.sql_load_fr_db(u'''select obsid, date_time, head_cm, temp_degc, cond_mscm, level_masl, comment from w_levels_logger'''))
                    reference_string = ur'''(True, [(rb1, 2016-03-15 10:30:00, None, None, 1.0, None, None)])'''
                    assert test_string == reference_string


class _TestInterlab4Importer():
    def setUp(self):
        self.importinstance = midv_data_importer()

    def test_interlab4_parse_filesettings_utf16(self):
        interlab4_lines = (
                    u"#Interlab",
                    u"#Version=4.0",
                    u"#Tecken=UTF-16",
                    u"#Textavgränsare=Nej",
                    u"#Decimaltecken=,",
                    u"#Provadm",
                    u"Lablittera;Namn;Adress;Postnr;Ort;Kommunkod;Projekt;Laboratorium;Provtyp;Provtagare;Registertyp;ProvplatsID;Provplatsn",
                        )
        with utils.tempinput(u'\n'.join(interlab4_lines), 'utf-16') as testfile:
            result_string = str(utils_for_tests.dict_to_sorted_list(self.importinstance.interlab4_parse_filesettings(testfile)))

        reference_string = "['False', '4.0', 'utf-16', ',', 'False']"

        assert result_string == reference_string

    def test_interlab4_parse_filesettings_utf8(self):
        interlab4_lines = (
                    u"#Interlab",
                    u"#Version=4.0",
                    u"#Tecken=UTF-8",
                    u"#Textavgränsare=Nej",
                    u"#Decimaltecken=,",
                    u"#Provadm",
                    u"Lablittera;Namn;Adress;Postnr;Ort;Kommunkod;Projekt;Laboratorium;Provtyp;Provtagare;Registertyp;ProvplatsID;Provplatsn",
                        )
        with utils.tempinput(u'\n'.join(interlab4_lines), 'utf-8') as testfile:
            result_string = str(utils_for_tests.dict_to_sorted_list(self.importinstance.interlab4_parse_filesettings(testfile)))

        reference_string = "['False', '4.0', 'utf-8', ',', 'False']"

        assert result_string == reference_string

    def test_parse_interlab4_utf16(self):

        interlab4_lines = (
                    u"#Interlab",
                    u"#Version=4.0",
                    u"#Tecken=UTF-16",
                    u"#Textavgränsare=Nej",
                    u"#Decimaltecken=,",
                    u"#Provadm",
                    u"Lablittera;Namn;Adress;Postnr;Ort;Kommunkod;Projekt;Laboratorium;Provtyp;Provtagare;Registertyp;ProvplatsID;Provplatsnamn;Specifik provplats;Provtagningsorsak;Provtyp;Provtypspecifikation;Bedömning;Kemisk bedömning;Mikrobiologisk bedömning;Kommentar;År;Provtagningsdatum;Provtagningstid;Inlämningsdatum;Inlämningstid;",
                    u"DM-990908-2773;MFR;PG Vejdes väg 15;351 96;Växjö;0780;Demoproj;Demo-Laboratoriet;NSG;DV;;Demo1 vattenverk;;Föreskriven regelbunden undersökning enligt SLVFS 2001:30;Dricksvatten enligt SLVFS 2001:30;Utgående;Nej;Tjänligt;;;;2010;2010-09-07;10:15;2010-09-07;14:15;",
                    u"#Provdat",
                    u"Lablittera;Metodbeteckning;Parameter;Mätvärdetext;Mätvärdetal;Mätvärdetalanm;Enhet;Rapporteringsgräns;Detektionsgräns;Mätosäkerhet;Mätvärdespår;Parameterbedömning;Kommentar;",
                    u"DM-990908-2773;SS-EN ISO 7887-1/4;Färgtal;;5;;mg/l Pt;;;;;;;",
                    u"DM-990908-2773;ISO 17294-2;Järn;;0,06;;mg/l;;;;;;;",
                    u"DM-990908-2773;Saknas;Temperatur vid provtagning;;14,5;;grader C;;;;;;;",
                    u"DM-990908-2773;SLV METOD1990-01-01 TA;Temperatur vid ankomst;;16,8;;grader C;;;;;;Ej kylt;",
                    u"DM-990908-2773;ISO 17294-2;Mangan;;0,001;<;mg/l;;;;;;;",
                    u"#Provadm ",
                    u"Lablittera;Namn;Adress;Postnr;Ort;Kommunkod;Projekt;Laboratorium;Provtyp;Provtagare;Registertyp;ProvplatsID;Provplatsnamn;Specifik provplats;Provtagningsorsak;Provtyp;Provtypspecifikation;Bedömning;Kemisk bedömning;Mikrobiologisk bedömning;Kommentar;År;Provtagningsdatum;Provtagningstid;Inlämningsdatum;Inlämningstid;",
                    u"DM-990908-2774;MFR;;;;;;Demo-Laboratoriet;NSG;DV;VV1784;Demo2 vattenverk;;Föreskriven regelbunden undersökning enligt SLVFS 2001:30;Dricksvatten enligt SLVFS 2001:30;Utgående;Nej;Tjänligt;;;;2010;2010-09-07;11:30;2010-09-07;14:15;",
                    u"#Provdat",
                    u"Lablittera;Metodbeteckning;Parameter;Mätvärdetext;Mätvärdetal;Mätvärdetalanm;Enhet;Rapporteringsgräns;Detektionsgräns;Mätosäkerhet;Mätvärdespår;Parameterbedömning;Kommentar;",
                    u"DM-990908-2774;SS-EN ISO 7887-1/4;Färgtal;;6,5;;mg/l Pt;;;;;;;",
                    u"DM-990908-2774;ISO 17294-2;Järn;;0,05;<;mg/l;;;;;;;",
                    u"DM-990908-2774;Saknas;Temperatur vid provtagning;;14,8;;grader C;;;;;;;",
                    u"DM-990908-2774;Saknas;Temperatur vid ankomst;;17,3;;grader C;;;;;;Ej kylt;",
                    u"DM-990908-2774;ISO 17294-2;Mangan;;0,004;;mg/l;;;;;;; ",
                    u"#Slut"
                        )

        with utils.tempinput(u'\n'.join(interlab4_lines), 'utf-16') as testfile:
            result = self.importinstance.parse_interlab4([testfile])
        result_string = ';'.join(utils_for_tests.dict_to_sorted_list(self.importinstance.parse_interlab4([testfile])))
        reference_string = 'DM-990908-2773;Färgtal;enhet;mg/l Pt;lablittera;DM-990908-2773;metodbeteckning;SS-EN ISO 7887-1/4;mätvärdetal;5;parameter;Färgtal;Järn;enhet;mg/l;lablittera;DM-990908-2773;metodbeteckning;ISO 17294-2;mätvärdetal;0.06;parameter;Järn;Mangan;enhet;mg/l;lablittera;DM-990908-2773;metodbeteckning;ISO 17294-2;mätvärdetal;0.001;mätvärdetalanm;<;parameter;Mangan;Temperatur vid ankomst;enhet;grader C;kommentar;Ej kylt;lablittera;DM-990908-2773;metodbeteckning;SLV METOD1990-01-01 TA;mätvärdetal;16.8;parameter;Temperatur vid ankomst;Temperatur vid provtagning;enhet;grader C;lablittera;DM-990908-2773;metodbeteckning;Saknas;mätvärdetal;14.5;parameter;Temperatur vid provtagning;metadata;adress;PG Vejdes väg 15;bedömning;Tjänligt;inlämningsdatum;2010-09-07;inlämningstid;14:15;kommunkod;0780;lablittera;DM-990908-2773;laboratorium;Demo-Laboratoriet;namn;MFR;ort;Växjö;postnr;351 96;projekt;Demoproj;provplatsid;Demo1 vattenverk;provtagare;DV;provtagningsdatum;2010-09-07;provtagningsorsak;Dricksvatten enligt SLVFS 2001:30;provtagningstid;10:15;provtyp;Utgående;provtypspecifikation;Nej;specifik provplats;Föreskriven regelbunden undersökning enligt SLVFS 2001:30;år;2010;DM-990908-2774;Färgtal;enhet;mg/l Pt;lablittera;DM-990908-2774;metodbeteckning;SS-EN ISO 7887-1/4;mätvärdetal;6.5;parameter;Färgtal;Järn;enhet;mg/l;lablittera;DM-990908-2774;metodbeteckning;ISO 17294-2;mätvärdetal;0.05;mätvärdetalanm;<;parameter;Järn;Mangan;enhet;mg/l;lablittera;DM-990908-2774;metodbeteckning;ISO 17294-2;mätvärdetal;0.004;parameter;Mangan;Temperatur vid ankomst;enhet;grader C;kommentar;Ej kylt;lablittera;DM-990908-2774;metodbeteckning;Saknas;mätvärdetal;17.3;parameter;Temperatur vid ankomst;Temperatur vid provtagning;enhet;grader C;lablittera;DM-990908-2774;metodbeteckning;Saknas;mätvärdetal;14.8;parameter;Temperatur vid provtagning;metadata;bedömning;Tjänligt;inlämningsdatum;2010-09-07;inlämningstid;14:15;lablittera;DM-990908-2774;laboratorium;Demo-Laboratoriet;namn;MFR;provplatsid;Demo2 vattenverk;provtagare;DV;provtagningsdatum;2010-09-07;provtagningsorsak;Dricksvatten enligt SLVFS 2001:30;provtagningstid;11:30;provtyp;Utgående;provtypspecifikation;Nej;registertyp;VV1784;specifik provplats;Föreskriven regelbunden undersökning enligt SLVFS 2001:30;år;2010'

        assert result_string == reference_string

    def test_parse_interlab4_iso_8859_1(self):

        interlab4_lines = (
                    u"#Interlab",
                    u"#Version=4.0",
                    u"#Tecken=ISO-8859-1",
                    u"#Textavgränsare=Nej",
                    u"#Decimaltecken=,",
                    u"#Provadm",
                    u"Lablittera;Namn;Adress;Postnr;Ort;Kommunkod;Projekt;Laboratorium;Provtyp;Provtagare;Registertyp;ProvplatsID;Provplatsnamn;Specifik provplats;Provtagningsorsak;Provtyp;Provtypspecifikation;Bedömning;Kemisk bedömning;Mikrobiologisk bedömning;Kommentar;År;Provtagningsdatum;Provtagningstid;Inlämningsdatum;Inlämningstid;",
                    u"DM-990908-2773;MFR;PG Vejdes väg 15;351 96;Växjö;0780;Demoproj;Demo-Laboratoriet;NSG;DV;;Demo1 vattenverk;;Föreskriven regelbunden undersökning enligt SLVFS 2001:30;Dricksvatten enligt SLVFS 2001:30;Utgående;Nej;Tjänligt;;;;2010;2010-09-07;10:15;2010-09-07;14:15;",
                    u"#Provdat",
                    u"Lablittera;Metodbeteckning;Parameter;Mätvärdetext;Mätvärdetal;Mätvärdetalanm;Enhet;Rapporteringsgräns;Detektionsgräns;Mätosäkerhet;Mätvärdespår;Parameterbedömning;Kommentar;",
                    u"DM-990908-2773;SS-EN ISO 7887-1/4;Färgtal;;5;;mg/l Pt;;;;;;;",
                    u"DM-990908-2773;ISO 17294-2;Järn;;0,06;;mg/l;;;;;;;",
                    u"DM-990908-2773;Saknas;Temperatur vid provtagning;;14,5;;grader C;;;;;;;",
                    u"DM-990908-2773;SLV METOD1990-01-01 TA;Temperatur vid ankomst;;16,8;;grader C;;;;;;Ej kylt;",
                    u"DM-990908-2773;ISO 17294-2;Mangan;;0,001;<;mg/l;;;;;;;",
                    u"#Provadm ",
                    u"Lablittera;Namn;Adress;Postnr;Ort;Kommunkod;Projekt;Laboratorium;Provtyp;Provtagare;Registertyp;ProvplatsID;Provplatsnamn;Specifik provplats;Provtagningsorsak;Provtyp;Provtypspecifikation;Bedömning;Kemisk bedömning;Mikrobiologisk bedömning;Kommentar;År;Provtagningsdatum;Provtagningstid;Inlämningsdatum;Inlämningstid;",
                    u"DM-990908-2774;MFR;;;;;;Demo-Laboratoriet;NSG;DV;VV1784;Demo2 vattenverk;;Föreskriven regelbunden undersökning enligt SLVFS 2001:30;Dricksvatten enligt SLVFS 2001:30;Utgående;Nej;Tjänligt;;;;2010;2010-09-07;11:30;2010-09-07;14:15;",
                    u"#Provdat",
                    u"Lablittera;Metodbeteckning;Parameter;Mätvärdetext;Mätvärdetal;Mätvärdetalanm;Enhet;Rapporteringsgräns;Detektionsgräns;Mätosäkerhet;Mätvärdespår;Parameterbedömning;Kommentar;",
                    u"DM-990908-2774;SS-EN ISO 7887-1/4;Färgtal;;6,5;;mg/l Pt;;;;;;;",
                    u"DM-990908-2774;ISO 17294-2;Järn;;0,05;<;mg/l;;;;;;;",
                    u"DM-990908-2774;Saknas;Temperatur vid provtagning;;14,8;;grader C;;;;;;;",
                    u"DM-990908-2774;Saknas;Temperatur vid ankomst;;17,3;;grader C;;;;;;Ej kylt;",
                    u"DM-990908-2774;ISO 17294-2;Mangan;;0,004;;mg/l;;;;;;; ",
                    u"#Slut"
                        )

        with utils.tempinput(u'\n'.join(interlab4_lines), 'iso-8859-1') as testfile:
            result = self.importinstance.parse_interlab4([testfile])
        result_string = ';'.join(utils_for_tests.dict_to_sorted_list(self.importinstance.parse_interlab4([testfile])))
        reference_string = 'DM-990908-2773;Färgtal;enhet;mg/l Pt;lablittera;DM-990908-2773;metodbeteckning;SS-EN ISO 7887-1/4;mätvärdetal;5;parameter;Färgtal;Järn;enhet;mg/l;lablittera;DM-990908-2773;metodbeteckning;ISO 17294-2;mätvärdetal;0.06;parameter;Järn;Mangan;enhet;mg/l;lablittera;DM-990908-2773;metodbeteckning;ISO 17294-2;mätvärdetal;0.001;mätvärdetalanm;<;parameter;Mangan;Temperatur vid ankomst;enhet;grader C;kommentar;Ej kylt;lablittera;DM-990908-2773;metodbeteckning;SLV METOD1990-01-01 TA;mätvärdetal;16.8;parameter;Temperatur vid ankomst;Temperatur vid provtagning;enhet;grader C;lablittera;DM-990908-2773;metodbeteckning;Saknas;mätvärdetal;14.5;parameter;Temperatur vid provtagning;metadata;adress;PG Vejdes väg 15;bedömning;Tjänligt;inlämningsdatum;2010-09-07;inlämningstid;14:15;kommunkod;0780;lablittera;DM-990908-2773;laboratorium;Demo-Laboratoriet;namn;MFR;ort;Växjö;postnr;351 96;projekt;Demoproj;provplatsid;Demo1 vattenverk;provtagare;DV;provtagningsdatum;2010-09-07;provtagningsorsak;Dricksvatten enligt SLVFS 2001:30;provtagningstid;10:15;provtyp;Utgående;provtypspecifikation;Nej;specifik provplats;Föreskriven regelbunden undersökning enligt SLVFS 2001:30;år;2010;DM-990908-2774;Färgtal;enhet;mg/l Pt;lablittera;DM-990908-2774;metodbeteckning;SS-EN ISO 7887-1/4;mätvärdetal;6.5;parameter;Färgtal;Järn;enhet;mg/l;lablittera;DM-990908-2774;metodbeteckning;ISO 17294-2;mätvärdetal;0.05;mätvärdetalanm;<;parameter;Järn;Mangan;enhet;mg/l;lablittera;DM-990908-2774;metodbeteckning;ISO 17294-2;mätvärdetal;0.004;parameter;Mangan;Temperatur vid ankomst;enhet;grader C;kommentar;Ej kylt;lablittera;DM-990908-2774;metodbeteckning;Saknas;mätvärdetal;17.3;parameter;Temperatur vid ankomst;Temperatur vid provtagning;enhet;grader C;lablittera;DM-990908-2774;metodbeteckning;Saknas;mätvärdetal;14.8;parameter;Temperatur vid provtagning;metadata;bedömning;Tjänligt;inlämningsdatum;2010-09-07;inlämningstid;14:15;lablittera;DM-990908-2774;laboratorium;Demo-Laboratoriet;namn;MFR;provplatsid;Demo2 vattenverk;provtagare;DV;provtagningsdatum;2010-09-07;provtagningsorsak;Dricksvatten enligt SLVFS 2001:30;provtagningstid;11:30;provtyp;Utgående;provtypspecifikation;Nej;registertyp;VV1784;specifik provplats;Föreskriven regelbunden undersökning enligt SLVFS 2001:30;år;2010'

        assert result_string == reference_string

    def test_parse_interlab4_utf8(self):
        interlab4_lines = (
                    u"#Interlab",
                    u"#Version=4.0",
                    u"#Tecken=UTF-8",
                    u"#Textavgränsare=Nej",
                    u"#Decimaltecken=,",
                    u"#Provadm",
                    u"Lablittera;Namn;Adress;Postnr;Ort;Kommunkod;Projekt;Laboratorium;Provtyp;Provtagare;Registertyp;ProvplatsID;Provplatsnamn;Specifik provplats;Provtagningsorsak;Provtyp;Provtypspecifikation;Bedömning;Kemisk bedömning;Mikrobiologisk bedömning;Kommentar;År;Provtagningsdatum;Provtagningstid;Inlämningsdatum;Inlämningstid;",
                    u"DM-990908-2773;MFR;PG Vejdes väg 15;351 96;Växjö;0780;Demoproj;Demo-Laboratoriet;NSG;DV;;Demo1 vattenverk;;Föreskriven regelbunden undersökning enligt SLVFS 2001:30;Dricksvatten enligt SLVFS 2001:30;Utgående;Nej;Tjänligt;;;;2010;2010-09-07;10:15;2010-09-07;14:15;",
                    u"#Provdat",
                    u"Lablittera;Metodbeteckning;Parameter;Mätvärdetext;Mätvärdetal;Mätvärdetalanm;Enhet;Rapporteringsgräns;Detektionsgräns;Mätosäkerhet;Mätvärdespår;Parameterbedömning;Kommentar;",
                    u"DM-990908-2773;SS-EN ISO 7887-1/4;Färgtal;;5;;mg/l Pt;;;;;;;",
                    u"DM-990908-2773;ISO 17294-2;Järn;;0,06;;mg/l;;;;;;;",
                    u"DM-990908-2773;Saknas;Temperatur vid provtagning;;14,5;;grader C;;;;;;;",
                    u"DM-990908-2773;SLV METOD1990-01-01 TA;Temperatur vid ankomst;;16,8;;grader C;;;;;;Ej kylt;",
                    u"DM-990908-2773;ISO 17294-2;Mangan;;0,001;<;mg/l;;;;;;;",
                    u"#Provadm ",
                    u"Lablittera;Namn;Adress;Postnr;Ort;Kommunkod;Projekt;Laboratorium;Provtyp;Provtagare;Registertyp;ProvplatsID;Provplatsnamn;Specifik provplats;Provtagningsorsak;Provtyp;Provtypspecifikation;Bedömning;Kemisk bedömning;Mikrobiologisk bedömning;Kommentar;År;Provtagningsdatum;Provtagningstid;Inlämningsdatum;Inlämningstid;",
                    u"DM-990908-2774;MFR;;;;;;Demo-Laboratoriet;NSG;DV;VV1784;Demo2 vattenverk;;Föreskriven regelbunden undersökning enligt SLVFS 2001:30;Dricksvatten enligt SLVFS 2001:30;Utgående;Nej;Tjänligt;;;;2010;2010-09-07;11:30;2010-09-07;14:15;",
                    u"#Provdat",
                    u"Lablittera;Metodbeteckning;Parameter;Mätvärdetext;Mätvärdetal;Mätvärdetalanm;Enhet;Rapporteringsgräns;Detektionsgräns;Mätosäkerhet;Mätvärdespår;Parameterbedömning;Kommentar;",
                    u"DM-990908-2774;SS-EN ISO 7887-1/4;Färgtal;;6,5;;mg/l Pt;;;;;;;",
                    u"DM-990908-2774;ISO 17294-2;Järn;;0,05;<;mg/l;;;;;;;",
                    u"DM-990908-2774;Saknas;Temperatur vid provtagning;;14,8;;grader C;;;;;;;",
                    u"DM-990908-2774;Saknas;Temperatur vid ankomst;;17,3;;grader C;;;;;;Ej kylt;",
                    u"DM-990908-2774;ISO 17294-2;Mangan;;0,004;;mg/l;;;;;;; ",
                    u"#Slut"
                        )

        with utils.tempinput(u'\n'.join(interlab4_lines), 'utf-8') as testfile:
            result = self.importinstance.parse_interlab4([testfile])
        result_string = ';'.join(utils_for_tests.dict_to_sorted_list(self.importinstance.parse_interlab4([testfile])))
        reference_string = 'DM-990908-2773;Färgtal;enhet;mg/l Pt;lablittera;DM-990908-2773;metodbeteckning;SS-EN ISO 7887-1/4;mätvärdetal;5;parameter;Färgtal;Järn;enhet;mg/l;lablittera;DM-990908-2773;metodbeteckning;ISO 17294-2;mätvärdetal;0.06;parameter;Järn;Mangan;enhet;mg/l;lablittera;DM-990908-2773;metodbeteckning;ISO 17294-2;mätvärdetal;0.001;mätvärdetalanm;<;parameter;Mangan;Temperatur vid ankomst;enhet;grader C;kommentar;Ej kylt;lablittera;DM-990908-2773;metodbeteckning;SLV METOD1990-01-01 TA;mätvärdetal;16.8;parameter;Temperatur vid ankomst;Temperatur vid provtagning;enhet;grader C;lablittera;DM-990908-2773;metodbeteckning;Saknas;mätvärdetal;14.5;parameter;Temperatur vid provtagning;metadata;adress;PG Vejdes väg 15;bedömning;Tjänligt;inlämningsdatum;2010-09-07;inlämningstid;14:15;kommunkod;0780;lablittera;DM-990908-2773;laboratorium;Demo-Laboratoriet;namn;MFR;ort;Växjö;postnr;351 96;projekt;Demoproj;provplatsid;Demo1 vattenverk;provtagare;DV;provtagningsdatum;2010-09-07;provtagningsorsak;Dricksvatten enligt SLVFS 2001:30;provtagningstid;10:15;provtyp;Utgående;provtypspecifikation;Nej;specifik provplats;Föreskriven regelbunden undersökning enligt SLVFS 2001:30;år;2010;DM-990908-2774;Färgtal;enhet;mg/l Pt;lablittera;DM-990908-2774;metodbeteckning;SS-EN ISO 7887-1/4;mätvärdetal;6.5;parameter;Färgtal;Järn;enhet;mg/l;lablittera;DM-990908-2774;metodbeteckning;ISO 17294-2;mätvärdetal;0.05;mätvärdetalanm;<;parameter;Järn;Mangan;enhet;mg/l;lablittera;DM-990908-2774;metodbeteckning;ISO 17294-2;mätvärdetal;0.004;parameter;Mangan;Temperatur vid ankomst;enhet;grader C;kommentar;Ej kylt;lablittera;DM-990908-2774;metodbeteckning;Saknas;mätvärdetal;17.3;parameter;Temperatur vid ankomst;Temperatur vid provtagning;enhet;grader C;lablittera;DM-990908-2774;metodbeteckning;Saknas;mätvärdetal;14.8;parameter;Temperatur vid provtagning;metadata;bedömning;Tjänligt;inlämningsdatum;2010-09-07;inlämningstid;14:15;lablittera;DM-990908-2774;laboratorium;Demo-Laboratoriet;namn;MFR;provplatsid;Demo2 vattenverk;provtagare;DV;provtagningsdatum;2010-09-07;provtagningsorsak;Dricksvatten enligt SLVFS 2001:30;provtagningstid;11:30;provtyp;Utgående;provtypspecifikation;Nej;registertyp;VV1784;specifik provplats;Föreskriven regelbunden undersökning enligt SLVFS 2001:30;år;2010'

        assert result_string == reference_string

    def test_parse_interlab4_ignore_bland_line(self):
        interlab4_lines = (
                    u"#Interlab",
                    u"#Version=4.0",
                    u"#Tecken=UTF-8",
                    u"#Textavgränsare=Nej",
                    u"#Decimaltecken=,",
                    u"#Provadm",
                    u"Lablittera;Namn;Adress;Postnr;Ort;Kommunkod;Projekt;Laboratorium;Provtyp;Provtagare;Registertyp;ProvplatsID;Provplatsnamn;Specifik provplats;Provtagningsorsak;Provtyp;Provtypspecifikation;Bedömning;Kemisk bedömning;Mikrobiologisk bedömning;Kommentar;År;Provtagningsdatum;Provtagningstid;Inlämningsdatum;Inlämningstid;",
                    u"DM-990908-2773;MFR;PG Vejdes väg 15;351 96;Växjö;0780;Demoproj;Demo-Laboratoriet;NSG;DV;;Demo1 vattenverk;;Föreskriven regelbunden undersökning enligt SLVFS 2001:30;Dricksvatten enligt SLVFS 2001:30;Utgående;Nej;Tjänligt;;;;2010;2010-09-07;10:15;2010-09-07;14:15;",
                    u"#Provdat",
                    u"Lablittera;Metodbeteckning;Parameter;Mätvärdetext;Mätvärdetal;Mätvärdetalanm;Enhet;Rapporteringsgräns;Detektionsgräns;Mätosäkerhet;Mätvärdespår;Parameterbedömning;Kommentar;",
                    u"DM-990908-2773;SS-EN ISO 7887-1/4;Färgtal;;5;;mg/l Pt;;;;;;;",
                    u"DM-990908-2773;ISO 17294-2;Järn;;0,06;;mg/l;;;;;;;",
                    u"DM-990908-2773;Saknas;Temperatur vid provtagning;;14,5;;grader C;;;;;;;",
                    u"DM-990908-2773;SLV METOD1990-01-01 TA;Temperatur vid ankomst;;16,8;;grader C;;;;;;Ej kylt;",
                    u"DM-990908-2773;ISO 17294-2;Mangan;;0,001;<;mg/l;;;;;;;",
                    u"#Provadm ",
                    u"Lablittera;Namn;Adress;Postnr;Ort;Kommunkod;Projekt;Laboratorium;Provtyp;Provtagare;Registertyp;ProvplatsID;Provplatsnamn;Specifik provplats;Provtagningsorsak;Provtyp;Provtypspecifikation;Bedömning;Kemisk bedömning;Mikrobiologisk bedömning;Kommentar;År;Provtagningsdatum;Provtagningstid;Inlämningsdatum;Inlämningstid;",
                    u"DM-990908-2774;MFR;;;;;;Demo-Laboratoriet;NSG;DV;VV1784;Demo2 vattenverk;;Föreskriven regelbunden undersökning enligt SLVFS 2001:30;Dricksvatten enligt SLVFS 2001:30;Utgående;Nej;Tjänligt;;;;2010;2010-09-07;11:30;2010-09-07;14:15;",
                    u"#Provdat",
                    u'',
                    u"Lablittera;Metodbeteckning;Parameter;Mätvärdetext;Mätvärdetal;Mätvärdetalanm;Enhet;Rapporteringsgräns;Detektionsgräns;Mätosäkerhet;Mätvärdespår;Parameterbedömning;Kommentar;",
                    u"DM-990908-2774;SS-EN ISO 7887-1/4;Färgtal;;6,5;;mg/l Pt;;;;;;;",
                    u"DM-990908-2774;ISO 17294-2;Järn;;0,05;<;mg/l;;;;;;;",
                    u"DM-990908-2774;Saknas;Temperatur vid provtagning;;14,8;;grader C;;;;;;;",
                    u"DM-990908-2774;Saknas;Temperatur vid ankomst;;17,3;;grader C;;;;;;Ej kylt;",
                    u"DM-990908-2774;ISO 17294-2;Mangan;;0,004;;mg/l;;;;;;; ",
                    u"#Slut"
                        )

        with utils.tempinput(u'\n'.join(interlab4_lines), 'utf-8') as testfile:
            result = self.importinstance.parse_interlab4([testfile])
        result_string = ';'.join(utils_for_tests.dict_to_sorted_list(self.importinstance.parse_interlab4([testfile])))
        reference_string = 'DM-990908-2773;Färgtal;enhet;mg/l Pt;lablittera;DM-990908-2773;metodbeteckning;SS-EN ISO 7887-1/4;mätvärdetal;5;parameter;Färgtal;Järn;enhet;mg/l;lablittera;DM-990908-2773;metodbeteckning;ISO 17294-2;mätvärdetal;0.06;parameter;Järn;Mangan;enhet;mg/l;lablittera;DM-990908-2773;metodbeteckning;ISO 17294-2;mätvärdetal;0.001;mätvärdetalanm;<;parameter;Mangan;Temperatur vid ankomst;enhet;grader C;kommentar;Ej kylt;lablittera;DM-990908-2773;metodbeteckning;SLV METOD1990-01-01 TA;mätvärdetal;16.8;parameter;Temperatur vid ankomst;Temperatur vid provtagning;enhet;grader C;lablittera;DM-990908-2773;metodbeteckning;Saknas;mätvärdetal;14.5;parameter;Temperatur vid provtagning;metadata;adress;PG Vejdes väg 15;bedömning;Tjänligt;inlämningsdatum;2010-09-07;inlämningstid;14:15;kommunkod;0780;lablittera;DM-990908-2773;laboratorium;Demo-Laboratoriet;namn;MFR;ort;Växjö;postnr;351 96;projekt;Demoproj;provplatsid;Demo1 vattenverk;provtagare;DV;provtagningsdatum;2010-09-07;provtagningsorsak;Dricksvatten enligt SLVFS 2001:30;provtagningstid;10:15;provtyp;Utgående;provtypspecifikation;Nej;specifik provplats;Föreskriven regelbunden undersökning enligt SLVFS 2001:30;år;2010;DM-990908-2774;Färgtal;enhet;mg/l Pt;lablittera;DM-990908-2774;metodbeteckning;SS-EN ISO 7887-1/4;mätvärdetal;6.5;parameter;Färgtal;Järn;enhet;mg/l;lablittera;DM-990908-2774;metodbeteckning;ISO 17294-2;mätvärdetal;0.05;mätvärdetalanm;<;parameter;Järn;Mangan;enhet;mg/l;lablittera;DM-990908-2774;metodbeteckning;ISO 17294-2;mätvärdetal;0.004;parameter;Mangan;Temperatur vid ankomst;enhet;grader C;kommentar;Ej kylt;lablittera;DM-990908-2774;metodbeteckning;Saknas;mätvärdetal;17.3;parameter;Temperatur vid ankomst;Temperatur vid provtagning;enhet;grader C;lablittera;DM-990908-2774;metodbeteckning;Saknas;mätvärdetal;14.8;parameter;Temperatur vid provtagning;metadata;bedömning;Tjänligt;inlämningsdatum;2010-09-07;inlämningstid;14:15;lablittera;DM-990908-2774;laboratorium;Demo-Laboratoriet;namn;MFR;provplatsid;Demo2 vattenverk;provtagare;DV;provtagningsdatum;2010-09-07;provtagningsorsak;Dricksvatten enligt SLVFS 2001:30;provtagningstid;11:30;provtyp;Utgående;provtypspecifikation;Nej;registertyp;VV1784;specifik provplats;Föreskriven regelbunden undersökning enligt SLVFS 2001:30;år;2010'

        assert result_string == reference_string

    def test_parse_interlab4_quotechar(self):
        interlab4_lines = (
                    u'#Interlab',
                    u'#Version=4.0',
                    u'#Tecken=UTF-8',
                    u'#Textavgränsare=Ja',
                    u'#Decimaltecken=,',
                    u'#Provadm',
                    u'"Lablittera";"Namn";"Adress";"Postnr";"Ort";',
                    u'"DM-990908-2773";"MFR";"PG Vejdes väg 15";"351 96";"Växjö";',
                    u'#Provdat',
                    u'"Lablittera";"Metodbeteckning";"Parameter";"Mätvärdetext";"Mätvärdetal";',
                    u'"DM-990908-2773";"SS-EN ISO 7887-1/4";"Färgtal";;"5";',
                    u'#Slut'
                        )

        with utils.tempinput(u'\n'.join(interlab4_lines), 'utf-8') as testfile:
            result = self.importinstance.parse_interlab4([testfile])
        result_string = ';'.join(utils_for_tests.dict_to_sorted_list(self.importinstance.parse_interlab4([testfile])))
        reference_string = 'DM-990908-2773;Färgtal;lablittera;DM-990908-2773;metodbeteckning;SS-EN ISO 7887-1/4;mätvärdetal;5;parameter;Färgtal;metadata;adress;PG Vejdes väg 15;lablittera;DM-990908-2773;namn;MFR;ort;Växjö;postnr;351 96'
        assert result_string == reference_string

    def test_parse_interlab4_quotechar_semicolon(self):
        interlab4_lines = (
                    u'#Interlab',
                    u'#Version=4.0',
                    u'#Tecken=UTF-8',
                    u'#Textavgränsare=Ja',
                    u'#Decimaltecken=,',
                    u'#Provadm',
                    u'"Lablittera";"Namn";"Adress";"Postnr";"Ort";',
                    u'"DM-990908-2773";"MFR";"PG ;Vejdes väg 15";"351 96";"Växjö";',
                    u'#Provdat',
                    u'"Lablittera";"Metodbeteckning";"Parameter";"Mätvärdetext";"Mätvärdetal";',
                    u'"DM-990908-2773";"SS-EN ISO 7887-1/4";"Färgtal";;"5";',
                    u'#Slut'
                        )

        with utils.tempinput(u'\n'.join(interlab4_lines), 'utf-8') as testfile:
            result = self.importinstance.parse_interlab4([testfile])
        result_string = '|'.join(utils_for_tests.dict_to_sorted_list(self.importinstance.parse_interlab4([testfile])))
        reference_string = 'DM-990908-2773|Färgtal|lablittera|DM-990908-2773|metodbeteckning|SS-EN ISO 7887-1/4|mätvärdetal|5|parameter|Färgtal|metadata|adress|PG ;Vejdes väg 15|lablittera|DM-990908-2773|namn|MFR|ort|Växjö|postnr|351 96'

        assert result_string == reference_string

    def test_interlab4_to_table(self):
        interlab4_lines = (
            u'#Interlab',
            u'#Version=4.0',
            u'#Tecken=UTF-8',
            u'#Textavgränsare=Nej',
            u'#Decimaltecken=,',
            u'#Provadm',
            u'Lablittera;Namn;Adress;Postnr;Ort;Kommunkod;Projekt;Laboratorium;Provtyp;Provtagare;Registertyp;ProvplatsID;Provplatsnamn;Specifik provplats;Provtagningsorsak;Provtyp;Provtypspecifikation;Bedömning;Kemisk bedömning;Mikrobiologisk bedömning;Kommentar;År;Provtagningsdatum;Provtagningstid;Inlämningsdatum;Inlämningstid;',
            u'DM-990908-2773;MFR;PG Vejdes väg 15;351 96;Växjö;0780;Demoproj;Demo-Laboratoriet;NSG;DV;;Demo1 vattenverk;;Föreskriven regelbunden undersökning enligt SLVFS 2001:30;Dricksvatten enligt SLVFS 2001:30;Utgående;Nej;Tjänligt;;;;2010;2010-09-07;10:15;2010-09-07;14:15;',
            u'#Provdat',
            u'Lablittera;Metodbeteckning;Parameter;Mätvärdetext;Mätvärdetal;Mätvärdetalanm;Enhet;Rapporteringsgräns;Detektionsgräns;Mätosäkerhet;Mätvärdespår;Parameterbedömning;Kommentar;',
            u'DM-990908-2773;SS-EN ISO 7887-1/4;Färgtal;;5;;mg/l Pt;;;;;;;',
            u'#Slut'
                )

        with utils.tempinput(u'\n'.join(interlab4_lines), 'utf-8') as testfile:
            parsed_result = self.importinstance.parse_interlab4([testfile])

        result_string = utils_for_tests.create_test_string(self.importinstance.interlab4_to_table(parsed_result))

        # "obsid, depth, report, project, staff, date_time, anameth, parameter, reading_num, reading_txt, unit, comment"
        reference_string = u'[[obsid, depth, report, project, staff, date_time, anameth, parameter, reading_num, reading_txt, unit, comment], [Demo1 vattenverk Föreskriven regelbunden undersökning enligt SLVFS 2001:30, None, DM-990908-2773, Demoproj, DV, 2010-09-07 10:15:00, SS-EN ISO 7887-1/4, Färgtal, 5, 5, mg/l Pt, provtagningsorsak: Dricksvatten enligt SLVFS 2001:30. provtyp: Utgående. provtypspecifikation: Nej. bedömning: Tjänligt]]'

        assert result_string == reference_string

    def test_interlab4_to_table_kalium_above_2_5(self):
        interlab4_lines = (
            u'#Interlab',
            u'#Version=4.0',
            u'#Tecken=UTF-8',
            u'#Textavgränsare=Nej',
            u'#Decimaltecken=,',
            u'#Provadm',
            u'Lablittera;Namn;Adress;Postnr;Ort;Kommunkod;Projekt;Laboratorium;Provtyp;Provtagare;Registertyp;ProvplatsID;Provplatsnamn;Specifik provplats;Provtagningsorsak;Provtyp;Provtypspecifikation;Bedömning;Kemisk bedömning;Mikrobiologisk bedömning;Kommentar;År;Provtagningsdatum;Provtagningstid;Inlämningsdatum;Inlämningstid;',
            u'DM-990908-2773;MFR;PG Vejdes väg 15;351 96;Växjö;0780;Demoproj;Demo-Laboratoriet;NSG;DV;;Demo1 vattenverk;;Föreskriven regelbunden undersökning enligt SLVFS 2001:30;Dricksvatten enligt SLVFS 2001:30;Utgående;Nej;Tjänligt;;;;2010;2010-09-07;10:15;2010-09-07;14:15;',
            u'#Provdat',
            u'Lablittera;Metodbeteckning;Parameter;Mätvärdetext;Mätvärdetal;Mätvärdetalanm;Enhet;Rapporteringsgräns;Detektionsgräns;Mätosäkerhet;Mätvärdespår;Parameterbedömning;Kommentar;',
            u'DM-990908-2773;SS-EN ISO 7887-1/4;Kalium;5;5;;mg/l Pt;;;;;;;',
            u'DM-990908-2773;SS-EN ISO 7887-1/4;Kalium;4;4;;mg/l Pt;;;;;;;',
            u'#Slut'
                )

        with utils.tempinput(u'\n'.join(interlab4_lines), 'utf-8') as testfile:
            parsed_result = self.importinstance.parse_interlab4([testfile])

        result_string = utils_for_tests.create_test_string(self.importinstance.interlab4_to_table(parsed_result))

        # "obsid, depth, report, project, staff, date_time, anameth, parameter, reading_num, reading_txt, unit, comment"
        reference_string = u'[[obsid, depth, report, project, staff, date_time, anameth, parameter, reading_num, reading_txt, unit, comment], [Demo1 vattenverk Föreskriven regelbunden undersökning enligt SLVFS 2001:30, None, DM-990908-2773, Demoproj, DV, 2010-09-07 10:15:00, SS-EN ISO 7887-1/4, Kalium, 4, 4, mg/l Pt, provtagningsorsak: Dricksvatten enligt SLVFS 2001:30. provtyp: Utgående. provtypspecifikation: Nej. bedömning: Tjänligt]]'
        assert result_string == reference_string

    def test_interlab4_to_table_kalium_between_1_and_2_5(self):
        interlab4_lines = (
            u'#Interlab',
            u'#Version=4.0',
            u'#Tecken=UTF-8',
            u'#Textavgränsare=Nej',
            u'#Decimaltecken=,',
            u'#Provadm',
            u'Lablittera;Namn;Adress;Postnr;Ort;Kommunkod;Projekt;Laboratorium;Provtyp;Provtagare;Registertyp;ProvplatsID;Provplatsnamn;Specifik provplats;Provtagningsorsak;Provtyp;Provtypspecifikation;Bedömning;Kemisk bedömning;Mikrobiologisk bedömning;Kommentar;År;Provtagningsdatum;Provtagningstid;Inlämningsdatum;Inlämningstid;',
            u'DM-990908-2773;MFR;PG Vejdes väg 15;351 96;Växjö;0780;Demoproj;Demo-Laboratoriet;NSG;DV;;Demo1 vattenverk;;Föreskriven regelbunden undersökning enligt SLVFS 2001:30;Dricksvatten enligt SLVFS 2001:30;Utgående;Nej;Tjänligt;;;;2010;2010-09-07;10:15;2010-09-07;14:15;',
            u'#Provdat',
            u'Lablittera;Metodbeteckning;Parameter;Mätvärdetext;Mätvärdetal;Mätvärdetalanm;Enhet;Rapporteringsgräns;Detektionsgräns;Mätosäkerhet;Mätvärdespår;Parameterbedömning;Kommentar;',
            u'DM-990908-2773;SS-EN ISO 7887-1/4;Kalium;<2,5;2,5;;mg/l Pt;;;;;;;',
            u'DM-990908-2773;SS-EN ISO 7887-1/4;Kalium;1,5;1,5;;mg/l Pt;;;;;;;',
            u'#Slut'
                )

        with utils.tempinput(u'\n'.join(interlab4_lines), 'utf-8') as testfile:
            parsed_result = self.importinstance.parse_interlab4([testfile])

        result_string = utils_for_tests.create_test_string(self.importinstance.interlab4_to_table(parsed_result))

        # "obsid, depth, report, project, staff, date_time, anameth, parameter, reading_num, reading_txt, unit, comment"
        reference_string = u'[[obsid, depth, report, project, staff, date_time, anameth, parameter, reading_num, reading_txt, unit, comment], [Demo1 vattenverk Föreskriven regelbunden undersökning enligt SLVFS 2001:30, None, DM-990908-2773, Demoproj, DV, 2010-09-07 10:15:00, SS-EN ISO 7887-1/4, Kalium, 1.5, 1,5, mg/l Pt, provtagningsorsak: Dricksvatten enligt SLVFS 2001:30. provtyp: Utgående. provtypspecifikation: Nej. bedömning: Tjänligt]]'
        assert result_string == reference_string

    def test_interlab4_to_table_kalium_below_1(self):
        interlab4_lines = (
            u'#Interlab',
            u'#Version=4.0',
            u'#Tecken=UTF-8',
            u'#Textavgränsare=Nej',
            u'#Decimaltecken=,',
            u'#Provadm',
            u'Lablittera;Namn;Adress;Postnr;Ort;Kommunkod;Projekt;Laboratorium;Provtyp;Provtagare;Registertyp;ProvplatsID;Provplatsnamn;Specifik provplats;Provtagningsorsak;Provtyp;Provtypspecifikation;Bedömning;Kemisk bedömning;Mikrobiologisk bedömning;Kommentar;År;Provtagningsdatum;Provtagningstid;Inlämningsdatum;Inlämningstid;',
            u'DM-990908-2773;MFR;PG Vejdes väg 15;351 96;Växjö;0780;Demoproj;Demo-Laboratoriet;NSG;DV;;Demo1 vattenverk;;Föreskriven regelbunden undersökning enligt SLVFS 2001:30;Dricksvatten enligt SLVFS 2001:30;Utgående;Nej;Tjänligt;;;;2010;2010-09-07;10:15;2010-09-07;14:15;',
            u'#Provdat',
            u'Lablittera;Metodbeteckning;Parameter;Mätvärdetext;Mätvärdetal;Mätvärdetalanm;Enhet;Rapporteringsgräns;Detektionsgräns;Mätosäkerhet;Mätvärdespår;Parameterbedömning;Kommentar;',
            u'DM-990908-2773;SS-EN ISO 7887-1/4;Kalium;<2,5;2,5;;mg/l Pt;;;;;;;',
            u'DM-990908-2773;SS-EN ISO 7887-1/4;Kalium;<1;1;;mg/l Pt;;;;;;;',
            u'#Slut'
                )

        with utils.tempinput(u'\n'.join(interlab4_lines), 'utf-8') as testfile:
            parsed_result = self.importinstance.parse_interlab4([testfile])

        result_string = utils_for_tests.create_test_string(self.importinstance.interlab4_to_table(parsed_result))

        # "obsid, depth, report, project, staff, date_time, anameth, parameter, reading_num, reading_txt, unit, comment"
        reference_string = u'[[obsid, depth, report, project, staff, date_time, anameth, parameter, reading_num, reading_txt, unit, comment], [Demo1 vattenverk Föreskriven regelbunden undersökning enligt SLVFS 2001:30, None, DM-990908-2773, Demoproj, DV, 2010-09-07 10:15:00, SS-EN ISO 7887-1/4, Kalium, 1, <1, mg/l Pt, provtagningsorsak: Dricksvatten enligt SLVFS 2001:30. provtyp: Utgående. provtypspecifikation: Nej. bedömning: Tjänligt]]'
        assert result_string == reference_string

    def test_interlab4_to_table_kalium_using_resolution(self):
        interlab4_lines = (
            u'#Interlab',
            u'#Version=4.0',
            u'#Tecken=UTF-8',
            u'#Textavgränsare=Nej',
            u'#Decimaltecken=,',
            u'#Provadm',
            u'Lablittera;Namn;Adress;Postnr;Ort;Kommunkod;Projekt;Laboratorium;Provtyp;Provtagare;Registertyp;ProvplatsID;Provplatsnamn;Specifik provplats;Provtagningsorsak;Provtyp;Provtypspecifikation;Bedömning;Kemisk bedömning;Mikrobiologisk bedömning;Kommentar;År;Provtagningsdatum;Provtagningstid;Inlämningsdatum;Inlämningstid;',
            u'DM-990908-2773;MFR;PG Vejdes väg 15;351 96;Växjö;0780;Demoproj;Demo-Laboratoriet;NSG;DV;;Demo1 vattenverk;;Föreskriven regelbunden undersökning enligt SLVFS 2001:30;Dricksvatten enligt SLVFS 2001:30;Utgående;Nej;Tjänligt;;;;2010;2010-09-07;10:15;2010-09-07;14:15;',
            u'#Provdat',
            u'Lablittera;Metodbeteckning;Parameter;Mätvärdetext;Mätvärdetal;Mätvärdetalanm;Enhet;Rapporteringsgräns;Detektionsgräns;Mätosäkerhet;Mätvärdespår;Parameterbedömning;Kommentar;',
            u'DM-990908-2773;SS-EN ISO 7887-1/4;Kalium;3;3;;mg/l Pt;;;±1;;;;',
            u'DM-990908-2773;SS-EN ISO 7887-1/4;Kalium;10;10;;mg/l Pt;;;±0.1;;;;',
            u'#Slut'
                )

        with utils.tempinput(u'\n'.join(interlab4_lines), 'utf-8') as testfile:
            parsed_result = self.importinstance.parse_interlab4([testfile])

        result_string = utils_for_tests.create_test_string(self.importinstance.interlab4_to_table(parsed_result))

        # "obsid, depth, report, project, staff, date_time, anameth, parameter, reading_num, reading_txt, unit, comment"
        reference_string = u'[[obsid, depth, report, project, staff, date_time, anameth, parameter, reading_num, reading_txt, unit, comment], [Demo1 vattenverk Föreskriven regelbunden undersökning enligt SLVFS 2001:30, None, DM-990908-2773, Demoproj, DV, 2010-09-07 10:15:00, SS-EN ISO 7887-1/4, Kalium, 10, 10, mg/l Pt, provtagningsorsak: Dricksvatten enligt SLVFS 2001:30. provtyp: Utgående. provtypspecifikation: Nej. bedömning: Tjänligt. mätosäkerhet: ±0.1]]'
        assert result_string == reference_string

    def test_interlab4_to_table_kalium_using_resolution_same_resolution_use_last_one(self):
        interlab4_lines = (
            u'#Interlab',
            u'#Version=4.0',
            u'#Tecken=UTF-8',
            u'#Textavgränsare=Nej',
            u'#Decimaltecken=,',
            u'#Provadm',
            u'Lablittera;Namn;Adress;Postnr;Ort;Kommunkod;Projekt;Laboratorium;Provtyp;Provtagare;Registertyp;ProvplatsID;Provplatsnamn;Specifik provplats;Provtagningsorsak;Provtyp;Provtypspecifikation;Bedömning;Kemisk bedömning;Mikrobiologisk bedömning;Kommentar;År;Provtagningsdatum;Provtagningstid;Inlämningsdatum;Inlämningstid;',
            u'DM-990908-2773;MFR;PG Vejdes väg 15;351 96;Växjö;0780;Demoproj;Demo-Laboratoriet;NSG;DV;;Demo1 vattenverk;;Föreskriven regelbunden undersökning enligt SLVFS 2001:30;Dricksvatten enligt SLVFS 2001:30;Utgående;Nej;Tjänligt;;;;2010;2010-09-07;10:15;2010-09-07;14:15;',
            u'#Provdat',
            u'Lablittera;Metodbeteckning;Parameter;Mätvärdetext;Mätvärdetal;Mätvärdetalanm;Enhet;Rapporteringsgräns;Detektionsgräns;Mätosäkerhet;Mätvärdespår;Parameterbedömning;Kommentar;',
            u'DM-990908-2773;SS-EN ISO 7887-1/4;Kalium;3;3;;mg/l Pt;;;±1;;;;',
            u'DM-990908-2773;SS-EN ISO 7887-1/4;Kalium;10;10;;mg/l Pt;;;±1;;;;',
            u'#Slut'
                )

        with utils.tempinput(u'\n'.join(interlab4_lines), 'utf-8') as testfile:
            parsed_result = self.importinstance.parse_interlab4([testfile])

        result_string = utils_for_tests.create_test_string(self.importinstance.interlab4_to_table(parsed_result))

        # "obsid, depth, report, project, staff, date_time, anameth, parameter, reading_num, reading_txt, unit, comment"
        reference_string = u'[[obsid, depth, report, project, staff, date_time, anameth, parameter, reading_num, reading_txt, unit, comment], [Demo1 vattenverk Föreskriven regelbunden undersökning enligt SLVFS 2001:30, None, DM-990908-2773, Demoproj, DV, 2010-09-07 10:15:00, SS-EN ISO 7887-1/4, Kalium, 10, 10, mg/l Pt, provtagningsorsak: Dricksvatten enligt SLVFS 2001:30. provtyp: Utgående. provtypspecifikation: Nej. bedömning: Tjänligt. mätosäkerhet: ±1]]'
        assert result_string == reference_string

    def test_interlab4_to_table_matvardetalanm(self):
        interlab4_lines = (
            u'#Interlab',
            u'#Version=4.0',
            u'#Tecken=UTF-8',
            u'#Textavgränsare=Nej',
            u'#Decimaltecken=,',
            u'#Provadm',
            u'Lablittera;Namn;Adress;Postnr;Ort;Kommunkod;Projekt;Laboratorium;Provtyp;Provtagare;Registertyp;ProvplatsID;Provplatsnamn;Specifik provplats;Provtagningsorsak;Provtyp;Provtypspecifikation;Bedömning;Kemisk bedömning;Mikrobiologisk bedömning;Kommentar;År;Provtagningsdatum;Provtagningstid;Inlämningsdatum;Inlämningstid;',
            u'DM-990908-2773;MFR;PG Vejdes väg 15;351 96;Växjö;0780;Demoproj;Demo-Laboratoriet;NSG;DV;;Demo1 vattenverk;;Föreskriven regelbunden undersökning enligt SLVFS 2001:30;Dricksvatten enligt SLVFS 2001:30;Utgående;Nej;Tjänligt;;;;2010;2010-09-07;10:15;2010-09-07;14:15;',
            u'#Provdat',
            u'Lablittera;Metodbeteckning;Parameter;Mätvärdetext;Mätvärdetal;Mätvärdetalanm;Enhet;Rapporteringsgräns;Detektionsgräns;Mätosäkerhet;Mätvärdespår;Parameterbedömning;Kommentar;',
            u'DM-990908-2773;SS-EN ISO 7887-1/4;Färgtal;;5;<;mg/l Pt;;;±1;;;;',
            u'#Slut'
                )

        with utils.tempinput(u'\n'.join(interlab4_lines), 'utf-8') as testfile:
            parsed_result = self.importinstance.parse_interlab4([testfile])

        result_string = utils_for_tests.create_test_string(self.importinstance.interlab4_to_table(parsed_result))

        # "obsid, depth, report, project, staff, date_time, anameth, parameter, reading_num, reading_txt, unit, comment"
        reference_string = u'[[obsid, depth, report, project, staff, date_time, anameth, parameter, reading_num, reading_txt, unit, comment], [Demo1 vattenverk Föreskriven regelbunden undersökning enligt SLVFS 2001:30, None, DM-990908-2773, Demoproj, DV, 2010-09-07 10:15:00, SS-EN ISO 7887-1/4, Färgtal, 5, <5, mg/l Pt, provtagningsorsak: Dricksvatten enligt SLVFS 2001:30. provtyp: Utgående. provtypspecifikation: Nej. bedömning: Tjänligt. mätosäkerhet: ±1]]'
        assert result_string == reference_string
        
    def tearDown(self):
        self.importinstance = None
        pass


class _TestInterlab4ImporterDB(object):
    answer_yes = mock_answer('yes')
    answer_no = mock_answer('no')
    CRS_question = MockUsingReturnValue([3006])
    mocked_iface = MockQgisUtilsIface()  #Used for not getting messageBar errors
    mock_askuser = MockReturnUsingDictIn({u'It is a strong': answer_no.get_v(), u'Please note!\nThere are ': answer_yes.get_v(), u'Please note!\nForeign keys will': answer_yes.get_v()}, 1)
    skip_popup = MockUsingReturnValue('')
    mock_encoding = MockUsingReturnValue([True, u'utf-8'])

    @mock.patch('create_db.utils.NotFoundQuestion')
    @mock.patch('midvatten_utils.askuser', answer_yes.get_v)
    @mock.patch('midvatten_utils.QgsProject.instance')
    @mock.patch('create_db.PyQt4.QtGui.QInputDialog.getInteger')
    @mock.patch('create_db.PyQt4.QtGui.QFileDialog.getSaveFileName')
    def setUp(self, mock_savefilename, mock_crsquestion, mock_qgsproject_instance, mock_locale):
        mock_crsquestion.return_value = [3006]
        mock_savefilename.return_value = TEMP_DB_PATH
        mock_qgsproject_instance.return_value.readEntry = MIDV_DICT

        self.dummy_iface = DummyInterface2()
        self.iface = self.dummy_iface.mock
        self.midvatten = midvatten(self.iface)

        try:
            os.remove(TEMP_DB_PATH)
        except OSError:
            pass
        mock_locale.return_value.answer = u'ok'
        mock_locale.return_value.value = u'sv_SE'
        self.midvatten.new_db()
        self.importinstance = midv_data_importer()

    def tearDown(self):
        #Delete database
        os.remove(TEMP_DB_PATH)

    @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
    def test_interlab4_full_test_to_db(self):

        utils.sql_alter_db(u'''insert into zz_staff (staff) values ('DV')''')

        utils.sql_alter_db(u'INSERT INTO obs_points ("obsid") VALUES ("Demo1 vattenverk")')

        interlab4_lines = (
            u'#Interlab',
            u'#Version=4.0',
            u'#Tecken=UTF-8',
            u'#Textavgränsare=Nej',
            u'#Decimaltecken=,',
            u'#Provadm',
            u'Lablittera;Namn;Adress;Postnr;Ort;Kommunkod;Projekt;Laboratorium;Provtyp;Provtagare;Registertyp;ProvplatsID;Provplatsnamn;Specifik provplats;Provtagningsorsak;Provtyp;Provtypspecifikation;Bedömning;Kemisk bedömning;Mikrobiologisk bedömning;Kommentar;År;Provtagningsdatum;Provtagningstid;Inlämningsdatum;Inlämningstid;',
            u'DM-990908-2773;MFR;PG Vejdes väg 15;351 96;Växjö;0780;Demoproj;Demo-Laboratoriet;NSG;DV;;Demo1 vattenverk;;Föreskriven regelbunden undersökning enligt SLVFS 2001:30;Dricksvatten enligt SLVFS 2001:30;Utgående;Nej;Tjänligt;;;;2010;2010-09-07;10:15;2010-09-07;14:15;',
            u'#Provdat',
            u'Lablittera;Metodbeteckning;Parameter;Mätvärdetext;Mätvärdetal;Mätvärdetalanm;Enhet;Rapporteringsgräns;Detektionsgräns;Mätosäkerhet;Mätvärdespår;Parameterbedömning;Kommentar;',
            u'DM-990908-2773;SS-EN ISO 7887-1/4;Kalium;<2,5;2,5;;mg/l Pt;;;;;;;',
            u'DM-990908-2773;SS-EN ISO 7887-1/4;Kalium;<1;1;;mg/l Pt;;;;;;;',
            u'#Slut'
                )

        with utils.tempinput(u'\n'.join(interlab4_lines), 'utf-8') as filename:
            @mock.patch('midvatten_utils.NotFoundQuestion')
            @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
            @mock.patch('import_data_to_db.utils.askuser', TestInterlab4ImporterDB.mock_askuser.get_v)
            @mock.patch('qgis.utils.iface', autospec=True)
            @mock.patch('import_data_to_db.utils.pop_up_info', autospec=True)
            @mock.patch('import_data_to_db.PyQt4.QtGui.QFileDialog.getOpenFileNames')
            def _test(self, filename, mock_filenames, mock_skippopup, mock_iface, mock_not_found_question):
                mock_not_found_question.return_value.answer = u'ok'
                mock_not_found_question.return_value.value = u'Demo1 vattenverk'
                mock_filenames.return_value = filename
                self.mock_iface = mock_iface
                self.importinstance.import_interlab4()


            _test(self, filename)
        test_string = utils_for_tests.create_test_string(utils.sql_load_fr_db(u'''select * from w_qual_lab'''))
        reference_string = ur'''(True, [(Demo1 vattenverk, None, DM-990908-2773, Demoproj, DV, 2010-09-07 10:15:00, SS-EN ISO 7887-1/4, Kalium, 1.0, <1, mg/l Pt, provtagningsorsak: Dricksvatten enligt SLVFS 2001:30. provtyp: Utgående. provtypspecifikation: Nej. bedömning: Tjänligt)])'''
        assert test_string == reference_string


class _TestDbCalls(object):
    temp_db_path = u'/tmp/tmp_midvatten_temp_db.sqlite'
    #temp_db_path = '/home/henrik/temp/tmp_midvatten_temp_db.sqlite'
    answer_yes = mock_answer('yes')
    answer_no = mock_answer('no')
    CRS_question = MockUsingReturnValue([3006])
    dbpath_question = MockUsingReturnValue(temp_db_path)
    mocked_iface = MockQgisUtilsIface()  #Used for not getting messageBar errors
    mock_dbpath = MockUsingReturnValue(MockQgsProjectInstance([temp_db_path]))
    mock_askuser = MockReturnUsingDictIn({u'It is a strong': answer_no.get_v(), u'Please note!\nThere are ': answer_yes.get_v(), u'Please note!\nForeign keys will': answer_yes.get_v()}, 1)
    skip_popup = MockUsingReturnValue('')
    #mocked_qgsproject = MockQgsProject(mocked_qgsinstance)

    @mock.patch('create_db.utils.NotFoundQuestion')
    @mock.patch('midvatten_utils.askuser', answer_yes.get_v)
    @mock.patch('create_db.PyQt4.QtGui.QInputDialog.getInteger', CRS_question.get_v)
    @mock.patch('create_db.PyQt4.QtGui.QFileDialog.getSaveFileName', dbpath_question.get_v)
    def setUp(self, mock_locale):
        self.iface = DummyInterface()
        self.midvatten = midvatten(self.iface)
        try:
            os.remove(TestDbCalls.temp_db_path)
        except OSError:
            pass
        mock_locale.return_value.answer = u'ok'
        mock_locale.return_value.value = u'sv_SE'
        self.midvatten.new_db()
        self.importinstance = midv_data_importer()
        #utils.verify_table_exists(u'comments')

    def tearDown(self):
        #Delete database
        os.remove(TestDbCalls.temp_db_path)

    @mock.patch('midvatten_utils.QgsProject.instance', mock_dbpath.get_v)
    def test_verify_table_exists(self):
        exists = utils.verify_table_exists(u'obs_points')
        assert exists


class TestImportObsPoints(object):
    temp_db_path = TEMP_DB_PATH
    #temp_db_path = '/home/henrik/temp/tmp_midvatten_temp_db.sqlite'
    answer_yes = mock_answer('yes')
    answer_no = mock_answer('no')
    CRS_question = MockUsingReturnValue([3006])
    dbpath_question = MockUsingReturnValue(temp_db_path)
    mocked_iface = MockQgisUtilsIface()  #Used for not getting messageBar errors
    mock_dbpath = MockUsingReturnValue(MockQgsProjectInstance([temp_db_path]))
    mock_askuser = MockReturnUsingDictIn({u'It is a strong': answer_no.get_v(), u'Please note!\nThere are ': answer_yes.get_v(), u'Please note!\nForeign keys will': answer_yes.get_v()}, 1)
    skip_popup = MockUsingReturnValue('')
    mock_encoding = MockUsingReturnValue([True, u'utf-8'])
    #mocked_qgsproject = MockQgsProject(mocked_qgsinstance)

    @mock.patch('create_db.utils.NotFoundQuestion')
    @mock.patch('midvatten_utils.askuser', answer_yes.get_v)
    @mock.patch('create_db.PyQt4.QtGui.QInputDialog.getInteger', CRS_question.get_v)
    @mock.patch('create_db.PyQt4.QtGui.QFileDialog.getSaveFileName', dbpath_question.get_v)
    def setUp(self, mock_locale):
        self.iface = DummyInterface()
        self.midvatten = midvatten(self.iface)
        try:
            os.remove(TestImportObsPoints.temp_db_path)
        except OSError:
            pass
        mock_locale.return_value.answer = u'ok'
        mock_locale.return_value.value = u'sv_SE'
        self.midvatten.new_db()
        self.importinstance = midv_data_importer()

    def tearDown(self):
        #Delete database
        os.remove(TestImportObsPoints.temp_db_path)

    @mock.patch('qgis.utils.iface', mocked_iface)
    @mock.patch('midvatten_utils.QgsProject.instance', mock_dbpath.get_v)
    @mock.patch('import_data_to_db.utils.askuser', mock_askuser.get_v)
    def _test_import_obsids_directly(self):
        utils.sql_alter_db(u'INSERT INTO obs_points ("obsid") VALUES ("obsid1")')
        utils.sql_alter_db(u'INSERT INTO obs_points ("obsid") VALUES ("obsid2")')
        result = utils.sql_load_fr_db(u'select * from obs_points')

        msgbar = TestImportObsPoints.mocked_iface.messagebar.messages
        if msgbar:
            print str(msgbar)

        assert result == (True, [(u'obsid1', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None), (u'obsid2', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)])

    @mock.patch('qgis.utils.iface', mocked_iface)
    @mock.patch('midvatten_utils.QgsProject.instance', mock_dbpath.get_v)
    @mock.patch('import_data_to_db.utils.askuser', mock_askuser.get_v)
    def _test_import_obs_points(self):

        self.importinstance.charsetchoosen = [u'utf-8']

        f = [[u'obsid', u'name', u'place', u'type', u'length', u'drillstop', u'diam', u'material', u'screen', u'capacity', u'drilldate', u'wmeas_yn', u'wlogg_yn', u'east', u'north', u'ne_accur', u'ne_source', u'h_toc', u'h_tocags', u'h_gs', u'h_accur', u'h_syst', u'h_source', u'source', u'com_onerow', u'com_html'],
             [u'rb1', u'rb1', u'a', u'pipe', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'421484', u'6542696', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1']]

        with utils.tempinput(u'\n'.join([u';'.join(_x) for _x in f])) as filename:
            selected_file = MockUsingReturnValue(filename)

            @mock.patch('PyQt4.QtGui.QInputDialog.getText', TestImportObsPoints.mock_encoding.get_v)
            @mock.patch('import_data_to_db.PyQt4.QtGui.QFileDialog.getOpenFileName', selected_file.get_v)
            @mock.patch('midvatten_utils.QgsProject.instance', TestImportObsPoints.mock_dbpath.get_v)
            @mock.patch('import_data_to_db.utils.askuser', TestImportObsPoints.mock_askuser.get_v)
            @mock.patch('import_data_to_db.utils.pop_up_info', TestImportObsPoints.skip_popup.get_v)
            @mock.patch('qgis.utils.iface', autospec=True)
            def _test_import_obs_points_using_obsp_import(self, mock_iface):
                self.importinstance.general_csv_import(goal_table=u'obs_points')
            _test_import_obs_points_using_obsp_import(self)

        test_string = utils_for_tests.create_test_string(utils.sql_load_fr_db(u'''select "obsid", "name", "place", "type", "length", "drillstop", "diam", "material", "screen", "capacity", "drilldate", "wmeas_yn", "wlogg_yn", "east", "north", "ne_accur", "ne_source", "h_toc", "h_tocags", "h_gs", "h_accur", "h_syst", "h_source", "source", "com_onerow", "com_html", AsText(geometry) from obs_points'''))
        msgbar = TestImportObsPoints.mocked_iface.messagebar.messages
        if msgbar:
            print str(msgbar)

        reference_string = ur'''(True, [(rb1, rb1, a, pipe, 1.0, 1, 1.0, 1, 1, 1, 1, 1, 1, 421484.0, 6542696.0, 1.0, 1, 1.0, 1.0, 1.0, 1.0, 1, 1, 1, 1, 1, POINT(421484 6542696))])'''
        assert test_string == reference_string

    @mock.patch('qgis.utils.iface', mocked_iface)
    @mock.patch('midvatten_utils.QgsProject.instance', mock_dbpath.get_v)
    @mock.patch('import_data_to_db.utils.askuser', mock_askuser.get_v)
    def _test_import_obs_points_already_exist(self):

        utils.sql_alter_db(u'''insert into obs_points ("obsid") values ('rb1')''')
        self.importinstance.charsetchoosen = [u'utf-8']

        f = [[u'obsid', u'name', u'place', u'type', u'length', u'drillstop', u'diam', u'material', u'screen', u'capacity', u'drilldate', u'wmeas_yn', u'wlogg_yn', u'east', u'north', u'ne_accur', u'ne_source', u'h_toc', u'h_tocags', u'h_gs', u'h_accur', u'h_syst', u'h_source', u'source', u'com_onerow', u'com_html'],
             [u'rb1', u'rb1', u'a', u'pipe', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'421484', u'6542696', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1']]

        with utils.tempinput(u'\n'.join([u';'.join(_x) for _x in f])) as filename:
            selected_file = MockUsingReturnValue(filename)

            @mock.patch('PyQt4.QtGui.QInputDialog.getText', TestImportObsPoints.mock_encoding.get_v)
            @mock.patch('import_data_to_db.PyQt4.QtGui.QFileDialog.getOpenFileName', selected_file.get_v)
            @mock.patch('midvatten_utils.QgsProject.instance', TestImportObsPoints.mock_dbpath.get_v)
            @mock.patch('import_data_to_db.utils.askuser', TestImportObsPoints.mock_askuser.get_v)
            @mock.patch('import_data_to_db.utils.pop_up_info', TestImportObsPoints.skip_popup.get_v)
            @mock.patch('qgis.utils.iface', autospec=True)
            def _test_import_obs_points_using_obsp_import(self, mock_iface):
                self.importinstance.general_csv_import(goal_table=u'obs_points')
                assert call.messageBar().createMessage(u'0 rows imported and 1 excluded for table obs_points. See log message panel for details') in mock_iface.mock_calls

            _test_import_obs_points_using_obsp_import(self)

        test_string = utils_for_tests.create_test_string(utils.sql_load_fr_db(u'''select "obsid", "name", "place", "type", "length", "drillstop", "diam", "material", "screen", "capacity", "drilldate", "wmeas_yn", "wlogg_yn", "east", "north", "ne_accur", "ne_source", "h_toc", "h_tocags", "h_gs", "h_accur", "h_syst", "h_source", "source", "com_onerow", "com_html", AsText(geometry) from obs_points'''))
        msgbar = TestImportObsPoints.mocked_iface.messagebar.messages

        #if msgbar:
        #    print str(msgbar)

        reference_string = ur'''(True, [(rb1, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)])'''
        assert test_string == reference_string

    @mock.patch('qgis.utils.iface', mocked_iface)
    @mock.patch('midvatten_utils.QgsProject.instance', mock_dbpath.get_v)
    @mock.patch('import_data_to_db.utils.askuser', mock_askuser.get_v)
    def _test_import_obs_points_duplicates(self):

        self.importinstance.charsetchoosen = [u'utf-8']

        f = [[u'obsid', u'name', u'place', u'type', u'length', u'drillstop', u'diam', u'material', u'screen', u'capacity', u'drilldate', u'wmeas_yn', u'wlogg_yn', u'east', u'north', u'ne_accur', u'ne_source', u'h_toc', u'h_tocags', u'h_gs', u'h_accur', u'h_syst', u'h_source', u'source', u'com_onerow', u'com_html'],
             [u'rb1', u'rb1', u'a', u'pipe', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'421484', u'6542696', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1'],
             [u'rb1', u'rb2', u'a', u'pipe', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'421485', u'6542697', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1'],
             [u'rb1', u'rb3', u'a', u'pipe', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'421484', u'6542696', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1']]

        with utils.tempinput(u'\n'.join([u';'.join(_x) for _x in f])) as filename:
            selected_file = MockUsingReturnValue(filename)

            @mock.patch('PyQt4.QtGui.QInputDialog.getText', TestImportObsPoints.mock_encoding.get_v)
            @mock.patch('import_data_to_db.PyQt4.QtGui.QFileDialog.getOpenFileName', selected_file.get_v)
            @mock.patch('midvatten_utils.QgsProject.instance', TestImportObsPoints.mock_dbpath.get_v)
            @mock.patch('import_data_to_db.utils.askuser', TestImportObsPoints.mock_askuser.get_v)
            @mock.patch('import_data_to_db.utils.pop_up_info', TestImportObsPoints.skip_popup.get_v)
            @mock.patch('qgis.utils.iface', autospec=True)
            def _test_import_obs_points_using_obsp_import(self, mock_iface):
                self.importinstance.general_csv_import(goal_table=u'obs_points')
                assert call.messageBar().createMessage(u'1 rows imported and 2 excluded for table obs_points. See log message panel for details') in mock_iface.mock_calls
            _test_import_obs_points_using_obsp_import(self)

        test_string = utils_for_tests.create_test_string(utils.sql_load_fr_db(u'''select "obsid", "name", "place", "type", "length", "drillstop", "diam", "material", "screen", "capacity", "drilldate", "wmeas_yn", "wlogg_yn", "east", "north", "ne_accur", "ne_source", "h_toc", "h_tocags", "h_gs", "h_accur", "h_syst", "h_source", "source", "com_onerow", "com_html", AsText(geometry) from obs_points'''))
        msgbar = TestImportObsPoints.mocked_iface.messagebar.messages
        #if msgbar:
        #    print str(msgbar)

        reference_string = ur'''(True, [(rb1, rb1, a, pipe, 1.0, 1, 1.0, 1, 1, 1, 1, 1, 1, 421484.0, 6542696.0, 1.0, 1, 1.0, 1.0, 1.0, 1.0, 1, 1, 1, 1, 1, POINT(421484 6542696))])'''
        assert test_string == reference_string

    @mock.patch('qgis.utils.iface', mocked_iface)
    @mock.patch('midvatten_utils.QgsProject.instance', mock_dbpath.get_v)
    @mock.patch('import_data_to_db.utils.askuser', mock_askuser.get_v)
    def _test_import_obs_points_no_east_north(self):
        self.importinstance.charsetchoosen = [u'utf-8']

        f = [[u'obsid', u'name', u'place', u'type', u'length', u'drillstop', u'diam', u'material', u'screen', u'capacity', u'drilldate', u'wmeas_yn', u'wlogg_yn', u'east', u'north', u'ne_accur', u'ne_source', u'h_toc', u'h_tocags', u'h_gs', u'h_accur', u'h_syst', u'h_source', u'source', u'com_onerow', u'com_html'],
             [u'rb1', u'rb1', u'a', u'pipe', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'', u'', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1']]

        with utils.tempinput(u'\n'.join([u';'.join(_x) for _x in f])) as filename:
            selected_file = MockUsingReturnValue(filename)

            @mock.patch('PyQt4.QtGui.QInputDialog.getText', TestImportObsPoints.mock_encoding.get_v)
            @mock.patch('import_data_to_db.PyQt4.QtGui.QFileDialog.getOpenFileName', selected_file.get_v)
            @mock.patch('midvatten_utils.QgsProject.instance', TestImportObsPoints.mock_dbpath.get_v)
            @mock.patch('import_data_to_db.utils.askuser', TestImportObsPoints.mock_askuser.get_v)
            @mock.patch('import_data_to_db.utils.pop_up_info', TestImportObsPoints.skip_popup.get_v)
            @mock.patch('qgis.utils.iface', autospec=True)
            def _test_import_obs_points_using_obsp_import(self, mock_iface):
                self.importinstance.general_csv_import(goal_table=u'obs_points')
            _test_import_obs_points_using_obsp_import(self)

        test_string = utils_for_tests.create_test_string(utils.sql_load_fr_db(u'''select "obsid", "name", "place", "type", "length", "drillstop", "diam", "material", "screen", "capacity", "drilldate", "wmeas_yn", "wlogg_yn", "east", "north", "ne_accur", "ne_source", "h_toc", "h_tocags", "h_gs", "h_accur", "h_syst", "h_source", "source", "com_onerow", "com_html", AsText(geometry) from obs_points'''))
        msgbar = TestImportObsPoints.mocked_iface.messagebar.messages
        if msgbar:
            print str(msgbar)

        reference_string = ur'''(True, [(rb1, rb1, a, pipe, 1.0, 1, 1.0, 1, 1, 1, 1, 1, 1, None, None, 1.0, 1, 1.0, 1.0, 1.0, 1.0, 1, 1, 1, 1, 1, None)])'''
        assert test_string == reference_string

    @mock.patch('qgis.utils.iface', mocked_iface)
    @mock.patch('midvatten_utils.QgsProject.instance', mock_dbpath.get_v)
    @mock.patch('import_data_to_db.utils.askuser', mock_askuser.get_v)
    def test_import_obs_points_geometry_as_wkt(self):
        self.importinstance.charsetchoosen = [u'utf-8']

        f = [[u'obsid', u'name', u'place', u'type', u'length', u'drillstop', u'diam', u'material', u'screen', u'capacity', u'drilldate', u'wmeas_yn', u'wlogg_yn', u'east', u'north', u'ne_accur', u'ne_source', u'h_toc', u'h_tocags', u'h_gs', u'h_accur', u'h_syst', u'h_source', u'source', u'com_onerow', u'com_html', u'geometry'],
             [u'rb1', u'rb1', u'a', u'pipe', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'', u'', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u'1', u"'POINT(45 55)'"]]

        with utils.tempinput(u'\n'.join([u';'.join(_x) for _x in f])) as filename:
            selected_file = MockUsingReturnValue(filename)

            @mock.patch('PyQt4.QtGui.QInputDialog.getText', TestImportObsPoints.mock_encoding.get_v)
            @mock.patch('import_data_to_db.PyQt4.QtGui.QFileDialog.getOpenFileName', selected_file.get_v)
            @mock.patch('midvatten_utils.QgsProject.instance', TestImportObsPoints.mock_dbpath.get_v)
            @mock.patch('import_data_to_db.utils.askuser', TestImportObsPoints.mock_askuser.get_v)
            @mock.patch('import_data_to_db.utils.pop_up_info', TestImportObsPoints.skip_popup.get_v)
            @mock.patch('qgis.utils.iface', autospec=True)
            def _test(self, mock_iface):
                self.importinstance.general_csv_import(goal_table=u'obs_points')
                print(str(mock_iface.mock_calls))
            _test(self)

        test_string = utils_for_tests.create_test_string(utils.sql_load_fr_db(u'''select "obsid", "name", "place", "type", "length", "drillstop", "diam", "material", "screen", "capacity", "drilldate", "wmeas_yn", "wlogg_yn", "east", "north", "ne_accur", "ne_source", "h_toc", "h_tocags", "h_gs", "h_accur", "h_syst", "h_source", "source", "com_onerow", "com_html", AsText(geometry) from obs_points'''))
        msgbar = TestImportObsPoints.mocked_iface.messagebar.messages
        if msgbar:
            print str(msgbar)

        reference_string = ur'''(True, [(rb1, rb1, a, pipe, 1.0, 1, 1.0, 1, 1, 1, 1, 1, 1, None, None, 1.0, 1, 1.0, 1.0, 1.0, 1.0, 1, 1, 1, 1, 1, POINT(45 55)])'''
        print(test_string)
        assert test_string == reference_string


class _TestWquallabImport(object):
    temp_db_path = u'/tmp/tmp_midvatten_temp_db.sqlite'
    answer_yes = mock_answer('yes')
    answer_no = mock_answer('no')
    CRS_question = MockUsingReturnValue([3006])
    dbpath_question = MockUsingReturnValue(temp_db_path)
    mocked_iface = MockQgisUtilsIface()  #Used for not getting messageBar errors
    mock_dbpath = MockUsingReturnValue(MockQgsProjectInstance([temp_db_path]))
    mock_askuser = MockReturnUsingDictIn({u'It is a strong': answer_no.get_v(), u'Please note!\nThere are ': answer_yes.get_v(), u'Please note!\nForeign keys will': answer_yes.get_v()}, 1)
    skip_popup = MockUsingReturnValue('')
    mock_encoding = MockUsingReturnValue([True, u'utf-8'])

    @mock.patch('create_db.utils.NotFoundQuestion')
    @mock.patch('midvatten_utils.askuser', answer_yes.get_v)
    @mock.patch('midvatten_utils.QgsProject.instance')
    @mock.patch('create_db.PyQt4.QtGui.QInputDialog.getInteger')
    @mock.patch('create_db.PyQt4.QtGui.QFileDialog.getSaveFileName')
    def setUp(self, mock_savefilename, mock_crsquestion, mock_qgsproject_instance, mock_locale):
        mock_crsquestion.return_value = [3006]
        mock_savefilename.return_value = TestWquallabImport.temp_db_path
        mock_qgsproject_instance.return_value.readEntry = MIDV_DICT

        self.dummy_iface = DummyInterface2()
        self.iface = self.dummy_iface.mock
        self.midvatten = midvatten(self.iface)

        try:
            os.remove(TestWquallabImport.temp_db_path)
        except OSError:
            pass
        mock_locale.return_value.answer = u'ok'
        mock_locale.return_value.value = u'sv_SE'
        self.midvatten.new_db()
        self.importinstance = midv_data_importer()

    def tearDown(self):
        #Delete database
        os.remove(TestWquallabImport.temp_db_path)

    @mock.patch('midvatten_utils.QgsProject.instance', mock_dbpath.get_v)
    def test_wquallab_import_from_csvlayer(self):
        self.importinstance.charsetchoosen = [u'utf-8']

        utils.sql_alter_db('''insert into zz_staff (staff) values ('teststaff')''')

        utils.sql_alter_db(u'INSERT INTO obs_points ("obsid") VALUES ("obsid1")')
        f = [[u'obsid', u'depth', u'report', u'project', u'staff', u'date_time', u'anameth', u'parameter', u'reading_num', u'reading_txt', u'unit', u'comment'],
             [u'obsid1', u'2', u'testreport', u'testproject', u'teststaff', u'2011-10-19 12:30:00', u'testmethod', u'1,2-Dikloretan', u'1.5', u'<1.5', u'µg/l', u'testcomment']]

        with utils.tempinput(u'\n'.join([u';'.join(_x) for _x in f])) as filename:

            @mock.patch('midvatten_utils.QgsProject.instance', TestWquallabImport.mock_dbpath.get_v)
            @mock.patch('import_data_to_db.utils.askuser')
            @mock.patch('qgis.utils.iface', autospec=True)
            @mock.patch('PyQt4.QtGui.QInputDialog.getText')
            @mock.patch('import_data_to_db.utils.pop_up_info', autospec=True)
            @mock.patch('import_data_to_db.PyQt4.QtGui.QFileDialog.getOpenFileName')
            def _wquallab_import_from_csvlayer(self, filename, mock_filename, mock_skippopup, mock_encoding, mock_iface, mock_askuser):
                mock_filename.return_value = filename
                mock_encoding.return_value = [True, u'utf-8']
                self.mock_iface = mock_iface
                self.importinstance.general_csv_import(goal_table=u'w_qual_lab')
            _wquallab_import_from_csvlayer(self, filename)

        test_string = utils_for_tests.create_test_string(utils.sql_load_fr_db(u'''select * from w_qual_lab'''))

        reference_string = ur'''(True, [(obsid1, 2.0, testreport, testproject, teststaff, 2011-10-19 12:30:00, testmethod, 1,2-Dikloretan, 1.5, <1.5, µg/l, testcomment)])'''
        assert test_string == reference_string

    @mock.patch('midvatten_utils.QgsProject.instance', mock_dbpath.get_v)
    def test_wquallab_import_from_csvlayer_depth_empty_string(self):
        self.importinstance.charsetchoosen = [u'utf-8']

        utils.sql_alter_db('''insert into zz_staff (staff) values ('teststaff')''')

        utils.sql_alter_db(u'INSERT INTO obs_points ("obsid") VALUES ("obsid1")')
        f = [[u'obsid', u'depth', u'report', u'project', u'staff', u'date_time', u'anameth', u'parameter', u'reading_num', u'reading_txt', u'unit', u'comment'],
             [u'obsid1', u'', u'testreport', u'testproject', u'teststaff', u'2011-10-19 12:30:00', u'testmethod', u'1,2-Dikloretan', u'1.5', u'<1.5', u'µg/l', u'testcomment']]

        with utils.tempinput(u'\n'.join([u';'.join(_x) for _x in f])) as filename:

            @mock.patch('midvatten_utils.QgsProject.instance', TestWquallabImport.mock_dbpath.get_v)
            @mock.patch('import_data_to_db.utils.askuser')
            @mock.patch('qgis.utils.iface', autospec=True)
            @mock.patch('PyQt4.QtGui.QInputDialog.getText')
            @mock.patch('import_data_to_db.utils.pop_up_info', autospec=True)
            @mock.patch('import_data_to_db.PyQt4.QtGui.QFileDialog.getOpenFileName')
            def test_wquallab_import_from_csvlayer_depth_empty_string(self, filename, mock_filename, mock_skippopup, mock_encoding, mock_iface, mock_askuser):
                mock_filename.return_value = filename
                mock_encoding.return_value = [True, u'utf-8']
                self.mock_iface = mock_iface
                self.importinstance.general_csv_import(goal_table=u'w_qual_lab')
            test_wquallab_import_from_csvlayer_depth_empty_string(self, filename)

        test_string = utils_for_tests.create_test_string(utils.sql_load_fr_db(u'''select * from w_qual_lab'''))

        reference_string = ur'''(True, [(obsid1, None, testreport, testproject, teststaff, 2011-10-19 12:30:00, testmethod, 1,2-Dikloretan, 1.5, <1.5, µg/l, testcomment)])'''
        assert test_string == reference_string


    @mock.patch('midvatten_utils.QgsProject.instance', mock_dbpath.get_v)
    def test_wquallab_import_from_csvlayer_no_staff(self):
        self.importinstance.charsetchoosen = [u'utf-8']

        utils.sql_alter_db('''insert into zz_staff (staff) values ('teststaff')''')

        utils.sql_alter_db(u'INSERT INTO obs_points ("obsid") VALUES ("obsid1")')
        f = [[u'obsid', u'depth', u'report', u'project', u'date_time', u'anameth', u'parameter', u'reading_num', u'reading_txt', u'unit', u'comment'],
             [u'obsid1', u'2', u'testreport', u'testproject', u'2011-10-19 12:30:00', u'testmethod', u'1,2-Dikloretan', u'1.5', u'<1.5', u'µg/l', u'testcomment']]

        with utils.tempinput(u'\n'.join([u';'.join(_x) for _x in f])) as filename:

            @mock.patch('midvatten_utils.QgsProject.instance', TestWquallabImport.mock_dbpath.get_v)
            @mock.patch('import_data_to_db.utils.askuser')
            @mock.patch('qgis.utils.iface', autospec=True)
            @mock.patch('PyQt4.QtGui.QInputDialog.getText')
            @mock.patch('import_data_to_db.utils.pop_up_info', autospec=True)
            @mock.patch('import_data_to_db.PyQt4.QtGui.QFileDialog.getOpenFileName')
            def _wquallab_import_from_csvlayer(self, filename, mock_filename, mock_skippopup, mock_encoding, mock_iface, mock_askuser):
                mock_filename.return_value = filename
                mock_encoding.return_value = [True, u'utf-8']
                self.mock_iface = mock_iface
                self.importinstance.general_csv_import(goal_table=u'w_qual_lab')
            _wquallab_import_from_csvlayer(self, filename)

        test_string = utils_for_tests.create_test_string(utils.sql_load_fr_db(u'''select * from w_qual_lab'''))
        reference_string = ur'''(True, [(obsid1, 2.0, testreport, testproject, None, 2011-10-19 12:30:00, testmethod, 1,2-Dikloretan, 1.5, <1.5, µg/l, testcomment)])'''
        assert test_string == reference_string


class _TestWflowImport(object):
    answer_yes = mock_answer('yes')
    answer_no = mock_answer('no')
    CRS_question = MockUsingReturnValue([3006])
    mocked_iface = MockQgisUtilsIface()  #Used for not getting messageBar errors
    mock_askuser = MockReturnUsingDictIn({u'It is a strong': answer_no.get_v(), u'Please note!\nThere are ': answer_yes.get_v(), u'Please note!\nForeign keys will': answer_yes.get_v()}, 1)
    skip_popup = MockUsingReturnValue('')
    mock_encoding = MockUsingReturnValue([True, u'utf-8'])

    @mock.patch('create_db.utils.NotFoundQuestion')
    @mock.patch('midvatten_utils.askuser', answer_yes.get_v)
    @mock.patch('midvatten_utils.QgsProject.instance')
    @mock.patch('create_db.PyQt4.QtGui.QInputDialog.getInteger')
    @mock.patch('create_db.PyQt4.QtGui.QFileDialog.getSaveFileName')
    def setUp(self, mock_savefilename, mock_crsquestion, mock_qgsproject_instance, mock_locale):
        mock_crsquestion.return_value = [3006]
        mock_savefilename.return_value = TEMP_DB_PATH
        mock_qgsproject_instance.return_value.readEntry = MIDV_DICT

        self.dummy_iface = DummyInterface2()
        self.iface = self.dummy_iface.mock
        self.midvatten = midvatten(self.iface)

        try:
            os.remove(TEMP_DB_PATH)
        except OSError:
            pass
        mock_locale.return_value.answer = u'ok'
        mock_locale.return_value.value = u'sv_SE'
        self.midvatten.new_db()
        self.importinstance = midv_data_importer()

    def tearDown(self):
        #Delete database
        os.remove(TEMP_DB_PATH)

    @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
    def test_wflow_import_from_csvlayer(self):
        self.importinstance.charsetchoosen = [u'utf-8']

        utils.sql_alter_db(u'INSERT INTO obs_points ("obsid") VALUES ("obsid1")')
        f = [[u'obsid', u'instrumentid', u'flowtype', u'date_time', u'reading', u'unit', u'comment'],
             [u'obsid1', u'testid', u'Momflow', u'2011-10-19 12:30:00', u'2', u'l/s', u'testcomment']]

        with utils.tempinput(u'\n'.join([u';'.join(_x) for _x in f])) as filename:

            @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
            @mock.patch('import_data_to_db.utils.askuser')
            @mock.patch('qgis.utils.iface', autospec=True)
            @mock.patch('PyQt4.QtGui.QInputDialog.getText')
            @mock.patch('import_data_to_db.utils.pop_up_info', autospec=True)
            @mock.patch('import_data_to_db.PyQt4.QtGui.QFileDialog.getOpenFileName')
            def _test_wflow_import_from_csvlayer(self, filename, mock_filename, mock_skippopup, mock_encoding, mock_iface, mock_askuser):
                mock_filename.return_value = filename
                mock_encoding.return_value = [True, u'utf-8']
                self.mock_iface = mock_iface
                self.importinstance.general_csv_import(goal_table=u'w_flow')
            _test_wflow_import_from_csvlayer(self, filename)

        test_string = utils_for_tests.create_test_string(utils.sql_load_fr_db(u'''select * from w_flow'''))
        reference_string = ur'''(True, [(obsid1, testid, Momflow, 2011-10-19 12:30:00, 2.0, l/s, testcomment)])'''
        assert test_string == reference_string

    @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
    def test_wflow_import_from_csvlayer_type_missing(self):
        self.importinstance.charsetchoosen = [u'utf-8']

        utils.sql_alter_db(u'INSERT INTO obs_points ("obsid") VALUES ("obsid1")')
        f = [[u'obsid', u'instrumentid', u'flowtype', u'date_time', u'reading', u'unit', u'comment'],
             [u'obsid1', u'testid', u'Testtype', u'2011-10-19 12:30:00', u'2', u'l/s', u'testcomment']]

        with utils.tempinput(u'\n'.join([u';'.join(_x) for _x in f])) as filename:

            @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
            @mock.patch('import_data_to_db.utils.askuser')
            @mock.patch('qgis.utils.iface', autospec=True)
            @mock.patch('PyQt4.QtGui.QInputDialog.getText')
            @mock.patch('import_data_to_db.utils.pop_up_info', autospec=True)
            @mock.patch('import_data_to_db.PyQt4.QtGui.QFileDialog.getOpenFileName')
            def _test_wflow_import_from_csvlayer(self, filename, mock_filename, mock_skippopup, mock_encoding, mock_iface, mock_askuser):
                mock_filename.return_value = filename
                mock_encoding.return_value = [True, u'utf-8']
                self.mock_iface = mock_iface
                self.importinstance.general_csv_import(goal_table=u'w_flow')
            _test_wflow_import_from_csvlayer(self, filename)

        test_string = utils_for_tests.create_test_string(utils.sql_load_fr_db(u'''select * from w_flow'''))
        reference_string = ur'''(True, [(obsid1, testid, Testtype, 2011-10-19 12:30:00, 2.0, l/s, testcomment)])'''
        assert test_string == reference_string

    @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
    def test_wflow_new_param_into_zz_flowtype(self):
        self.importinstance.charsetchoosen = [u'utf-8']

        utils.sql_alter_db(u'INSERT INTO obs_points ("obsid") VALUES ("obsid1")')
        f = [[u'obsid', u'instrumentid', u'flowtype', u'date_time', u'reading', u'unit', u'comment'],
             [u'obsid1', u'testid', u'Momflow2', u'2011-10-19 12:30:00', u'2', u'l/s', u'testcomment']]

        with utils.tempinput(u'\n'.join([u';'.join(_x) for _x in f])) as filename:

            @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
            @mock.patch('import_data_to_db.utils.askuser')
            @mock.patch('qgis.utils.iface', autospec=True)
            @mock.patch('PyQt4.QtGui.QInputDialog.getText')
            @mock.patch('import_data_to_db.utils.pop_up_info', autospec=True)
            @mock.patch('import_data_to_db.PyQt4.QtGui.QFileDialog.getOpenFileName')
            def _test(self, filename, mock_filename, mock_skippopup, mock_encoding, mock_iface, mock_askuser):
                mock_filename.return_value = filename
                mock_encoding.return_value = [True, u'utf-8']
                self.mock_iface = mock_iface
                self.importinstance.general_csv_import(goal_table=u'w_flow')
            _test(self, filename)

        test_string = utils_for_tests.create_test_string(utils.sql_load_fr_db(u'''select * from w_flow'''))
        reference_string = ur'''(True, [(obsid1, testid, Momflow2, 2011-10-19 12:30:00, 2.0, l/s, testcomment)])'''
        assert test_string == reference_string
        test_string = utils_for_tests.create_test_string(utils.sql_load_fr_db(u'''select * from zz_flowtype'''))
        reference_string = ur'''(True, [(Accvol, Accumulated volume), (Momflow, Momentary flow rate), (Aveflow, Average flow since last reading), (Momflow2, None)])'''
        assert test_string == reference_string


class _TestWqualfieldImport(object):
    answer_yes = mock_answer('yes')
    answer_no = mock_answer('no')
    CRS_question = MockUsingReturnValue([3006])
    mocked_iface = MockQgisUtilsIface()  #Used for not getting messageBar errors
    mock_askuser = MockReturnUsingDictIn({u'It is a strong': answer_no.get_v(), u'Please note!\nThere are ': answer_yes.get_v(), u'Please note!\nForeign keys will': answer_yes.get_v()}, 1)
    skip_popup = MockUsingReturnValue('')
    mock_encoding = MockUsingReturnValue([True, u'utf-8'])

    @mock.patch('create_db.utils.NotFoundQuestion')
    @mock.patch('midvatten_utils.askuser', answer_yes.get_v)
    @mock.patch('midvatten_utils.QgsProject.instance')
    @mock.patch('create_db.PyQt4.QtGui.QInputDialog.getInteger')
    @mock.patch('create_db.PyQt4.QtGui.QFileDialog.getSaveFileName')
    def setUp(self, mock_savefilename, mock_crsquestion, mock_qgsproject_instance, mock_locale):
        mock_crsquestion.return_value = [3006]
        mock_savefilename.return_value = TEMP_DB_PATH
        mock_qgsproject_instance.return_value.readEntry = MIDV_DICT

        self.dummy_iface = DummyInterface2()
        self.iface = self.dummy_iface.mock
        self.midvatten = midvatten(self.iface)

        try:
            os.remove(TEMP_DB_PATH)
        except OSError:
            pass
        mock_locale.return_value.answer = u'ok'
        mock_locale.return_value.value = u'sv_SE'
        self.midvatten.new_db()
        self.importinstance = midv_data_importer()

    def tearDown(self):
        #Delete database
        os.remove(TEMP_DB_PATH)

    @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
    def test_w_qual_field_import_from_csvlayer(self):
        self.importinstance.charsetchoosen = [u'utf-8']

        utils.sql_alter_db(u'INSERT INTO obs_points ("obsid") VALUES ("obsid1")')
        f = [[u'obsid', u'staff', u'date_time', u'instrument', u'parameter', u'reading_num', u'reading_txt', u'unit', u'depth', u'comment'],
             [u'obsid1', u'teststaff', u'2011-10-19 12:30:00', u'testinstrument', u'DO', u'12', u'<12', u'%', u'22', u'testcomment']]

        #utils.sql_alter_db(u'''insert into w_qual_field (obsid, date_time, parameter, reading_num, unit) values ('1', '2011-10-19 12:30:01', 'testp', '123', 'testunit')''')

        with utils.tempinput(u'\n'.join([u';'.join(_x) for _x in f])) as filename:

            @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
            @mock.patch('import_data_to_db.utils.askuser')
            @mock.patch('qgis.utils.iface', autospec=True)
            @mock.patch('PyQt4.QtGui.QInputDialog.getText')
            @mock.patch('import_data_to_db.utils.pop_up_info', autospec=True)
            @mock.patch('import_data_to_db.PyQt4.QtGui.QFileDialog.getOpenFileName')
            def _test_w_qual_field_import_from_csvlayer(self, filename, mock_filename, mock_skippopup, mock_encoding, mock_iface, mock_askuser):
                mock_filename.return_value = filename
                mock_encoding.return_value = [True, u'utf-8']
                self.mock_iface = mock_iface
                self.importinstance.general_csv_import(goal_table=u'w_qual_field')
            _test_w_qual_field_import_from_csvlayer(self, filename)

        test_string = utils_for_tests.create_test_string(utils.sql_load_fr_db(u'''select * from w_qual_field'''))
        reference_string = ur'''(True, [(obsid1, teststaff, 2011-10-19 12:30:00, testinstrument, DO, 12.0, <12, %, 22.0, testcomment)])'''
        assert test_string == reference_string

    @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
    def test_w_qual_field_import_from_csvlayer_no_depth(self):
        self.importinstance.charsetchoosen = [u'utf-8']

        utils.sql_alter_db(u'INSERT INTO obs_points ("obsid") VALUES ("obsid1")')
        f = [[u'obsid', u'staff', u'date_time', u'instrument', u'parameter', u'reading_num', u'reading_txt', u'unit', u'depth', u'comment'],
             [u'obsid1', u'teststaff', u'2011-10-19 12:30:00', u'testinstrument', u'DO', u'12', u'<12', u'%', u'', u'testcomment']]

        with utils.tempinput(u'\n'.join([u';'.join(_x) for _x in f])) as filename:

            @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
            @mock.patch('import_data_to_db.utils.askuser')
            @mock.patch('qgis.utils.iface', autospec=True)
            @mock.patch('PyQt4.QtGui.QInputDialog.getText')
            @mock.patch('import_data_to_db.utils.pop_up_info', autospec=True)
            @mock.patch('import_data_to_db.PyQt4.QtGui.QFileDialog.getOpenFileName')
            def _test_w_qual_field_import_from_csvlayer(self, filename, mock_filename, mock_skippopup, mock_encoding, mock_iface, mock_askuser):
                mock_filename.return_value = filename
                mock_encoding.return_value = [True, u'utf-8']
                self.mock_iface = mock_iface
                self.importinstance.general_csv_import(goal_table=u'w_qual_field')
            _test_w_qual_field_import_from_csvlayer(self, filename)

        test_string = utils_for_tests.create_test_string(utils.sql_load_fr_db(u'''select * from w_qual_field'''))
        reference_string = ur'''(True, [(obsid1, teststaff, 2011-10-19 12:30:00, testinstrument, DO, 12.0, <12, %, None, testcomment)])'''
        assert test_string == reference_string

    @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
    def test_w_qual_field_no_parameter(self):
        self.importinstance.charsetchoosen = [u'utf-8']

        utils.sql_alter_db(u'INSERT INTO obs_points ("obsid") VALUES ("obsid1")')
        f = [[u'obsid', u'staff', u'date_time', u'instrument',
              u'reading_num', u'reading_txt', u'unit', u'depth', u'comment'],
             [u'obsid1', u'teststaff', u'2011-10-19 12:30:00', u'testinstrument',
              u'12', u'<12', u'%', u'22', u'testcomment']]

        # utils.sql_alter_db(u'''insert into w_qual_field (obsid, date_time, parameter, reading_num, unit) values ('1', '2011-10-19 12:30:01', 'testp', '123', 'testunit')''')

        with utils.tempinput(u'\n'.join([u';'.join(_x) for _x in f])) as filename:
            @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
            @mock.patch('import_data_to_db.utils.askuser')
            @mock.patch('qgis.utils.iface', autospec=True)
            @mock.patch('PyQt4.QtGui.QInputDialog.getText')
            @mock.patch('import_data_to_db.utils.pop_up_info', autospec=True)
            @mock.patch(
                'import_data_to_db.PyQt4.QtGui.QFileDialog.getOpenFileName')
            def _test_w_qual_field_import_from_csvlayer(self, filename,
                                                        mock_filename,
                                                        mock_skippopup,
                                                        mock_encoding, mock_iface, mock_askuser):
                mock_filename.return_value = filename
                mock_encoding.return_value = [True, u'utf-8']
                self.mock_iface = mock_iface
                self.importinstance.general_csv_import(goal_table=u'w_qual_field')
                mock_iface.messageBar.return_value.createMessage.assert_called_with(u'Error: Import failed, see log message panel')

            _test_w_qual_field_import_from_csvlayer(self, filename)

        test_string = utils_for_tests.create_test_string(
            utils.sql_load_fr_db(u'''select * from w_qual_field'''))
        reference_string = ur'''(True, [])'''
        assert test_string == reference_string

    @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
    def test_w_qual_field_parameter_empty_string(self):
        self.importinstance.charsetchoosen = [u'utf-8']

        utils.sql_alter_db(u'INSERT INTO obs_points ("obsid") VALUES ("obsid1")')
        f = [[u'obsid', u'staff', u'date_time', u'instrument', u'parameter', u'reading_num', u'reading_txt', u'unit', u'depth', u'comment'],
             [u'obsid1', u'teststaff', u'2011-10-19 12:30:00', u'testinstrument', u'DO', u'12', u'<12', u'%', u'22', u'testcomment'],
             [u'obsid2', u'teststaff', u'2011-10-19 12:30:00', u'testinstrument', u'', u'12', u'<12', u'%', u'22', u'testcomment']]

        # utils.sql_alter_db(u'''insert into w_qual_field (obsid, date_time, parameter, reading_num, unit) values ('1', '2011-10-19 12:30:01', 'testp', '123', 'testunit')''')

        with utils.tempinput(u'\n'.join([u';'.join(_x) for _x in f])) as filename:
            @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
            @mock.patch('import_data_to_db.utils.askuser')
            @mock.patch('qgis.utils.iface', autospec=True)
            @mock.patch('PyQt4.QtGui.QInputDialog.getText')
            @mock.patch('import_data_to_db.utils.pop_up_info', autospec=True)
            @mock.patch(
                'import_data_to_db.PyQt4.QtGui.QFileDialog.getOpenFileName')
            def _test_w_qual_field_import_from_csvlayer(self, filename,
                                                        mock_filename,
                                                        mock_skippopup,
                                                        mock_encoding, mock_iface, mock_askuser):
                mock_filename.return_value = filename
                mock_encoding.return_value = [True, u'utf-8']
                self.mock_iface = mock_iface
                self.importinstance.general_csv_import(goal_table=u'w_qual_field')
                mock_iface.messageBar.return_value.createMessage.assert_called_with(u'1 rows imported and 1 excluded for table w_qual_field. See log message panel for details')

            _test_w_qual_field_import_from_csvlayer(self, filename)

        test_string = utils_for_tests.create_test_string(
            utils.sql_load_fr_db(u'''select * from w_qual_field'''))
        reference_string = ur'''(True, [(obsid1, teststaff, 2011-10-19 12:30:00, testinstrument, DO, 12.0, <12, %, 22.0, testcomment)])'''
        assert test_string == reference_string

    @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
    def test_w_qual_field_staff_null(self):
        self.importinstance.charsetchoosen = [u'utf-8']

        utils.sql_alter_db(u'INSERT INTO obs_points ("obsid") VALUES ("obsid1")')
        utils.sql_alter_db(u'INSERT INTO obs_points ("obsid") VALUES ("obsid2")')
        f = [[u'obsid', u'staff', u'date_time', u'instrument', u'parameter', u'reading_num', u'reading_txt', u'unit', u'depth', u'comment'],
             [u'obsid1', u'', u'2011-10-19 12:30:00', u'testinstrument', u'DO', u'12', u'<12', u'%', u'22', u'testcomment'],
             [u'obsid2', u'', u'2011-10-19 12:30:00', u'testinstrument', u'DO', u'12', u'<12', u'%', u'22', u'testcomment']]

        # utils.sql_alter_db(u'''insert into w_qual_field (obsid, date_time, parameter, reading_num, unit) values ('1', '2011-10-19 12:30:01', 'testp', '123', 'testunit')''')

        with utils.tempinput(u'\n'.join([u';'.join(_x) for _x in f])) as filename:
            @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
            @mock.patch('import_data_to_db.utils.askuser')
            @mock.patch('qgis.utils.iface', autospec=True)
            @mock.patch('PyQt4.QtGui.QInputDialog.getText')
            @mock.patch('import_data_to_db.utils.pop_up_info', autospec=True)
            @mock.patch(
                'import_data_to_db.PyQt4.QtGui.QFileDialog.getOpenFileName')
            def _test_w_qual_field_import_from_csvlayer(self, filename,
                                                        mock_filename,
                                                        mock_skippopup,
                                                        mock_encoding, mock_iface, mock_askuser):
                mock_filename.return_value = filename
                mock_encoding.return_value = [True, u'utf-8']
                self.mock_iface = mock_iface
                self.importinstance.general_csv_import(goal_table=u'w_qual_field')
                mock_iface.messageBar.return_value.createMessage.assert_called_with(u'2 rows imported and 0 excluded for table w_qual_field. See log message panel for details')

            _test_w_qual_field_import_from_csvlayer(self, filename)

        test_string = utils_for_tests.create_test_string(
            utils.sql_load_fr_db(u'''select * from w_qual_field'''))
        reference_string = ur'''(True, [(obsid1, None, 2011-10-19 12:30:00, testinstrument, DO, 12.0, <12, %, 22.0, testcomment), (obsid2, None, 2011-10-19 12:30:00, testinstrument, DO, 12.0, <12, %, 22.0, testcomment)])'''
        assert test_string == reference_string

        test_string = utils_for_tests.create_test_string(
            utils.sql_load_fr_db(u'''select * from zz_staff'''))
        reference_string = ur'''(True, [])'''
        assert test_string == reference_string


class _TestWlevelsImport(object):
    answer_yes = mock_answer('yes')
    answer_no = mock_answer('no')
    CRS_question = MockUsingReturnValue([3006])
    mocked_iface = MockQgisUtilsIface()  #Used for not getting messageBar errors
    mock_askuser = MockReturnUsingDictIn({u'It is a strong': answer_no.get_v(), u'Please note!\nThere are ': answer_yes.get_v(), u'Please note!\nForeign keys will': answer_yes.get_v()}, 1)
    skip_popup = MockUsingReturnValue('')
    mock_encoding = MockUsingReturnValue([True, u'utf-8'])

    @mock.patch('create_db.utils.NotFoundQuestion')
    @mock.patch('midvatten_utils.askuser', answer_yes.get_v)
    @mock.patch('midvatten_utils.QgsProject.instance')
    @mock.patch('create_db.PyQt4.QtGui.QInputDialog.getInteger')
    @mock.patch('create_db.PyQt4.QtGui.QFileDialog.getSaveFileName')
    def setUp(self, mock_savefilename, mock_crsquestion, mock_qgsproject_instance, mock_locale):
        mock_crsquestion.return_value = [3006]
        mock_savefilename.return_value = TEMP_DB_PATH
        mock_qgsproject_instance.return_value.readEntry = MIDV_DICT

        self.dummy_iface = DummyInterface2()
        self.iface = self.dummy_iface.mock
        self.midvatten = midvatten(self.iface)

        try:
            os.remove(TEMP_DB_PATH)
        except OSError:
            pass
        mock_locale.return_value.answer = u'ok'
        mock_locale.return_value.value = u'sv_SE'
        self.midvatten.new_db()
        self.importinstance = midv_data_importer()

    def tearDown(self):
        #Delete database
        os.remove(TEMP_DB_PATH)

    @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
    def test_w_level_import_from_csvlayer(self):
        self.importinstance.charsetchoosen = [u'utf-8']

        utils.sql_alter_db(u'INSERT INTO obs_points ("obsid") VALUES ("obsid1")')
        f = [[u'obsid', u'date_time', u'meas', u'comment'],
             [u'obsid1', u'2011-10-19 12:30:00', u'2', u'testcomment']]

        with utils.tempinput(u'\n'.join([u';'.join(_x) for _x in f])) as filename:

            @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
            @mock.patch('import_data_to_db.utils.askuser')
            @mock.patch('qgis.utils.iface', autospec=True)
            @mock.patch('PyQt4.QtGui.QInputDialog.getText')
            @mock.patch('import_data_to_db.utils.pop_up_info', autospec=True)
            @mock.patch('import_data_to_db.PyQt4.QtGui.QFileDialog.getOpenFileName')
            def _test_wlvl_import_from_csvlayer(self, filename, mock_filename, mock_skippopup, mock_encoding, mock_iface, mock_askuser):
                mock_filename.return_value = filename
                mock_encoding.return_value = [True, u'utf-8']
                self.mock_iface = mock_iface
                self.importinstance.general_csv_import(goal_table=u'w_levels')
            _test_wlvl_import_from_csvlayer(self, filename)

        test_string = utils_for_tests.create_test_string(utils.sql_load_fr_db(u'''select * from w_levels'''))
        reference_string = ur'''(True, [(obsid1, 2011-10-19 12:30:00, 2.0, None, None, testcomment)])'''
        assert test_string == reference_string

    @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
    def _test_w_level_import_from_csvlayer_missing_columns(self):
        self.importinstance.charsetchoosen = [u'utf-8']

        utils.sql_alter_db(u'INSERT INTO obs_points ("obsid") VALUES ("obsid1")')
        #f = [[u'obsid', u'date_time', u'meas', u'comment'],
        #     [u'obsid1', u'2011-10-19 12:30:00', u'2', u'testcomment']]
        f = [[u'obsid', u'date_time', u'meas'],
             [u'obsid1', u'2011-10-19 12:30:00', u'2']]

        with utils.tempinput(u'\n'.join([u';'.join(_x) for _x in f])) as filename:

            @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
            @mock.patch('import_data_to_db.utils.askuser')
            @mock.patch('qgis.utils.iface', autospec=True)
            @mock.patch('PyQt4.QtGui.QInputDialog.getText')
            @mock.patch('import_data_to_db.utils.pop_up_info', autospec=True)
            @mock.patch('import_data_to_db.PyQt4.QtGui.QFileDialog.getOpenFileName')
            def _test_wlvl_import_from_csvlayer(self, filename, mock_filename, mock_skippopup, mock_encoding, mock_iface, mock_askuser):
                mock_filename.return_value = filename
                mock_encoding.return_value = [True, u'utf-8']
                self.mock_iface = mock_iface
                self.importinstance.general_csv_import(goal_table=u'w_levels')
            _test_wlvl_import_from_csvlayer(self, filename)

        test_string = utils_for_tests.create_test_string(utils.sql_load_fr_db(u'''select * from w_levels'''))
        reference_string = ur'''(True, [])'''
        assert test_string == reference_string


class _TestWlevelsImportOldWlevels(object):
    """
    This test is for an older version of w_levels where level_masl was not null
    but had a default value of -999
    """
    answer_yes = mock_answer('yes')
    answer_no = mock_answer('no')
    CRS_question = MockUsingReturnValue([3006])
    mocked_iface = MockQgisUtilsIface()  #Used for not getting messageBar errors
    mock_askuser = MockReturnUsingDictIn({u'It is a strong': answer_no.get_v(), u'Please note!\nThere are ': answer_yes.get_v(), u'Please note!\nForeign keys will': answer_yes.get_v()}, 1)
    skip_popup = MockUsingReturnValue('')
    mock_encoding = MockUsingReturnValue([True, u'utf-8'])

    @mock.patch('create_db.utils.NotFoundQuestion')
    @mock.patch('midvatten_utils.askuser', answer_yes.get_v)
    @mock.patch('midvatten_utils.QgsProject.instance')
    @mock.patch('create_db.PyQt4.QtGui.QInputDialog.getInteger')
    @mock.patch('create_db.PyQt4.QtGui.QFileDialog.getSaveFileName')
    def setUp(self, mock_savefilename, mock_crsquestion, mock_qgsproject_instance, mock_locale):
        mock_crsquestion.return_value = [3006]
        mock_savefilename.return_value = TEMP_DB_PATH
        mock_qgsproject_instance.return_value.readEntry = MIDV_DICT

        self.dummy_iface = DummyInterface2()
        self.iface = self.dummy_iface.mock
        self.midvatten = midvatten(self.iface)

        try:
            os.remove(TEMP_DB_PATH)
        except OSError:
            pass
        mock_locale.return_value.answer = u'ok'
        mock_locale.return_value.value = u'sv_SE'
        self.midvatten.new_db()

        utils.sql_alter_db(u'drop table w_levels')
        utils.sql_alter_db(u'CREATE TABLE "w_levels" ("obsid" text not null, "date_time" text not null, "meas" double, "h_toc" double, "level_masl" double not null default -999, "comment" text, primary key (obsid, date_time), foreign key(obsid) references obs_points(obsid))')

        self.importinstance = midv_data_importer()

    def tearDown(self):
        #Delete database
        os.remove(TEMP_DB_PATH)

    @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
    def test_w_level_import_from_csvlayer(self):
        self.importinstance.charsetchoosen = [u'utf-8']

        utils.sql_alter_db(u'INSERT INTO obs_points ("obsid") VALUES ("obsid1")')
        f = [[u'obsid', u'date_time', u'meas', u'comment'],
             [u'obsid1', u'2011-10-19 12:30:00', u'2', u'testcomment']]

        with utils.tempinput(u'\n'.join([u';'.join(_x) for _x in f])) as filename:

            @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
            @mock.patch('import_data_to_db.utils.askuser')
            @mock.patch('qgis.utils.iface', autospec=True)
            @mock.patch('PyQt4.QtGui.QInputDialog.getText')
            @mock.patch('import_data_to_db.utils.pop_up_info', autospec=True)
            @mock.patch('import_data_to_db.PyQt4.QtGui.QFileDialog.getOpenFileName')
            def _test_wlvl_import_from_csvlayer(self, filename, mock_filename, mock_skippopup, mock_encoding, mock_iface, mock_askuser):
                mock_filename.return_value = filename
                mock_encoding.return_value = [True, u'utf-8']
                self.mock_iface = mock_iface
                self.importinstance.general_csv_import(goal_table=u'w_levels')
            _test_wlvl_import_from_csvlayer(self, filename)

        test_string = utils_for_tests.create_test_string(utils.sql_load_fr_db(u'''select * from w_levels'''))
        reference_string = ur'''(True, [(obsid1, 2011-10-19 12:30:00, 2.0, None, -999.0, testcomment)])'''
        assert test_string == reference_string

    @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
    def _test_w_level_import_from_csvlayer_missing_columns(self):
        self.importinstance.charsetchoosen = [u'utf-8']

        utils.sql_alter_db(u'INSERT INTO obs_points ("obsid") VALUES ("obsid1")')
        #f = [[u'obsid', u'date_time', u'meas', u'comment'],
        #     [u'obsid1', u'2011-10-19 12:30:00', u'2', u'testcomment']]
        f = [[u'obsid', u'date_time', u'meas'],
             [u'obsid1', u'2011-10-19 12:30:00', u'2']]

        with utils.tempinput(u'\n'.join([u';'.join(_x) for _x in f])) as filename:

            @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
            @mock.patch('import_data_to_db.utils.askuser')
            @mock.patch('qgis.utils.iface', autospec=True)
            @mock.patch('PyQt4.QtGui.QInputDialog.getText')
            @mock.patch('import_data_to_db.utils.pop_up_info', autospec=True)
            @mock.patch('import_data_to_db.PyQt4.QtGui.QFileDialog.getOpenFileName')
            def _test_wlvl_import_from_csvlayer(self, filename, mock_filename, mock_skippopup, mock_encoding, mock_iface, mock_askuser):
                mock_filename.return_value = filename
                mock_encoding.return_value = [True, u'utf-8']
                self.mock_iface = mock_iface
                self.importinstance.general_csv_import(goal_table=u'w_levels')
            _test_wlvl_import_from_csvlayer(self, filename)

        test_string = utils_for_tests.create_test_string(utils.sql_load_fr_db(u'''select * from w_levels'''))
        reference_string = ur'''(True, [])'''
        assert test_string == reference_string


class _TestSeismicImport(object):
    answer_yes = mock_answer('yes')
    answer_no = mock_answer('no')
    CRS_question = MockUsingReturnValue([3006])
    mocked_iface = MockQgisUtilsIface()  #Used for not getting messageBar errors
    mock_askuser = MockReturnUsingDictIn({u'It is a strong': answer_no.get_v(), u'Please note!\nThere are ': answer_yes.get_v(), u'Please note!\nForeign keys will': answer_yes.get_v()}, 1)
    skip_popup = MockUsingReturnValue('')
    mock_encoding = MockUsingReturnValue([True, u'utf-8'])

    @mock.patch('create_db.utils.NotFoundQuestion')
    @mock.patch('midvatten_utils.askuser', answer_yes.get_v)
    @mock.patch('midvatten_utils.QgsProject.instance')
    @mock.patch('create_db.PyQt4.QtGui.QInputDialog.getInteger')
    @mock.patch('create_db.PyQt4.QtGui.QFileDialog.getSaveFileName')
    def setUp(self, mock_savefilename, mock_crsquestion, mock_qgsproject_instance, mock_locale):
        mock_crsquestion.return_value = [3006]
        mock_savefilename.return_value = TEMP_DB_PATH
        mock_qgsproject_instance.return_value.readEntry = MIDV_DICT

        self.dummy_iface = DummyInterface2()
        self.iface = self.dummy_iface.mock
        self.midvatten = midvatten(self.iface)

        try:
            os.remove(TEMP_DB_PATH)
        except OSError:
            pass
        mock_locale.return_value.answer = u'ok'
        mock_locale.return_value.value = u'sv_SE'
        self.midvatten.new_db()
        self.importinstance = midv_data_importer()

    def tearDown(self):
        #Delete database
        os.remove(TEMP_DB_PATH)

    @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
    def test_seismic_import_from_csvlayer(self):
        self.importinstance.charsetchoosen = [u'utf-8']

        utils.sql_alter_db(u'INSERT INTO obs_lines ("obsid") VALUES ("obsid1")')
        f = [[u'obsid', u'length', u'ground', u'bedrock', u'gw_table', u'comment'],
             [u'obsid1', u'500', u'2', u'4', u'3', u'acomment']]

        with utils.tempinput(u'\n'.join([u';'.join(_x) for _x in f])) as filename:

            @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
            @mock.patch('import_data_to_db.utils.askuser')
            @mock.patch('qgis.utils.iface', autospec=True)
            @mock.patch('PyQt4.QtGui.QInputDialog.getText')
            @mock.patch('import_data_to_db.utils.pop_up_info', autospec=True)
            @mock.patch('import_data_to_db.PyQt4.QtGui.QFileDialog.getOpenFileName')
            def _test_import_seismic_from_csvlayer(self, filename, mock_filename, mock_skippopup, mock_encoding, mock_iface, mock_askuser):
                mock_filename.return_value = filename
                mock_encoding.return_value = [True, u'utf-8']
                self.mock_iface = mock_iface
                self.importinstance.general_csv_import(goal_table=u'seismic_data')
            _test_import_seismic_from_csvlayer(self, filename)

        test_string = utils_for_tests.create_test_string(utils.sql_load_fr_db(u'''select * from seismic_data'''))
        reference_string = ur'''(True, [(obsid1, 500.0, 2.0, 4.0, 3.0, acomment)])'''
        assert test_string == reference_string


class _TestCommentsImport(object):
    answer_yes = mock_answer('yes')
    answer_no = mock_answer('no')
    CRS_question = MockUsingReturnValue([3006])
    mocked_iface = MockQgisUtilsIface()  #Used for not getting messageBar errors
    mock_askuser = MockReturnUsingDictIn({u'It is a strong': answer_no.get_v(), u'Please note!\nThere are ': answer_yes.get_v(), u'Please note!\nForeign keys will': answer_yes.get_v()}, 1)
    skip_popup = MockUsingReturnValue('')
    mock_encoding = MockUsingReturnValue([True, u'utf-8'])

    @mock.patch('create_db.utils.NotFoundQuestion')
    @mock.patch('midvatten_utils.askuser', answer_yes.get_v)
    @mock.patch('midvatten_utils.QgsProject.instance')
    @mock.patch('create_db.PyQt4.QtGui.QInputDialog.getInteger')
    @mock.patch('create_db.PyQt4.QtGui.QFileDialog.getSaveFileName')
    def setUp(self, mock_savefilename, mock_crsquestion, mock_qgsproject_instance, mock_locale):
        mock_crsquestion.return_value = [3006]
        mock_savefilename.return_value = TEMP_DB_PATH
        mock_qgsproject_instance.return_value.readEntry = MIDV_DICT

        self.dummy_iface = DummyInterface2()
        self.iface = self.dummy_iface.mock
        self.midvatten = midvatten(self.iface)

        try:
            os.remove(TEMP_DB_PATH)
        except OSError:
            pass
        mock_locale.return_value.answer = u'ok'
        mock_locale.return_value.value = u'sv_SE'
        self.midvatten.new_db()
        self.importinstance = midv_data_importer()

    def tearDown(self):
        #Delete database
        os.remove(TEMP_DB_PATH)

    @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
    def test_comments_import_from_csvlayer(self):
        self.importinstance.charsetchoosen = [u'utf-8']

        utils.sql_alter_db(u'INSERT INTO obs_points ("obsid") VALUES ("obsid1")')
        f = [[u'obsid', u'date_time', u'comment', u'staff'],
             [u'obsid1', u'2011-10-19 12:30:00', u'testcomment', u'teststaff']]

        with utils.tempinput(u'\n'.join([u';'.join(_x) for _x in f])) as filename:

            @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
            @mock.patch('import_data_to_db.utils.askuser')
            @mock.patch('qgis.utils.iface', autospec=True)
            @mock.patch('PyQt4.QtGui.QInputDialog.getText')
            @mock.patch('import_data_to_db.utils.pop_up_info', autospec=True)
            @mock.patch('import_data_to_db.PyQt4.QtGui.QFileDialog.getOpenFileName')
            def _test_wlvl_import_from_csvlayer(self, filename, mock_filename, mock_skippopup, mock_encoding, mock_iface, mock_askuser):
                mock_filename.return_value = filename
                mock_encoding.return_value = [True, u'utf-8']
                self.mock_iface = mock_iface
                self.importinstance.general_csv_import(goal_table=u'comments')
            _test_wlvl_import_from_csvlayer(self, filename)

        test_string = utils_for_tests.create_test_string(utils.sql_load_fr_db(u'''select * from comments'''))
        reference_string = ur'''(True, [(obsid1, 2011-10-19 12:30:00, testcomment, teststaff)])'''
        assert test_string == reference_string


class _TestStratImport(object):
    answer_yes = mock_answer('yes')
    answer_no = mock_answer('no')
    CRS_question = MockUsingReturnValue([3006])
    mocked_iface = MockQgisUtilsIface()  #Used for not getting messageBar errors
    mock_askuser = MockReturnUsingDictIn({u'It is a strong': answer_no.get_v(), u'Please note!\nThere are ': answer_yes.get_v(), u'Please note!\nForeign keys will': answer_yes.get_v()}, 1)
    skip_popup = MockUsingReturnValue('')
    mock_encoding = MockUsingReturnValue([True, u'utf-8'])

    @mock.patch('create_db.utils.NotFoundQuestion')
    @mock.patch('midvatten_utils.askuser', answer_yes.get_v)
    @mock.patch('midvatten_utils.QgsProject.instance')
    @mock.patch('create_db.PyQt4.QtGui.QInputDialog.getInteger')
    @mock.patch('create_db.PyQt4.QtGui.QFileDialog.getSaveFileName')
    def setUp(self, mock_savefilename, mock_crsquestion, mock_qgsproject_instance, mock_locale):
        mock_crsquestion.return_value = [3006]
        mock_savefilename.return_value = TEMP_DB_PATH
        mock_qgsproject_instance.return_value.readEntry = MIDV_DICT

        self.dummy_iface = DummyInterface2()
        self.iface = self.dummy_iface.mock
        self.midvatten = midvatten(self.iface)

        try:
            os.remove(TEMP_DB_PATH)
        except OSError:
            pass
        mock_locale.return_value.answer = u'ok'
        mock_locale.return_value.value = u'sv_SE'
        self.midvatten.new_db()
        self.importinstance = midv_data_importer()

    def tearDown(self):
        #Delete database
        os.remove(TEMP_DB_PATH)

    @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
    def test_strat_import_from_csvlayer(self):
        self.importinstance.charsetchoosen = [u'utf-8']

        utils.sql_alter_db(u'INSERT INTO obs_points ("obsid") VALUES ("obsid1")')
        f = [[u'obsid', u'stratid', u'depthtop', u'depthbot', u'geology', u'geoshort', u'capacity', u'development', u'comment'],
             [u'obsid1', u'1', u'0', u'1', u'grusig sand', u'sand', u'5', u'(j)', u'acomment'],
             [u'obsid1', u'2', u'1', u'4', u'siltigt sandigt grus', u'grus', u'4+', u'(j)', u'acomment2']]

        with utils.tempinput(u'\n'.join([u';'.join(_x) for _x in f])) as filename:

            @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
            @mock.patch('import_data_to_db.utils.askuser')
            @mock.patch('qgis.utils.iface', autospec=True)
            @mock.patch('PyQt4.QtGui.QInputDialog.getText')
            @mock.patch('import_data_to_db.utils.pop_up_info', autospec=True)
            @mock.patch('import_data_to_db.PyQt4.QtGui.QFileDialog.getOpenFileName')
            def _test(self, filename, mock_filename, mock_skippopup, mock_encoding, mock_iface, mock_askuser):
                mock_filename.return_value = filename
                mock_encoding.return_value = [True, u'utf-8']
                self.mock_iface = mock_iface
                self.importinstance.general_csv_import(goal_table=u'stratigraphy') #goal_table=u'stratigraphy')
            _test(self, filename)

        test_string = utils_for_tests.create_test_string(utils.sql_load_fr_db(u'''select * from stratigraphy'''))
        reference_string = u'''(True, [(obsid1, 1, 0.0, 1.0, grusig sand, sand, 5, (j), acomment), (obsid1, 2, 1.0, 4.0, siltigt sandigt grus, grus, 4+, (j), acomment2)])'''
        assert test_string == reference_string

    @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
    def test_strat_import_from_csvlayer_eleven_layers(self):
        self.importinstance.charsetchoosen = [u'utf-8']

        utils.sql_alter_db(u'INSERT INTO obs_points ("obsid") VALUES ("obsid1")')
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

        with utils.tempinput(u'\n'.join([u';'.join(_x) for _x in f])) as filename:

            @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
            @mock.patch('import_data_to_db.utils.askuser')
            @mock.patch('qgis.utils.iface', autospec=True)
            @mock.patch('PyQt4.QtGui.QInputDialog.getText')
            @mock.patch('import_data_to_db.utils.pop_up_info', autospec=True)
            @mock.patch('import_data_to_db.PyQt4.QtGui.QFileDialog.getOpenFileName')
            def _test(self, filename, mock_filename, mock_skippopup, mock_encoding, mock_iface, mock_askuser):
                mock_filename.return_value = filename
                mock_encoding.return_value = [True, u'utf-8']
                self.mock_iface = mock_iface
                self.importinstance.general_csv_import(goal_table=u'stratigraphy') #goal_table=u'stratigraphy')
            _test(self, filename)

        test_string = utils_for_tests.create_test_string(utils.sql_load_fr_db(u'''select * from stratigraphy'''))
        reference_string = u'''(True, [(obsid1, 1, 0.0, 1.0, s, s, 1, (j), acomment), (obsid1, 2, 1.0, 2.0, s, s, 1, (j), acomment), (obsid1, 3, 2.0, 3.0, s, s, 1, (j), acomment), (obsid1, 4, 3.0, 4.0, s, s, 1, (j), acomment), (obsid1, 5, 4.0, 5.0, s, s, 1, (j), acomment), (obsid1, 6, 5.0, 6.0, s, s, 1, (j), acomment), (obsid1, 7, 6.0, 7.0, s, s, 1, (j), acomment), (obsid1, 8, 7.0, 8.0, s, s, 1, (j), acomment), (obsid1, 9, 8.0, 9.0, s, s, 1, (j), acomment), (obsid1, 10, 9.0, 12.1, s, s, 1, (j), acomment), (obsid1, 11, 12.1, 13.0, s, s, 1, (j), acomment)])'''
        assert test_string == reference_string

    @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
    def test_strat_import_one_obs_fail_stratid_gaps(self):
        self.importinstance.charsetchoosen = [u'utf-8']

        utils.sql_alter_db(u'INSERT INTO obs_points ("obsid") VALUES ("obsid1")')
        f = [[u'obsid', u'stratid', u'depthtop', u'depthbot', u'geology', u'geoshort', u'capacity', u'development', u'comment'],
             [u'obsid1', u'1', u'0', u'1', u'grusig sand', u'sand', u'5', u'(j)', u'acomment'],
             [u'obsid1', u'2', u'1', u'4', u'siltigt sandigt grus', u'grus', u'4+', u'(j)', u'acomment2'],
             [u'obsid2', u'1', u'0', u'1', u'grusig sand', u'sand', u'5', u'(j)', u'acomment'],
             [u'obsid2', u'3', u'1', u'4', u'siltigt sandigt grus', u'grus', u'4+', u'(j)', u'acomment2']]

        with utils.tempinput(u'\n'.join([u';'.join(_x) for _x in f])) as filename:

            @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
            @mock.patch('import_data_to_db.utils.askuser')
            @mock.patch('qgis.utils.iface', autospec=True)
            @mock.patch('PyQt4.QtGui.QInputDialog.getText')
            @mock.patch('import_data_to_db.utils.pop_up_info', autospec=True)
            @mock.patch('import_data_to_db.PyQt4.QtGui.QFileDialog.getOpenFileName')
            def _test(self, filename, mock_filename, mock_skippopup, mock_encoding, mock_iface, mock_askuser):
                mock_filename.return_value = filename
                mock_encoding.return_value = [True, u'utf-8']
                self.mock_iface = mock_iface
                self.importinstance.general_csv_import(goal_table=u'stratigraphy') #goal_table=u'stratigraphy')
            _test(self, filename)

        test_string = utils_for_tests.create_test_string(utils.sql_load_fr_db(u'''select * from stratigraphy'''))
        reference_string = u'''(True, [(obsid1, 1, 0.0, 1.0, grusig sand, sand, 5, (j), acomment), (obsid1, 2, 1.0, 4.0, siltigt sandigt grus, grus, 4+, (j), acomment2)])'''
        assert test_string == reference_string

    @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
    def test_strat_import_one_obs_fail_depthbot_gaps(self):
        self.importinstance.charsetchoosen = [u'utf-8']

        utils.sql_alter_db(u'INSERT INTO obs_points ("obsid") VALUES ("obsid1")')
        f = [[u'obsid', u'stratid', u'depthtop', u'depthbot', u'geology', u'geoshort', u'capacity', u'development', u'comment'],
             [u'obsid1', u'1', u'0', u'1', u'grusig sand', u'sand', u'5', u'(j)', u'acomment'],
             [u'obsid1', u'2', u'1', u'4', u'siltigt sandigt grus', u'grus', u'4+', u'(j)', u'acomment2'],
             [u'obsid2', u'1', u'0', u'1', u'grusig sand', u'sand', u'5', u'(j)', u'acomment'],
             [u'obsid2', u'2', u'3', u'4', u'siltigt sandigt grus', u'grus', u'4+', u'(j)', u'acomment2']]

        with utils.tempinput(u'\n'.join([u';'.join(_x) for _x in f])) as filename:

            @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
            @mock.patch('import_data_to_db.utils.askuser')
            @mock.patch('qgis.utils.iface', autospec=True)
            @mock.patch('PyQt4.QtGui.QInputDialog.getText')
            @mock.patch('import_data_to_db.utils.pop_up_info', autospec=True)
            @mock.patch('import_data_to_db.PyQt4.QtGui.QFileDialog.getOpenFileName')
            def _test(self, filename, mock_filename, mock_skippopup, mock_encoding, mock_iface, mock_askuser):
                mock_filename.return_value = filename
                mock_encoding.return_value = [True, u'utf-8']
                self.mock_iface = mock_iface
                self.importinstance.general_csv_import(goal_table=u'stratigraphy') #goal_table=u'stratigraphy')
            _test(self, filename)

        test_string = utils_for_tests.create_test_string(utils.sql_load_fr_db(u'''select * from stratigraphy'''))
        reference_string = u'''(True, [(obsid1, 1, 0.0, 1.0, grusig sand, sand, 5, (j), acomment), (obsid1, 2, 1.0, 4.0, siltigt sandigt grus, grus, 4+, (j), acomment2)])'''
        assert test_string == reference_string


class _TestMeteoImport(object):
    answer_yes = mock_answer('yes')
    answer_no = mock_answer('no')
    CRS_question = MockUsingReturnValue([3006])
    mocked_iface = MockQgisUtilsIface()  #Used for not getting messageBar errors
    mock_askuser = MockReturnUsingDictIn({u'It is a strong': answer_no.get_v(), u'Please note!\nThere are ': answer_yes.get_v(), u'Please note!\nForeign keys will': answer_yes.get_v()}, 1)
    skip_popup = MockUsingReturnValue('')
    mock_encoding = MockUsingReturnValue([True, u'utf-8'])

    @mock.patch('create_db.utils.NotFoundQuestion')
    @mock.patch('midvatten_utils.askuser', answer_yes.get_v)
    @mock.patch('midvatten_utils.QgsProject.instance')
    @mock.patch('create_db.PyQt4.QtGui.QInputDialog.getInteger')
    @mock.patch('create_db.PyQt4.QtGui.QFileDialog.getSaveFileName')
    def setUp(self, mock_savefilename, mock_crsquestion, mock_qgsproject_instance, mock_locale):
        mock_crsquestion.return_value = [3006]
        mock_savefilename.return_value = TEMP_DB_PATH
        mock_qgsproject_instance.return_value.readEntry = MIDV_DICT

        self.dummy_iface = DummyInterface2()
        self.iface = self.dummy_iface.mock
        self.midvatten = midvatten(self.iface)

        try:
            os.remove(TEMP_DB_PATH)
        except OSError:
            pass
        mock_locale.return_value.answer = u'ok'
        mock_locale.return_value.value = u'sv_SE'
        self.midvatten.new_db()
        self.importinstance = midv_data_importer()

    def tearDown(self):
        #Delete database
        os.remove(TEMP_DB_PATH)

    @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
    def test_meteo_import_from_csvlayer(self):
        self.importinstance.charsetchoosen = [u'utf-8']

        utils.sql_alter_db(u'INSERT INTO obs_points ("obsid") VALUES ("obsid1")')
        f = [[u'obsid', u'instrumentid', u'parameter', u'date_time', u'reading_num', u'reading_txt', u'unit', u'comment'],
             [u'obsid1', u'ints1', u'pressure', u'2016-01-01 00:00:00', u'1100', u'1100', u'aunit', u'acomment']]
        with utils.tempinput(u'\n'.join([u';'.join(_x) for _x in f])) as filename:

            @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
            @mock.patch('import_data_to_db.utils.askuser')
            @mock.patch('qgis.utils.iface', autospec=True)
            @mock.patch('PyQt4.QtGui.QInputDialog.getText')
            @mock.patch('import_data_to_db.utils.pop_up_info', autospec=True)
            @mock.patch('import_data_to_db.PyQt4.QtGui.QFileDialog.getOpenFileName')
            def _test_import_meteo_from_csvlayer(self, filename, mock_filename, mock_skippopup, mock_encoding, mock_iface, mock_askuser):
                mock_filename.return_value = filename
                mock_encoding.return_value = [True, u'utf-8']
                self.mock_iface = mock_iface
                self.importinstance.general_csv_import(goal_table=u'meteo')
            _test_import_meteo_from_csvlayer(self, filename)

        test_string = utils_for_tests.create_test_string(utils.sql_load_fr_db(u'''select * from meteo'''))
        reference_string = u'''(True, [(obsid1, ints1, pressure, 2016-01-01 00:00:00, 1100.0, 1100, aunit, acomment)])'''
        assert test_string == reference_string


class _TestVlfImport(object):
    answer_yes = mock_answer('yes')
    answer_no = mock_answer('no')
    CRS_question = MockUsingReturnValue([3006])
    mocked_iface = MockQgisUtilsIface()  #Used for not getting messageBar errors
    mock_askuser = MockReturnUsingDictIn({u'It is a strong': answer_no.get_v(), u'Please note!\nThere are ': answer_yes.get_v(), u'Please note!\nForeign keys will': answer_yes.get_v()}, 1)
    skip_popup = MockUsingReturnValue('')
    mock_encoding = MockUsingReturnValue([True, u'utf-8'])

    @mock.patch('create_db.utils.NotFoundQuestion')
    @mock.patch('midvatten_utils.askuser', answer_yes.get_v)
    @mock.patch('midvatten_utils.QgsProject.instance')
    @mock.patch('create_db.PyQt4.QtGui.QInputDialog.getInteger')
    @mock.patch('create_db.PyQt4.QtGui.QFileDialog.getSaveFileName')
    def setUp(self, mock_savefilename, mock_crsquestion, mock_qgsproject_instance, mock_locale):
        mock_crsquestion.return_value = [3006]
        mock_savefilename.return_value = TEMP_DB_PATH
        mock_qgsproject_instance.return_value.readEntry = MIDV_DICT

        self.dummy_iface = DummyInterface2()
        self.iface = self.dummy_iface.mock
        self.midvatten = midvatten(self.iface)

        try:
            os.remove(TEMP_DB_PATH)
        except OSError:
            pass
        mock_locale.return_value.answer = u'ok'
        mock_locale.return_value.value = u'sv_SE'
        self.midvatten.new_db()
        self.importinstance = midv_data_importer()

    def tearDown(self):
        #Delete database
        os.remove(TEMP_DB_PATH)

    @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
    def test_vlf_import_from_csvlayer(self):
        self.importinstance.charsetchoosen = [u'utf-8']

        utils.sql_alter_db(u'INSERT INTO obs_lines ("obsid") VALUES ("obsid1")')
        f = [[u'obsid', u'length', u'real_comp', u'imag_comp', u'comment'],
             [u'obsid1', u'500', u'2', u'10', u'acomment']]
        with utils.tempinput(u'\n'.join([u';'.join(_x) for _x in f])) as filename:

            @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
            @mock.patch('import_data_to_db.utils.askuser')
            @mock.patch('qgis.utils.iface', autospec=True)
            @mock.patch('PyQt4.QtGui.QInputDialog.getText')
            @mock.patch('import_data_to_db.utils.pop_up_info', autospec=True)
            @mock.patch('import_data_to_db.PyQt4.QtGui.QFileDialog.getOpenFileName')
            def _test_import_vlf_from_csvlayer(self, filename, mock_filename, mock_skippopup, mock_encoding, mock_iface, mock_askuser):
                mock_filename.return_value = filename
                mock_encoding.return_value = [True, u'utf-8']
                self.mock_iface = mock_iface
                self.importinstance.general_csv_import(goal_table=u'vlf_data')
            _test_import_vlf_from_csvlayer(self, filename)

        test_string = utils_for_tests.create_test_string(utils.sql_load_fr_db(u'''select * from vlf_data'''))
        reference_string = u'''(True, [(obsid1, 500.0, 2.0, 10.0, acomment)])'''
        assert test_string == reference_string

    @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
    def test_vlf_import_from_csvlayer_no_obs_line(self):
        self.importinstance.charsetchoosen = [u'utf-8']

        f = [[u'obsid', u'length', u'real_comp', u'imag_comp', u'comment'],
             [u'obsid1', u'500', u'2', u'10', u'acomment']]
        with utils.tempinput(u'\n'.join([u';'.join(_x) for _x in f])) as filename:

            @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
            @mock.patch('import_data_to_db.utils.askuser')
            @mock.patch('qgis.utils.iface', autospec=True)
            @mock.patch('PyQt4.QtGui.QInputDialog.getText')
            @mock.patch('import_data_to_db.utils.pop_up_info', autospec=True)
            @mock.patch('import_data_to_db.PyQt4.QtGui.QFileDialog.getOpenFileName')
            def _test_import_vlf_from_csvlayer(self, filename, mock_filename, mock_skippopup, mock_encoding, mock_iface, mock_askuser):
                mock_filename.return_value = filename
                mock_encoding.return_value = [True, u'utf-8']
                self.mock_iface = mock_iface
                self.importinstance.general_csv_import(goal_table=u'vlf_data')
            _test_import_vlf_from_csvlayer(self, filename)

        test_string = utils_for_tests.create_test_string(utils.sql_load_fr_db(u'''select * from vlf_data'''))
        reference_string = u'''(True, [])'''
        assert test_string == reference_string


class TestObsLinesImport(object):
    answer_yes = mock_answer('yes')
    answer_no = mock_answer('no')
    CRS_question = MockUsingReturnValue([3006])
    mocked_iface = MockQgisUtilsIface()  #Used for not getting messageBar errors
    mock_askuser = MockReturnUsingDictIn({u'It is a strong': answer_no.get_v(), u'Please note!\nThere are ': answer_yes.get_v(), u'Please note!\nForeign keys will': answer_yes.get_v()}, 1)
    skip_popup = MockUsingReturnValue('')
    mock_encoding = MockUsingReturnValue([True, u'utf-8'])

    @mock.patch('create_db.utils.NotFoundQuestion')
    @mock.patch('midvatten_utils.askuser', answer_yes.get_v)
    @mock.patch('midvatten_utils.QgsProject.instance')
    @mock.patch('create_db.PyQt4.QtGui.QInputDialog.getInteger')
    @mock.patch('create_db.PyQt4.QtGui.QFileDialog.getSaveFileName')
    def setUp(self, mock_savefilename, mock_crsquestion, mock_qgsproject_instance, mock_locale):
        mock_crsquestion.return_value = [3006]
        mock_savefilename.return_value = TEMP_DB_PATH
        mock_qgsproject_instance.return_value.readEntry = MIDV_DICT

        self.dummy_iface = DummyInterface2()
        self.iface = self.dummy_iface.mock
        self.midvatten = midvatten(self.iface)

        try:
            os.remove(TEMP_DB_PATH)
        except OSError:
            pass
        mock_locale.return_value.answer = u'ok'
        mock_locale.return_value.value = u'sv_SE'
        self.midvatten.new_db()
        self.importinstance = midv_data_importer()

    def tearDown(self):
        #Delete database
        os.remove(TEMP_DB_PATH)

    @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
    def test_obs_lines_import_from_csvlayer(self):
        self.importinstance.charsetchoosen = [u'utf-8']

        f = [[u'obsid', u'name', u'place', u'type', u'source'],
             [u'obsid1', u'aname', u'aplace', u'atype', u'asource']]
        with utils.tempinput(u'\n'.join([u';'.join(_x) for _x in f])) as filename:

            @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
            @mock.patch('import_data_to_db.utils.askuser')
            @mock.patch('qgis.utils.iface', autospec=True)
            @mock.patch('PyQt4.QtGui.QInputDialog.getText')
            @mock.patch('import_data_to_db.utils.pop_up_info', autospec=True)
            @mock.patch('import_data_to_db.PyQt4.QtGui.QFileDialog.getOpenFileName')
            def _test_obs_lines_import_from_csvlayer(self, filename, mock_filename, mock_skippopup, mock_encoding, mock_iface, mock_askuser):
                mock_filename.return_value = filename
                mock_encoding.return_value = [True, u'utf-8']
                self.mock_iface = mock_iface
                self.importinstance.general_csv_import(goal_table=u'obs_lines')
            _test_obs_lines_import_from_csvlayer(self, filename)

        test_string = utils_for_tests.create_test_string(utils.sql_load_fr_db(u'''select * from obs_lines'''))
        reference_string = u'''(True, [(obsid1, aname, aplace, atype, asource, None)])'''
        assert test_string == reference_string


class _TestGetForeignKeys(object):
    answer_yes = mock_answer('yes')
    answer_no = mock_answer('no')
    CRS_question = MockUsingReturnValue([3006])
    mocked_iface = MockQgisUtilsIface()  #Used for not getting messageBar errors
    mock_askuser = MockReturnUsingDictIn({u'It is a strong': answer_no.get_v(), u'Please note!\nThere are ': answer_yes.get_v(), u'Please note!\nForeign keys will': answer_yes.get_v()}, 1)
    skip_popup = MockUsingReturnValue('')
    mock_encoding = MockUsingReturnValue([True, u'utf-8'])

    @mock.patch('create_db.utils.NotFoundQuestion')
    @mock.patch('midvatten_utils.askuser', answer_yes.get_v)
    @mock.patch('midvatten_utils.QgsProject.instance')
    @mock.patch('create_db.PyQt4.QtGui.QInputDialog.getInteger')
    @mock.patch('create_db.PyQt4.QtGui.QFileDialog.getSaveFileName')
    def setUp(self, mock_savefilename, mock_crsquestion, mock_qgsproject_instance, mock_locale):
        mock_crsquestion.return_value = [3006]
        mock_savefilename.return_value = TEMP_DB_PATH
        mock_qgsproject_instance.return_value.readEntry = MIDV_DICT

        self.dummy_iface = DummyInterface2()
        self.iface = self.dummy_iface.mock
        self.midvatten = midvatten(self.iface)

        try:
            os.remove(TEMP_DB_PATH)
        except OSError:
            pass
        mock_locale.return_value.answer = u'ok'
        mock_locale.return_value.value = u'sv_SE'
        self.midvatten.new_db()
        self.importinstance = midv_data_importer()

    def tearDown(self):
        #Delete database
        os.remove(TEMP_DB_PATH)

    @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
    @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
    @mock.patch('import_data_to_db.utils.askuser')
    @mock.patch('qgis.utils.iface', autospec=True)
    @mock.patch('PyQt4.QtGui.QInputDialog.getText')
    @mock.patch('import_data_to_db.utils.pop_up_info', autospec=True)
    @mock.patch('import_data_to_db.PyQt4.QtGui.QFileDialog.getOpenFileName')
    def test_get_foreign_columns(self, mock_filename, mock_skippopup, mock_encoding, mock_iface, mock_askuser):
        mock_encoding.return_value = [True, u'utf-8']
        self.mock_iface = mock_iface
        self.importinstance.charsetchoosen = [u'utf-8']

        test = get_foreign_keys(u'w_levels')
        assert len(test) > 0
        assert isinstance(test, (dict, OrderedDict))
        for k, v in test.iteritems():
            assert isinstance(v, (list, tuple))


class _TestFilterDatesFromFiledata(object):

    def setUp(self):
        self.importinstance = midv_data_importer()

    def test_filter_dates_from_filedata(self):

        file_data = [[u'obsid', u'date_time'], [u'rb1', u'2015-05-01 00:00:00'], [u'rb1', u'2016-05-01 00:00'], [u'rb2', u'2015-05-01 00:00:00'], [u'rb2', u'2016-05-01 00:00'], [u'rb3', u'2015-05-01 00:00:00'], [u'rb3', u'2016-05-01 00:00']]
        obsid_last_imported_dates = {u'rb1': [(datestring_to_date(u'2016-01-01 00:00:00'),)], u'rb2': [(datestring_to_date(u'2017-01-01 00:00:00'),)]}
        test_file_data = utils_for_tests.create_test_string(self.importinstance.filter_dates_from_filedata(file_data, obsid_last_imported_dates))

        reference_file_data = u'''[[obsid, date_time], [rb1, 2016-05-01 00:00], [rb3, 2015-05-01 00:00:00], [rb3, 2016-05-01 00:00]]'''

        assert test_file_data == reference_file_data


class _TestDeleteExistingDateTimesFromTemptable(object):
    answer_yes = mock_answer('yes')
    answer_no = mock_answer('no')
    CRS_question = MockUsingReturnValue([3006])
    mocked_iface = MockQgisUtilsIface()  #Used for not getting messageBar errors
    mock_askuser = MockReturnUsingDictIn({u'It is a strong': answer_no.get_v(), u'Please note!\nThere are ': answer_yes.get_v(), u'Please note!\nForeign keys will': answer_yes.get_v()}, 1)
    skip_popup = MockUsingReturnValue('')
    mock_encoding = MockUsingReturnValue([True, u'utf-8'])

    @mock.patch('create_db.utils.NotFoundQuestion')
    @mock.patch('midvatten_utils.askuser', answer_yes.get_v)
    @mock.patch('midvatten_utils.QgsProject.instance')
    @mock.patch('create_db.PyQt4.QtGui.QInputDialog.getInteger')
    @mock.patch('create_db.PyQt4.QtGui.QFileDialog.getSaveFileName')
    def setUp(self, mock_savefilename, mock_crsquestion, mock_qgsproject_instance, mock_locale):
        mock_crsquestion.return_value = [3006]
        mock_savefilename.return_value = TEMP_DB_PATH
        mock_qgsproject_instance.return_value.readEntry = MIDV_DICT

        self.dummy_iface = DummyInterface2()
        self.iface = self.dummy_iface.mock
        self.midvatten = midvatten(self.iface)

        try:
            os.remove(TEMP_DB_PATH)
        except OSError:
            pass
        mock_locale.return_value.answer = u'ok'
        mock_locale.return_value.value = u'sv_SE'
        self.midvatten.new_db()
        self.importinstance = midv_data_importer()

    def tearDown(self):
        #Delete database
        os.remove(TEMP_DB_PATH)

    @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
    def test_delete_existing_date_times_from_temptable_00_already_exists(self):
        self.importinstance.charsetchoosen = [u'utf-8']

        utils.sql_alter_db(u'INSERT INTO obs_points ("obsid") VALUES ("obsid1")')
        utils.sql_alter_db(u'INSERT INTO w_levels ("obsid", "date_time", "level_masl") VALUES ("obsid1", "2016-01-01 00:00:00", "123.0")')

        f = [[u'obsid', u'date_time', u'level_masl'],
             [u'obsid1', u'2016-01-01 00:00', u'345']]

        with utils.tempinput(u'\n'.join([u';'.join(_x) for _x in f])) as filename:

            @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
            @mock.patch('import_data_to_db.utils.askuser')
            @mock.patch('qgis.utils.iface', autospec=True)
            @mock.patch('PyQt4.QtGui.QInputDialog.getText')
            @mock.patch('import_data_to_db.utils.pop_up_info', autospec=True)
            @mock.patch('import_data_to_db.PyQt4.QtGui.QFileDialog.getOpenFileName')
            def _test(self, filename, mock_filename, mock_skippopup, mock_encoding, mock_iface, mock_askuser):
                mock_filename.return_value = filename
                mock_encoding.return_value = [True, u'utf-8']
                self.mock_iface = mock_iface
                self.importinstance.general_csv_import(goal_table=u'w_levels')
            _test(self, filename)

        test_string = utils_for_tests.create_test_string(utils.sql_load_fr_db(u'''select * from w_levels'''))
        reference_string = ur'''(True, [(obsid1, 2016-01-01 00:00:00, None, None, 123.0, None)])'''
        assert test_string == reference_string


    @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
    def test_delete_existing_date_times_from_temptable_00_already_exists(self):
        self.importinstance.charsetchoosen = [u'utf-8']

        utils.sql_alter_db(u'INSERT INTO obs_points ("obsid") VALUES ("obsid1")')
        utils.sql_alter_db(
            u'INSERT INTO w_levels ("obsid", "date_time", "level_masl") VALUES ("obsid1", "2016-01-01 00:00:00", "123.0")')

        f = [[u'obsid', u'date_time', u'level_masl'],
             [u'obsid1', u'2016-01-01 00:00', u'345']]

        with utils.tempinput(u'\n'.join([u';'.join(_x) for _x in f])) as filename:
            @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
            @mock.patch('import_data_to_db.utils.askuser')
            @mock.patch('qgis.utils.iface', autospec=True)
            @mock.patch('PyQt4.QtGui.QInputDialog.getText')
            @mock.patch('import_data_to_db.utils.pop_up_info', autospec=True)
            @mock.patch(
                'import_data_to_db.PyQt4.QtGui.QFileDialog.getOpenFileName')
            def _test(self, filename, mock_filename, mock_skippopup, mock_encoding,
                      mock_iface, mock_askuser):
                mock_filename.return_value = filename
                mock_encoding.return_value = [True, u'utf-8']
                self.mock_iface = mock_iface
                self.importinstance.general_csv_import(goal_table=u'w_levels')

            _test(self, filename)

        test_string = utils_for_tests.create_test_string(
            utils.sql_load_fr_db(u'''select * from w_levels'''))
        reference_string = ur'''(True, [(obsid1, 2016-01-01 00:00:00, None, None, 123.0, None)])'''
        assert test_string == reference_string

    @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
    def test_delete_existing_date_times_from_temptable_minute_already_exists(self):
        self.importinstance.charsetchoosen = [u'utf-8']

        utils.sql_alter_db(u'INSERT INTO obs_points ("obsid") VALUES ("obsid1")')
        utils.sql_alter_db(
            u'INSERT INTO w_levels ("obsid", "date_time", "level_masl") VALUES ("obsid1", "2016-01-01 00:00", "123.0")')

        f = [[u'obsid', u'date_time', u'level_masl'],
             [u'obsid1', u'2016-01-01 00:00:00', u'345'],
             [u'obsid1', u'2016-01-01 00:00:01', u'456'],
             [u'obsid1', u'2016-01-01 00:02:00', u'789']]

        with utils.tempinput(u'\n'.join([u';'.join(_x) for _x in f])) as filename:
            @mock.patch('midvatten_utils.QgsProject.instance', MOCK_DBPATH.get_v)
            @mock.patch('import_data_to_db.utils.askuser')
            @mock.patch('qgis.utils.iface', autospec=True)
            @mock.patch('PyQt4.QtGui.QInputDialog.getText')
            @mock.patch('import_data_to_db.utils.pop_up_info', autospec=True)
            @mock.patch(
                'import_data_to_db.PyQt4.QtGui.QFileDialog.getOpenFileName')
            def _test(self, filename, mock_filename, mock_skippopup, mock_encoding,
                      mock_iface, mock_askuser):
                mock_filename.return_value = filename
                mock_encoding.return_value = [True, u'utf-8']
                self.mock_iface = mock_iface
                self.importinstance.general_csv_import(goal_table=u'w_levels')

            _test(self, filename)

        test_string = utils_for_tests.create_test_string(
            utils.sql_load_fr_db(u'''select * from w_levels'''))
        reference_string = ur'''(True, [(obsid1, 2016-01-01 00:00, None, None, 123.0, None), (obsid1, 2016-01-01 00:02:00, None, None, 789.0, None)])'''
        assert test_string == reference_string


