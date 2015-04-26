%% Plotting TropiNet Data 
% INEL5607 SPRING 2015 
% EXAM#2 

%% Opening file and accesing variables from file

%Open file  - edit the name
File_name='Aguirre.netcdf'; ncid = netcdf.open(File_name,'NC_NOWRITE');%Read NETCDF

%% Retrieve variables and filter 
CR_id=netcdf.inqVarID(ncid,'CorrectedReflectivity'); %Reflectividad Corregida
CorrectedReflectivity=double(netcdf.getVar(ncid,CR_id));

Vel_id=netcdf.inqVarID(ncid,'Velocity'); %velocity
Velocity=double(netcdf.getVar(ncid,Vel_id));

%Filter data for accepted range of values
PHV_id=netcdf.inqVarID(ncid,'CrossPolCorrelation'); %for filtering purposes
RHVX=netcdf.getVar(ncid,PHV_id);
CorrectedReflectivity(CorrectedReflectivity ==-99900) = NaN;
CorrectedReflectivity(CorrectedReflectivity<0) = NaN;
CorrectedReflectivity(RHVX < 0.6) = NaN;
Velocity(isnan(CorrectedReflectivity))=NaN;

%Getting Azimuth, Elevation and Range Gate info

A_id=netcdf.inqVarID(ncid, 'Azimuth'); az_set=netcdf.getVar(ncid,A_id); %Azimutos
Elevation_id=netcdf.inqVarID(ncid,'Elevation');
Elevation=netcdf.getVar(ncid,Elevation_id); elevX=Elevation(2); 

GateWidth_id=netcdf.inqVarID(ncid,'GateWidth');
GateWidth=netcdf.getVar(ncid,GateWidth_id);

RangeToFirstGate=0; drX=GateWidth(1)/1000000;
RngX=(drX*RangeToFirstGate):drX:(40.161-drX);

aziX=az_set;
aziXr = -(aziX-90)*pi/180;
[RngXM,aziXrM]=meshgrid(RngX,aziXr);
X = RngXM.*cos(aziXrM); Y = RngXM.*sin(aziXrM);

%% Reflectivity Plot
% Reflectivity Plot
cr= figure(1); pcolor (X,Y,CorrectedReflectivity');
axis equal tight; shading 'interp'; 
caxis ([0 75]); %Plot Legend of possible values
colorbar('FontSize',12); load('MyColormaps','mycmap');
set(cr,'Colormap',mycmap); set(gca,'FontSize',12);
title('TropiNet Corrected Reflectivity [dBZ]','FontSize',12);
xlabel('Range [km]','FontSize',12); ylabel('Range [km]','FontSize',12);
grid on; h = colorbar; hTitle = get(h,'Title'); set(hTitle,'String','[dBZ]')

%Velocity plot
vv= figure(2); pcolor (X,Y,Velocity');
axis equal tight; shading 'interp'; 
caxis ([0 75]); %Plot Legend of possible values
colorbar('FontSize',12); load('MyColormaps','mycmap');
set(vv,'Colormap',mycmap); set(gca,'FontSize',12);
title('TropiNet Doppler Velocity [m/s]','FontSize',12);
xlabel('Range [km]','FontSize',12); ylabel('Range [km]','FontSize',12);
grid on; h = colorbar; hTitle = get(h,'Title'); set(hTitle,'String','[m/s]')

reflectivity = 10.^(CorrectedReflectivity/.10)

rainfall = (reflectivity/.300)^.(1/1.4)

%Nexrad rainfall rate plot
vv= figure(3); pcolor (X,Y,rainfall');
axis equal tight; shading 'interp'; 
caxis ([0 75]); %Plot Legend of possible values
colorbar('FontSize',12); load('MyColormaps','mycmap');
set(vv,'Colormap',mycmap); set(gca,'FontSize',12);
title('NEXRAD Rainfall Rate [m/s]','FontSize',12);
xlabel('Range [km]','FontSize',12); ylabel('Range [km]','FontSize',12);
grid on; h = colorbar; hTitle = get(h,'Title'); set(hTitle,'String','[m/s]')

rainfall = (reflectivity/.31)^.(1/1.71)

%Puerto Rico rainfall rate
vv= figure(5); pcolor (X,Y,rainfall');
axis equal tight; shading 'interp'; 
caxis ([0 75]); %Plot Legend of possible values
colorbar('FontSize',12); load('MyColormaps','mycmap');
set(vv,'Colormap',mycmap); set(gca,'FontSize',12);
title('NEXRAD Rainfall Rate [m/s]','FontSize',12);
xlabel('Range [km]','FontSize',12); ylabel('Range [km]','FontSize',12);
grid on; h = colorbar; hTitle = get(h,'Title'); set(hTitle,'String','[m/s]')


%% 


