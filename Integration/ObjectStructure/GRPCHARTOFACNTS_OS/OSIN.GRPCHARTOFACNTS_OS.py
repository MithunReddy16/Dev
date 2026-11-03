from psdi import server 
from psdi.server import MXServer 
from psdi import mbo 
def beforeProcess(ctx):
	glComp01=ctx.getData().getCurrentDataAsString("GLCOMP01") ;
	glComp01Desc=ctx.getData().getCurrentDataAsString("SEGMENT1_DESC_NP");
	glComp02=ctx.getData().getCurrentDataAsString("GLCOMP02") ;
	glComp02Desc=ctx.getData().getCurrentDataAsString("SEGMENT2_DESC_NP");
	glComp03=ctx.getData().getCurrentDataAsString("GLCOMP03") ;
	glComp03Desc=ctx.getData().getCurrentDataAsString("SEGMENT3_DESC_NP");
	glComp04=ctx.getData().getCurrentDataAsString("GLCOMP04") ;
	glComp04Desc=ctx.getData().getCurrentDataAsString("SEGMENT4_DESC_NP");
	glComp05=ctx.getData().getCurrentDataAsString("GLCOMP05") ;
	glComp05Desc=ctx.getData().getCurrentDataAsString("SEGMEN5_DESC_NP");
	glComp06=ctx.getData().getCurrentDataAsString("GLCOMP06") ;
	glComp06Desc=ctx.getData().getCurrentDataAsString("SEGMENT6_DESC_NP");
	glComp07=ctx.getData().getCurrentDataAsString("GLCOMP07") ;
	glComp07Desc=ctx.getData().getCurrentDataAsString("SEGMENT7_DESC_NP");
	glComp08=ctx.getData().getCurrentDataAsString("GLCOMP08") ;
	glComp08Desc=ctx.getData().getCurrentDataAsString("SEGMENT8_DESC_NP");
	mxServer = MXServer.getMXServer()
	if (glComp01 is not None and glComp01!=""):
		mboSet = mxServer.getMboSet("GLCOMPONENTS", mxServer.getSystemUserInfo());
		mboSet.setWhere("glorder='0' and orgid='DMORG' and compvalue='"+glComp01+"'");
		mboSet.reset();
		if (mboSet.isEmpty()):
			glCompMbo = mboSet.add();
			glCompMbo.setValue("COMPVALUE", glComp01, 11L);
			glCompMbo.setValue("COMPTEXT", glComp01Desc, 2L);
			glCompMbo.setValue("GLORDER", '0', 2L);
			glCompMbo.setValue("ORGID", "DMORG", 2L);
			glCompMbo.setValue("active",'1',2L);
			mboSet.save();
	if (glComp02 is not None and glComp02!=""):
		mboSet = mxServer.getMboSet("GLCOMPONENTS", mxServer.getSystemUserInfo());
		mboSet.setWhere("glorder='1' and orgid='DMORG' and compvalue='"+glComp02+"'");
		mboSet.reset();
		if (mboSet.isEmpty()):
			glCompMbo = mboSet.add();
			glCompMbo.setValue("COMPVALUE", glComp02, 11L);
			glCompMbo.setValue("COMPTEXT", glComp02Desc, 2L);
			glCompMbo.setValue("GLORDER", '1', 2L);
			glCompMbo.setValue("ORGID", "DMORG", 2L);
			glCompMbo.setValue("active",'1',2L);
			mboSet.save();
	if (glComp03 is not None and glComp03!=""):
		mboSet = mxServer.getMboSet("GLCOMPONENTS", mxServer.getSystemUserInfo());
		mboSet.setWhere("glorder='2' and orgid='DMORG' and compvalue='"+glComp03+"'");
		mboSet.reset();
		if (mboSet.isEmpty()):
			glCompMbo = mboSet.add();
			glCompMbo.setValue("GLORDER", '2', 2L);
			glCompMbo.setValue("COMPVALUE", glComp03, 11L);
			glCompMbo.setValue("COMPTEXT", glComp03Desc, 2L);
			glCompMbo.setValue("ORGID", "DMORG", 2L);
			glCompMbo.setValue("active",'1',2L);
			mboSet.save();
	if (glComp04 is not None and glComp04!=""):
		mboSet = mxServer.getMboSet("GLCOMPONENTS", mxServer.getSystemUserInfo());
		mboSet.setWhere("glorder='3' and orgid='DMORG' and compvalue='"+glComp04+"'");
		mboSet.reset();
		if (mboSet.isEmpty()):
			glCompMbo = mboSet.add();
			glCompMbo.setValue("GLORDER", '3', 2L);
			glCompMbo.setValue("COMPVALUE", glComp04, 11L);
			glCompMbo.setValue("COMPTEXT", glComp04Desc, 2L);
			glCompMbo.setValue("ORGID", "DMORG", 2L);
			glCompMbo.setValue("active",'1',2L);
			mboSet.save();
	if (glComp05 is not None and glComp05!=""):
		mboSet = mxServer.getMboSet("GLCOMPONENTS", mxServer.getSystemUserInfo());
		mboSet.setWhere("glorder='4' and orgid='DMORG' and compvalue='"+glComp05+"'");
		mboSet.reset();
		if (mboSet.isEmpty()):
			glCompMbo = mboSet.add();
			glCompMbo.setValue("GLORDER", '4', 2L);
			glCompMbo.setValue("COMPVALUE", glComp05, 11L);
			glCompMbo.setValue("COMPTEXT", glComp05Desc, 2L);
			glCompMbo.setValue("ORGID", "DMORG", 2L);
			glCompMbo.setValue("active",'1',2L);
			mboSet.save();
	if (glComp06 is not None and glComp06!=""):
		mboSet = mxServer.getMboSet("GLCOMPONENTS", mxServer.getSystemUserInfo());
		mboSet.setWhere("glorder='5' and orgid='DMORG' and compvalue='"+glComp06+"'");
		mboSet.reset();
		if (mboSet.isEmpty()):
			glCompMbo = mboSet.add();
			glCompMbo.setValue("GLORDER", '5', 2L);
			glCompMbo.setValue("COMPVALUE", glComp06, 11L);
			glCompMbo.setValue("COMPTEXT", glComp06Desc, 2L);
			glCompMbo.setValue("ORGID", "DMORG", 2L);
			glCompMbo.setValue("active",'1',2L);
			mboSet.save();
	if (glComp07 is not None and glComp07!=""):
		mboSet = mxServer.getMboSet("GLCOMPONENTS", mxServer.getSystemUserInfo());
		mboSet.setWhere("glorder='6' and orgid='DMORG' and compvalue='"+glComp07+"'");
		mboSet.reset();
		if (mboSet.isEmpty()):
			glCompMbo = mboSet.add();
			glCompMbo.setValue("GLORDER", '6', 2L);
			glCompMbo.setValue("COMPVALUE", glComp07, 11L);
			glCompMbo.setValue("COMPTEXT", glComp07Desc, 2L);
			glCompMbo.setValue("ORGID", "DMORG", 2L);
			glCompMbo.setValue("active",'1',2L);
			mboSet.save();
	if (glComp08 is not None and glComp08!=""):
		mboSet = mxServer.getMboSet("GLCOMPONENTS", mxServer.getSystemUserInfo());
		mboSet.setWhere("glorder='7' and orgid='DMORG' and compvalue='"+glComp08+"'");
		mboSet.reset();
		if (mboSet.isEmpty()):
			glCompMbo = mboSet.add();
			glCompMbo.setValue("GLORDER", '7', 2L);
			glCompMbo.setValue("COMPVALUE", glComp08, 11L);
			glCompMbo.setValue("COMPTEXT", glComp08Desc, 2L);
			glCompMbo.setValue("ORGID", "DMORG", 2L);
			glCompMbo.setValue("active",'1',2L);
			mboSet.save();