#### Code Modified By Mithun to bypass if comodity code is not found in Midroute approval application .

from psdi.server import MXServer
from psdi.util.logging import MXLoggerFactory

myLogger = MXLoggerFactory.getLogger("maximo.custom")

mrnum = mbo.getString("MRNUM")
evalresult = False

MRLineSet = mbo.getMboSet("MRLINE")
line = MRLineSet.moveFirst()

commodity_found = False   # to know if any line had a commodity at all

if line is None:
    myLogger.debug("MR " + mrnum + " has no lines.")
else:
    myLogger.debug("Checking MR " + mrnum + " with " + str(MRLineSet.count()) + " lines.")

while line:
    mrlinenum = line.getInt("MRLINENUM")
    itemnum   = line.getString("ITEMNUM")
    dm_ccappr = line.getBoolean("DM_CCAPPR")
    dm_appr   = line.getBoolean("DM_APPR")
    dm_muappr = line.getBoolean("DM_MUAPPR")

    myLogger.debug("Line " + str(mrlinenum) + " item " + itemnum +" dm_ccappr=" + str(dm_ccappr) + " dm_appr="   + str(dm_appr) + " dm_muappr=" + str(dm_muappr))

    # ******First condition: commodity exists AND dm_ccappr is False ****
    if not dm_ccappr and not dm_appr and itemnum:
        ItemSet = MXServer.getMXServer().getMboSet("ITEM", mbo.getUserInfo())
        ItemSet.setWhere("itemnum = '" + itemnum + "'")
        ItemSet.reset()

        if not ItemSet.isEmpty():
            item = ItemSet.getMbo(0)
            commodity = item.getString("COMMODITY")

            if commodity:
                commodity_found = True
                myLogger.debug("Line " + str(mrlinenum) +" has commodity " + commodity)

                # ************* Second condition: check DM_MRA range  *****
                parts = commodity.split("-")
                if len(parts) > 1:
                    commodity_prefix = parts[0]

                    try:
                        commodity_number = int(parts[1])
                    except:
                        myLogger.debug("Commodity " + commodity + " has non-numeric part, skipping.")
                        line = MRLineSet.moveNext()
                        continue

                    DM_MRA_Set = MXServer.getMXServer().getMboSet("DM_MRA",mbo.getUserInfo())
                    DM_MRA_Set.reset()
                    dm_mra = DM_MRA_Set.moveFirst()
                    match_found = False

                    while dm_mra:
                        from_category = dm_mra.getString("FROMCATEGORY")
                        to_category   = dm_mra.getString("TOCATEGORY")

                        from_parts = from_category.split("-")
                        to_parts   = to_category.split("-")

                        if len(from_parts) > 1 and len(to_parts) > 1:

                            if from_parts[0] == commodity_prefix and to_parts[0]   == commodity_prefix:

                                try:
                                    from_num = int(from_parts[1])
                                    to_num   = int(to_parts[1])
                                except:
                                    dm_mra = DM_MRA_Set.moveNext()
                                    continue

                                if from_num <= commodity_number <= to_num:
                                    match_found = True
                                    break

                        dm_mra = DM_MRA_Set.moveNext()

                    if match_found:
                        myLogger.debug("MR " + mrnum + " line " + str(mrlinenum) + " matched DM_MRA range. Condition TRUE.")
                        evalresult = True
                        break
                    else:
                        myLogger.debug("MR " + mrnum + " line " + str(mrlinenum) + " did NOT match any DM_MRA range.")

    # now it will move to next mr line 
    line = MRLineSet.moveNext()

# if no commodity found in any line overall result False and move to main user condition node 
if not commodity_found:
    myLogger.debug("No commodity found on any line for MR " + mrnum + ". Condition FALSE.")
    evalresult = False