from psdi import server
from psdi.server import MXServer
from psdi import mbo

def beforeProcess(ctx):
    struc = ctx.getData()
    orgCode= struc.getCurrentData("DM_GRPORG")
    itemNum = struc.getCurrentData("ITEMNUM")
    userInfo = MXServer.getMXServer().getSystemUserInfo()
    ctx.getData().setCurrentData("ITEMSETID","ITEMSET")
    status = struc.getCurrentData("STATUS")
    uom = struc.getCurrentData("ORDERUNIT")
    #if (uom is not None and uom =='EA'):
        #ctx.getData().setCurrentData("ORDERUNIT","EACH")
    if (status is not None and status =='Active'):
        ctx.getData().setCurrentData("STATUS","ACTIVE")
    else:
        ctx.getData().setCurrentData("STATUS","INACTIVE")
        
    if (orgCode is not None and orgCode=='M00'):
            commodityCode = ctx.getData().getCurrentData("COMMODITY")
            if commodityCode is not None:
    		    cg = commodityCode.split("-")[1]
	            if (cg is not None and cg!='000'):
		            parent = commodityCode.split("-")[0]
		    ctx.getData().setCurrentData("COMMODITYGROUP",parent)
    else:
        ctx.skipTxn();