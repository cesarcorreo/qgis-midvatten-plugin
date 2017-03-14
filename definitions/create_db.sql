﻿﻿# -*- coding: utf-8 -*- This line is just for your information, the python plugin will not use the first line
SPATIALITE SELECT InitSpatialMetadata(1);
CREATE TABLE about_db ("tablename" text, "columnname" text, "data_type" text, "not_null" text, "default_value" text, "primary_key" text, "foreign_key" text, "description" text, "upd_date" text, "upd_sign" text);
INSERT INTO about_db VALUES('*', '*', '', '', '', '', '', 'This db was created by Midvatten plugin CHANGETOPLUGINVERSION, running QGIS version CHANGETOQGISVERSION on top of SpatiaLite version CHANGETOSPLITEVERSION', '', '');
INSERT INTO about_db VALUES('*', '*', '', '', '', '', '', 'locale:CHANGETOLOCALE', '', '');
INSERT INTO about_db VALUES('about_db', '*', '', '', '', '', '', 'A status log for the tables in the db', '', '');
INSERT INTO about_db VALUES('about_db', 'table', 'text', '', '', '', '', 'Name of a table in the db', '', '');
INSERT INTO about_db VALUES('about_db', 'column', 'text', '', '', '', '', 'Name of column', '', '');
INSERT INTO about_db VALUES('about_db', 'upd_date', 'text', '', '', '', '', 'Date for last update', '', '');
INSERT INTO about_db VALUES('about_db', 'upd_sign', 'text', '', '', '', '', 'Person responsible for update', '', '');
INSERT INTO about_db VALUES('about_db', 'contents', 'text', '', '', '', '', 'Contents', '', '');
INSERT INTO about_db VALUES('comments', '*', '', '', '', '', '', 'comments connected to obsids', '', '');
INSERT INTO about_db VALUES('comments', 'obsid', 'text', '1', '', '1', 'obs_points(obsid)', 'ID for the observation point, eg Well01, Br1201, Rb1201', '', '');
INSERT INTO about_db VALUES('comments', 'date_time', 'text', '1', '', '1', '', 'Date and Time for the comment, on format yyyy-mm-dd hh:mm:ss', '', '');
INSERT INTO about_db VALUES('comments', 'comment', 'text', '1', '', '', '', 'comments connected to obsids', '', '');
INSERT INTO about_db VALUES('comments', 'staff', 'text', '1', '', '', 'zz_staff(staff)', 'comments connected to obsids', '', '');
INSERT INTO about_db VALUES('meteo', '*', '', '', '', '', '', 'meteorological observations', '', '');
INSERT INTO about_db VALUES('meteo', 'obsid', 'text', '1', '', '1', 'obs_points(obsid)', 'obsid linked to obs_points.obsid', '', '');
INSERT INTO about_db VALUES('meteo', 'instrumentid', 'text', '1', '', '1', '', 'Instrument Id, may use several different temperature sensors or precipitaion meters at same station', '', '');
INSERT INTO about_db VALUES('meteo', 'parameter', 'text', '1', '', '1', 'zz_meteoparam(parameter)', 'The meteorological parameter, e.g. precipitation, temperature etc', '', '');
INSERT INTO about_db VALUES('meteo', 'date_time', 'text', '1', '', '1', '', 'Date and Time for the observation, on format yyyy-mm-dd hh:mm:ss', '', '');
INSERT INTO about_db VALUES('meteo', 'reading_num', 'double', '', '', '', '', 'Value (real number) reading for the parameter', '', '');
INSERT INTO about_db VALUES('meteo', 'reading_txt', 'text', '', '', '', '', 'Value (text string) reading for the parameter', '', '');
INSERT INTO about_db VALUES('meteo', 'unit', 'text', '', '', '', '', 'Unit corresponding to the value reading', '', '');
INSERT INTO about_db VALUES('meteo', 'comment', 'text', '', '', '', '', 'Comment', '', '');
INSERT INTO about_db VALUES('obs_points', '*', '', '', '', '', '', 'One of the two main tables. This table holds all point observation objects.', '', '');
INSERT INTO about_db VALUES('obs_points', 'obsid', 'text', '1', '', '1', '', 'ID for the observation point, eg Well01, Br1201, Rb1201', '', '');
INSERT INTO about_db VALUES('obs_points', 'name', 'text', '', '', '', '', 'Ordinary name for the observation, e.g. Pumping well no 1, Brunn 123, Flow gauge A, pegel 3 etc ', '', '');
INSERT INTO about_db VALUES('obs_points', 'place', 'text', '', '', '', '', 'Place for the observation. E.g. estate, property, site', '', '');
INSERT INTO about_db VALUES('obs_points', 'type', 'text', '', '', '', '', 'Type of observation', '', '');
INSERT INTO about_db VALUES('obs_points', 'length', 'double', '', '', '', '', 'Borehole length from ground surface to bottom (equals to depth if vertical)', '', '');
INSERT INTO about_db VALUES('obs_points', 'drillstop', 'text', '', '', '', '', 'Drill stop, e.g. probing/direct push drilling stopped against rock', '', '');
INSERT INTO about_db VALUES('obs_points', 'diam', 'double', '', '', '', '', 'Inner diameter for casing or upper part of borehol', '', '');
INSERT INTO about_db VALUES('obs_points', 'material', 'text', '', '', '', '', 'Well material', '', '');
INSERT INTO about_db VALUES('obs_points', 'screen', 'text', '', '', '', '', 'Type of well screen, including description, e.g. 1 m Johnson Well Screen 2,5mm ', '', '');
INSERT INTO about_db VALUES('obs_points', 'capacity', 'text', '', '', '', '', 'Well capacity', '', '');
INSERT INTO about_db VALUES('obs_points', 'drilldate', 'text', '', '', '', '', 'Date when drilling was completed', '', '');
INSERT INTO about_db VALUES('obs_points', 'wmeas_yn', 'integer', '', '', '', '', '1/0 if water level is to be measured for this point or not', '', '');
INSERT INTO about_db VALUES('obs_points', 'wlogg_yn', 'integer', '', '', '', '', '1/0 if water level if borehole is equipped with a logger or not', '', '');
INSERT INTO about_db VALUES('obs_points', 'east', 'double', '', '', '', '', 'Eastern coordinate (in the corresponding CRS)', '', '');
INSERT INTO about_db VALUES('obs_points', 'north', 'double', '', '', '', '', 'Northern coordinate (in the corresponding CRS)', '', '');
INSERT INTO about_db VALUES('obs_points', 'ne_accur', 'double', '', '', '', '', 'Approximate inaccuracy for coordinates', '', '');
INSERT INTO about_db VALUES('obs_points', 'ne_source', 'text', '', '', '', '', 'Source for the given position, e.g. from an old map or measured in field campaign', '', '');
INSERT INTO about_db VALUES('obs_points', 'h_toc', 'double', '', '', '', '', 'Elevation (masl) for the measuring point, the point from which water level is measured, normally Top Of Casing', '', '');
INSERT INTO about_db VALUES('obs_points', 'h_tocags', 'double', '', '', '', '', 'Distance from Measuring point to Ground Surface (m), Top Of Casing Above Ground Surface', '', '');
INSERT INTO about_db VALUES('obs_points', 'h_gs', 'double', '', '', '', '', 'Ground Surface level (m). ', '', '');
INSERT INTO about_db VALUES('obs_points', 'h_accur', 'double', '', '', '', '', 'Inaccuracy (m) for Measuring Point level, h_toc', '', '');
INSERT INTO about_db VALUES('obs_points', 'h_syst', 'text', '', '', '', '', 'Reference system for elevation', '', '');
INSERT INTO about_db VALUES('obs_points', 'h_source', 'text', '', '', '', '', 'Source for the measuring point elevation (consultancy report or similar)', '', '');
INSERT INTO about_db VALUES('obs_points', 'source', 'text', '', '', '', '', 'The source for the observation point, eg full reference to consultancy report or authority and year', '', '');
INSERT INTO about_db VALUES('obs_points', 'com_onerow', 'text', '', '', '', '', 'onerow comment, appropriate for map labels', '', '');
INSERT INTO about_db VALUES('obs_points', 'com_html', 'text', '', '', '', '', 'multiline formatted comment in html format', '', '');
INSERT INTO about_db VALUES('obs_points', 'geometry', 'BLOB point', '', '', '', '', 'The geometry of OGR/FDO type point', '', '');
INSERT INTO about_db VALUES('obs_lines', '*', '', '', '', '', '', 'One of the two main tables. This table holds all line observation objects.', '', '');
INSERT INTO about_db VALUES('obs_lines', 'obsid', 'text', '1', '', '1', '', 'ID for observation line, e.g. S1.', '', '');
INSERT INTO about_db VALUES('obs_lines', 'name', 'text', '', '', '', '', 'Ordinary name for the observation, e.g. Seismic profile no 1', '', '');
INSERT INTO about_db VALUES('obs_lines', 'place', 'text', '', '', '', '', 'Place for the observation', '', '');
INSERT INTO about_db VALUES('obs_lines', 'type', 'text', '', '', '', '', 'Type of observation, e.g. vlf, seismics or gpr', '', '');
INSERT INTO about_db VALUES('obs_lines', 'source', 'text', '', '', '', '', 'The origin for the observation, eg full reference to consultancy report', '', '');
INSERT INTO about_db VALUES('obs_lines', 'geometry', 'BLOB linestring', '', '', '', '', 'The geometry of OGR/FDO type linestring', '', '');
INSERT INTO about_db VALUES('seismic_data', '*', '', '', '', '', '', 'Interpreted data from seismic measurements', '', '');
INSERT INTO about_db VALUES('seismic_data', 'obsid', 'text', '1', '', '1', 'obs_lines(obsid)', 'obsid linked to obs_lines.obsid', '', '');
INSERT INTO about_db VALUES('seismic_data', 'length', 'double', '1', '', '1', '', 'Length along line', '', '');
INSERT INTO about_db VALUES('seismic_data', 'ground', 'double', '', '', '', '', 'Ground surface level', '', '');
INSERT INTO about_db VALUES('seismic_data', 'bedrock', 'double', '', '', '', '', 'Interpreted level for bedrock surface', '', '');
INSERT INTO about_db VALUES('seismic_data', 'gw_table', 'double', '', '', '', '', 'Interpreted level for limit between unsaturated/saturated conditions', '', '');
INSERT INTO about_db VALUES('seismic_data', 'comment', 'text', '', '', '', '', 'Additional info', '', '');
INSERT INTO about_db VALUES('stratigraphy', '*', '', '', '', '', '', 'stratigraphy information from drillings, probings etc', '', '');
INSERT INTO about_db VALUES('stratigraphy', 'obsid', 'text', '1', '', '1', 'obs_points(obsid)', 'obsid linked to obs_points.obsid', '', '');
INSERT INTO about_db VALUES('stratigraphy', 'stratid', 'integer', '1', '', '1', '', 'Stratigraphy layer ID for the OBSID, starts with layer 1 from ground surface and increases below', '', '');
INSERT INTO about_db VALUES('stratigraphy', 'depthtop', 'double', '', '', '', '', 'Depth, from surface level, to top of the stratigraphy layer', '', '');
INSERT INTO about_db VALUES('stratigraphy', 'depthbot', 'double', '', '', '', '', 'Depth, from surface level, to bottom of the stratigraphy layer', '', '');
INSERT INTO about_db VALUES('stratigraphy', 'geology', 'text', '', '', '', '', 'Full description of geology', '', '');
INSERT INTO about_db VALUES('stratigraphy', 'geoshort', 'text', '', '', '', '', 'Short description of geology, should correspond to the dictionaries used. Stratigraphy plot looks in this field and relates to coded dictionaries with fill patterns and colors.', '', '');
INSERT INTO about_db VALUES('stratigraphy', 'capacity', 'text', '', '', '', '', 'Well development at the layer, may also be waterloss or similar. If using notations 1, 2, 3, 4-, 4, and so on until 6+ it will match color codes in Midvatten plugin (see midvatten_defs.py). ', '', '');
INSERT INTO about_db VALUES('stratigraphy', 'development', 'text', '', '', '', '', 'Well development - Is the flushed water clear and free of suspended solids? ', '', '');
INSERT INTO about_db VALUES('stratigraphy', 'comment', 'text', '', '', '', '', 'Comment', '', '');
INSERT INTO about_db VALUES('vlf_data', '*', '', '', '', '', '', 'Raw data from VLF measurements', '', '');
INSERT INTO about_db VALUES('vlf_data', 'obsid', 'text', '1', '', '1', 'obs_lines(obsid)', 'obsid linked to obs_lines.obsid', '', '');
INSERT INTO about_db VALUES('vlf_data', 'length', 'double', '1', '', '1', '', 'Length along line', '', '');
INSERT INTO about_db VALUES('vlf_data', 'real_comp', 'double', '', '', '', '', 'Raw data real component (in-phase(%))', '', '');
INSERT INTO about_db VALUES('vlf_data', 'imag_comp', 'double', '', '', '', '', 'Raw data imaginary component', '', '');
INSERT INTO about_db VALUES('vlf_data', 'comment', 'text', '', '', '', '', 'Additional info', '', '');
INSERT INTO about_db VALUES('w_flow', '*', '', '', '', '', '', 'Water flow', '', '');
INSERT INTO about_db VALUES('w_flow', 'obsid', 'text', '1', '', '1', 'obs_points(obsid)', 'obsid linked to obs_points.obsid', '', '');
INSERT INTO about_db VALUES('w_flow', 'instrumentid', 'text', '1', '', '1', '', 'Instrument Id, may use several flowmeters at same borehole', '', '');
INSERT INTO about_db VALUES('w_flow', 'flowtype', 'text', '1', '', '1', '', 'Flowtype must correspond to type in flowtypes - Accumulated volume, momentary flow etc', '', '');
INSERT INTO about_db VALUES('w_flow', 'date_time', 'text', '1', '', '1', 'zz_flowtype(type)', 'Date and Time for the observation, on format yyyy-mm-dd hh:mm:ss', '', '');
INSERT INTO about_db VALUES('w_flow', 'reading', 'double', '', '', '', '', 'Value (real number) reading for the flow rate, accumulated volume etc', '', '');
INSERT INTO about_db VALUES('w_flow', 'unit', 'text', '', '', '', '', 'Unit corresponding to the value reading', '', '');
INSERT INTO about_db VALUES('w_flow', 'comment', 'text', '', '', '', '', 'Comment', '', '');
INSERT INTO about_db VALUES('w_levels', '*', '', '', '', '', '', 'Manual water level measurements', '', '');
INSERT INTO about_db VALUES('w_levels', 'obsid', 'text', '1', '', '1', 'obs_points(obsid)', 'obsid linked to obs_points.obsid', '', '');
INSERT INTO about_db VALUES('w_levels', 'date_time', 'text', '1', '', '1', '', 'Date and Time for the observation, on format yyyy-mm-dd hh:mm:ss', '', '');
INSERT INTO about_db VALUES('w_levels', 'meas', 'double', '', '', '', '', 'distance from measuring point to water level', '', '');
INSERT INTO about_db VALUES('w_levels', 'h_toc', 'double', '', '', '', '', 'Elevation (masl) for the measuring point at the particular date_time (measuring point elevation may vary by time)', '', '');
INSERT INTO about_db VALUES('w_levels', 'level_masl', 'double', '', '', '', '', 'Water level elevation (masl) calculated from measuring point and distance from measuring point to water level', '', '');
INSERT INTO about_db VALUES('w_levels', 'comment', 'text', '', '', '', '', 'Comment', '', '');
INSERT INTO about_db VALUES('w_levels_logger', '*', '', '', '', '', '', 'Automatic Water Level Readings', '', '');
INSERT INTO about_db VALUES('w_levels_logger', 'obsid', 'text', '1', '', '1', 'obs_points(obsid)', 'obsid linked to obs_points.obsid', '', '');
INSERT INTO about_db VALUES('w_levels_logger', 'date_time', 'text', '1', '', '1', '', 'Date and Time for the observation, on format yyyy-mm-dd hh:mm:ss', '', '');
INSERT INTO about_db VALUES('w_levels_logger', 'head_cm', 'double', '', '', '', '', 'pressure (cm water column) on pressure transducer', '', '');
INSERT INTO about_db VALUES('w_levels_logger', 'temp_degc', 'double', '', '', '', '', 'temperature degrees C', '', '');
INSERT INTO about_db VALUES('w_levels_logger', 'cond_mscm', 'double', '', '', '', '', 'electrical conductivity mS/cm', '', '');
INSERT INTO about_db VALUES('w_levels_logger', 'level_masl', 'double', '1', '-999', '', '', 'Corresponding Water level elevation (masl)', '', '');
INSERT INTO about_db VALUES('w_levels_logger', 'comment', 'text', '', '', '', '', 'Comment', '', '');
INSERT INTO about_db VALUES('w_qual_field', '*', '', '', '', '', '', 'Water quality from field measurements', '', '');
INSERT INTO about_db VALUES('w_qual_field', 'obsid', 'text', '1', '', '1', 'obs_points(obsid)', 'obsid linked to obs_points.obsid', '', '');
INSERT INTO about_db VALUES('w_qual_field', 'staff', 'text', '', '', '', '', 'Field staff', '', '');
INSERT INTO about_db VALUES('w_qual_field', 'date_time', 'text', '1', '', '1', '', 'Date and Time for the observation, on format yyyy-mm-dd hh:mm:ss', '', '');
INSERT INTO about_db VALUES('w_qual_field', 'instrument', 'text', '', '', '', '', 'Instrument ID', '', '');
INSERT INTO about_db VALUES('w_qual_field', 'parameter', 'text', '1', '', '1', '', 'Measured parameter', '', '');
INSERT INTO about_db VALUES('w_qual_field', 'reading_num', 'double', '', '', '', '', 'Value AS real number', '', '');
INSERT INTO about_db VALUES('w_qual_field', 'reading_txt', 'text', '', '', '', '', 'Value AS text, incl more than and less than symbols', '', '');
INSERT INTO about_db VALUES('w_qual_field', 'unit', 'text', '', '', '1', '', 'Unit', '', '');
INSERT INTO about_db VALUES('w_qual_field', 'depth', 'double', '', '', '', '', 'The depth at which the measurement was done', '', '');
INSERT INTO about_db VALUES('w_qual_field', 'comment', 'text', '', '', '', '', 'Comment', '', '');
INSERT INTO about_db VALUES('w_qual_lab', '*', '', '', '', '', '', 'Water quality from laboratory analysis', '', '');
INSERT INTO about_db VALUES('w_qual_lab', 'obsid', 'text', '1', '', '', 'obs_points(obsid)', 'obsid linked to obs_points.obsid', '', '');
INSERT INTO about_db VALUES('w_qual_lab', 'depth', 'double', '', '', '', '', 'Depth (m below h_gs) from where sample is taken', '', '');
INSERT INTO about_db VALUES('w_qual_lab', 'report', 'text', '1', '', '1', '', 'Report no from laboratory', '', '');
INSERT INTO about_db VALUES('w_qual_lab', 'project', 'text', '', '', '', '', 'Project number', '', '');
INSERT INTO about_db VALUES('w_qual_lab', 'staff', 'text', '', '', '', 'zz_staff(staff)', 'Field staff', '', '');
INSERT INTO about_db VALUES('w_qual_lab', 'date_time', 'text', '', '', '', '', 'Date and Time for the observation, on format yyyy-mm-dd hh:mm:ss', '', '');
INSERT INTO about_db VALUES('w_qual_lab', 'anameth', 'text', '', '', '', '', 'Analysis method, preferrably code relating to analysis standard', '', '');
INSERT INTO about_db VALUES('w_qual_lab', 'parameter', 'text', '1', '', '1', '', 'Measured parameter', '', '');
INSERT INTO about_db VALUES('w_qual_lab', 'reading_num', 'double', '', '', '', '', 'Value AS real number', '', '');
INSERT INTO about_db VALUES('w_qual_lab', 'reading_txt', 'text', '', '', '', '', 'Value AS text, incl more than and less than symbols', '', '');
INSERT INTO about_db VALUES('w_qual_lab', 'unit', 'text', '', '', '', '', 'Unit', '', '');
INSERT INTO about_db VALUES('w_qual_lab', 'comment', 'text', '', '', '', '', 'Comments', '', '');
INSERT INTO about_db VALUES('zz_flowtype', '*', '', '', '', '', '', 'data domain for flowtypes in table w_flow', '', '');
INSERT INTO about_db VALUES('zz_flowtype', 'type', 'text', '1', 'Accvol, Aveflow or Momflow', '1', '', 'Existing types of measurements related to water flow', '', '');
INSERT INTO about_db VALUES('zz_flowtype', 'explanation', 'text', '', '', '', '', 'Explanation of the flowtypes', '', '');
INSERT INTO about_db VALUES('zz_meteoparam', '*', '', '', '', '', '', 'data domain for meteorological parameters in meteo', '', '');
INSERT INTO about_db VALUES('zz_meteoparam', 'parameter', 'text', '1', 'precip, temp', '1', '', 'Existing types of parameter related to meteorological observations', '', '');
INSERT INTO about_db VALUES('zz_meteoparam', 'explanation', 'text', '', '', '', '', 'Explanation of the parameters', '', '');
INSERT INTO about_db VALUES('zz_staff', '*', '', '', '', '', '', 'data domain for field staff used when importing data', '', '');
INSERT INTO about_db VALUES('zz_staff', 'staff', 'text', '', '', '1', '', 'initials of the field staff', '', '');
INSERT INTO about_db VALUES('zz_staff', 'name', 'text', '', '', '', '', 'name of the field staff', '', '');
insert into about_db values('zz_strat', '*', '', '', '', '', '', 'data domain for stratigraphy classes, plot colors, symbols and geological short names used by the plugin', '', '');
insert into about_db values('zz_strat', 'geoshort', 'text', '1', '', '', '', 'abbreviation for the strata (stratigraphy class)', '', '');
insert into about_db values('zz_strat', 'strata', 'text', '1', 'gravel, sand, silt, clay etc', '1', '', 'stratigraphy classes', '', '');
insert into about_db values('zz_stratigraphy_plots', '*', '', '', '', '', '', 'data domain for stratigraphy plot colors and symbols used by the plugin', '', '');
insert into about_db values('zz_stratigraphy_plots', 'strata', 'text', '1', 'gravel, sand, silt, clay etc', '1', '', 'stratigraphy classes', '', '');
insert into about_db values('zz_stratigraphy_plots', 'color_mplot', 'text', '1', '', '', '', 'color codes for matplotlib plots', '', '');
insert into about_db values('zz_stratigraphy_plots', 'hatch_mplot', 'text', '1', '', '', '', 'hatch codes for matplotlib plots', '', '');
insert into about_db values('zz_stratigraphy_plots', 'color_qt', 'text', '1', '', '', '', 'color codes for Qt plots', '', '');
insert into about_db values('zz_stratigraphy_plots', 'brush_qt', 'text', '1', '', '', '', 'brush types for Qt plots', '', '');
insert into about_db values('zz_capacity', '*', '', '', '', '', '', 'data domain for stratigraphy classes and geological short names used by the plugin', '', '');
insert into about_db values('zz_capacity', 'capacity', 'text', '1', 'Default: 1, 2, 3, 4, 5, 6', '1', '', 'water capacity classes, typically used for stratigraphy layers', '', '');
insert into about_db values('zz_capacity', 'explanation', 'text', '1', '', '', '', 'description of water capacity classes', '', '');
insert into about_db values('zz_capacity_plots', '*', '', '', '', '', '', 'data domain for capacity plot colors used by the plugin', '', '');
insert into about_db values('zz_capacity_plots', 'capacity', 'text', '1', 'Default: 1, 2, 3, 4, 5, 6', '1', '', 'water capacity classes, typically used for stratigraphy layers', '', '');
insert into about_db values('zz_capacity_plots', 'color_qt', 'text', '1', '', '', '', 'hatchcolor codes for Qt plots', '', '');
CREATE TABLE zz_staff (staff text, name text, PRIMARY KEY(staff));
CREATE TABLE zz_flowtype (type text NOT NULL, explanation text, PRIMARY KEY(type));
CREATE TABLE zz_meteoparam (parameter text NOT NULL,explanation text, PRIMARY KEY(parameter));
CREATE TABLE zz_strat (geoshort text NOT NULL, strata text NOT NULL, PRIMARY KEY(geoshort));
CREATE TABLE zz_stratigraphy_plots (strata text NOT NULL, color_mplot text NOT NULL, hatch_mplot text NOT NULL, color_qt text NOT NULL, brush_qt text NOT NULL, PRIMARY KEY(strata));
CREATE TABLE zz_capacity (capacity text NOT NULL, explanation text NOT NULL, PRIMARY KEY(capacity));
CREATE TABLE zz_capacity_plots (capacity text NOT NULL, color_qt text NOT NULL, PRIMARY KEY(capacity), FOREIGN KEY(capacity) REFERENCES zz_capacity(capacity));
CREATE TABLE obs_points ( obsid text NOT NULL, name text, place text, type text, length double, drillstop text, diam double, material text, screen text, capacity text, drilldate text, wmeas_yn integer, wlogg_yn integer, east double, north double, ne_accur double, ne_source text,  h_toc double, h_tocags double, h_gs double, h_accur double, h_syst text, h_source text, source text, com_onerow text, com_html text, PRIMARY KEY (obsid));
SPATIALITE SELECT AddGeometryColumn('obs_points', 'geometry', CHANGETORELEVANTEPSGID, 'POINT', 'XY', 0);
POSTGIS ALTER TABLE obs_points ADD COLUMN geometry geometry(Point,CHANGETORELEVANTEPSGID)
CREATE TABLE obs_lines (obsid text  NOT NULL, name text, place text, type text, source text, PRIMARY KEY (obsid));
SPATIALITE SELECT AddGeometryColumn('obs_lines', 'geometry', CHANGETORELEVANTEPSGID, 'LINESTRING', 'XY', 0);
POSTGIS ALTER TABLE obs_lines ADD COLUMN geometry geometry(Linestring,CHANGETORELEVANTEPSGID)
CREATE TABLE w_levels (obsid text NOT NULL, date_time text NOT NULL, meas double, h_toc double, level_masl double, comment text, PRIMARY KEY (obsid, date_time),  FOREIGN KEY(obsid) REFERENCES obs_points(obsid));
CREATE TABLE w_levels_logger (obsid text NOT NULL, date_time text NOT NULL, head_cm double, temp_degc double, cond_mscm double, level_masl double, comment text, PRIMARY KEY (obsid, date_time),  FOREIGN KEY(obsid) REFERENCES obs_points(obsid));
CREATE TABLE stratigraphy (obsid text NOT NULL, stratid integer NOT NULL, depthtop double, depthbot double, geology text, geoshort text, capacity text, development text,  comment text, PRIMARY KEY (obsid, stratid), FOREIGN KEY(obsid) REFERENCES obs_points(obsid));
CREATE TABLE w_qual_field (obsid text NOT NULL, staff text, date_time text NOT NULL, instrument text, parameter text NOT NULL, reading_num double, reading_txt text, unit text, depth double, comment text, PRIMARY KEY(obsid, date_time, parameter, unit), FOREIGN KEY(obsid) REFERENCES obs_points(obsid), FOREIGN KEY(staff) REFERENCES zz_staff(staff));
CREATE TABLE w_qual_lab (obsid text NOT NULL, depth double, report text NOT NULL, project text, staff text, date_time text, anameth text, parameter text NOT NULL, reading_num double, reading_txt text, unit text, comment text, PRIMARY KEY(report, parameter), FOREIGN KEY(obsid) REFERENCES obs_points(obsid), FOREIGN KEY(staff) REFERENCES zz_staff(staff));
CREATE TABLE w_flow (obsid text NOT NULL, instrumentid text NOT NULL, flowtype text NOT NULL, date_time text NOT NULL, reading double, unit text, comment text, PRIMARY KEY (obsid, instrumentid, flowtype, date_time), FOREIGN KEY(obsid) REFERENCES obs_points(obsid), FOREIGN KEY (flowtype) REFERENCES zz_flowtype(type));
CREATE TABLE meteo (obsid text NOT NULL, instrumentid text NOT NULL, parameter text NOT NULL, date_time text NOT NULL, reading_num double, reading_txt text, unit text, comment text, PRIMARY KEY (obsid, instrumentid, parameter, date_time), FOREIGN KEY(obsid) REFERENCES obs_points(obsid), FOREIGN KEY (parameter) REFERENCES zz_meteoparam(parameter));
CREATE TABLE seismic_data (obsid text NOT NULL, length double NOT NULL, ground double, bedrock double, gw_table double, comment text, PRIMARY KEY (obsid, Length), FOREIGN KEY (obsid) REFERENCES obs_lines(obsid));
CREATE TABLE vlf_data (obsid text NOT NULL, length double NOT NULL, real_comp double, imag_comp double, comment text, PRIMARY KEY (obsid, Length), FOREIGN KEY (obsid) REFERENCES obs_lines(obsid));
CREATE TABLE comments (obsid text NOT NULL, date_time text NOT NULL, comment text NOT NULL, staff text NOT NULL, PRIMARY KEY(obsid, date_time), FOREIGN KEY(obsid) REFERENCES obs_points(obsid), FOREIGN KEY(staff) REFERENCES zz_staff(staff));
SPATIALITE CREATE VIEW obs_p_w_qual_field AS SELECT DISTINCT a.rowid AS rowid, a.obsid AS obsid, a.geometry AS geometry FROM obs_points AS a JOIN w_qual_field AS b using (obsid);
SPATIALITE CREATE VIEW obs_p_w_qual_lab AS SELECT DISTINCT a.rowid AS rowid, a.obsid AS obsid, a.geometry AS geometry FROM obs_points AS a JOIN w_qual_lab AS b using (obsid);
SPATIALITE CREATE VIEW obs_p_w_strat AS SELECT DISTINCT a.rowid AS rowid, a.obsid AS obsid, a.h_toc AS h_toc, a.h_gs AS h_gs, a.geometry AS geometry FROM obs_points AS a JOIN stratigraphy AS b using (obsid);
SPATIALITE CREATE VIEW obs_p_w_lvl AS SELECT DISTINCT a.rowid AS rowid, a.obsid AS obsid, a.geometry AS geometry FROM obs_points AS a JOIN w_levels AS b USING (obsid);
SPATIALITE CREATE VIEW w_lvls_last_geom AS SELECT b.rowid AS rowid, a.obsid AS obsid, MAX(a.date_time) AS date_time,  a.meas AS meas,  a.level_masl AS level_masl, b.geometry AS geometry FROM w_levels AS a JOIN obs_points AS b using (obsid) GROUP BY obsid;
SPATIALITE CREATE VIEW w_qual_field_geom AS SELECT w_qual_field.rowid AS rowid, w_qual_field.obsid AS obsid, w_qual_field.staff AS staff, w_qual_field.date_time AS date_time, w_qual_field.instrument AS instrument, w_qual_field.parameter AS parameter, w_qual_field.reading_num AS reading_num, w_qual_field.reading_txt AS reading_txt, w_qual_field.unit AS unit, w_qual_field.comment AS comment, obs_points.geometry AS geometry FROM w_qual_field AS w_qual_field left join obs_points using (obsid);
SPATIALITE CREATE VIEW w_qual_lab_geom AS SELECT w_qual_lab.rowid AS rowid, w_qual_lab.obsid, w_qual_lab.depth, w_qual_lab.report, w_qual_lab.staff, w_qual_lab.date_time, w_qual_lab.anameth, w_qual_lab.parameter, w_qual_lab.reading_txt, w_qual_lab.reading_num, w_qual_lab.unit, obs_points.geometry AS geometry  FROM w_qual_lab, obs_points where w_qual_lab.obsid=obs_points.obsid;
SPATIALITE CREATE VIEW w_levels_geom AS SELECT b.rowid AS rowid, a.obsid AS obsid, a.date_time AS date_time,  a.meas AS meas,  a.h_toc AS h_toc,  a.level_masl AS level_masl, b.geometry AS geometry FROM w_levels AS a join obs_points AS b using (obsid);
SPATIALITE INSERT INTO views_geometry_columns (view_name, view_geometry, view_rowid, f_table_name, f_geometry_column, read_only) VALUES ('obs_p_w_qual_field', 'geometry', 'rowid', 'obs_points', 'geometry',1);
SPATIALITE INSERT INTO views_geometry_columns (view_name, view_geometry, view_rowid, f_table_name, f_geometry_column, read_only) VALUES ('obs_p_w_qual_lab', 'geometry', 'rowid', 'obs_points', 'geometry',1);
SPATIALITE INSERT INTO views_geometry_columns (view_name, view_geometry, view_rowid, f_table_name, f_geometry_column, read_only) VALUES ('obs_p_w_strat', 'geometry', 'rowid', 'obs_points', 'geometry',1);
SPATIALITE INSERT INTO views_geometry_columns (view_name, view_geometry, view_rowid, f_table_name, f_geometry_column, read_only) VALUES ('obs_p_w_lvl', 'geometry', 'rowid', 'obs_points', 'geometry',1);
SPATIALITE INSERT INTO views_geometry_columns (view_name, view_geometry, view_rowid, f_table_name, f_geometry_column, read_only) VALUES ('w_lvls_last_geom', 'geometry', 'rowid', 'obs_points', 'geometry',1);
SPATIALITE INSERT INTO views_geometry_columns (view_name, view_geometry, view_rowid, f_table_name, f_geometry_column, read_only) VALUES ('w_qual_field_geom', 'geometry', 'rowid', 'obs_points', 'geometry',1);
SPATIALITE INSERT INTO views_geometry_columns (view_name, view_geometry, view_rowid, f_table_name, f_geometry_column, read_only) VALUES ('w_qual_lab_geom', 'geometry', 'rowid', 'obs_points', 'geometry',1);
SPATIALITE INSERT INTO views_geometry_columns (view_name, view_geometry, view_rowid, f_table_name, f_geometry_column, read_only) VALUES ('w_levels_geom', 'geometry', 'rowid', 'obs_points', 'geometry',1);
POSTGIS CREATE VIEW obs_p_w_qual_field AS SELECT DISTINCT a.obsid AS obsid, a.geometry AS geometry FROM obs_points AS a JOIN w_qual_field AS b using (obsid);
POSTGIS CREATE VIEW obs_p_w_qual_lab AS SELECT DISTINCT a.obsid AS obsid, a.geometry AS geometry FROM obs_points AS a JOIN w_qual_lab AS b using (obsid);
POSTGIS CREATE VIEW obs_p_w_strat AS SELECT DISTINCT a.obsid AS obsid, a.h_toc AS h_toc, a.h_gs AS h_gs, a.geometry AS geometry FROM obs_points AS a JOIN stratigraphy AS b using (obsid);
POSTGIS CREATE VIEW obs_p_w_lvl AS SELECT DISTINCT a.obsid AS obsid, a.geometry AS geometry FROM obs_points AS a JOIN w_levels AS b USING (obsid);
POSTGIS CREATE VIEW w_lvls_last_geom AS SELECT a.obsid AS obsid, a.date_time AS date_time, a.meas AS meas, a.level_masl AS level_masl, c.geometry AS geometry FROM w_levels AS a JOIN (SELECT obsid, max(date_time) as date_time FROM w_levels GROUP BY obsid) as b ON a.obsid=b.obsid and a.date_time=b.date_time JOIN obs_points AS c ON a.obsid=c.obsid;
POSTGIS CREATE VIEW w_qual_field_geom AS SELECT w_qual_field.obsid AS obsid, w_qual_field.staff AS staff, w_qual_field.date_time AS date_time, w_qual_field.instrument AS instrument, w_qual_field.parameter AS parameter, w_qual_field.reading_num AS reading_num, w_qual_field.reading_txt AS reading_txt, w_qual_field.unit AS unit, w_qual_field.comment AS comment, obs_points.geometry AS geometry FROM w_qual_field AS w_qual_field left join obs_points using (obsid);
POSTGIS CREATE VIEW w_qual_lab_geom AS SELECT w_qual_lab.obsid, w_qual_lab.depth, w_qual_lab.report, w_qual_lab.staff, w_qual_lab.date_time, w_qual_lab.anameth, w_qual_lab.parameter, w_qual_lab.reading_txt, w_qual_lab.reading_num, w_qual_lab.unit, obs_points.geometry AS geometry FROM w_qual_lab, obs_points where w_qual_lab.obsid=obs_points.obsid;
POSTGIS CREATE VIEW w_levels_geom AS SELECT a.obsid AS obsid, a.date_time AS date_time,  a.meas AS meas,  a.h_toc AS h_toc,  a.level_masl AS level_masl, b.geometry AS geometry FROM w_levels AS a join obs_points AS b using (obsid);
CREATE VIEW w_flow_momflow AS SELECT obsid AS obsid,instrumentid AS instrumentid,date_time AS date_time,reading AS reading, unit AS unit, comment AS comment FROM w_flow where flowtype='Momflow';
CREATE VIEW w_flow_aveflow AS SELECT obsid AS obsid,instrumentid AS instrumentid,date_time AS date_time,reading AS reading, unit AS unit, comment AS comment FROM w_flow where flowtype='Aveflow';
CREATE VIEW w_flow_accvol AS SELECT obsid AS obsid,instrumentid AS instrumentid,date_time AS date_time,reading AS reading, unit AS unit, comment AS comment FROM w_flow where flowtype='Accvol';
CREATE INDEX idx_wquallab_odtp ON w_qual_lab(obsid, date_time, parameter);
CREATE INDEX idx_wquallab_odtpu ON w_qual_lab(obsid, date_time, parameter, unit);
CREATE INDEX idx_wqualfield_odtpu ON w_qual_field(obsid, date_time, parameter, unit);
