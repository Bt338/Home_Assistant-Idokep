import pytz
import datetime as dt

TIMEZONE='Europe/Budapest'

def parseDate(dateStr) -> dt.datetime:
    month=['január', 'február', 'március', 'április', 'május', 'június', 'július', 'augusztus', 'szeptember', 'november', 'december' ]
    y=dateStr.split(" ")[0].replace(".","").replace("\n","").replace("\r","").replace(" ","")
    m=month.index(dateStr.split(" ")[1].replace(".","").replace("\n","").replace("\r","").replace(" ","").lower())+1
    d=dateStr.split(" ")[2].replace(".","").replace("\n","").replace("\r","").replace(" ","")
    return dt.datetime(int(y),int(m),int(d),0,0,0, tzinfo=pytz.timezone(TIMEZONE))
