def overrideValues(ctx):
    workorderMbo = ctx.getMbo()
    if (workorderMbo is not None and not workorderMbo.getMboSet("DM_ACCIDENT").isEmpty()):
        accidentSet = workorderMbo.getMboSet("DM_ACCIDENT")
        accidentMbo =  accidentSet.moveFirst()
        ctx.overrideCol("DM_ACCIDENTDATE",accidentMbo.getDate("ACCIDENTDATE"))
        ctx.overrideCol("DM_CREATEDATE",accidentMbo.getDate("CREATEDATE"))

            
        ctx.overrideCol("DM_PoliceRPTTYPE",accidentMbo.getString("DM_PoliceRPTTYPE"))
       
       
        ctx.overrideCol("DM_POLICERPTNUM",accidentMbo.getString("DM_POLICERPTNUM"))
        print ("Rifai -----------")
        
        ctx.overrideCol("DM_COUNTFATAL",accidentMbo.getString("DM_COUNTFATAL"))
        ctx.overrideCol("DM_CAUSEBY",accidentMbo.getString("CAUSEBY"))
        areaValue=""
        roadValue=""
       
        if (not accidentMbo.getMboSet("DM_ACCIDENTAREA").isEmpty()):
               areaSet = accidentMbo.getMboSet("DM_ACCIDENTAREA")
               areaMbo =  areaSet.moveFirst()
               areaValue=areaMbo.getString("AREADESC")
               
        if (not accidentMbo.getMboSet("ROAD").isEmpty()):       
               roadSet = accidentMbo.getMboSet("DM_ACCIDENTAREA")
               roadMbo =  roadSet.moveFirst()
               roadValue=roadMbo.getString("AREADESC")
               
        if(len(areaValue) !=0 or  len(roadValue) !=0):
            ctx.overrideCol("DM_AREADESC",areaValue+" "+roadValue)
        else:
            ctx.overrideCol("DM_AREADESC","N/A")
            
            
        if (not workorderMbo.getDate("ACTSTART")):
            ctx.overrideCol("ACTSTART",workorderMbo.getDate("STATUSDATE"))
        if (not workorderMbo.getDate("SCHEDFINISH")):
            ctx.overrideCol("SCHEDFINISH",workorderMbo.getDate("STATUSDATE"))
            
    if (workorderMbo is not None and not workorderMbo.getMboSet("FTS_LASTODO").isEmpty()):
        ctx.overrideCol("DM_STARTODO",workorderMbo.getMboSet("FTS_LASTODO").moveFirst().getInt("LASTREADING"))