from java.text import SimpleDateFormat
from java.util import Calendar
erData.breakData();
convertionDate = erData.getCurrentDataAsDate("ACTIVEDATE")
if (convertionDate is not None):
    cal = Calendar.getInstance()
    cal.setTime(convertionDate)
    cal.set(Calendar.HOUR_OF_DAY, 23)
    cal.set(Calendar.MINUTE, 59)
    cal.set(Calendar.SECOND, 59)
    erData.setCurrentData("EXPIREDATE",cal.getTime())
    cal.setTime(convertionDate)
    cal.set(Calendar.HOUR_OF_DAY, 00)
    cal.set(Calendar.MINUTE, 00)
    cal.set(Calendar.SECOND, 00)
    erData.setCurrentData("ACTIVEDATE",cal.getTime())