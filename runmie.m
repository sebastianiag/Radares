clear all
close all
close hidden

i = 1;
for k=0:0.001:2
    sigma = mie(k, 3.16-1i*0.02, 0);
    sigs(i) = sigma;
    i = i + 1;
end

figure
ax1 = subplot(2,1,1)
i=0:0.001:2;
sigs = sigs/max(sigs);
sigdB = 10*(log10(sigs));
plot(ax1, i, sigdB)

l=1;
for m=0:0.001:2
    sigma = mie(m, 80 - 25*1i, 0);
    sigs(l) = sigma;
    l = l + 1;
end


ax2 = subplot(2,1,2)

sigs = sigs/max(sigs);
sigdB = 10*(log10(sigs));
plot(ax2, i, sigdB)
axis([ax1, ax2], [0 2 -Inf 10])