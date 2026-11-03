def overrideValues(ctx):
    woMbo = ctx.getMbo()
    if (woMbo is not None and not woMbo.getMboSet("FTS_LASTODO").isEmpty()):
        ctx.overrideCol("DM_ODOMETER",woMbo.getMboSet("FTS_LASTODO").moveFirst().getDouble("LASTREADING"))
    else:
        ctx.overrideCol("DM_ODOMETER",0.0)
        
    if (not woMbo.getDate("SCHEDSTART")):
        
        ctx.overrideCol("SCHEDSTART",woMbo.getDate("STATUSDATE"))
    if (not woMbo.getDate("SCHEDFINISH")):
        ctx.overrideCol("SCHEDFINISH",woMbo.getDate("STATUSDATE"))