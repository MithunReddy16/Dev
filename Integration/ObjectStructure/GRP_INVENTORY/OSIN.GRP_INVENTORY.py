# Author Mithun Redddy 
# To set default and business values in inventory mbo


from psdi import server
from psdi.server import MXServer
from psdi import mbo

def beforeProcess(ctx):
    struc = ctx.getData()
    category = struc.getCurrentData("CATEGORY")
    userInfo = MXServer.getMXServer().getSystemUserInfo()
    if (category is not None and category=='STK'):
        ctx.getData().setCurrentData("REORDER",1)
    else:
        category = "NS"