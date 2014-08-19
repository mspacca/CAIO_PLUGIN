###########################################################################
#     Sint Wind PI
#     Copyright 2012 by Tonino Tarsi <tony.tarsi@gmail.com>
#   
#     Please refer to the LICENSE file for conditions 
#     Visit http://www.vololiberomontecucco.it
# 
##########################################################################

"""MeteoData class"""

import time
import sqlite3
import datetime
#import TTLib
#import config
import math
import os
import globalvars

class MeteoData(object):
    
    def __init__(self,cfg=None):
        
        self.cfg = cfg
        
        self.last_measure_time = None
        self.previous_measure_time = None

        self.wind_trend = None
        self.pressure_trend = None
        # Station data
        self.idx = None
        self.status = -9999
        self.wind_dir = None
        self.wind_ave = None
        self.wind_gust = None

        self.temp_out = None
        self.hum_out = None
        self.abs_pressure = None
        self.rel_pressure = None
        self.rain = None
        self.rain_rate = None
        self.rain_rate_24h = None
        self.rain_rate_1h= None
        
        self.temp_in = None
        self.hum_in = None
        self.uv = None
        self.illuminance = None        
        
        if ( cfg != None):
            self.rb_wind_dir = TTLib.RingBuffer(cfg.number_of_measure_for_wind_dir_average)
            self.rb_wind_trend = TTLib.RingBuffer(cfg.number_of_measure_for_wind_trend)
            
        #calculated values
        self.wind_dir_code = None
        self.wind_chill = None
        self.temp_apparent = None
        self.dew_point = None
        self.cloud_base_altitude = None
        
        self.previous_rain = None   
        
        self.wind_dir_ave = None
        
 
if __name__ == '__main__':

    configfile = 'swpi.cfg'
    
    cfg = config.config(configfile)
   
    mt = MeteoData(cfg)
    
    conn = sqlite3.connect('db/swpi.s3db',200)    
    dbCursor = conn.cursor()
    dbCursor.execute("SELECT * FROM METEO where datetime(TIMESTAMP_LOCAL) > datetime('now','-1 day','localtime') order by rowid asc limit 1")
    data = dbCursor.fetchall()
    if ( len(data) == 1):
        therain = (data[0][9])    
        mt.rain_rate_24h = therain
        print  mt.rain_rate_24h
    else : print " nodara"
    dbCursor.execute("SELECT * FROM METEO where datetime(TIMESTAMP_LOCAL) > datetime('now','-1 hour','localtime') order by rowid asc limit 1")
    data = dbCursor.fetchall()
    if ( len(data) == 1):
        therain = (data[0][9])    
        mt.rain_rate_1h = therain  
        print  mt.rain_rate_1h
    else : print " nodara" 
    if conn:        
        conn.close()
#        except:
#            pass
    
#    mt.getLastFromDB()
#    mt.getLastTodayFromDB()
    
 

