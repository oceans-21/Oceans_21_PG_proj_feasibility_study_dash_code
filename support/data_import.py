# -*- coding: utf-8 -*-
"""
Created on Wed Apr 08 11:10:36 2015

@author: GWessels
"""

from datetime import datetime
try:
    ## Python 2.x
    from itertools import izip
except ImportError:
    ## Python 3.x
    izip = zip

class Data_Import:
    def __init__(self):
        self.data = []
        self.referencedate = datetime(1900,1,1,0,0)
        self.date_time = []
        self.minutes = []
        self.columns = {'date':-1, 'year':-1, 'month':-1, 'day':-1, 'time':-1, 
               'hour':-1, 'minutes':-1, 'tempavg':-1, 'tempmin':-1, 
               'tempmax':-1, 'timeof_tempmax':-1, 'timeof_tempmin':-1, 
               'barometricpress':-1, 'fog':-1, 'rainfall':-1, 'relhumidity':-1, 
               'solarrad':-1, 'solarradmax':-1, 'winddir':-1, 
               'windspeedavg':-1, 'windspeedmin':-1, 'windspeedmax':-1, 
               'windspeedmaxdur':-1, 'timeof_windspeedmax':-1, 
               'windspeedstddev':-1, 'windspeedmaxdir':-1, 'hmo':-1, 'h1f':-1, 
               'tp':-1, 'tz':-1, 'tcf':-1, 'tbf':-1, 'dir':-1, 'spr':-1, 
               'hs':-1, 'hmax':-1, 'instrcode':-1, 'currentspeed':-1, 
               'currentdir':-1, 'watertemp':-1, 'vertvel':-1, 'ph':-1, 
               'salinity':-1, 'disolved_O2':-1, 'currentx':-1, 'currenty':-1}
        self.column_names = {'date':'Date', 'year':'Year', 'month':'Month', 
               'day':'Day', 'time':'Time', 'hour':'Hour', 'minutes':'Minutes', 
               'tempavg':'Average Temperature', 
               'tempmin':'Minimum Temperature',
               'tempmax':'Maximum Temperature',
               'timeof_tempmax':'Time of Max. Temperature', 
               'timeof_tempmin':'Time of Min. Temperature', 
               'barometricpress':'Barometric Pressure', 'fog':'Fog',
               'rainfall':'Rainfall', 'relhumidity':'Relative Humidity',
               'solarrad':'Solar Radiation', 
               'solarradmax':'Solar Radiation Maximum', 
               'winddir':'Wind Direction', 'windspeedavg':'Wind Speed Average', 
               'windspeedmin':'Wind Speed Minimum', 
               'windspeedmax':'Wind Speed Maximum',
               'windspeedmaxdur':'Duraton of Wind Speed Maximum',
               'timeof_windspeedmax':'Time of Wind Speed Maximum', 
               'windspeedstddev':'Wind Speed Standard Deviation', 
               'windspeedmaxdir':'Wind Speed Maximum Direction', 'hmo':'HMO', 
               'h1f':'H1F', 'tp':'TP', 'tz':'TZ', 'tcf':'TCF', 'tbf':'TBF', 
               'dir':'DIR', 'spr':'SPR', 'hs':'HS', 'hmax':'HMAX', 
               'instrcode':'INSTR CODE', 'currentspeed':'Current Speed', 
               'currentdir':'Current Direction', 
               'watertemp':'Water Temperature', 'vertvel':'Vertical Velocity', 
               'ph':'pH', 'salinity':'Salinity', 
               'disolved_O2':'Disolved Oxygen', 
               'currentx':'Current Speed X Compenent', 
               'currenty':'Current Speed Y Compenent'}
        self.column_nodata = {'date':9999-99-99, 'year':9999, 'month':99, 
               'day':99, 'time':9999, 'hour':99, 'minutes':99, 'tempavg':99.99, 
               'tempmin':99.99, 'tempmax':99.99, 'timeof_tempmax':99.99, 
               'timeof_tempmin':99.99, 'barometricpress':9999.9, 'fog':999.9, 
               'rainfall':999.9, 'relhumidity':999.9, 'solarrad':9999.9, 
               'solarradmax':9999.9, 'winddir':999.9, 'windspeedavg':99.99, 
               'windspeedmin':99.99, 'windspeedmax':99.99, 
               'windspeedmaxdur':99, 'timeof_windspeedmax':99.99, 
               'windspeedstddev':99.99, 'windspeedmaxdir':999.9, 'hmo':999.99, 
               'h1f':999.99, 'tp':999.99, 'tz':999.99, 'tcf':999.99, 
               'tbf':999.99, 'dir':999.99, 'spr':999.99, 'hs':999.99, 
               'hmax':999.99, 'instrcode':999.99, 'currentspeed':999.999, 
               'currentdir':999.9, 'watertemp':99.99, 'vertvel':99.99, 
               'ph':99.99, 'salinity':99.99, 'disolved_O2':99.99,
               'currentx':999.999, 'currenty':999.999}
    
    def read_data(self,dat_file):
        
        sort_col = self.active_columns()        
        
        datetimeopt = True
        
        if self.columns['date'] == -1:
            datetimeopt = False

        
        with open(dat_file,'r') as f:
            for line in f:
                if line[0:4] == 'DATA':
                    break
                
            self.data = []
            for line in f:
                if line[0:3] != 'END':
                    tmp = []
                    for col in sort_col:
                        try:
                            tmp.append(line.split()[self.columns[col]])
                        except:
                            print("Missing col: "+str(col))
                    
                    self.data.append(tmp)
                    
                    if datetimeopt:
                        tmp_str = line.split()[self.columns['date']]+' '+line.split()[self.columns['time']]
                        dt = datetime.strptime(tmp_str,"%Y-%m-%d %H:%M")
                        self.date_time.append(dt)
                        self.minutes.append(self.difference_in_minutes(dt))
                    else:
                        if self.columns['time']<0:
                            y = int(line.split()[self.columns['year']])
                            m = int(line.split()[self.columns['month']])
                            d = int(line.split()[self.columns['day']])
                            h = int(line.split()[self.columns['hour']])
                            mm = int(line.split()[self.columns['minutes']])
                        else:
                            y = int(line.split()[self.columns['year']])
                            m = int(line.split()[self.columns['month']])
                            d = int(line.split()[self.columns['day']])
                            t = int(line.split()[self.columns['time']])
                            h = int(t/100)
                            mm = int(t-h*100)
                            
                        self.date_time.append(datetime(y,m,d,h,mm))
                        self.minutes.append(self.difference_in_minutes(datetime(y,m,d,h,mm)))
                    

    def set_reference_date(self,y,mth,d,h,m):
        self.referencedate = datetime(y,mth,d,h,m)

    def difference_in_minutes(self,dt):
        td = dt - self.referencedate
        return td.days*24*60 + td.seconds/60
        
    def return_limits(self, start_datetime, end_datetime):
        return_data = []
        
        try:
            if start_datetime > end_datetime:
                raise ValueError()
        except TypeError as err:
            print("Type Error")
            print(err.args) 
        except ValueError as err:
            print("Value Error: Start date needs to be smaller than end date")
            print(err.args)
        
        for x,y,z in izip(self.date_time, self.minutes, self.data):
            if start_datetime <= x and end_datetime >= x:
                return_data.append([x,y,z])
                
        return return_data

    def set_date_column(self,c):
        self.columns['date'] = c
    def set_year_column(self,c):
        self.columns['year'] = c
    def set_month_column(self,c):
        self.columns['month'] = c
    def set_day_column(self,c):
        self.columns['day'] = c
    def set_time_column(self,c):
        self.columns['time'] = c
    def set_hour_column(self,c):
        self.columns['hour'] = c
    def set_minute_column(self,c):
        self.columns['minutes'] = c
        
    def set_tempavg_column(self,c):
        self.columns['tempavg'] = c
    def set_tempmin_column(self,c):
        self.columns['tempmin'] = c
    def set_tempmax_column(self,c):
        self.columns['tempmax'] = c
    def set_timeof_tempmax_column(self,c):
        self.columns['timeof_tempmax'] = c
    def set_timeof_tempmin_column(self,c):
        self.columns['timeof_tempmin'] = c
    def set_barometricpress_column(self,c):
        self.columns['barometricpress'] = c
    def set_fog_column(self,c):
        self.columns['fog'] = c
    def set_rainfall_column(self,c):
        self.columns['rainfall'] = c
    def set_relhumidity_column(self,c):
        self.columns['relhumidity'] = c
    def set_solarrad_column(self,c):
        self.columns['solarrad'] = c
    def set_solarradmax_column(self,c):
        self.columns['solarradmax'] = c
    def set_winddir_column(self,c):
        self.columns['winddir'] = c
    def set_windspeedavg_column(self,c):
        self.columns['windspeedavg'] = c
    def set_windspeedmin_column(self,c):
        self.columns['windspeedmin'] = c
    def set_windspeedmax_column(self,c):
        self.columns['windspeedmax'] = c
    def set_timeof_windspeedmax_column(self,c):
        self.columns['timof_windspeedmax'] = c
    def set_windspeedmaxdur_column(self,c):
        self.columns['windspeedmaxdur'] = c
    def set_windspeedstddev_column(self,c):
        self.columns['windspeedstddev'] = c
    def set_windspeedmaxdir_column(self,c):
        self.columns['windspeedmaxdir'] = c
        
    def set_hmo_column(self,c):
        self.columns['hmo'] = c
    def set_h1f_column(self,c):
        self.columns['h1f'] = c
    def set_tp_column(self,c):            
        self.columns['tp'] = c
    def set_tz_column(self,c):
        self.columns['tz'] = c
    def set_tcf_column(self,c):
        self.columns['tcf'] = c
    def set_tbf_column(self,c):
        self.columns['tbf'] = c
    def set_dir_column(self,c):
        self.columns['dir'] = c
    def set_spr_column(self,c):
        self.columns['spr'] = c
    def set_hs_column(self,c):
        self.columns['hs'] = c
    def set_hmax_column(self,c):
        self.columns['hmax'] = c
    def set_instrcode_column(self,c):
        self.columns['instrcode'] = c
        
    def set_currentspeed_column(self,c):
        self.columns['currentspeed'] = c
    def set_currentdir_column(self,c):
        self.columns['currentdir'] = c
    def set_watertemp_column(self,c):
        self.columns['watertemp'] = c
    def set_vertvel_column(self,c):
        self.columns['vertvel'] = c
    def set_ph_column(self,c):
        self.columns['ph'] = c
    def set_salinity_column(self,c):
        self.columns['salinity'] = c
    def set_disolved_O2_column(self,c):
        self.columns['disolved_O2'] = c
        
    def set_currentx_column(self,c):
        self.columns['currentx'] = c
    def set_currenty_column(self,c):
        self.columns['currenty'] = c
        
    def set_date_placeholder(self,c):
        self.column_nodata['date'] = c
    def set_year_placeholder(self,c):
        self.column_nodata['year'] = c
    def set_month_placeholder(self,c):
        self.column_nodata['month'] = c
    def set_day_placeholder(self,c):
        self.column_nodata['day'] = c
    def set_time_placeholder(self,c):
        self.column_nodata['time'] = c
    def set_hour_placeholder(self,c):
        self.column_nodata['hour'] = c
    def set_minute_placeholder(self,c):
        self.column_nodata['minutes'] = c
        
    def set_tempavg_placeholder(self,c):
        self.column_nodata['tempavg'] = c
    def set_tempmin_placeholder(self,c):
        self.column_nodata['tempmin'] = c
    def set_tempmax_placeholder(self,c):
        self.column_nodata['tempmax'] = c
    def set_timeof_tempmax_placeholder(self,c):
        self.column_nodata['timeof_tempmax'] = c
    def set_timeof_tempmin_placeholder(self,c):
        self.column_nodata['timeof_tempmin'] = c
    def set_barometricpress_placeholder(self,c):
        self.column_nodata['barometricpress'] = c
    def set_fog_placeholder(self,c):
        self.column_nodata['fog'] = c
    def set_rainfall_placeholder(self,c):
        self.column_nodata['rainfall'] = c
    def set_relhumidity_placeholder(self,c):
        self.column_nodata['relhumidity'] = c
    def set_solarrad_placeholder(self,c):
        self.column_nodata['solarrad'] = c
    def set_solarradmax_placeholder(self,c):
        self.column_nodata['solarradmax'] = c
    def set_winddir_placeholder(self,c):
        self.column_nodata['winddir'] = c
    def set_windspeedavg_placeholder(self,c):
        self.column_nodata['windspeedavg'] = c
    def set_windspeedmin_placeholder(self,c):
        self.column_nodata['windspeedmin'] = c
    def set_windspeedmax_placeholder(self,c):
        self.column_nodata['windspeedmax'] = c
    def set_timeof_windspeedmax_placeholder(self,c):
        self.column_nodata['timof_windspeedmax'] = c
    def set_windspeedmaxdur_placeholder(self,c):
        self.column_nodata['windspeedmaxdur'] = c
    def set_windspeedstddev_placeholder(self,c):
        self.column_nodata['windspeedstddev'] = c
    def set_windspeedmaxdir_placeholder(self,c):
        self.column_nodata['windspeedmaxdir'] = c
        
    def set_hmo_placeholder(self,c):
        self.column_nodata['hmo'] = c
    def set_h1f_placeholder(self,c):
        self.column_nodata['h1f'] = c
    def set_tp_placeholder(self,c):            
        self.column_nodata['tp'] = c
    def set_tz_placeholder(self,c):
        self.column_nodata['tz'] = c
    def set_tcf_placeholder(self,c):
        self.column_nodata['tcf'] = c
    def set_tbf_placeholder(self,c):
        self.column_nodata['tbf'] = c
    def set_dir_placeholder(self,c):
        self.column_nodata['dir'] = c
    def set_spr_placeholder(self,c):
        self.column_nodata['spr'] = c
    def set_hs_placeholder(self,c):
        self.column_nodata['hs'] = c
    def set_hmax_placeholder(self,c):
        self.column_nodata['hmax'] = c
    def set_instrcode_placeholder(self,c):
        self.column_nodata['instrcode'] = c
        
    def set_currentspeed_placeholder(self,c):
        self.column_nodata['currentspeed'] = c
    def set_currentdir_placeholder(self,c):
        self.column_nodata['currentdir'] = c
    def set_watertemp_placeholder(self,c):
        self.column_nodata['watertemp'] = c
    def set_vertvel_placeholder(self,c):
        self.column_nodata['vertvel'] = c
    def set_ph_placeholder(self,c):
        self.column_nodata['ph'] = c
    def set_salinity_placeholder(self,c):
        self.column_nodata['salinity'] = c
    def set_disolved_O2_placeholder(self,c):
        self.column_nodata['disolved_O2'] = c
    
    def set_currentx_placeholder(self,c):
        self.column_nodata['currentx'] = c
    def set_currenty_placeholder(self,c):
        self.column_nodata['currenty'] = c

    def reset_columns(self):
        for key in self.columns.keys():
            self.columns[key] = -1
        
    def set_default_adcp_columns(self):
        self.reset_columns()
        self.set_date_column(0)
        self.set_time_column(1)
        self.set_currentspeed_column(2)
        self.set_currentdir_column(3)
        self.set_watertemp_column(4)
        self.set_vertvel_column(5)
        self.set_ph_column(10)
        self.set_salinity_column(11)        
        self.set_disolved_O2_column(12)
    
    def set_default_wind_columns(self):
        self.reset_columns()
        self.set_year_column(1)
        self.set_month_column(2)
        self.set_day_column(3)
        self.set_hour_column(4)
        self.set_minute_column(5)
        self.set_tempavg_column(6)
        self.set_tempmin_column(7)
        self.set_timeof_tempmin_column(8)
        self.set_tempmax_column(9)        
        self.set_timeof_tempmax_column(10)
        self.set_barometricpress_column(11)
        self.set_fog_column(12)
        self.set_rainfall_column(13)
        self.set_relhumidity_column(14)
        self.set_solarrad_column(15)
        self.set_solarradmax_column(16)
        self.set_winddir_column(17)
        self.set_windspeedavg_column(18)
        self.set_windspeedmin_column(19)
        self.set_windspeedmax_column(20)
        self.set_timeof_windspeedmax_column(21)
        self.set_windspeedmaxdur_column(22)
        self.set_windspeedstddev_column(23)
        self.set_windspeedmaxdir_column(24)

    def set_default_ncep_wave_columns(self):
        self.reset_columns()
        self.set_year_column(1)
        self.set_month_column(2)
        self.set_day_column(3)
        self.set_time_column(4)
#        self.set_hour_column(4)
#        self.set_minute_column(5)
        self.set_hmo_column(5)
        self.set_h1f_column(6)
        self.set_tp_column(7)
        self.set_tz_column(8)
        self.set_tcf_column(9)
        self.set_tbf_column(10)
        self.set_dir_column(11)
        self.set_spr_column(12)
        self.set_hs_column(13)
        self.set_hmax_column(14)
        self.set_instrcode_column(15)
        
    
    def print_columns_numbers(self):
        sort = self.active_columns()
        for item in sort:
            print(str(self.columns[item]) + ": " + self.column_names[item])
            
    def active_columns(self):
        temp_key = [key for key in self.columns.keys()]
        sort = sorted(temp_key, key=self.columns.__getitem__)
        returnlist = []
        for item in sort:
            if self.columns[item]>-1:
                returnlist.append(item)
        return returnlist
        
    def print_minutes(self):
                
        
        for item in self.minutes:        
            print(item)