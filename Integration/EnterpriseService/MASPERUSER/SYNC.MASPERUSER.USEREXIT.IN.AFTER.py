from com.ibm.tivoli.maximo.oslc import OslcUtils
from com.ibm.tivoli.maximo.oslc.provider import OslcJSONStructureData
from psdi.mbo import MboConstants
from psdi.util.logging import MXLoggerFactory
from psdi.server import MXServer

logger = MXLoggerFactory.getLogger("maximo.custom")

userInfo= MXServer.getMXServer().getSystemUserInfo()

data = irData.getDataAsBytes()
dataEr = erData.getDataAsBytes()

jo = OslcUtils.bytesToJSONObject(data)
erJo = OslcUtils.bytesToJSONObject(dataEr)

logger.debug('AMIR-MASPER-jo' + str(jo))
logger.debug('AMIR-MASPER-erJo' + str(erJo))

#emailjo = jo.get("email")
#emailAdd = emailjo.get("emailaddress")
emailAdd = jo["email"][0]["emailaddress"]


logger.debug('AMIR-MASPER-EmailAddress:' + str(emailAdd.upper()))

EmailSet = MXServer.getMXServer().getMboSet('EMAIL',userInfo)
EmailSet.setWhere("upper(emailaddress) = '" + emailAdd.upper() + "'")
EmailSet.reset()
EmailRecord = EmailSet.moveFirst()
if EmailRecord:
    logger.debug('AMIR-MASPER-Person Found:' + str(EmailRecord.getString('PERSONID')))
    jo.put("personid",EmailRecord.getString('PERSONID'))
    irData = OslcJSONStructureData(jo,"MASPERUSER","PERSON",userInfo,"Sync",True)
else:
    logger.debug('AMIR-MASPER-Person NOT Found:')
'''

if erJo.get("owner").upper() == 'SCIM':
   extjo = jo.get("extension")
   empno = extjo.get("employeeNumber")
   jo.put("personid",empno)
   irData = OslcJSONStructureData(jo,"MASPERUSER","PERSON",userInfo,"Sync",True)
'''