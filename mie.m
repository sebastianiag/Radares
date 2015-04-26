function [sig] = mie(x,refrel,nang)



 mxang=1500;
 nmxx=150000;

 s1=zeros(1,2*mxang-1);     
 s2=zeros(1,2*mxang-1);
 d=zeros(1,nmxx);
 amu=zeros(1,mxang);
 pi=zeros(1,mxang);
 pi0=zeros(1,mxang);
 pi1=zeros(1,mxang);
 tau=zeros(1,mxang);

 if (nang < 2)
   nang = 2;
 end

  pii = 4.*atan(1.);
  dx = x;
  
  drefrl = refrel;
  y = x*drefrl;
  ymod = abs(y);


 xstop = x + 4.*x^0.3333 + 2.;
 nmx = max(xstop,ymod) + 15;
 nmx=fix(nmx);
 

      nstop = xstop;

     

      dang = 0.;
      if (nang > 1)
        dang = .5*pii/ (nang-1);
      end
      for j=1: nang
          theta =  (j-1)*dang;
          amu(j) = cos(theta);
      end
      for j=1: nang
          pi0(j) = 0.;
          pi1(j) = 1.;
      end

      nn = nmx - 1;
      for n=1: nn  
          en = nmx - n + 1;
          d(nmx-n) = (en/y) - (1./ (d(nmx-n+1)+en/y));
      end 

      psi0 = cos(dx);
      psi1 = sin(dx);
      chi0 = -sin(dx);
      chi1 = cos(dx);
      xi1 = psi1-chi1*1i;
      sig =0.;
      gsca = 0.;
      p = -1;
      for n=1: nstop 
          en = n;
          fn = (2.*en+1.)/ (en* (en+1.));

          psi = (2.*en-1.)*psi1/dx - psi0;
          chi = (2.*en-1.)*chi1/dx - chi0;
          xi = psi-chi*1i;

          if (n > 1)
              an1 = an;
              bn1 = bn;
         end 

          an = (d(n)/drefrl+en/dx)*psi - psi1;
          an = an/ ((d(n)/drefrl+en/dx)*xi-xi1);
          bn = (drefrl*d(n)+en/dx)*psi - psi1;
          bn = bn/ ((drefrl*d(n)+en/dx)*xi-xi1);

          sig = sig + (2.*en+1.)* (abs(an)^2+abs(bn)^2);
          gsca = gsca + ((2.*en+1.)/ (en* (en+1.)))* ...
             ( real(an)* real(bn)+imag(an)*imag(bn));

          if (n > 1)
                     gsca = gsca + ((en-1.)* (en+1.)/en)*...
                    ( real(an1)* real(an)+imag(an1)*imag(an)+...
                     real(bn1)* real(bn)+imag(bn1)*imag(bn));

          end

          for j=1: nang 
              
              pi(j) = pi1(j);
              tau(j) = en*amu(j)*pi(j) - (en+1.)*pi0(j);
              s1(j) = s1(j) + fn* (an*pi(j)+bn*tau(j));
              s2(j) = s2(j) + fn* (an*tau(j)+bn*pi(j));
          end

          p = -p;
          for j=1: nang-1   
              jj = 2*nang - j;
              s1(jj) = s1(jj) + fn*p* (an*pi(j)-bn*tau(j));
              s2(jj) = s2(jj) + fn*p* (bn*pi(j)-an*tau(j));
          end
          psi0 = psi1;
          psi1 = psi;
          chi0 = chi1;
          chi1 = chi;
          xi1 = psi1-chi1*1i;

          for j=1: nang 
              pi1(j) = ((2.*en+1.)*amu(j)*pi(j)- (en+1.)*pi0(j))/...
                      en;
              pi0(j) = pi(j);
           end 
      end 

     
      sig = (2./ (dx*dx))*sig;
      
      clear s1 s2
      
      

    
