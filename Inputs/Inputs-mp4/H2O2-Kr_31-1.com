%mem=8GB
%nproc=8
%Chk=/home/matheus/.tcc/chk/H2O2-Kr_0.0.chk
#p mp4/aug-cc-PVTz int=ultrafine counterpoise=2 Scan

TCC

0,1 0,1 0,1
O(Fragment=1)   0.0  0.0  0.725
O(Fragment=1)   0.0  0.0  -0.725
H(Fragment=1)   -0.7037808063803964  0.5905422150634392  1.0235104165661992
H(Fragment=1)   0.0  0.9187205947411183  -1.0235104165661992
Kr(Fragment=2)   0.    R1    0.
 Variables:
 R1 3.25 S 10 +0.1

