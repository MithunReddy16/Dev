#-----------------------------------------------------------------------------------------
# Script:	SYNC.MATUSETRANS.USEREXIT.OUT.AFTER
# Author:	Mithun Reddy
# Version:   1.0 - 26-Mar-2025
# Purpose:   Sets formatted values during outbound publish from MATUSETRANS
# Channel:   SYNCMATUSETRANS (After External Exit)
#-----------------------------------------------------------------------------------------

from psdi.iface.mic import StructureData
from psdi.server import MXServer
from psdi.util import MXException
from psdi.mbo import MboRemote, MboSetRemote
from psdi.util.logging import MXLoggerFactory
from psdi.mbo import SqlFormat
from java.text import SimpleDateFormat


logger = MXLoggerFactory.getLogger("maximo.integration.userexit")
logger.debug("*** SYNC.MATUSETRANS.USEREXIT.OUT.AFTER: START ***")

erData.breakData()
curMbo = irData.getCurrentMbo()

#-----------------------------------------------------------------------------------------
# Format bin number into required format: XXYY-ZZ-000
#-----------------------------------------------------------------------------------------
def formatBinNumber(bin_num):
	if not bin_num or bin_num=="":
		return None
	parts = bin_num.split("-")
	if len(parts) != 4:
		logger.debug("*** Invalid bin number format: " + str(bin_num))
		return None

	seg1, seg2, seg3, seg4 = parts
	merged_seg = seg1 + seg2
	#formatted_seg4 = seg4.zfill(3)
	#return merged_seg + "-" + seg3 + "-" + formatted_seg4
	return merged_seg + "-" + seg3 + "-" + seg4


#-----------------------------------------------------------------------------------------
# Set basic transaction data
#-----------------------------------------------------------------------------------------
def getGRPUoM(UOM):
	GRPUoM = UOM
	UoMSet = MXServer.getMXServer().getMboSet("MEASUREUNIT", MXServer.getMXServer().getSystemUserInfo())
	where = SqlFormat(UoMSet.getUserInfo(), "MEASUREUNITID = :1")
	where.setObject(1, "MEASUREUNIT", "MEASUREUNITID", UOM)
	
	UoMSet.setWhere(where.format())
	UoMSet.reset()
	
	UoMMbo = UoMSet.moveFirst()
	if UoMMbo and not UoMMbo.isNull('DM_GRPUNITID'):
		GRPUoM = UoMMbo.getString('DM_GRPUNITID')
	UoMSet.cleanup()
	UoMSet.close()
	
	return  GRPUoM
#-----------------------------------------------------------------------------------------
# Set base values from MATUSETRANS
#-----------------------------------------------------------------------------------------
def setBaseData():
	erData.setCurrentData("pSourceCode", "MAXIMO")
	logger.debug("Set pSourceCode = MAXIMO")

	uom = curMbo.getString("ISSUEUNIT")
	logger.debug("*** Unit of Measure: " + str(uom))
	erData.setCurrentData("pUnitOfMeasure", getGRPUoM(uom))
	#erData.setCurrentData("pUnitOfMeasure", uom)

	qty = curMbo.getDouble("QUANTITY")
	if qty is not None:
		erData.setCurrentData("pTransactionQty", str(abs(qty)))
		logger.debug("Set pTransactionQty = " + str(abs(qty)))
	cost = curMbo.getDouble("UNITCOST")
	if cost is not None:
		erData.setCurrentData("pUnitPrice", str(cost))
		logger.debug("Set pUnitPrice = " + str(cost))
		
	ActualDate = curMbo.getDate("ACTUALDATE")
	if ActualDate is not None:
		dateFormat = SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss")
		formattedActualDate = dateFormat.format(ActualDate)
		erData.setCurrentData("pTransactionDate", str(formattedActualDate))
		logger.debug("Set pTransactionDate = " + str(formattedActualDate))


#-----------------------------------------------------------------------------------------
# Set item segment values
#-----------------------------------------------------------------------------------------
def setItemSegments():
	itemNum = irData.getCurrentDataAsString("ITEMNUM")
	if itemNum:
		segments  = itemNum.split("-", 1)
		seg1 = segments[0]
		seg2 = segments[1] if len(segments) > 1 else None		
		erData.setCurrentData("pItemSegment1", seg1)
		if seg2 is not None:
			erData.setCurrentData("pItemSegment2", seg2)
		else:
			erData.setCurrentData("pItemSegment2", "")

	else:
		erData.setCurrentDataNull("pItemSegment1")
		erData.setCurrentDataNull("pItemSegment2")

#-----------------------------------------------------------------------------------------
# Set locator and subinventory based on BIN
#-----------------------------------------------------------------------------------------
def setBinDetails():
	issuetype = irData.getCurrentDataAsString("ISSUETYPE")
	logger.debug("*** Issue Type: " + str(issuetype))

	if issuetype in ("ISSUE", "RETURN"):
		bin = irData.getCurrentDataAsString("BINNUM")
		bin_format = formatBinNumber(bin)

		if bin_format:
			erData.setCurrentData("pLocator", bin_format)

			if bin:
				subinventory = "Shed "+bin[0:1]
				erData.setCurrentData("pSubInventory", subinventory)

#-----------------------------------------------------------------------------------------
# Set store location and lot number
#-----------------------------------------------------------------------------------------
def setStoreAndLot():
	issuetype = irData.getCurrentDataAsString("ISSUETYPE")
	if issuetype in ("ISSUE", "RETURN"):
		#erData.setCurrentData("pOrganizationId", irData.getCurrentDataAsString("STORELOC"))
		erData.setCurrentData("pOrganizationId", str(curMbo.getInt("LOCATIONS.DM_GRPORGID")))
		erData.setCurrentData("pLotNumber", irData.getCurrentDataAsString("LOTNUM"))

#-----------------------------------------------------------------------------------------
# Set GL Debit Account Segments (Explicitly without loop)
#-----------------------------------------------------------------------------------------
def setGLSegments():
	if curMbo.getString("ISSUETYPE") in ("RETURN"):
		gldebit = curMbo.getString("GLCREDITACCT")
	else:
		gldebit = curMbo.getString("GLDEBITACCT")
	logger.debug("*** GL Debit Account: " + str(gldebit))

	if gldebit and gldebit != '':
		segments = gldebit.split("-")
		seg_count = len(segments)

		if seg_count == 8:
			seg1, seg2, seg3, seg4, seg5, seg6, seg7, seg8 = segments
			erData.setCurrentData("psegment1", seg1)
			erData.setCurrentData("psegment2", seg2)
			erData.setCurrentData("psegment3", seg3)
			erData.setCurrentData("psegment4", seg4)
			erData.setCurrentData("psegment5", seg5)
			erData.setCurrentData("psegment6", seg6)
			erData.setCurrentData("psegment7", seg7)
			erData.setCurrentData("psegment8", seg8)

		elif seg_count == 4:
			seg1, seg2, seg3, seg4 = segments
			erData.setCurrentData("psegment1", seg1)
			erData.setCurrentData("psegment2", seg2)
			erData.setCurrentData("psegment3", seg3)
			erData.setCurrentData("psegment4", seg4)
			erData.setCurrentDataNull("psegment5")
			erData.setCurrentDataNull("psegment6")
			erData.setCurrentDataNull("psegment7")
			erData.setCurrentDataNull("psegment8")
	else:
		erData.setCurrentDataNull("psegment1")
		erData.setCurrentDataNull("psegment2")
		erData.setCurrentDataNull("psegment3")
		erData.setCurrentDataNull("psegment4")
		erData.setCurrentDataNull("psegment5")
		erData.setCurrentDataNull("psegment6")
		erData.setCurrentDataNull("psegment7")
		erData.setCurrentDataNull("psegment8")

#-----------------------------------------------------------------------------------------
# Set transaction reference
#-----------------------------------------------------------------------------------------
def setTransactionRef():
	transRef = irData.getCurrentDataAsString("MATUSETRANSID")
	if transRef:
		erData.setCurrentData("pTransRef", "MATUSETRANS-" +transRef)
	else:
		erData.setCurrentDataNull("pTransRef")

#-----------------------------------------------------------------------------------------
# Set transaction Type
#-----------------------------------------------------------------------------------------
def setTransactionType():

	issuetype = irData.getCurrentDataAsString("ISSUETYPE")
	if issuetype == "ISSUE":
		erData.setCurrentData("pTransactionType", "Miscellaneous issue")
	elif issuetype == "RETURN":
		erData.setCurrentData("pTransactionType", "Miscellaneous receipt")

#-----------------------------------------------------------------------------------------
# Execute all steps
#-----------------------------------------------------------------------------------------
setBaseData()
setItemSegments()
setBinDetails()
setStoreAndLot()
setGLSegments()
setTransactionRef()
setTransactionType()
logger.debug("*** SYNC.MATUSETRANS.USEREXIT.OUT.AFTER: END ***")