import pytz
import datetime as dt

TIMEZONE='Europe/Budapest'

def parseDate(dateStr) -> dt.datetime:
    month=['január', 'február', 'március', 'április', 'május', 'június', 'július', 'augusztus', 'szeptember', 'november', 'december' ]
    y=dateStr.lower().split(" ")[0].replace(".","").replace("\n","").replace("\r","").replace(" ","")
    m=month.index(dateStr.lower().split(" ")[1].replace(".","").replace("\n","").replace("\r","").replace(" ","").lower())+1
    d=dateStr.lower().split(" ")[2].replace(".","").replace("\n","").replace("\r","").replace(" ","")
    return dt.datetime(int(y),int(m),int(d),0,0,0, tzinfo=pytz.timezone(TIMEZONE)).astimezone(pytz.UTC)

def parseAstronomicalTime(timeStr) -> dt.datetime:
    tstr=timeStr.split(":");
    ts=dt.datetime.now(pytz.timezone(TIMEZONE))
    ts=ts.replace(hour=int(tstr[0]),minute=int(tstr[1]),second=0,microsecond=0)
    if ts<dt.datetime.now(pytz.timezone(TIMEZONE)):
        ts=ts+dt.timedelta(days=1)
    return ts.astimezone(pytz.UTC);
    
def getNow() -> dt.datetime:
    return dt.datetime.now(pytz.timezone(TIMEZONE)).astimezone(pytz.UTC);

def getToday() -> dt.datetime:
    ts=dt.datetime.now(pytz.timezone(TIMEZONE))
    ts=ts.replace(hour=0,minute=0,second=0,microsecond=0)
    return ts.astimezone(pytz.UTC);
       