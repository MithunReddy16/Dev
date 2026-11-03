from psdi.iface.mic import StructureData
from psdi.server import MXServer
from psdi.util import MXException
from psdi.mbo import MboRemote,MboSetRemote
from psdi.mbo import SqlFormat

erData.breakData();
mxServer=MXServer.getMXServer()
userInfo=mxServer.getUserInfo("CNSADMIN")
vinNum= erData.getCurrentDataAsString("DM_INT_VINNUM");
assetSet =  mxServer.getMboSet("ASSET", userInfo);
assetSet.setWhere("DM_VINNUM='"+vinNum+"'");
count = assetSet.count()
print "RifaiCount=";
print count;
if count >0:
    asset = assetSet.moveFirst();
    siteID=asset.getString("SITEID")
    assetnum=asset.getString("ASSETNUM")
    erData.setCurrentData("SITEID", "DM");
    erData.setCurrentData("ASSETNUM", assetnum);