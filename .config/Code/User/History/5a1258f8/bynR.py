def verify(l):
    if l[0] < l[1]:
        for i in range(1,len(l),2):
            if i+1 != len(l):
                if i[i] < l[i+1]:
                    return False
    elif l[0] > l[1]:
        for i in range(1,len(l),2):
            if i+1 != len(l):
                if i[i] > l[i+1]:
                    return False
    else:
        return False
    return True
