def verify(l):
    if l[0] < l[1]:
        for i in range(1,len(l),2):
            if i+1 != len(l):
                if l[i] < l[i+1]:
                    return False
    elif l[0] > l[1]:
        for i in range(1,len(l),2):
            if i+1 != len(l):
                if l[i] > l[i+1]:
                    return False
    else:
        return False
    return True

print(verify([10,9,2,8,4,7,5,6,2,4,2]))
