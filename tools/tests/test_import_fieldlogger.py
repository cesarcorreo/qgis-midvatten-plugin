# -*- coding: utf-8 -*-
from collections import OrderedDict

import import_fieldlogger
import midvatten_utils as utils
import mock
from date_utils import datestring_to_date
from import_fieldlogger import FieldloggerImport, InputFields, DateTimeFilter
from mock import MagicMock, call
from nose.plugins.attrib import attr

import utils_for_tests
from utils_for_tests import create_test_string


@attr(status='on')
class TestFieldLoggerImporterNoDb(object):

    @mock.patch('import_fieldlogger.utils.NotFoundQuestion')
    @mock.patch('import_fieldlogger.utils.get_last_used_flow_instruments')
    def test_prepare_w_flow_data(self, mock_flow_instruments, mock_instrument_not_found):
        mock_flow_instruments = [True, {}]
        mock_instrument_not_found.return_value.answer = u'ok'
        mock_instrument_not_found.return_value.value = u'inst1'
        observations = [{u'sublocation': u'obs1.sub', u'obsid': u'obs1', u'flowtype': u'atype', u'date_time': datestring_to_date(u'2016-01-01 00:00'), u'unit': u'aunit', u'value': u'123,4'}]
        test_string = create_test_string(FieldloggerImport.prepare_w_flow_data(observations))
        reference_string = u'[[obsid, instrumentid, flowtype, date_time, reading, unit, comment], [obs1, inst1, atype, 2016-01-01 00:00:00, 123.4, aunit, ]]'
        assert test_string == reference_string

    def test_prepare_w_levels_data_to_meas(self):
        observations = [{u'obsid': u'obs1', u'date_time': datestring_to_date(u'2016-01-01 00:00'), u'meas': u'123,4'}]
        test_string = create_test_string(FieldloggerImport.prepare_w_levels_data(observations))
        reference_string = u'[[obsid, date_time, meas, h_toc, level_masl, comment], [obs1, 2016-01-01 00:00:00, 123.4, , , ]]'
        print(test_string)
        assert test_string == reference_string

    def test_prepare_w_levels_data_to_level_masl(self):
        observations = [{u'obsid': u'obs1', u'date_time': datestring_to_date(u'2016-01-01 00:00'), u'value': u'123,4', u'level_masl': u'567'}]
        test_string = create_test_string(FieldloggerImport.prepare_w_levels_data(observations))
        reference_string = u'[[obsid, date_time, meas, h_toc, level_masl, comment], [obs1, 2016-01-01 00:00:00, , , 567, ]]'
        print(test_string)
        assert test_string == reference_string

    def test_prepare_w_levels_data_to_both(self):
        observations = [{u'obsid': u'obs1', u'date_time': datestring_to_date(u'2016-01-01 00:00'), u'value': u'123,4', u'level_masl': u'567'},
                        {u'obsid': u'obs1', u'date_time': datestring_to_date(u'2016-01-01 00:02'), u'meas': u'897'}]
        test_string = create_test_string(FieldloggerImport.prepare_w_levels_data(observations))
        reference_string = u'[[obsid, date_time, meas, h_toc, level_masl, comment], [obs1, 2016-01-01 00:00:00, , , 567, ], [obs1, 2016-01-01 00:02:00, 897, , , ]]'
        print(test_string)
        assert test_string == reference_string

    def test_prepare_w_levels_data_calculated_level_masl(self):
        observations = [{u'obsid': u'obs1', u'date_time': datestring_to_date(u'2016-01-01 00:00'), u'value': u'123,4', u'meas': u'456,4', u'level_masl': u'567', u'h_toc': '5'},
                        {u'obsid': u'obs1', u'date_time': datestring_to_date(u'2016-01-01 00:02'), u'meas': u'897'}]
        test_string = create_test_string(FieldloggerImport.prepare_w_levels_data(observations))
        reference_string = u'[[obsid, date_time, meas, h_toc, level_masl, comment], [obs1, 2016-01-01 00:00:00, 456.4, 5, 567, ], [obs1, 2016-01-01 00:02:00, 897, , , ]]'
        assert test_string == reference_string

    def test_parse_rows_skip_empty_rows(self):
        f = [u'Br2;12-12-2016;15:33:30;123;w_lvl', u'Br1;12-12-2016;15:34:30;;w_lvl']
        observations = FieldloggerImport.parse_rows(f)
        test = create_test_string(observations)
        reference = u'[{date_time: 2016-12-12 15:33:30, parametername: w_lvl, sublocation: Br2, value: 123}]'
        assert test == reference

    @mock.patch('import_fieldlogger.utils.NotFoundQuestion')
    @mock.patch('import_fieldlogger.utils.get_last_used_flow_instruments')
    def test_prepare_w_flow_data_assert_only_ask_instrument_once(self, mock_flow_instruments,
                                 mock_instrument_not_found):
        mock_flow_instruments = [True, {}]
        mock_instrument_not_found.return_value.answer = u'ok'
        mock_instrument_not_found.return_value.value = u'inst1'
        observations = [{u'sublocation': u'obs1.sub',
                         u'obsid': u'obs1', u'flowtype': u'atype',
                         u'date_time': datestring_to_date(u'2016-01-01 00:00'),
                         u'unit': u'aunit', u'value': u'123,4'},
                        {u'sublocation': u'obs1.sub',
                         u'obsid': u'obs1', u'flowtype': u'atype',
                         u'date_time': datestring_to_date(u'2016-01-02 00:00'),
                         u'unit': u'aunit', u'value': u'223,4'}]
        test_string = create_test_string(FieldloggerImport.prepare_w_flow_data(observations))
        mock_instrument_not_found.assert_called_once_with(combobox_label=u'Instrument id:s in database for obsid obs1.\nThe last used instrument id for obsid obs1 is prefilled:', default_value=u'', dialogtitle=u'Submit instrument id', existing_list=[u''], msg=u'Submit the instrument id for the measurement:\n obs1.sub, obs1, 2016-01-01 00:00:00, atype, aunit')
        reference_string = u'[[obsid, instrumentid, flowtype, date_time, reading, unit, comment], [obs1, inst1, atype, 2016-01-01 00:00:00, 123.4, aunit, ], [obs1, inst1, atype, 2016-01-02 00:00:00, 223.4, aunit, ]]'
        assert test_string == reference_string

    @mock.patch('import_fieldlogger.utils.NotFoundQuestion')
    @mock.patch('import_fieldlogger.utils.get_last_used_flow_instruments')
    def test_prepare_w_flow_data_assert_only_ask_instrument_twice(self, mock_flow_instruments,
                                 mock_instrument_not_found):
        mock_flow_instruments = [True, {}]
        mock_instrument_not_found.return_value.answer = u'ok'
        mock_instrument_not_found.return_value.value = u'inst1'
        observations = [{u'sublocation': u'obs1.sub',
                         u'obsid': u'obs1', u'flowtype': u'atype',
                         u'date_time': datestring_to_date(u'2016-01-01 00:00'),
                         u'unit': u'aunit', u'value': u'123,4'},
                        {u'sublocation': u'obs2.sub',
                         u'obsid': u'obs2', u'flowtype': u'atype',
                         u'date_time': datestring_to_date(u'2016-01-02 00:00'),
                         u'unit': u'aunit', u'value': u'223,4'},
                        {u'sublocation': u'obs2.sub',
                         u'obsid': u'obs2', u'flowtype': u'atype',
                         u'date_time': datestring_to_date(u'2016-01-03 00:00'),
                         u'unit': u'aunit', u'value': u'223,4'}]
        test_string = create_test_string(FieldloggerImport.prepare_w_flow_data(observations))
        expected_calls = [call(combobox_label=u'Instrument id:s in database for obsid obs1.\nThe last used instrument id for obsid obs1 is prefilled:', default_value=u'', dialogtitle=u'Submit instrument id', existing_list=[u''], msg=u'Submit the instrument id for the measurement:\n obs1.sub, obs1, 2016-01-01 00:00:00, atype, aunit'),
 call(combobox_label=u'Instrument id:s in database for obsid obs2.\nThe last used instrument id for obsid obs2 is prefilled:', default_value=u'', dialogtitle=u'Submit instrument id', existing_list=[u''], msg=u'Submit the instrument id for the measurement:\n obs2.sub, obs2, 2016-01-02 00:00:00, atype, aunit')]
        assert mock_instrument_not_found.mock_calls == expected_calls
        reference_string = u'[[obsid, instrumentid, flowtype, date_time, reading, unit, comment], [obs1, inst1, atype, 2016-01-01 00:00:00, 123.4, aunit, ], [obs2, inst1, atype, 2016-01-02 00:00:00, 223.4, aunit, ], [obs2, inst1, atype, 2016-01-03 00:00:00, 223.4, aunit, ]]'
        assert test_string == reference_string

    def test_load_file(self):
        f = [
            u"LOCATION;DATE;TIME;VALUE;TYPE\n",
            u"Rb1202.sample;30-03-2016;15:31:30;hej2;s.comment\n",
            u"Rb1608.level;30-03-2016;15:34:40;testc;l.comment\n",
            u"Rb1615.flow;30-03-2016;15:30:09;357;f.Accvol.m3\n",
            u"Rb1615.flow;30-03-2016;15:30:09;gick bra;f.comment\n",
            u"Rb1608.level;30-03-2016;15:34:13;ergv;l.comment\n",
            u"Rb1608.level;30-03-2016;15:34:13;555;l.meas.m\n",
            u"Rb1512.sample;30-03-2016;15:31:30;899;s.turbiditet.FNU\n",
            u"Rb1505.quality;30-03-2016;15:29:26;hej;q.comment\n",
            u"Rb1505.quality;30-03-2016;15:29:26;863;q.konduktivitet.µS/cm\n",
            u"Rb1512.quality;30-03-2016;15:30:39;test;q.comment\n",
            u"Rb1512.quality;30-03-2016;15:30:39;67;q.syre.mg/L\n",
            u"Rb1512.quality;30-03-2016;15:30:39;8;q.temperatur.grC\n",
            u"Rb1512.quality;30-03-2016;15:30:40;58;q.syre.%\n",
            ]

        with utils.tempinput(''.join(f)) as filename:
            @mock.patch('import_fieldlogger.utils.QtGui.QFileDialog.getOpenFileNames')
            @mock.patch('import_fieldlogger.utils.QtGui.QInputDialog.getText')
            @mock.patch('import_fieldlogger.utils.MessagebarAndLog')
            def _test(self, filename, mock_MessagebarAndLog, mock_charset, mock_savefilename ):
                mock_charset.return_value = ('utf-8', True)
                mock_savefilename.return_value = [filename]

                test_string = create_test_string(FieldloggerImport.select_file_and_parse_rows(FieldloggerImport.parse_rows))
                return test_string

            test_string = _test(self, filename)
            reference = u'[{date_time: 2016-03-30 15:29:26, parametername: q.comment, sublocation: Rb1505.quality, value: hej}, {date_time: 2016-03-30 15:30:39, parametername: q.syre.mg/L, sublocation: Rb1512.quality, value: 67}, {date_time: 2016-03-30 15:31:30, parametername: s.turbiditet.FNU, sublocation: Rb1512.sample, value: 899}, {date_time: 2016-03-30 15:29:26, parametername: q.konduktivitet.µS/cm, sublocation: Rb1505.quality, value: 863}, {date_time: 2016-03-30 15:30:09, parametername: f.comment, sublocation: Rb1615.flow, value: gick bra}, {date_time: 2016-03-30 15:30:40, parametername: q.syre.%, sublocation: Rb1512.quality, value: 58}, {date_time: 2016-03-30 15:34:13, parametername: l.meas.m, sublocation: Rb1608.level, value: 555}, {date_time: 2016-03-30 15:30:39, parametername: q.comment, sublocation: Rb1512.quality, value: test}, {date_time: 2016-03-30 15:31:30, parametername: s.comment, sublocation: Rb1202.sample, value: hej2}, {date_time: 2016-03-30 15:34:40, parametername: l.comment, sublocation: Rb1608.level, value: testc}, {date_time: 2016-03-30 15:30:09, parametername: f.Accvol.m3, sublocation: Rb1615.flow, value: 357}, {date_time: 2016-03-30 15:34:13, parametername: l.comment, sublocation: Rb1608.level, value: ergv}, {date_time: 2016-03-30 15:30:39, parametername: q.temperatur.grC, sublocation: Rb1512.quality, value: 8}]'
            assert test_string == reference

    def test_load_file_cp1252(self):

        f = [
            u"LOCATION;DATE;TIME;VALUE;TYPE\n",
            u"Rb1202.sample;30-03-2016;15:31:30;hej2;s.comment\n",
            u"Rb1608.level;30-03-2016;15:34:40;testc;l.comment\n",
            u"Rb1615.flow;30-03-2016;15:30:09;357;f.Accvol.m3\n",
            u"Rb1615.flow;30-03-2016;15:30:09;gick bra;f.comment\n",
            u"Rb1608.level;30-03-2016;15:34:13;ergv;l.comment\n",
            u"Rb1608.level;30-03-2016;15:34:13;555;l.meas.m\n",
            u"Rb1512.sample;30-03-2016;15:31:30;899;s.turbiditet.FNU\n",
            u"Rb1505.quality;30-03-2016;15:29:26;hej;q.comment\n",
            u"Rb1505.quality;30-03-2016;15:29:26;863;q.konduktivitet.µS/cm\n",
            u"Rb1512.quality;30-03-2016;15:30:39;test;q.comment\n",
            u"Rb1512.quality;30-03-2016;15:30:39;67;q.syre.mg/L\n",
            u"Rb1512.quality;30-03-2016;15:30:39;8;q.temperatur.grC\n",
            u"Rb1512.quality;30-03-2016;15:30:40;58;q.syre.%\n",
            ]

        with utils.tempinput(''.join(f), charset=u'cp1252') as filename:
            @mock.patch('import_fieldlogger.utils.QtGui.QFileDialog.getOpenFileNames')
            @mock.patch('import_fieldlogger.utils.QtGui.QInputDialog.getText')
            @mock.patch('import_fieldlogger.utils.MessagebarAndLog')
            def _test(self, filename, mock_MessagebarAndLog, mock_charset, mock_savefilename ):
                mock_charset.return_value = ('utf-8', True)
                mock_savefilename.return_value = [filename]

                test_string = create_test_string(FieldloggerImport.select_file_and_parse_rows(FieldloggerImport.parse_rows))
                return test_string

            test_string = _test(self, filename)
            reference = u'[{date_time: 2016-03-30 15:29:26, parametername: q.comment, sublocation: Rb1505.quality, value: hej}, {date_time: 2016-03-30 15:30:39, parametername: q.syre.mg/L, sublocation: Rb1512.quality, value: 67}, {date_time: 2016-03-30 15:31:30, parametername: s.turbiditet.FNU, sublocation: Rb1512.sample, value: 899}, {date_time: 2016-03-30 15:29:26, parametername: q.konduktivitet.µS/cm, sublocation: Rb1505.quality, value: 863}, {date_time: 2016-03-30 15:30:09, parametername: f.comment, sublocation: Rb1615.flow, value: gick bra}, {date_time: 2016-03-30 15:30:40, parametername: q.syre.%, sublocation: Rb1512.quality, value: 58}, {date_time: 2016-03-30 15:34:13, parametername: l.meas.m, sublocation: Rb1608.level, value: 555}, {date_time: 2016-03-30 15:30:39, parametername: q.comment, sublocation: Rb1512.quality, value: test}, {date_time: 2016-03-30 15:31:30, parametername: s.comment, sublocation: Rb1202.sample, value: hej2}, {date_time: 2016-03-30 15:34:40, parametername: l.comment, sublocation: Rb1608.level, value: testc}, {date_time: 2016-03-30 15:30:09, parametername: f.Accvol.m3, sublocation: Rb1615.flow, value: 357}, {date_time: 2016-03-30 15:34:13, parametername: l.comment, sublocation: Rb1608.level, value: ergv}, {date_time: 2016-03-30 15:30:39, parametername: q.temperatur.grC, sublocation: Rb1512.quality, value: 8}]'
            assert test_string == reference

    def test_load_file_comma_separated(self):

        f = [
            u"LOCATION,DATE,TIME,VALUE,TYPE\n",
            u"Rb1202.sample,30-03-2016,15:31:30,hej2,s.comment\n",
            u"Rb1608.level,30-03-2016,15:34:40,testc,l.comment\n",
            u"Rb1615.flow,30-03-2016,15:30:09,357,f.Accvol.m3\n",
            u"Rb1615.flow,30-03-2016,15:30:09,gick bra,f.comment\n",
            u"Rb1608.level,30-03-2016,15:34:13,ergv,l.comment\n",
            u"Rb1608.level,30-03-2016,15:34:13,555,l.meas.m\n",
            u"Rb1512.sample,30-03-2016,15:31:30,899,s.turbiditet.FNU\n",
            u"Rb1505.quality,30-03-2016,15:29:26,hej,q.comment\n",
            u"Rb1505.quality,30-03-2016,15:29:26,863,q.konduktivitet.µS/cm\n",
            u"Rb1512.quality,30-03-2016,15:30:39,test,q.comment\n",
            u"Rb1512.quality,30-03-2016,15:30:39,67,q.syre.mg/L\n",
            u"Rb1512.quality,30-03-2016,15:30:39,8,q.temperatur.grC\n",
            u"Rb1512.quality,30-03-2016,15:30:40,58,q.syre.%\n",
            ]

        with utils.tempinput(''.join(f)) as filename:
            @mock.patch('import_fieldlogger.utils.QtGui.QFileDialog.getOpenFileNames')
            @mock.patch('import_fieldlogger.utils.QtGui.QInputDialog.getText')
            @mock.patch('import_fieldlogger.utils.MessagebarAndLog')
            def _test(self, filename, mock_MessagebarAndLog, mock_charset, mock_savefilename ):
                mock_charset.return_value = ('utf-8', True)
                mock_savefilename.return_value = [filename]

                test_string = create_test_string(FieldloggerImport.select_file_and_parse_rows(FieldloggerImport.parse_rows))
                return test_string

            test_string = _test(self, filename)
            reference = u'[{date_time: 2016-03-30 15:29:26, parametername: q.comment, sublocation: Rb1505.quality, value: hej}, {date_time: 2016-03-30 15:30:39, parametername: q.syre.mg/L, sublocation: Rb1512.quality, value: 67}, {date_time: 2016-03-30 15:31:30, parametername: s.turbiditet.FNU, sublocation: Rb1512.sample, value: 899}, {date_time: 2016-03-30 15:29:26, parametername: q.konduktivitet.µS/cm, sublocation: Rb1505.quality, value: 863}, {date_time: 2016-03-30 15:30:09, parametername: f.comment, sublocation: Rb1615.flow, value: gick bra}, {date_time: 2016-03-30 15:30:40, parametername: q.syre.%, sublocation: Rb1512.quality, value: 58}, {date_time: 2016-03-30 15:34:13, parametername: l.meas.m, sublocation: Rb1608.level, value: 555}, {date_time: 2016-03-30 15:30:39, parametername: q.comment, sublocation: Rb1512.quality, value: test}, {date_time: 2016-03-30 15:31:30, parametername: s.comment, sublocation: Rb1202.sample, value: hej2}, {date_time: 2016-03-30 15:34:40, parametername: l.comment, sublocation: Rb1608.level, value: testc}, {date_time: 2016-03-30 15:30:09, parametername: f.Accvol.m3, sublocation: Rb1615.flow, value: 357}, {date_time: 2016-03-30 15:34:13, parametername: l.comment, sublocation: Rb1608.level, value: ergv}, {date_time: 2016-03-30 15:30:39, parametername: q.temperatur.grC, sublocation: Rb1512.quality, value: 8}]'
            assert test_string == reference

    def test_load_file_delimitor_not_found(self):

        f = [
            u"LOCATION;DATE;TIME;VALUE;TYPE\n",
            u"Rb1202.sample,30-03-2016,15:31:30,hej2,s.comment\n",
            u"Rb1608.level,30-03-2016,15:34:40,testc,l.comment\n",
            u"Rb1615.flow,30-03-2016,15:30:09,357,f.Accvol.m3\n",
            u"Rb1615.flow,30-03-2016,15:30:09,gick bra,f.comment\n",
            u"Rb1608.level,30-03-2016,15:34:13,ergv,l.comment\n",
            u"Rb1608.level,30-03-2016,15:34:13,555,l.meas.m\n",
            u"Rb1512.sample,30-03-2016,15:31:30,899,s.turbiditet.FNU\n",
            u"Rb1505.quality,30-03-2016,15:29:26,hej,q.comment\n",
            u"Rb1505.quality,30-03-2016,15:29:26,863,q.konduktivitet.µS/cm\n",
            u"Rb1512.quality,30-03-2016,15:30:39,test,q.comment\n",
            u"Rb1512.quality,30-03-2016,15:30:39,67,q.syre.mg/L\n",
            u"Rb1512.quality,30-03-2016,15:30:39,8,q.temperatur.grC\n",
            u"Rb1512.quality,30-03-2016,15:30:40,58,q.syre.%\n",
            ]

        with utils.tempinput(''.join(f)) as filename:
            @mock.patch('import_fieldlogger.utils.ask_for_delimiter')
            @mock.patch('import_fieldlogger.utils.QtGui.QFileDialog.getOpenFileNames')
            @mock.patch('import_fieldlogger.utils.QtGui.QInputDialog.getText')
            @mock.patch('import_fieldlogger.utils.MessagebarAndLog')
            def _test(self, filename, mock_MessagebarAndLog, mock_charset, mock_savefilename, mock_delimiter_question):
                mock_delimiter_question.return_value = (u',', True)
                mock_charset.return_value = (u'utf-8', True)
                mock_savefilename.return_value = [filename]

                test_string = FieldloggerImport.select_file_and_parse_rows(FieldloggerImport.parse_rows)
                return test_string

            test_string = utils_for_tests.create_test_string(_test(self, filename))
            reference = u'[{date_time: 2016-03-30 15:29:26, parametername: q.comment, sublocation: Rb1505.quality, value: hej}, {date_time: 2016-03-30 15:30:39, parametername: q.syre.mg/L, sublocation: Rb1512.quality, value: 67}, {date_time: 2016-03-30 15:31:30, parametername: s.turbiditet.FNU, sublocation: Rb1512.sample, value: 899}, {date_time: 2016-03-30 15:29:26, parametername: q.konduktivitet.µS/cm, sublocation: Rb1505.quality, value: 863}, {date_time: 2016-03-30 15:30:09, parametername: f.comment, sublocation: Rb1615.flow, value: gick bra}, {date_time: 2016-03-30 15:30:40, parametername: q.syre.%, sublocation: Rb1512.quality, value: 58}, {date_time: 2016-03-30 15:34:13, parametername: l.meas.m, sublocation: Rb1608.level, value: 555}, {date_time: 2016-03-30 15:30:39, parametername: q.comment, sublocation: Rb1512.quality, value: test}, {date_time: 2016-03-30 15:31:30, parametername: s.comment, sublocation: Rb1202.sample, value: hej2}, {date_time: 2016-03-30 15:34:40, parametername: l.comment, sublocation: Rb1608.level, value: testc}, {date_time: 2016-03-30 15:30:09, parametername: f.Accvol.m3, sublocation: Rb1615.flow, value: 357}, {date_time: 2016-03-30 15:34:13, parametername: l.comment, sublocation: Rb1608.level, value: ergv}, {date_time: 2016-03-30 15:30:39, parametername: q.temperatur.grC, sublocation: Rb1512.quality, value: 8}]'
            assert test_string == reference

    def test_prepare_w_qual_field_data(self):
        observations = [{u'obsid': u'obs1', u'date_time': datestring_to_date(u'2016-01-01 00:00'),
                         u'parameter': u'par1', u'unit': u'unit1', u'staff': u'staff1', u'instrument': u'inst1',
                         u'comment': u'comment1', u'value': u'1.23'}]
        test_string = create_test_string(FieldloggerImport.prepare_w_qual_field_data(observations))
        reference_string = u'[[obsid, staff, date_time, instrument, parameter, reading_num, reading_txt, unit, depth, comment], [obs1, staff1, 2016-01-01 00:00:00, inst1, par1, 1.23, 1.23, unit1, , comment1]]'
        assert test_string == reference_string

    def test_prepare_w_qual_field_data_comma_decimal(self):
        observations = [{u'obsid': u'obs1', u'date_time': datestring_to_date(u'2016-01-01 00:00'),
                         u'parameter': u'par1', u'unit': u'unit1', u'staff': u'staff1', u'instrument': u'inst1',
                         u'comment': u'comment1', u'value': u'1,23'}]
        test_string = create_test_string(FieldloggerImport.prepare_w_qual_field_data(observations))
        reference_string = u'[[obsid, staff, date_time, instrument, parameter, reading_num, reading_txt, unit, depth, comment], [obs1, staff1, 2016-01-01 00:00:00, inst1, par1, 1.23, 1,23, unit1, , comment1]]'
        assert test_string == reference_string

    def test_prepare_w_qual_field_data_with_depth(self):
        observations = [{u'obsid': u'obs1', u'date_time': datestring_to_date(u'2016-01-01 00:00'),
                         u'parameter': u'par1', u'unit': u'unit1', u'staff': u'staff1', u'instrument': u'inst1',
                         u'comment': u'comment1', u'value': u'1.23', u'depth': u'123.4'}]
        test_string = create_test_string(FieldloggerImport.prepare_w_qual_field_data(observations))
        reference_string = u'[[obsid, staff, date_time, instrument, parameter, reading_num, reading_txt, unit, depth, comment], [obs1, staff1, 2016-01-01 00:00:00, inst1, par1, 1.23, 1.23, unit1, 123.4, comment1]]'
        assert test_string == reference_string

    def test_prepare_w_qual_field_data_with_depth_comma_sep(self):
        observations = [{u'obsid': u'obs1', u'date_time': datestring_to_date(u'2016-01-01 00:00'),
                         u'parameter': u'par1', u'unit': u'unit1', u'staff': u'staff1', u'instrument': u'inst1',
                         u'comment': u'comment1', u'value': u'1.23', u'depth': u'123,4'}]
        test_string = create_test_string(FieldloggerImport.prepare_w_qual_field_data(observations))
        reference_string = u'[[obsid, staff, date_time, instrument, parameter, reading_num, reading_txt, unit, depth, comment], [obs1, staff1, 2016-01-01 00:00:00, inst1, par1, 1.23, 1.23, unit1, 123.4, comment1]]'
        print(str(test_string))
        assert test_string == reference_string

@attr(status='on')
class TestCommentsImportFields(object):
    def setUp(self):
        mock_import_method_chooser = MagicMock()
        mock_import_method_chooser.parameter_name = u'comment'
        self.comments_import = import_fieldlogger.CommentsImportFields(mock_import_method_chooser, None)

    def test_alter_data(self):
        observations = [{u'parametername': u'comment',
                         u'date_time': datestring_to_date(u'2016-01-01'),
                         u'sublocation': u'1',
                         u'value': u'shared_comment'},
                        {u'parametername': u'par_get_shared_comment',
                         u'date_time': datestring_to_date(u'2016-01-01'),
                         u'sublocation': u'1',
                         u'value': u'1'},
                        {u'parametername': u'par_not_get_shared_comment',
                         u'date_time': datestring_to_date(u'2016-01-02'),
                         u'sublocation': u'2',
                         u'value': u'1'},
                        {u'parametername': u'par_not_get_shared_comment',
                         u'date_time': datestring_to_date(u'2016-01-04'),
                         u'sublocation': u'1',
                         u'value': u'1'},
                        {u'parametername': u'comment',
                         u'date_time': datestring_to_date(u'2016-01-03'),
                         u'sublocation': u'1',
                         u'value': u'not_shared_comment'}
                        ]
        observations = self.comments_import.alter_data(observations)

        test_string = create_test_string(observations)
        reference_string = u'[{date_time: 2016-01-01 00:00:00, parametername: comment, skip_comment_import: True, sublocation: 1, value: shared_comment}, {comment: shared_comment, date_time: 2016-01-01 00:00:00, parametername: par_get_shared_comment, sublocation: 1, value: 1}, {date_time: 2016-01-02 00:00:00, parametername: par_not_get_shared_comment, sublocation: 2, value: 1}, {date_time: 2016-01-04 00:00:00, parametername: par_not_get_shared_comment, sublocation: 1, value: 1}, {date_time: 2016-01-03 00:00:00, parametername: comment, sublocation: 1, value: not_shared_comment}]'
        assert test_string == reference_string

@attr(status='on')
class TestStaffQuestion(object):

    @mock.patch('import_fieldlogger.defs.staff_list')
    def setUp(self, mock_stafflist):
        mock_stafflist.return_value = (True, [u'staff1', u'staff2'])
        self.staff_question = import_fieldlogger.StaffQuestion()

    def test_alter_data(self):
        observation = {u'sublocation': u'1'}

        self.staff_question.staff = u'teststaff'
        test_string = create_test_string(self.staff_question.alter_data(observation))
        reference_string = u'{staff: teststaff, sublocation: 1}'
        assert test_string == reference_string

@attr(status='on')
class TestObsidFilter(object):
    def setUp(self):
        self.obsid_filter = import_fieldlogger.ObsidFilter()

    @mock.patch('import_fieldlogger.utils.get_all_obsids')
    def test_alter_data(self, mock_get_all_obsids):
        mock_get_all_obsids.return_value = [u'rb1', u'rb2']

        observations = [{u'sublocation': u'rb1'}, {u'sublocation': u'rb2'}]

        test_string = create_test_string(self.obsid_filter.alter_data(observations))
        reference_string = u'[{obsid: rb1, sublocation: rb1}, {obsid: rb2, sublocation: rb2}]'
        assert test_string == reference_string

@attr(status='on')
@mock.patch('import_fieldlogger.utils.MessagebarAndLog')
@mock.patch('import_fieldlogger.defs.w_qual_field_parameter_units')
def _test_set_parameters_using_stored_settings(mock_w_qual_field_parameter_units, mock_mock_message_bar):
    mock_w_qual_field_parameter_units.retun_value = {}

    stored_settings = [[u's.comment', [[u'import_method', u'comments']]],
                   [u'l.meas.m', [[u'import_method', u'w_levels'], [u'value_column', u'level_masl']]],
                   [u'f.Accvol.m3', [[u'import_method', u'w_flow'], [u'flowtype', u'Accvol'], [u'unit', u'm3']]],
                   [u's.turbiditet.FNU', [[u'import_method', u'w_qual_field'], [u'parameter', u'turbiditet'], [u'unit', u'FNU'], [u'depth', u'1'], [u'instrument', u'testid']]]]

    mock_connect = MagicMock()
    input_fields = InputFields(mock_connect)
    input_fields.parameter_imports = OrderedDict([(k, import_fieldlogger.ImportMethodChooser(k, [x[0] for x in stored_settings], mock_connect)) for k in [x[0] for x in stored_settings]])

    input_fields.set_parameters_using_stored_settings(stored_settings)

    settings = []
    for k, v in input_fields.parameter_imports.iteritems():
        try:
            setting = v.parameter_import_fields.get_settings()
        except Exception, e:
            pass
        else:
            settings.append((k, setting))
    test_string = create_test_string(settings)
    reference_string = u'[(l.meas.m, ((value_column, level_masl))), (f.Accvol.m3, ((flowtype, Accvol), (unit, m3))), (s.turbiditet.FNU, ((parameter, turbiditet), (unit, FNU), (depth, 1), (instrument, testid)))]'
    assert test_string == reference_string

    new_stored = []
    input_fields.update_stored_settings(new_stored)
    test_string = create_test_string(new_stored)
    reference_string = u'[[s.comment, [(import_method, comments)]], [l.meas.m, [(import_method, w_levels), (value_column, level_masl)]], [f.Accvol.m3, [(import_method, w_flow), (flowtype, Accvol), (unit, m3)]], [s.turbiditet.FNU, [(import_method, w_qual_field), (parameter, turbiditet), (unit, FNU), (depth, 1), (instrument, testid)]]]'
    assert test_string == reference_string

@attr(status='on')
def _test_SublocationFilter():
    sublocation_filter = import_fieldlogger.SublocationFilter([u'a.1', u'a.2'])

    assert u'{sublocation: a.1}' == create_test_string(sublocation_filter.alter_data({u'sublocation': u'a.1'}))

    sublocation_filter.set_selection([u'a.1'], False)
    assert sublocation_filter.alter_data({u'sublocation': u'a.1'}) is None
    assert u'{sublocation: a.2}' == create_test_string(sublocation_filter.alter_data({u'sublocation': u'a.2'}))

    sublocation_filter.set_selection([u'a.1'], True)
    assert u'{sublocation: a.1}' == create_test_string(sublocation_filter.alter_data({u'sublocation': u'a.1'}))
    assert u'{sublocation: a.2}' == create_test_string(sublocation_filter.alter_data({u'sublocation': u'a.2'}))

@attr(status='on')
class TestDateTimeFilter(object):
    def test_date_time_filter_observation_should_be_none(self):
        datetimefilter = DateTimeFilter()
        datetimefilter.from_date = u'2016-01-01'
        datetimefilter.to_date = u'2016-01-10'
        observation = datetimefilter.alter_data({u'date_time': datestring_to_date(u'2015-01-01')})
        assert observation is None

    def test_date_time_filter_observation_return_observation(self):
        datetimefilter = DateTimeFilter()
        datetimefilter.from_date = u'2016-01-01'
        datetimefilter.to_date = u'2016-01-10'
        observation = datetimefilter.alter_data({u'date_time': datestring_to_date(u'2016-01-05')})
        test_string = create_test_string(observation)
        reference = u'{date_time: 2016-01-05 00:00:00}'
        assert test_string == reference

    def test_date_time_filter_observation_return_observation_one_second_to_to(self):
        datetimefilter = DateTimeFilter()
        datetimefilter.from_date = u'2016-01-01'
        datetimefilter.to_date = u'2016-01-10'
        observation = datetimefilter.alter_data({u'date_time': datestring_to_date(u'2016-01-09 23:59:59')})
        test_string = create_test_string(observation)
        reference = u'{date_time: 2016-01-09 23:59:59}'
        assert test_string == reference

    def test_date_time_filter_observation_skip_from(self):
        datetimefilter = DateTimeFilter()
        datetimefilter.from_date = u'2016-01-01'
        datetimefilter.to_date = u'2016-01-10'
        observation = datetimefilter.alter_data({u'date_time': datestring_to_date(u'2016-01-01')})
        assert observation is None

    def test_date_time_filter_observation_skip_to(self):
        datetimefilter = DateTimeFilter()
        datetimefilter.from_date = u'2016-01-01'
        datetimefilter.to_date = u'2016-01-10'
        observation = datetimefilter.alter_data({u'date_time': datestring_to_date(u'2016-01-10')})
        assert observation is None







