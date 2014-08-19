###########################################################################
#     Sint Wind PI
#     Copyright 2012 by Tonino Tarsi <tony.tarsi@gmail.com>
#
#     USB comunication based pywws by 'Jim Easterbrook' <jim@jim-easterbrook.me.uk>
#     Please refer to the LICENSE file for conditions
#     Visit http://www.vololiberomontecucco.it
#
#     plugin per invio dati a vecchia configurazione meteo caio
#     (C) Mauro Pelagatti 2014
#     
#     V 1.0     18/08/2014
##########################################################################

"""caio plugin."""

import threading
import random
import datetime
import sys
import subprocess
import sys
import os
import thread
import time
import requests
import globalvars
import meteodata
import urllib
from TTLib import  *

class swpi_plugin(threading.Thread):  #  do not change the name of the class

    def __init__(self):

        ###################### Plugin Initialization ################
        self.last_measure_time = None
        self.sleep_time=600         # Attesa 10 Minuti
        self.url = "http://www.deltaeparapendio.it/a.php"
        self.station = "CAIO"
        self.pluginName = str(sys.modules[__name__])
        
        threading.Thread.__init__(self)
        ###################### End Initialization ##################

    def logToServer(self):

        if ( globalvars.meteo_data.last_measure_time == None):
            return


        if(globalvars.meteo_data.last_measure_time == self.last_measure_time):
            log("CaioPlugin: No change detected")
            return


    #           globalvars.meteo_data.hum_out = hum
    #           globalvars.meteo_data.temp_out = temp
    #           globalvars.meteo_data.wind_ave   = Wind_speed
    #           globalvars.meteo_data.wind_gust = Gust_Speed
    #           globalvars.meteo_data.wind_dir = dire*22.5
    #           globalvars.meteo_data.wind_dir_code = dir_code
    #           globalvars.meteo_data.rain = rain
    #           globalvars.meteo_data.winDayMin
    #           globalvars.meteo_data.rain_rate
    #           globalvars.meteo_data.wind_chill
    #           globalvars.meteo_data.temp_apparent
    #           globalvars.meteo_data.dew_point
    #           globalvars.meteo_data.winDayMax
    #           globalvars.meteo_data.winDayGustMin
    #           globalvars.meteo_data.winDayGustMax
    #           globalvars.meteo_data.TempOutMin
    #           globalvars.meteo_data.TempOutMax
    #           globalvars.meteo_data.wind_dir_ave
    #           globalvars.meteo_data.rain_rate_24h
    #           globalvars.meteo_data.rain_rate_1h
    #           globalvars.meteo_data.battery
    #

        self.last_measure_time = globalvars.meteo_data.last_measure_time
        param_list = []

        param_list.append("2")      # Unita di misura in Km/h
        if globalvars.meteo_data.wind_dir != None : param_list.append(self._direzione_testo(int(globalvars.meteo_data.wind_dir)))
        else :
            param_list.append("XXX");
        if globalvars.meteo_data.wind_gust != None : param_list.append(int(globalvars.meteo_data.wind_gust))
        else :
            param_list.append("0");
        if globalvars.meteo_data.winDayMax != None : param_list.append(int(globalvars.meteo_data.winDayMax))
        else :
            param_list.append("0");
        if globalvars.meteo_data.wind_ave != None : param_list.append(int(globalvars.meteo_data.wind_ave))
        else :
            param_list.append("0");
        if globalvars.meteo_data.wind_dir_ave != None : param_list.append(self._direzione_testo(int(globalvars.meteo_data.wind_dir_ave)))
        else :
            param_list.append("XXX");
        if globalvars.meteo_data.temp_out != None : param_list.append(int(globalvars.meteo_data.temp_out))
        else :
            param_list.append("0");
        
        DataOra = str(datetime.now()) 
        
        Data = "%s/%s/%s" % (DataOra[8:10],DataOra[5:7],DataOra[0:4])  # dd/mm/yyyy
        Ora = "%s:%s" % (DataOra[11:13],DataOra[14:16])                # hh:mm
        
        param_list.append(Data)
        param_list.append(Ora)
        
        parameters = '?K=c46483fcc5&' + _crea_url(param_list) # Crea la stringa parametri da passare all'url
        
        log(self.pluginName + " url: " + self.url + " - Parameters: " + parameters)
        try:
            r = requests.get(self.url+parameters,timeout=10)
            msg = r.text.splitlines()
            if len(msg) > 0:
                log("Log to " + self.station + " Result: " +  msg[0])
            else:
                log("Log to " + self.station + " Result ok")
        except Exception,e:
            log("Error Logging to " + self.station & " " + str(e) )


    def _crea_url(self, parameters_list):
        ''' CHIAMATA URL e PASSAGGIO VALORI PER IL SITO 
        2 =unita di misura in Km/h, DIR ISTANT, VEL REALE,VEL MAX,VEL MED, DIR MEDIA, TEMPERATURA, DATA, ORA 
        '''
        lista_nomi_parametri = ["U","DI","VI","VX","VM","DP","T","D","H"]   # NOMI PARAMETRI DA PASSARE ALL'URL
        
        diz_params = {}
        for p, v in zip(lista_nomi_parametri, parameters_list):
            diz_params[p] = v        # CREO DIZIONARIO NOME:VALORE
        
        params = urllib.urlencode(diz_params) 
        #   http://www.deltaeparapendio.it/a.php?K=c46483fcc5&U=2&DI=NNE&VI=1&VX=80&VM=50&DP=SSE&T=24&D=0%H=0"
        #   print (url+"?%s" % params)
        return(params)

    def _direzione_testo(self,direzione_gradi):
        direzione_text = ""
        if direzione_gradi >=0 and direzione_gradi <= 22.5:
            direzione_text = "N"
        elif direzione_gradi >22.5 and direzione_gradi <= 45:
            direzione_text = "NNE"
        elif direzione_gradi >45 and  direzione_gradi <= 67.5:
            direzione_text = "NE"
        elif direzione_gradi >67.5 and direzione_gradi <= 90:
            direzione_text = "ENE"
        elif direzione_gradi >90 and direzione_gradi <= 112.5:
            direzione_text = "E"
        elif direzione_gradi >112.5 and direzione_gradi <= 135:
            direzione_text = "ESE"
        elif direzione_gradi >135 and direzione_gradi <= 157.5:
            direzione_text = "SE"
        elif direzione_gradi >=157.5 and direzione_gradi <= 180:
            direzione_text = "SSE"
        elif direzione_gradi >180 and direzione_gradi <= 202.5:
            direzione_text = "S"
        elif direzione_gradi >202.5 and direzione_gradi <= 225:
            direzione_text = "SSO"
        elif direzione_gradi >225 and direzione_gradi <= 247.5:
            direzione_text = "SO"
        elif direzione_gradi >247.5 and direzione_gradi <= 270:
            direzione_text = "OSO"
        elif direzione_gradi >270 and direzione_gradi <= 292.5:
            direzione_text = "O"
        elif direzione_gradi >292.5 and direzione_gradi <= 315:
            direzione_text = "ONO"
        elif direzione_gradi >315 and direzione_gradi <= 337.5:
            direzione_text = "NO"
        elif direzione_gradi >337.5 and direzione_gradi <= 360:
            direzione_text = "NNO"
        else:
            direzione_text = "errore"
        return (direzione_text)

    def run(self):
        log("Starting plugin : %s" % sys.modules[__name__])
        while 1:
        ###################### Plugin run ######################
            time.sleep(self.sleep_time)
            if ( globalvars.meteo_data.status == 0 ):
                if ( globalvars.meteo_data.last_measure_time != None and  globalvars.meteo_data.status == 0 ) :
                    log("Logging data to %s " % self.pluginName )
                    self.logToServer()
        ###################### end of Plugin run ######################

if __name__ == '__main__':
    a = swpi_plugin()
    a.run()
    
    
    
