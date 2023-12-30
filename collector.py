import aiohttp
import asyncio
import datetime
import logging
import requests

from homeassistant.util import Throttle

from .const import (
    MAP_MDI_ICON, MAP_UV,
    URL_NORMAL,
    URL_DETAILED,
    URL_BASE,
    CURRENT_WEATHER_DESCRIPTION, 
    CURRENT_WEATHER_SHORT_DESCRIPTION,
    CURRENT_WEATHER_TEMP, 
    CURRENT_WEATHER_TEXT,
    SUNRISE,
    SUNSET,
    FORCAST_EXTENDED_DESCRIPTION,
    HOURLY_FORCAST,
    HOURLY_FORCAST_HOUR,
    HOURLY_FORCAST_TEMP,
    HOURLY_FORCAST_RAIN_CHANCE,
    HOURLY_FORCAST_RAIN_LEVEL,
    HOURLY_FORCAST_WIND, 
    HOURLY_FORCAST_ICON_CONTAINER,
    HOURLY_FORCAST_ICON,
    HOURLY_FORCAST_ALERT,
    DAILY_FORCAST,
    DAILY_FORCAST_DAY,
    DAILY_FORCAST_DESCRIPTION,
    DAILY_FORCAST_DESCRIPTION_LINE,
    DAILY_FORCAST_TEMP_MIN,
    DAILY_FORCAST_TEMP_MAX,
    DAILY_FORCAST_TEMP_RECORD_MIN,
    DAILY_FORCAST_TEMP_RECORD_MAX,
    DAILY_FORCAST_TEMP_RECORD_MIN_LOCATION,
    DAILY_FORCAST_TEMP_RECORD_MAX_LOCATION,
    DAILY_FORCAST_RAIN,
    DAILY_FORCAST_RAIN_LEVEL,
    DAILY_FORCAST_ICON,
    DAILY_FORCAST_ALERT_ICON,
    
    ATTR_API_TEMP,
    ATTR_API_TEMP_FEELS_LIKE,
    ATTR_API_MAX_TEMP,
    ATTR_API_MIN_TEMP,
    ATTR_API_RAIN_SINCE_9AM,
    ATTR_API_HUMIDITY, 
    ATTR_API_WIND_SPEED_KILOMETRE,
    ATTR_API_WIND_SPEED_KNOT,
    ATTR_API_WIND_DIRECTION,
    ATTR_API_GUST_SPEED_KILOMETRE,
    ATTR_API_GUST_SPEED_KNOT,

    ATTR_API_TEMP_MAX,
    ATTR_API_TEMP_MIN,
    ATTR_API_EXTENDED_TEXT,
    ATTR_API_ICON_DESCRIPTOR,
    ATTR_API_MDI_ICON,
    ATTR_API_SHORT_TEXT,
    ATTR_API_UV_CATEGORY,
    ATTR_API_UV_MAX_INDEX,
    ATTR_API_UV_START_TIME,
    ATTR_API_UV_END_TIME,
    ATTR_API_UV_FORECAST,
    ATTR_API_RAIN_AMOUNT_MIN,
    ATTR_API_RAIN_AMOUNT_MAX,
    ATTR_API_RAIN_AMOUNT_RANGE,
    ATTR_API_RAIN_CHANCE,
    ATTR_API_FIRE_DANGER,
    ATTR_API_NON_NOW_LABEL,
    ATTR_API_NON_TEMP_NOW,
    ATTR_API_NOW_LATER_LABEL,
    ATTR_API_NOW_TEMP_LATER,
    ATTR_API_ASTRONOMICAL_SUNRISE_TIME,
    ATTR_API_ASTRONOMICAL_SUNSET_TIME,
    ATTR_API_WARNINGS,
)
from .helpers import (
    TIMEZONE,
    parseDate, parseAstronomicalTime, getNow, getToday,
    convert_int,
)

from bs4 import BeautifulSoup

_LOGGER = logging.getLogger(__name__)

class Collector:

    def __init__(self, city):
        """Init collector."""
        self.locations_data = None
        self.daily_forecasts_data = None
        self.hourly_forecasts_data = None
        self.warnings_data = None
        self.city = city

    @Throttle(datetime.timedelta(minutes=5))
    async def async_update(self):
        rain_chance_max=0
        """Collecting main informations"""
        async with aiohttp.ClientSession() as session:
            async with session.get(URL_BASE + URL_NORMAL + self.city) as resp:
                soup = BeautifulSoup(await resp.text(), features="html.parser")
                loc_data = dict()

                loc_data["current"] = {
                    ATTR_API_TEMP : float(soup.find('div', attrs={'class': CURRENT_WEATHER_TEMP}).text.replace("\n","").replace("\r","").replace("˚C","").strip()),
                    ATTR_API_SHORT_TEXT : soup.find('div', attrs={'class': CURRENT_WEATHER_SHORT_DESCRIPTION}).text.replace("\n","").replace("\r","").strip() + " - " + soup.find('div', attrs={'class': CURRENT_WEATHER_DESCRIPTION}).text.replace("\n","").replace("\r","").strip()
                }
                hfc=soup.find('div', attrs={'class': CURRENT_WEATHER_TEXT})
                idx1=hfc.text.lower().index(SUNRISE+" ")
                idx2=hfc.text.index("\n",idx1)
                loc_data["current"].update({ATTR_API_ASTRONOMICAL_SUNRISE_TIME : parseAstronomicalTime(hfc.text[idx1+9:idx2])})
                idx1=hfc.text.lower().index(SUNSET+" ")
                idx2=hfc.text.index("\n",idx1)
                loc_data["current"].update({ATTR_API_ASTRONOMICAL_SUNSET_TIME : parseAstronomicalTime(hfc.text[idx1+10:idx2])})
                loc_data.update({"timezone": TIMEZONE})
                 
        """Collecting hourly informations"""
        async with aiohttp.ClientSession() as session:
            async with session.get(URL_BASE + URL_DETAILED + self.city) as resp:
                soup = BeautifulSoup(await resp.text(), features="html.parser")
                hf_data=dict()
                hfc=soup.find_all('div', attrs={'class': HOURLY_FORCAST})
                hours = len(hfc)
                
                dtime=getToday()
                
                loc_data["current"].update({ATTR_API_EXTENDED_TEXT: soup.find('div', attrs={'class': FORCAST_EXTENDED_DESCRIPTION}).text})
                
                for hour in range(0, hours):
                    soup2 = BeautifulSoup(str(hfc[hour].contents), features="html.parser")
                    if hour == 0:                    
                        hs=soup2.find('div', attrs={'class': HOURLY_FORCAST_HOUR}).text.replace("\n","").replace("\r","").strip()
                        dtime = dtime + datetime.timedelta(hours=int(hs[0:hs.index(":")]))
                        
                    tmp_dict = dict()
                    tmp_dict = {
                        "time" : dtime + datetime.timedelta(hours=hour),
                        ATTR_API_TEMP_MAX : soup2.find('div', attrs={'class': HOURLY_FORCAST_TEMP}).text.replace("\n","").replace("\r","").strip()
                    }
                    t=soup2.find('div', attrs={'class': HOURLY_FORCAST_RAIN_CHANCE})
                    if (t is not None) and (t != ''):
                        rc=convert_int(t.text.replace("\n","").replace("\r","").replace("%","").strip())
                        tmp_dict.update({ATTR_API_RAIN_CHANCE : rc})
                        if hour>24 and rain_chance_max<rc:
                            rain_chance_max=rc
                    else:    
                        tmp_dict.update({ATTR_API_RAIN_CHANCE : 0})

                    t=soup2.find('div', attrs={'class': HOURLY_FORCAST_RAIN_LEVEL})

                    if (t is not None) and (t != ""):
                        _LOGGER.debug("ATTR_API_RAIN_AMOUNT_MIN %s", t)
                        tmp_dict.update({ATTR_API_RAIN_AMOUNT_MIN : convert_int("".join(t.contents).replace("\n","").replace("\r","").replace("<--","").replace("-->","").replace("mm","").strip())})
                    else:    
                        tmp_dict.update({ATTR_API_RAIN_AMOUNT_MIN : 0})

                    t=soup2.find('div', attrs={'class': HOURLY_FORCAST_WIND})
                    if (t is not None) and (t != ''):
                        tmp_dict.update({"wind_description" : t.find("a").attrs["data-bs-content"].replace("\n","").replace("\r","").strip()})
                        tmp_dict.update({"wind_strenght" : t.find("div").attrs["class"][2].replace("\n","").replace("\r","").strip()})
                        tmp_dict.update({ATTR_API_WIND_DIRECTION : convert_int(t.find("div").attrs["class"][3].replace("\n","").replace("\r","").replace("r","").strip())})

                    t=soup2.find('div', attrs={'class': HOURLY_FORCAST_ICON_CONTAINER})
                    if (t is not None) and (t != ''):
                        tmp_dict.update({ATTR_API_SHORT_TEXT : t.find("a").attrs["data-bs-content"].replace("\n","").replace("\r","").strip()})
                    else:    
                        tmp_dict.update({ATTR_API_SHORT_TEXT : ""})

                    t=soup2.find('img', attrs={'class': HOURLY_FORCAST_ICON})
                    if (t is not None) and (t != ''):
                        icon_d=t.attrs["src"].replace("\n","").replace("\r","").strip()
                        try:
                            tmp_dict.update({ATTR_API_ICON_DESCRIPTOR : icon_d })
                        except:
                            _LOGGER.exception("unsupported icon desciptor: %s", icon_d)                            
                    else:    
                        tmp_dict.update({"icon" : ""})

                    t=soup2.find('div', attrs={'class': HOURLY_FORCAST_ALERT})
                    if (t is not None) and (t != ''):
                        tmp_dict.update({"alert" : t.text.replace("\n","").replace("\r","").strip()})
                    else:    
                        tmp_dict.update({"alert" : ""})

                    hf_data[hour] = tmp_dict

                
                """Collecting daily informations"""
                df_data=dict()
                dfc=soup.find_all('div', attrs={'class': DAILY_FORCAST})
                days = len(dfc)
                
                for day in range(0, days):
                    soup2 = BeautifulSoup(str(dfc[day].contents), features="html.parser")
                    tmp_dict = dict()
                    
                    t=soup2.find('div', attrs={'class': DAILY_FORCAST_DAY})
                    if t is not None:
                        dtt=t.find('a').attrs["title"]
                        dtt=dtt[dtt.index("<br>")+4:]
                        dtv=parseDate(dtt)
                        tmp_dict.update({"date" : dtv})
                    
#                   t=soup2.find('div', attrs={'class': DAILY_FORCAST_RAIN})
#                   if t is not None:
#                       tmp=convert_int(t.text.replace("\n","").replace("\r","").replace("%","").replace(".","1").strip())
#                       tmp_dict.update({ATTR_API_RAIN_CHANCE : tmp})
#                       if day == 0:
#                           loc_data["current"].update({ATTR_API_RAIN_CHANCE: 0})
#                   else:    
#                       tmp_dict.update({ATTR_API_RAIN_CHANCE : 0})
#                       if day == 0:
#                           loc_data["current"].update({ATTR_API_RAIN_CHANCE: 0})
                        
                    t=soup2.find('div', attrs={'class': DAILY_FORCAST_RAIN_LEVEL})
                    if (t is not None) and (t != ''):
                        tmp=convert_int("".join(t.contents).replace("\n","").replace("\r","").replace("<--","").replace("-->","").replace("mm","").strip())
                        tmp_dict.update({ATTR_API_RAIN_AMOUNT_MIN : tmp})
                        if day == 0:
                            loc_data["current"].update({ATTR_API_RAIN_AMOUNT_MIN: tmp})
                    else:    
                        tmp_dict.update({ATTR_API_RAIN_AMOUNT_MIN : 0})
                        if day == 0:
                            loc_data["current"].update({ATTR_API_RAIN_AMOUNT_MIN: 0})

                    t=soup2.find('div', attrs={'class': DAILY_FORCAST_TEMP_MAX})
                    if (t is not None) and (t != ''):
                        tmp=convert_int(t.find("a").text.replace("\n","").replace("\r","").replace("C","").replace("°","").strip())
                        tmp_dict.update({ATTR_API_TEMP_MAX : tmp})
                        if day == 0:
                            loc_data["current"].update({ATTR_API_MAX_TEMP: tmp})
                    else:    
                        tmp_dict.update({ATTR_API_TEMP_MAX : 100})
                        if day == 0:
                            loc_data["current"].update({ATTR_API_MAX_TEMP: 100})

                    t=soup2.find('div', attrs={'class': DAILY_FORCAST_TEMP_MIN})
                    if (t is not None) and (t != ''):
                        tmp=convert_int(t.find("a").text.replace("\n","").replace("\r","").replace("C","").replace("°","").strip())
                        tmp_dict.update({ATTR_API_TEMP_MIN : tmp})
                        if day == 0:
                            loc_data["current"].update({ATTR_API_MIN_TEMP: tmp})
                    else:    
                        tmp_dict.update({ATTR_API_TEMP_MIN : -50})
                        if day == 0:
                            loc_data["current"].update({ATTR_API_MIN_TEMP: -50})

                    t=soup2.find('div', attrs={'class': DAILY_FORCAST_DESCRIPTION})
                    if t is not None:
                        soup3 = BeautifulSoup(str(t.find('a').attrs["data-bs-content"]), features="html.parser")
                        z=soup3.find_all("div",attrs={'class': DAILY_FORCAST_DESCRIPTION_LINE})
                        xx=""
                        for i in range(0,len(z)):
                            xx+=z[i].text
                        tmp_dict.update({ATTR_API_SHORT_TEXT : (xx.strip())})
                        
                        icon_d=soup3.find("div",attrs={'class': DAILY_FORCAST_DESCRIPTION_LINE}).text.strip()
                        try:
                            tmp_dict.update({ATTR_API_ICON_DESCRIPTOR : icon_d})
                            tmp_dict.update({ATTR_API_MDI_ICON : MAP_MDI_ICON[icon_d]})
                        except:
                            _LOGGER.exception("unsupported mdi desciptor: %s", icon_d)                            
                            tmp_dict.update({ATTR_API_MDI_ICON : "mdi:help"})
                    else:    
                        tmp_dict.update({ATTR_API_SHORT_TEXT : ""})
                        tmp_dict.update({ATTR_API_MDI_ICON : "mdi:help"})

                    df_data[day] = tmp_dict

                loc_data["current"].update({ATTR_API_RAIN_CHANCE: rain_chance_max})
                self.locations_data = loc_data
                _LOGGER.debug("%s", self.locations_data)

                self.hourly_forecasts_data = hf_data
                _LOGGER.debug("%s", self.hourly_forecasts_data)

                self.daily_forecasts_data = df_data
                _LOGGER.debug("%s", self.daily_forecasts_data)                
