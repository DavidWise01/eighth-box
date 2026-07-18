import numpy as np
print("=== SIDE A: THE LEDGER (is 8 in the books?) ===")
rail={5:1.0,4:0.8,3:0.6,2:0.4,1:0.2,0:0.0}
seam_toll=round(rail[3]-rail[2],10)
print(f"A1 rail forensics: toll paid at the seam = {seam_toll}  (one fold = 0.2, hidden traversal would charge 0.4)")
print(f"   -> {'ONE fold charged: box 8 was never tolled. EMPTY in the ledger.' if seam_toll==0.2 else 'ANOMALY'}")
pair=lambda n:2*2**n; single=lambda n:2**n
print(f"A2 currency collision: pair-ledger at n=2 -> {pair(2)}, single-ledger at n=3 -> {single(3)}")
print(f"   identity pair(n)==single(n+1) for n=0..5: {all(pair(n)==single(n+1) for n in range(6))}")
print("   -> 8 is claimed by BOTH ledgers and written by NEITHER: doubly-defined, unassignable.")

print("\n=== SIDE B: THE WAVEFUNCTION (does amplitude live in 8?) ===")
# 3-level ladder |16>,|8>,|4>: H=[[0,g,0],[g,D,g],[0,g,0]], g=1, middle detuned D.
# superexchange: effective 16<->4 coupling J=g^2/D; transfer at t=pi/(2J); P8 ~ 1/D^2.
def run(D,steps_per=400):
    H=np.array([[0,1,0],[1,D,1],[0,1,0]],dtype=complex)
    J=1.0/D; T=np.pi/(2*J); n=int(T*steps_per); dt=T/n
    c=np.array([1,0,0],dtype=complex); p8max=0
    f=lambda c:-1j*(H@c)
    for _ in range(n):
        k1=f(c);k2=f(c+dt/2*k1);k3=f(c+dt/2*k2);k4=f(c+dt*k3)
        c=c+dt/6*(k1+2*k2+2*k3+k4)
        p8max=max(p8max,abs(c[1])**2)
    return abs(c[2])**2,p8max
print("   D/g   transfer P(4)   max P(8)     D^2*maxP8")
Ds=[5,10,20,40]; ps=[]
for D in Ds:
    p4,p8=run(D); ps.append(p8)
    print(f"   {D:3d}   {p4:.4f}         {p8:.6f}     {D*D*p8:.3f}")
slope=np.polyfit(np.log(Ds),np.log(ps),1)[0]
print(f"   log-log slope of maxP8 vs D: {slope:.3f}  (theory: -2)")
print("   -> transport 16->4 SUCCEEDS while population of 8 vanishes as 1/D^2:")
print("      OCCUPIED in amplitude (the path runs through it), EMPTY in population.")
print("BAKED:", {"Ds":Ds,"p8":[round(p,6) for p in ps],"slope":round(float(slope),3)})
