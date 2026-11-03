from psdi.server import MXServer
from psdi.util.logging import MXLoggerFactory

myLogger = MXLoggerFactory.getLogger("maximo.custom")
prnum = mbo.getString('PRNUM')

evalresult = False

prlineSet = mbo.getMboSet("prline")
line = prlineSet.moveFirst()

commodity_found = False

while line:
    prlinenum = line.getInt("prlinenum")
    itemnum = line.getString("ITEMNUM")  
    ItemSet = MXServer.getMXServer().getMboSet("ITEM", mbo.getUserInfo())
    ItemSet.setWhere("itemnum = '{}'".format(itemnum))
    
    if not ItemSet.isEmpty():
        item = ItemSet.getMbo(0)
        commodity = item.getString("COMMODITY")
        if commodity:
            commodity_found = True
            dm_ccappr = line.getBoolean("dm_ccappr")
            if not dm_ccappr:
                evalresult = True
                break
    
    line = prlineSet.moveNext()

if not commodity_found:
    evalresult = False

service.log("Evaluation result: {}".format(evalresult))