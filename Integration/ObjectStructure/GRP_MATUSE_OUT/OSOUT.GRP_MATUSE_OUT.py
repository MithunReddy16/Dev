#-----------------------------------------------------------------------------------------
# Script Name : OSOUT.GRP_MATUSE_OUT
# Description : OS out script for GRP_MATUSE outbound  interface.
#
# Publish Channel    : GRP_MATUSE
# Object Structure   : GRP_MATUSE

# Author             : Mithun Reddy
# Version            : 1.0
# Date               : 18-Apr-2025
#-----------------------------------------------------------------------------------------




print("** OSOUT GRP_MATUSETRANS started ***")
def skipMbo(ctx):
    if ctx.getMboName()=='MATUSETRANS':
        matuseMbo=ctx.getMbo()
        if matuseMbo.getString("ISSUETYPE") in ['ISSUE','RETURN']:
            if matuseMbo.isNull("ITEMNUM"):
                ctx.skipTxn()
            item=matuseMbo.getString("ITEMNUM")
            store=matuseMbo.getString("STORELOC")
            bin=matuseMbo.getString("BINNUM")
            invbalSet=matuseMbo.getMboSet("$rel","INVBALANCES","ITEMNUM='"+item+"' and LOCATION='"+store+"' and BINNUM='"+bin+"'")
            if not invbalSet.isEmpty :
                invMbo=invbalSet.moveFirst()
                if invMbo.getBoolean("STAGINGBIN") :
                    print("**SKIPING THE TRANSCATION, ITEM is a STAGING BIN ")
                    ctx.skipTxn()
        if matuseMbo.getString("STORELOC").startswith("VS") :
            ctx.skipTxn()