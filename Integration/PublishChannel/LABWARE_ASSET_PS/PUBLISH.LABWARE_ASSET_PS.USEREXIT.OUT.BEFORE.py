from psdi.iface.mic import StructureData
from psdi.server import MXServer
from psdi.util import MXException
from psdi.mbo import MboRemote,MboSetRemote
from psdi.mbo import SqlFormat

#------Added by Pramod on 03-jul-2025---------------------------
irData.setCurrentData("personid", "");
irData.setCurrentData("order_number", "");
irData.setCurrentData("locationid", irData.getCurrentDataAsString("LOCATION"));
irData.setCurrentData("ponum", irData.getCurrentDataAsString("DM_PONUMBER"));
irData.setCurrentData("location_description", "");
status=irData.getCurrentDataAsString("STATUS")
irData.setCurrentData("trans","N" );
if status=="SOLD" or status=="DECOMMISSIONED":
   irData.setCurrentData("trans", "D");
   
if irData.getCurrentDataAsString("INSTALLDATE"):
    irData.setCurrentData("INSTALLDATE", irData.getCurrentDataAsString("INSTALLDATE").replace("+04:00", ""));
    irData.setCurrentData("INSTALLDATE", irData.getCurrentDataAsString("INSTALLDATE").replace("T", " "));
if irData.getCurrentDataAsString("WARRANTYEXPDATE"):
    irData.setCurrentData("WARRANTYEXPDATE", irData.getCurrentDataAsString("WARRANTYEXPDATE").replace("T", " "));
#-----------------------------------------------------------------------------
assetNum= irData.getCurrentDataAsString("ASSETNUM");
siteid= irData.getCurrentDataAsString("SITEID");
localSqlFormat =  SqlFormat(irData.getMboArray().get(0).getUserInfo(), "ASSETNUM = :1 and siteid = :2 and isprimary=1");
localSqlFormat.setObject(1, "ASSETLOCUSERCUST", "ASSETNUM", assetNum);
localSqlFormat.setObject(2, "ASSETLOCUSERCUST", "SITEID", siteid);

localMboSetRemote = MXServer.getMXServer().getMboSet("ASSETLOCUSERCUST", irData.getMboArray().get(0).getUserInfo());
localMboSetRemote.setWhere(localSqlFormat.format());
count = localMboSetRemote.count()
print count
if count >0:
    owner = localMboSetRemote.moveFirst();

    personid=owner.getString("personid")
    print personid
    irData.setCurrentData("dm_int_assignto", personid);
    irData.setCurrentData("personid", personid);
locationSet=irData.getCurrentMbo().getMboSet("LOCATION")
if locationSet.count()>0:
    location = locationSet.moveFirst();
    #locationid=location.getString("DM_GRPLOCATIONID")
    location_desc=location.getString("DESCRIPTION")
    irData.setCurrentData("location_description", location_desc);