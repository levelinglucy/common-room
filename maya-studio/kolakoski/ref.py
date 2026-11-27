import sys
def direct(a,b,N):
    s=[]; i=0
    while len(s)<N:
        sym = a if i%2==0 else b
        L = s[i] if i < len(s) else sym
        s.extend([sym]*L); i+=1
    return s[:N], i
if __name__=='__main__':
    a,b,N=map(int,sys.argv[1:4])
    s,_=direct(a,b,N); print(''.join(map(str,s)))
