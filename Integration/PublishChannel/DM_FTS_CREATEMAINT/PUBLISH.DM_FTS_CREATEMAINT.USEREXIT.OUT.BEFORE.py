if (irData.getCurrentDataAsString("WORKTYPE") == 'PM') :
   irData.setCurrentData("WORKTYPE","1")
else:
    irData.setCurrentData("WORKTYPE","2")

if (irData.getCurrentDataAsString("STATUS") == 'APPR') :
    irData.setCurrentData("STATUS","20")
elif (irData.getCurrentDataAsString("STATUS") == 'INPRG') :
    irData.setCurrentData("STATUS","15")
elif (irData.getCurrentDataAsString("STATUS") == 'PENDING') :
    irData.setCurrentData("STATUS","20")
elif (irData.getCurrentDataAsString("STATUS") == 'WAPPR') :
    irData.setCurrentData("STATUS","60")
elif (irData.getCurrentDataAsString("STATUS") == 'WORKCOMP') :
    irData.setCurrentData("STATUS","2")
elif (irData.getCurrentDataAsString("STATUS") == 'SCHD') :
    irData.setCurrentData("STATUS","83")