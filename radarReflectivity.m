syms D;

Nt1 = 1;
Dn = 300*10^(-6);

resultA = Nt1*Dn^(6)*10^8;
resultA = double(resultA)
10*log10(resultA)

Nt2 = 1.4*exp(4);
resultB = int((Nt2/Dn)*exp(-D/Dn), D, 0, inf)*10^8;
resultB = double(resultB)
10*log10(resultB)

Nt3 = 3.8*exp(4);
Dn1 = 100*10^(-6);
resultC = int((Nt3/gamma(3))*((D/Dn1)^(2))*(1/Dn1)*exp(-D/Dn1), D, 0, inf)*10^8;
resultC = double(resultC)
10*log10(resultC)