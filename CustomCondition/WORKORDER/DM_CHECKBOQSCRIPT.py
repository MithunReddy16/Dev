#------------------------------------
#created by: ram
#date: 09-Dec-2025
#if all the child workorder belongs to current parent in wpservice avaialbel evaluate to true else false
#-----------------------------------

from psdi.server import MXServer

evalresult = True

parentWO = mbo.getMboSet("PARENT").getMbo(0)

if parentWO is None:
    evalresult = False
else:
    childSet = parentWO.getMboSet("CHILDREN")
    child = childSet.moveFirst()

    if child is None:
        evalresult = False
    else:
        child_list = []
        wp_list = []

        while child:
            cwonum = child.getString("WONUM")
            child_list.append(cwonum)

            wpServiceSet = child.getMboSet("WPSERVICE")
            row = wpServiceSet.moveFirst()

            while row:
                wp_list.append(row.getString("WONUM"))
                row = wpServiceSet.moveNext()

            child = childSet.moveNext()

        for c in child_list:
            if c not in wp_list:
                evalresult = False
                break