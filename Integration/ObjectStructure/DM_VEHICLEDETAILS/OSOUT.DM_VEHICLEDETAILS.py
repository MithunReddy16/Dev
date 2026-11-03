def overrideValues(ctx):
    assetMbo = ctx.getMbo()
    
    if (assetMbo is not None and not assetMbo.getMboSet("TR_REGISTRATION").isEmpty()):
		licenseSet = assetMbo.getMboSet("TR_REGISTRATION")
		licenseSet.setOrderBy("enddate desc")
		licenseSet.reset()
		licenseMbo = licenseSet.moveFirst()
		ctx.overrideCol("DM_REGDATE",licenseMbo.getDate("STARTDATE"))
		ctx.overrideCol("DM_REGEXPDATE",licenseMbo.getDate("ENDDATE"))
    #else:
	#	ctx.overrideCol("DM_REGDATE","2000-01-12")
	#	ctx.overrideCol("DM_REGEXPDATE","2000-02-12T15:04:55")	    


    if (assetMbo is not None and not assetMbo.getMboSet("TR_SALIK").isEmpty()):
		licenseSet = assetMbo.getMboSet("TR_SALIK")
		licenseSet.setOrderBy ("enddate desc")
		licenseSet.reset()
		licenseMbo = licenseSet.moveFirst()
		ctx.overrideCol("DM_SALIKNUM",licenseMbo.getString("LICENSENUM"))
    else:
        
        ctx.overrideCol("DM_SALIKNUM","N/A")
        
    if (assetMbo is not None and not assetMbo.getMboSet("TR_INSURANCE").isEmpty()):
		licenseSet = assetMbo.getMboSet("TR_INSURANCE")
		licenseSet.setOrderBy ("enddate desc")
		licenseSet.reset()
		licenseMbo = licenseSet.moveFirst()
		ctx.overrideCol("DM_INSPOLICYNUM",licenseMbo.getString("LICENSENUM"))
		ctx.overrideCol("DM_INSDATE",licenseMbo.getDate("STARTDATE"))
		ctx.overrideCol("DM_INSEXPIRYDATE",licenseMbo.getDate("ENDDATE"))
    else:
        ctx.overrideCol("DM_INSPOLICYNUM","N/A")	
    if (assetMbo is not None and not assetMbo.getMboSet("TR_FUEL").isEmpty()):
		licenseSet = assetMbo.getMboSet("TR_FUEL")
		licenseSet.setOrderBy ("enddate desc")
		licenseSet.reset()
		licenseMbo = licenseSet.moveFirst()
		ctx.overrideCol("DM_FUELCARDNUM",licenseMbo.getString("LICENSENUM"))
		ctx.overrideCol("DM_FUELCARDDATE",licenseMbo.getDate("STARTDATE"))
		ctx.overrideCol("DM_FUELEXPDATE",licenseMbo.getDate("ENDDATE"))
    else:
        ctx.overrideCol("DM_FUELCARDNUM","N/A")