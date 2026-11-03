#-----------------------------------------------------------------------------------------
# Script Name : OSOUT.GRP_INVTRANS_OUT
# Description : OS out script for GRP_INVTRANS outbound  interface.
#
# Publish Channel    : GRP_INVTRANS
# Object Structure   : GRP_INVTRANS

# Author             : Mithun Reddy
# Version            : 1.0
# Date               : 18-Apr-2025
#-----------------------------------------------------------------------------------------


print("** OSOUT GRP_INVTRANS started ***")
def skipMbo(ctx):
    if ctx.getMboName()=='INVTRANS':
        matuseMbo=ctx.getMbo()
        if matuseMbo.getString("TRANSTYPE") not in ['RECBALADJ','CURBALADJ']:
            print("** skiping the TRANSCATION TYPE IS not in RECBALADJ,CURBALADJ ***")
            ctx.skipTxn()
        else :
            if matuseMbo.getString("TRANSTYPE") in ['RECBALADJ','CURBALADJ']:
                if matuseMbo.getInt("QUANTITY")==0 :
                    print("** skiping the TRANS TYPE IS RECBALADJ,CURBALADJ and quantity=0 ***")
                    ctx.skipTxn()
                    
                    
        if matuseMbo.getString("STORELOC").startswith("VS") :
            ctx.skipTxn()