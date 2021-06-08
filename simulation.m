%% Parameters
kT = 1;
unitTime = 0.669e-3;
sigma = 1;
gamma = 4130;

Diffusivity = kT/gamma;
ActiveVelocity = 15*(1/(sigma/unitTime));
SedimentationVelocity = -1*ActiveVelocity/4;

%ActiveVelocity = 0; %Test to see if the sendimentation profile without active velocity follows boltzmann distribution
%Diffusivity = 5;
%SedimentationVelocity = -1;

NumberOfParticles = 1000;
TotalTimesteps = 5000; %probably don't need 100000 steps
%% parameters 2
NumberOfParticles = 1000;
Diffusivity = 2;
ActiveVelocity = 10;
SedimentationVelocity = -3;
TotalTimesteps=4000;
%% Simulate the thing
E= Ensemble(NumberOfParticles,Diffusivity,ActiveVelocity,[0,SedimentationVelocity]);
E.timeE(TotalTimesteps)
%% Plot Trajectories
figure(1)
hold on
for i = 1:E.N
    plot(E.ens{i}.traj(:,1),E.ens{i}.traj(:,2))
end
%% Plot MSD
figure(2)
j=1;
msd=zeros(1,400);
for i = 1:10:4000
    msd(j) = E.MSD(i);
    j=j+1;
end
deltaT = 1:10:4000;
%deltaT = 0:10;
plot(deltaT, msd,'.')
xlabel('\Delta t')
ylabel('<\Delta r^2>')
title('MSD')
%% Get Sedimentation Profile
figure(3)
steadyTime = 2000;
reorientationTime = 10;
profile = E.sedP(steadyTime,reorientationTime);
xlabel('z')
ylabel('Count')
%%
Dr = 0.15;
sedProfileValues = profile.Values;
sedProfileBins = profile.BinEdges(2:end)-E.ens{1}.ymin;
GinotLambda = (100/(2*0.3*3))*(1-(7/4)*((3/10)^2));
%% a
figure(4)
hold on
plot(sedProfileBins, sedProfileValues,'o')

xfit = linspace(0,3000,1000);
yfit = 1e4*exp(-xfit/GinotLambda);
plot(xfit,yfit)

set(gca, 'YScale','log')
%% Orientation?
figure(5)
steadyTime = 1000;
reorientationTime = 10;
oP = E.oriP(steadyTime,reorientationTime);