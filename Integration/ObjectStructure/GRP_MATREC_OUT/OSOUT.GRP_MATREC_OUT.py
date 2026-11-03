#-----------------------------------------------------------------------------------------
# Script Name : OSOUT.GRP_MATREC_OUT
# Description : OS out script for GRP_MATREC outbound  interface.
#
# Publish Channel    : GRP_MATREC
# Object Structure   : GRP_MATREC

# Author             : Mithun Reddy
# Version            : 1.0
# Date               : 18-Apr-2025
#-----------------------------------------------------------------------------------------
from psdi.util.logging import MXLoggerFactory
logger = MXLoggerFactory.getLogger("maximo.integration.userexit")
logger.debug("*** Matrectrans OSOUT STARTED***")

def skipMbo(ctx):
    if ctx.getMboName()=='MATRECTRANS':
        matrecMbo=ctx.getMbo()
        logger.debug("***ISSUETYPE IS  ****"+matrecMbo.getString("ISSUETYPE"))
        if matrecMbo.getString("ISSUETYPE") in ['STAGETRANSFER','RECEIPT','VOIDSHIPRECEIPT','RETURN','SHIPCANCEL','VOIDRECEIPT'] :
            logger.debug("***SKIPING THE transcation  ****")
            ctx.skipTxn()
            
        elif matrecMbo.getString("ISSUETYPE")=='SHIPTRANSFER':
            item=matrecMbo.getString("ITEMNUM")
            store=matrecMbo.getString("FROMSTORELOC")
            bin=matrecMbo.getString("FROMBIN")
            invbalSet=matrecMbo.getMboSet("$rel","INVBALANCES","ITEMNUM='"+item+"' and LOCATION='"+store+"' and BINNUM='"+bin+"'")
            if not invbalSet.isEmpty :
                invMbo=invbalSet.moveFirst()
                if invMbo.getBoolean("STAGINGBIN") :
                    print("**SKIPING THE TRANSCATION, ITEM is a STAGING BIN ")
                    ctx.skipTxn()
        
        elif matrecMbo.getString("ISSUETYPE")=='SHIPRECEIPT':
            item=matrecMbo.getString("ITEMNUM")
            store=matrecMbo.getString("TOSTORELOC")
            bin=matrecMbo.getString("TOBIN")
            invbalSet=matrecMbo.getMboSet("$rel","INVBALANCES","ITEMNUM='"+item+"' and LOCATION='"+store+"' and BINNUM='"+bin+"'")
            if not invbalSet.isEmpty :
                invMbo=invbalSet.moveFirst()
                if invMbo.getBoolean("STAGINGBIN") :
                    print("**SKIPING THE TRANSCATION, ITEM is a STAGING BIN ")
                    ctx.skipTxn()
        
        elif matrecMbo.getString("ISSUETYPE")=='TRANSFER':
            logger.debug("***issue type is transfer  ****")
            poSet=matrecMbo.getMboSet("PO")
            logger.debug("***issue type is transfer  ****"+str(poSet.count()))
            poMbo=poSet.moveFirst()
            if poMbo :
                if not poMbo.getBoolean("INTERNAL") :
                    ctx.skipTxn()
                    
            
        """
            item=matrecMbo.getString("ITEMNUM")
            store=matrecMbo.getString("TOSTORELOC")
            bin=matrecMbo.getString("TOBIN")
            invbalSet=matrecMbo.getMboSet("$rel","INVBALANCES","ITEMNUM='"+item+"' and LOCATION='"+store+"' and BINNUM='"+bin+"'")
            if not invbalSet.isEmpty :
                invMbo=invbalSet.moveFirst()
                if invMbo.getBoolean("STAGINGBIN") :
                    print("**SKIPING THE TRANSCATION, ITEM is a STAGING BIN ")
                    ctx.skipTxn()
            """