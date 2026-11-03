from psdi.iface.mic import StructureData
from psdi.server import MXServer
from psdi.util import MXException
from psdi.mbo import MboRemote,MboSetRemote
from psdi.mbo import SqlFormat

print "Start RIfai SYNC.IOTMETER_ES.EXTEXIT.IN"
erData.breakData();

assetNum= erData.getCurrentDataAsString("ASSETNUM");
print assetNum
localSqlFormat =  SqlFormat(erData.getMboArray().get(0).getUserInfo(), "ASSETNUM = :1");
localSqlFormat.setObject(1, "ASSETLOCUSERCUST", "ASSETNUM", assetNum);
localMboSetRemote = MXServer.getMXServer().getMboSet("ASSET", erData.getMboArray().get(0).getUserInfo());
localMboSetRemote.setWhere(localSqlFormat.format());
count = localMboSetRemote.count()
print count
if count >0:
    owner = localMboSetRemote.moveFirst();

    siteId=owner.getString("SITEID")
    print personid
    
    erData.setCurrentData("SITEID", siteId);
    
    
print "END RIfai"