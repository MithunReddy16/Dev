#-----------------------------------------------------------------------------------------
# Script Name : OSOUT.GRP_PR_OUT
# Description : OS out script for GRP_PR_OUT outbound  interface.
#
# Publish Channel    : GRP_PR_OUT
# Object Structure   : GRP_PR_OUT

# Author             : Mithun Reddy
# Version            : 1.0
# Date               : 18-Apr-2025
#-----------------------------------------------------------------------------------------


print("** OSOUT GRP_PR_OUT started ***")
def skipMbo(ctx):
    if ctx.getMboName()=='PR':
        matuseMbo=ctx.getMbo()
        if matuseMbo.getString("STATUS") not in ['APPR']:
            print("**SKIPING THE TRANSCATION, PR status is not approved.**** ")
            ctx.skipTxn()