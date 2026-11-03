def overrideValues(ctx):
    woMbo = ctx.getMbo()
    ctx.overrideCol("DM_TOTMAINCOST",woMbo.getString("ACTTOTALCOST"))
    if (woMbo is not None and not woMbo.getMboSet("FTS_LASTODO").isEmpty()):
        ctx.overrideCol("DM_ENDODO",woMbo.getMboSet("FTS_LASTODO").moveFirst().getDouble("LASTREADING"))