from psdi.server import MXServer
from psdi.util.logging import MXLoggerFactory

myLogger = MXLoggerFactory.getLogger("maximo.custom")

mrnum = mbo.getString("MRNUM")
mrLineSet = mbo.getMboSet("MRLINE")
line = mrLineSet.moveFirst()
evalresult = False
while line:
	dm_appr   = line.getBoolean("DM_APPR")
	dm_muappr = line.getBoolean("DM_MUAPPR")
	
	# modified by Mithun We only care about lines where mainuser is 0: if (not dm_appr) and (not dm_muappr):
	if not dm_muappr and not dm_appr:
		itemnum   = line.getString("ITEMNUM")
		mrlinenum = line.getInt("MRLINENUM")
		myLogger.debug("Checking line " + str(mrlinenum) +" item " + itemnum + " for MAINUSER.")
		itemSet = MXServer.getMXServer().getMboSet("ITEM", mbo.getUserInfo())
		itemSet.setWhere("itemnum = '" + itemnum + "'")
		itemSet.reset()
		if not itemSet.isEmpty():
			item = itemSet.getMbo(0)
			dm_mainuser = item.getString("DM_MAINUSER")
			if dm_mainuser:
				MainUserSet = MXServer.getMXServer().getMboSet("PERSONGROUPTEAM", MXServer.getMXServer().getSystemUserInfo())
				
				WhereClause = "PERSONGROUP='" +dm_mainuser+"'"
				myLogger.info('Require MRA Where Clasue: {}'.format(WhereClause))
				MainUserSet.setWhere(WhereClause)
				MainUserSet.reset()
				
				MainUserMbo = MainUserSet.moveFirst()
				if MainUserMbo :
					evalresult = True			
				
				MainUserSet.cleanup()
				MainUserSet.close()				
				break

	#  next MR line
	line = mrLineSet.moveNext()
	
'''
from psdi.server import MXServer
from psdi.util.logging import MXLoggerFactory

myLogger = MXLoggerFactory.getLogger("maximo.custom")

evalresult = False

mrnum = mbo.getString("MRNUM")
mrLineSet = mbo.getMboSet("MRLINE")

mrLineSet.setOrderBy("MRLINENUM ASC")
line = mrLineSet.moveFirst()

while line:
    dm_appr   = line.getBoolean("DM_APPR")
    dm_muappr = line.getBoolean("DM_MUAPPR")

    # modified by Mithun We only care about lines where mainuser is 0: if (not dm_appr) and (not dm_muappr):
    if not dm_muappr:
        itemnum   = line.getString("ITEMNUM")
        mrlinenum = line.getInt("MRLINENUM")
        myLogger.debug("Checking line " + str(mrlinenum) +" item " + itemnum + " for MAINUSER.")
        itemSet = MXServer.getMXServer().getMboSet("ITEM", mbo.getUserInfo())
        itemSet.setWhere("itemnum = '" + itemnum + "'")
        itemSet.reset()
        if not itemSet.isEmpty():
            item = itemSet.getMbo(0)
            dm_mainuser = item.getString("DM_MAINUSER")
            if dm_mainuser:
                # MAINUSER is set present
                
                myLogger.debug("Line " + str(mrlinenum) +" has MAINUSER " + str(dm_mainuser) + " - condition TRUE.")
                evalresult = True
                break
            else:
                # MAINUSER not present 
                myLogger.debug("Line " + str(mrlinenum) + " has no MAINUSER – condition FALSE.")
                evalresult = False
                break
        else:
            # Item not found so  treat as FALSE
            myLogger.debug("Item " + itemnum + " not found in ITEM – condition FALSE.")
            evalresult = False
            break

    #  next MR line
    line = mrLineSet.moveNext()
    
'''