# -*- coding: utf-8 -*-
"""
/***************************************************************************
 This file contains dictionaries, lists and variable definitions for the Midvatten plugin. 
                              -------------------
        begin                : 2011-10-18
        copyright            : (C) 2011 by joskal
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

import locale
from collections import OrderedDict

def settingsdict():    #These are the default settings, they shall not be changed!!!
    dictionary = { 'database' : '',
            'tstable' : 'w_levels',
            'tscolumn' : 'level_masl',
            'tsdotmarkers' : 0,
            'tsstepplot' : 0,
            'xytable' : 'seismic_data',
            'xy_xcolumn' : 'length',
            'xy_y1column' : 'ground',
            'xy_y2column' : 'bedrock',
            'xy_y3column' : '',
            'xydotmarkers' : 0,
            'stratigraphytable' : 'stratigraphy',
            'wqualtable' : 'w_qual_lab',
            'wqual_paramcolumn' : 'parameter',
            'wqual_valuecolumn' : 'reading_txt',
            'wqual_date_time_format' : 'YYYY-MM-DD',
            'wqual_unitcolumn' : 'unit',
            'wqual_sortingcolumn' : '',
            'tabwidget' : 0,
            'secplotwlvltab' : 'w_levels',
            'secplotdates' : [],
            'secplottext' : '',
            'secplotdrillstop':'',
            'secplotbw':2,
            'secplotlocation':8,
            'secplotselectedDEMs':[],
            'stratigraphyplotted':0,
            'secplotlabelsplotted':0,
            'settingslocation':1,
            'custplot_tabwidget':0,
            'custplot_table1':'w_levels',
            'custplot_table2':'',
            'custplot_table3':'',
            'custplot_xcol1':'date_time',
            'custplot_xcol2':'',
            'custplot_xcol3':'',
            'custplot_ycol1':'level_masl',
            'custplot_ycol2':'',
            'custplot_ycol3':'',
            'custplot_maxtstep':0.0,
            'custplot_title':'',
            'custplot_xtitle':'',
            'custplot_ytitle':'',
            'custplot_legend':2,
            'custplot_grid':2,
            'custplot_filter1_1':'',
            'custplot_filter2_1':'',            
            'custplot_filter1_2':'',
            'custplot_filter2_2':'',            
            'custplot_filter1_3':'',
            'custplot_filter2_3':'',
            'custplot_filter1_1_selection':[],            
            'custplot_filter2_1_selection':[],            
            'custplot_filter1_2_selection':[],            
            'custplot_filter2_2_selection':[],            
            'custplot_filter1_3_selection':[],            
            'custplot_filter2_3_selection':[],
            'custplot_plottype1':'line',
            'custplot_plottype2':'line',
            'custplot_plottype3':'line',
            'piper_cl':'Klorid, Cl',
            'piper_hco3':'Alkalinitet, HCO3',
            'piper_so4':'Sulfat, SO4',
            'piper_na':'Natrium, Na',
            'piper_k':'Kalium, K',
            'piper_ca':'Kalcium, Ca',
            'piper_mg':'Magnesium, Mg',
            'piper_markers':'type'
            }
    return dictionary
    
def default_layers ():        #These may be changed
    list = ['obs_lines', 'obs_points', 'obs_p_w_qual_field', 'obs_p_w_qual_lab', 'obs_p_w_lvl', 'obs_p_w_strat', 'w_lvls_last_geom']    # This should be a list with all relevant tables and views that are to be loaded
    return list

def default_nonspatlayers():            # These may be changed
    list =  ['stratigraphy', 'w_levels', 'w_flow', 'w_qual_lab', 'w_qual_field']
    return list
    
def default_layers_w_ui():
    list = ['obs_lines', 'obs_points', 'w_lvls_last_geom']
    return list

def default_layers_w_form_logics():
    list = ['obs_lines', 'obs_points', 'w_levels', 'w_flow', 'stratigraphy']
    return list

def geocolorsymbols():    # STRATIGRAPHY PLOT - THIS IS WHERE YOU SHALL CHANGE TO YOUR OWN GEOLOGIC CODES, SYMBOLS AND COLORS
    dictionary  = { '': ('NoBrush', 'white'),
                ' ': ('NoBrush', 'white'),
                'berg': ('DiagCrossPattern', 'red'),
                'Berg': ('DiagCrossPattern', 'red'),
                'BERG': ('DiagCrossPattern', 'red'),
                'BERG': ('DiagCrossPattern', 'red'),
                'B': ('DiagCrossPattern', 'red'),
                'Rock': ('DiagCrossPattern', 'red'),
                'rock': ('DiagCrossPattern', 'red'),
                'Ro': ('DiagCrossPattern', 'red'),
                'ro': ('DiagCrossPattern', 'red'),
                'grovgrus': ('Dense6Pattern', 'darkGreen'),
                'Grovgrus': ('Dense6Pattern', 'darkGreen'),
                'Grg': ('Dense6Pattern', 'darkGreen'),
                'grg': ('Dense6Pattern', 'darkGreen'),
                'Coarse Gravel': ('Dense6Pattern', 'darkGreen'),
                'coarse Gravel': ('Dense6Pattern', 'darkGreen'),
                'coarse gravel': ('Dense6Pattern', 'darkGreen'),
                'CGr': ('Dense6Pattern', 'darkGreen'),
                'Cgr': ('Dense6Pattern', 'darkGreen'),
                'cGr': ('Dense6Pattern', 'darkGreen'),
                'cgr': ('Dense6Pattern', 'darkGreen'),
                'grus': ('Dense6Pattern', 'darkGreen'),
                'Grus': ('Dense6Pattern', 'darkGreen'),
                'GRUS': ('Dense6Pattern', 'darkGreen'),
                'Gr': ('Dense6Pattern', 'darkGreen'),
                'gr': ('Dense6Pattern', 'darkGreen'),
                'Gravel': ('Dense6Pattern', 'darkGreen'),
                'gravel': ('Dense6Pattern', 'darkGreen'),
                'mellangrus': ('Dense5Pattern', 'darkGreen'),
                'Mellangrus': ('Dense5Pattern', 'darkGreen'),
                'MELLANGRUS': ('Dense5Pattern', 'darkGreen'),
                'Grm': ('Dense5Pattern', 'darkGreen'),
                'grm': ('Dense5Pattern', 'darkGreen'),
                'Medium Gravel': ('Dense5Pattern', 'darkGreen'),
                'medium Gravel': ('Dense5Pattern', 'darkGreen'),
                'medium gravel': ('Dense5Pattern', 'darkGreen'),
                'MGr': ('Dense5Pattern', 'darkGreen'),
                'mGr': ('Dense5Pattern', 'darkGreen'),
                'Mgr': ('Dense5Pattern', 'darkGreen'),
                'mgr': ('Dense5Pattern', 'darkGreen'),
                'fingrus': ('Dense5Pattern', 'darkGreen'),
                'Fingrus': ('Dense5Pattern', 'darkGreen'),
                'FINGRUS': ('Dense5Pattern', 'darkGreen'),
                'Grf': ('Dense5Pattern', 'darkGreen'),
                'grf': ('Dense5Pattern', 'darkGreen'),
                'Fine Gravel': ('Dense5Pattern', 'darkGreen'),
                'fine Gravel': ('Dense5Pattern', 'darkGreen'),
                'fine gravel': ('Dense5Pattern', 'darkGreen'),
                'FGr': ('Dense5Pattern', 'darkGreen'),
                'Fgr': ('Dense5Pattern', 'darkGreen'),
                'fGr': ('Dense5Pattern', 'darkGreen'),
                'fgr': ('Dense5Pattern', 'darkGreen'),
                'grovsand': ('Dense4Pattern', 'green'),
                'Grovsand': ('Dense4Pattern', 'green'),
                'GROVSAND': ('Dense4Pattern', 'green'),
                'Sag': ('Dense4Pattern', 'green'),
                'sag': ('Dense4Pattern', 'green'),
                'Coarse Sand': ('Dense4Pattern', 'green'),
                'coarse Sand': ('Dense4Pattern', 'green'),
                'coarse sand': ('Dense4Pattern', 'green'),
                'CSa': ('Dense4Pattern', 'green'),
                'Csa': ('Dense4Pattern', 'green'),
                'cSa': ('Dense4Pattern', 'green'),
                'csa': ('Dense4Pattern', 'green'),
                'sand': ('Dense4Pattern', 'green'),
                'Sand': ('Dense4Pattern', 'green'),
                'SAND': ('Dense4Pattern', 'green'),
                'Sa': ('Dense4Pattern', 'green'),
                'sa': ('Dense4Pattern', 'green'),
                'mellansand': ('FDiagPattern', 'green'),
                'Mellansand': ('FDiagPattern', 'green'),
                'MELLANSAND': ('FDiagPattern', 'green'),
                'Sam': ('FDiagPattern', 'green'),
                'sam': ('FDiagPattern', 'green'),
                'Medium Sand': ('FDiagPattern', 'green'),
                'medium Sand': ('FDiagPattern', 'green'),
                'medium sand': ('FDiagPattern', 'green'),
                'MSa': ('FDiagPattern', 'green'),
                'Msa': ('FDiagPattern', 'green'),
                'msa': ('FDiagPattern', 'green'),
                'mSa': ('FDiagPattern', 'green'),
                'finsand': ('BDiagPattern', 'yellow'),
                'Finsand': ('BDiagPattern', 'yellow'),
                'FINSAND': ('BDiagPattern', 'yellow'),
                'Saf': ('BDiagPattern', 'yellow'),
                'saf': ('BDiagPattern', 'yellow'),
                'Fine Sand': ('BDiagPattern', 'yellow'),
                'fine Sand': ('BDiagPattern', 'yellow'),
                'fine Sand': ('BDiagPattern', 'yellow'),
                'FSa': ('BDiagPattern', 'yellow'),
                'Fsa': ('BDiagPattern', 'yellow'),
                'fSa': ('BDiagPattern', 'yellow'),
                'fsa': ('BDiagPattern', 'yellow'),
                'silt': ('VerPattern', 'yellow'),
                'Silt': ('VerPattern', 'yellow'),
                'SILT': ('VerPattern', 'yellow'),
                'Si': ('VerPattern', 'yellow'),
                'si': ('VerPattern', 'yellow'),
                'lera': ('HorPattern', 'darkYellow'),
                'Lera': ('HorPattern', 'darkYellow'),
                'LERA': ('HorPattern', 'darkYellow'),
                'Le': ('HorPattern', 'darkYellow'),
                'le': ('HorPattern', 'darkYellow'),
                'Clay': ('HorPattern', 'darkYellow'),
                'clay': ('HorPattern', 'darkYellow'),
                'Cl': ('HorPattern', 'darkYellow'),
                'cl': ('HorPattern', 'darkYellow'),
                'moran': ('CrossPattern', 'cyan'),
                'Moran': ('CrossPattern', 'cyan'),
                'MORAN': ('CrossPattern', 'cyan'),
                'Mn': ('CrossPattern', 'cyan'),
                'mn': ('CrossPattern', 'cyan'),
                'Till': ('CrossPattern', 'cyan'),
                'till': ('CrossPattern', 'cyan'),
                'Ti': ('CrossPattern', 'cyan'),
                'ti': ('CrossPattern', 'cyan'),
                'torv': ('NoBrush', 'darkGray'),
                'Torv': ('NoBrush', 'darkGray'),
                'TORV': ('NoBrush', 'darkGray'),
                'T': ('NoBrush', 'darkGray'),
                'Peat': ('NoBrush', 'darkGray'),
                'peat': ('NoBrush', 'darkGray'),
                'Pt': ('NoBrush', 'darkGray'),
                'pt': ('NoBrush', 'darkGray'),
                't': ('NoBrush', 'darkGray'),
                'fyll': ('DiagCrossPattern', 'white'),
                'Fyll': ('DiagCrossPattern', 'white'),
                'FYLL': ('DiagCrossPattern', 'white'),
                'fyllning': ('DiagCrossPattern', 'white'),
                'Fyllning': ('DiagCrossPattern', 'white'),
                'FYLLNING': ('DiagCrossPattern', 'white'),
                'F': ('DiagCrossPattern', 'white'),
                'f': ('DiagCrossPattern', 'white'),
                'Made Ground': ('DiagCrossPattern', 'white'),
                'Made ground': ('DiagCrossPattern', 'white'),
                'mage ground': ('DiagCrossPattern', 'white'),
                'MG': ('DiagCrossPattern', 'white'),
                'Mg': ('DiagCrossPattern', 'white'),
                'mg': ('DiagCrossPattern', 'white')
                }
    return dictionary
    
def hydrocolors(): # STRATIGRAPHY PLOT - THIS IS WHERE YOU SHALL CHANGE TO YOUR OWN capacity CODES AND COLORS
    dictionary = { '': ('okant', 'gray'),
                  ' ': ('okant', 'gray'),
                  '0': ('okant', 'gray'),
                  '0 ': ('okant', 'gray'),
                  '1': ('ovan gvy', 'red'),
                  '1 ': ('ovan gvy', 'red'),
                  '2': ('ingen', 'magenta'),
                  '2 ': ('ingen', 'magenta'),
                  '3-': ('obetydlig', 'yellow'),
                  '3': ('obetydlig', 'yellow'),
                  '3 ': ('obetydlig', 'yellow'),
                  '3+': ('obetydlig', 'darkYellow'),
                  '4-': ('mindre god', 'green'),
                  '4': ('mindre god', 'green'),
                  '4 ': ('mindre god', 'green'),
                  '4+': ('mindre god', 'darkGreen'),
                  '5-': ('god', 'cyan'),
                  '5': ('god', 'cyan'),
                  '5 ': ('god', 'cyan'),
                  '5+': ('god', 'darkCyan'),
                  '6-': ('mycket god', 'blue'),
                  '6': ('mycket god', 'blue'),
                  '6 ': ('mycket god', 'blue'),
                  '6+': ('mycket god', 'darkBlue'),
                }
    return dictionary

def stratitable(): # THIS IS THE NAME OF THE table WITH stratigraphy _ MUST NOT BE CHANGED
    return 'stratigraphy'

def standard_parameters_for_w_qual_field():
    """ Returns a dict with water quality parameters
    :return: A dict with parameter as key and unit as value
    """
    parameters = {u'konduktivitet': u'µS/cm',
                  u'pH': u'',
                  u'redoxpotential': u'mV',
                  u'syre': u'%',
                  u'syre': u'mg/L',
                  u'temperatur': u'grC',
                  u'turbiditet': u'FNU',
                  }
    return parameters

def standard_parameters_for_w_flow():
    """ Returns a dict with water flow parameters
    :return: A dict with parameter as key and unit as value
    """
    parameters = {u'Momflow': u'l/s',
                  u'Accvol': u'm3'
                  }
    return parameters

def PlotTypesDict(international='no'):#sectionplot - dictionary for possible geoshorts
    if international=='no' and  locale.getdefaultlocale()[0] == 'sv_SE': 
        """
        Dict = {u"Okänt" : u"not in ('berg','b','rock','ro','grovgrus','grg','coarse gravel','cgr','grus','gr','gravel','mellangrus','grm','medium gravel','mgr','fingrus','grf','fine gravel','fgr','grovsand','sag','coarse sand','csa','sand','sa','mellansand','sam','medium sand','msa','finsand','saf','fine sand','fsa','silt','si','lera','ler','le','clay','cl','morän','moran','mn','till','ti','torv','t','peat','pt','fyll','fyllning','f','made ground','mg','land fill')",
        "Berg"  : u"in ('berg','b','rock','ro')",
        "Grovgrus" : u"in ('grovgrus','grg','coarse gravel','cgr')",
        "Grus" : u"in ('grus','gr','gravel')",
        "Mellangrus" : u"in ('mellangrus','grm','medium gravel','mgr')",
        "Fingrus" : u"in ('fingrus','grf','fine gravel','fgr')",
        "Grovsand" : u"in ('grovsand','sag','coarse sand','csa')",
        "Sand" : u"in ('sand','sa')",
        "Mellansand" : u"in ('mellansand','sam','medium sand','msa')",
        "Finsand" : u"in ('finsand','saf','fine sand','fsa')",
        "Silt" : u"in ('silt','si')",
        "Lera" : u"in ('lera','ler','le','clay','cl')",
        u"Morän" : u"in ('morän','moran','mn','till','ti')",
        "Torv" : u"in ('torv','t','peat','pt')",
        "Fyll":u"in ('fyll','fyllning','f','made ground','mg','land fill')"}
        """
        Dict = OrderedDict([(u"Okänt" , u"not in ('berg','b','rock','ro','grovgrus','grg','coarse gravel','cgr','grus','gr','gravel','mellangrus','grm','medium gravel','mgr','fingrus','grf','fine gravel','fgr','grovsand','sag','coarse sand','csa','sand','sa','mellansand','sam','medium sand','msa','finsand','saf','fine sand','fsa','silt','si','lera','ler','le','clay','cl','morän','moran','mn','till','ti','torv','t','peat','pt','fyll','fyllning','f','made ground','mg','land fill')"),
        ("Berg"  , u"in ('berg','b','rock','ro')"),
        ("Grovgrus" , u"in ('grovgrus','grg','coarse gravel','cgr')"),
        ("Grus" , u"in ('grus','gr','gravel')"),
        ("Mellangrus" , u"in ('mellangrus','grm','medium gravel','mgr')"),
        ("Fingrus" , u"in ('fingrus','grf','fine gravel','fgr')"),
        ("Grovsand" , u"in ('grovsand','sag','coarse sand','csa')"),
        ("Sand" , u"in ('sand','sa')"),
        ("Mellansand" , u"in ('mellansand','sam','medium sand','msa')"),
        ("Finsand" , u"in ('finsand','saf','fine sand','fsa')"),
        ("Silt" , u"in ('silt','si')"),
        ("Lera" , u"in ('lera','ler','le','clay','cl')"),
        (u"Morän" , u"in ('morän','moran','mn','till','ti')"),
        ("Torv" , u"in ('torv','t','peat','pt')"),
        ("Fyll",u"in ('fyll','fyllning','f','made ground','mg','land fill')")])
    else:
        """
        Dict = {u"Unknown" : u"not in ('berg','b','rock','ro','grovgrus','grg','coarse gravel','cgr','grus','gr','gravel','mellangrus','grm','medium gravel','mgr','fingrus','grf','fine gravel','fgr','grovsand','sag','coarse sand','csa','sand','sa','mellansand','sam','medium sand','msa','finsand','saf','fine sand','fsa','silt','si','lera','ler','le','clay','cl','morän','moran','mn','till','ti','torv','t','peat','pt','fyll','fyllning','f','made ground','mg','land fill')",
        "Rock"  : u"in ('berg','b','rock','ro')",
        "Coarse gravel" : u"in ('grovgrus','grg','coarse gravel','cgr')",
        "Gravel" : u"in ('grus','gr','gravel')",
        "Medium gravel" : u"in ('mellangrus','grm','medium gravel','mgr')",
        "Fine gravel" : u"in ('fingrus','grf','fine gravel','fgr')",
        "Coarse sand" : u"in ('grovsand','sag','coarse sand','csa')",
        "Sand" : u"in ('sand','sa')",
        "Medium sand" : u"in ('mellansand','sam','medium sand','msa')",
        "Fine sand" : u"in ('finsand','saf','fine sand','fsa')",
        "Silt" : u"in ('silt','si')",
        "Clay" : u"in ('lera','ler','le','clay','cl')",
        "Till" : u"in ('morän','moran','mn','till','ti')",
        "Peat" : u"in ('torv','t','peat','pt')",
        "Fill":u"in ('fyll','fyllning','f','made ground','mg','land fill')"}
        """
        Dict = OrderedDict([("Unknown" , u"not in ('berg','b','rock','ro','grovgrus','grg','coarse gravel','cgr','grus','gr','gravel','mellangrus','grm','medium gravel','mgr','fingrus','grf','fine gravel','fgr','grovsand','sag','coarse sand','csa','sand','sa','mellansand','sam','medium sand','msa','finsand','saf','fine sand','fsa','silt','si','lera','ler','le','clay','cl','morän','moran','mn','till','ti','torv','t','peat','pt','fyll','fyllning','f','made ground','mg','land fill')"),
        ("Rock"  , u"in ('berg','b','rock','ro')"),
        ("Coarse gravel" , u"in ('grovgrus','grg','coarse gravel','cgr')"),
        ("Gravel" , u"in ('grus','gr','gravel')"),
        ("Medium gravel" , u"in ('mellangrus','grm','medium gravel','mgr')"),
        ("Fine gravel" , u"in ('fingrus','grf','fine gravel','fgr')"),
        ("Coarse sand" , u"in ('grovsand','sag','coarse sand','csa')"),
        ("Sand" , u"in ('sand','sa')"),
        ("Medium sand" , u"in ('mellansand','sam','medium sand','msa')"),
        ("Fine sand" , u"in ('finsand','saf','fine sand','fsa')"),
        ("Silt" , u"in ('silt','si')"),
        ("Clay" , u"in ('lera','ler','le','clay','cl')"),
        ("Till" , u"in ('morän','moran','mn','till','ti')"),
        ("Peat" , u"in ('torv','t','peat','pt')"),
        ("Fill",u"in ('fyll','fyllning','f','made ground','mg','land fill')")])
    return Dict

def PlotColorDict():#sectionplot - dictionary for geoshort-colors 
    if  locale.getdefaultlocale()[0] == 'sv_SE': #swedish forms are loaded only if locale settings indicate sweden
        Dict = {u"Okänt" : u"white",
        "Berg"  : u"red",
        "Grovgrus" : u"DarkGreen",
        "Grus" : u"DarkGreen",
        "Mellangrus" : u"DarkGreen",
        "Fingrus" : u"DarkGreen",
        "Grovsand" : u"green",
        "Sand" : u"green",
        "Mellansand" : u"green",
        "Finsand" : u"yellow",
        "Silt" : u"yellow",
        "Lera" : u"DarkOrange",
        u"Morän" : u"cyan",
        "Torv" : u"DarkGray",
        "Fyll":u"white"}
    else:
        Dict = {u"Unknown" : u"white",
        "Rock"  : u"red",
        "Coarse gravel" : u"DarkGreen",
        "Gravel" : u"DarkGreen",
        "Medium gravel" : u"DarkGreen",
        "Fine gravel" : u"DarkGreen",
        "Coarse sand" : u"green",
        "Sand" : u"green",
        "Medium sand" : u"green",
        "Fine sand" : u"yellow",
        "Silt" : u"yellow",
        "Clay" : u"DarkOrange",
        "Till" : u"cyan",
        "Peat" : u"DarkGray",
        "Fill":u"white"}
    return Dict

def PlotHatchDict():#sectionplot - dictionary for geoshort-hatch
    # hatch patterns : ('-', '+', 'x', '\\', '*', 'o', 'O', '.','/')
    if  locale.getdefaultlocale()[0] == 'sv_SE': #swedish forms are loaded only if locale settings indicate sweden
        Dict = {u"Okänt" : u"",
        "Berg"  : u"x",
        "Grovgrus" : u"O",
        "Grus" : u"O",
        "Mellangrus" : u"o",
        "Fingrus" : u"o",
        "Grovsand" : u"*",
        "Sand" : u"*",
        "Mellansand" : u".",
        "Finsand" : u".",
        "Silt" : u"\\",
        "Lera" : u"-",
        u"Morän" : u"/",
        "Torv" : u"+",
        "Fyll":u"+"}
    else:
        Dict = {u"Unknown" : u"",
        "Rock"  : u"x",
        "Coarse gravel" : u"O",
        "Gravel" : u"O",
        "Medium gravel" : u"o",
        "Fine gravel" : u"o",
        "Coarse sand" : u"*",
        "Sand" : u"*",
        "Medium sand" : u".",
        "Fine sand" : u".",
        "Silt" : u"\\",
        "Clay" : u"-",
        "Till" : u"/",
        "Peat" : u"+",
        "Fill":u"+"}
    return Dict
    
def SQLiteInternalTables():
    return r"""('geom_cols_ref_sys',
                'geometry_columns',
                'geometry_columns_time',
                'spatial_ref_sys',
                'spatialite_history',
                'vector_layers',
                'views_geometry_columns',
                'virts_geometry_columns',
                'geometry_columns_auth',
                'geometry_columns_fields_infos',
                'geometry_columns_field_infos',
                'geometry_columns_statistics',
                'sql_statements_log',
                'layer_statistics',
                'sqlite_sequence',
                'sqlite_stat1',
                'sqlite_stat3',
                'views_layer_statistics',
                'virts_layer_statistics',
                'vector_layers_auth',
                'vector_layers_field_infos',
                'vector_layers_statistics',
                'views_geometry_columns_auth',
                'views_geometry_columns_field_infos',
                'views_geometry_columns_statistics',
                'virts_geometry_columns_auth',
                'virts_geometry_columns_field_infos',
                'virts_geometry_columns_statistics' ,
                'geometry_columns',
                'spatialindex',
                'SpatialIndex')"""
