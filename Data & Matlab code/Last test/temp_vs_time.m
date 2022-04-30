%%{
% Data from Temp 1 
temp_sensor_1 = temp_data_1.Temperature(:);
time_1 = time_sec.time(1:5071,:);
% Data from Temp 2 
temp_sensor_2 = temp_data_2.Temperature(:);
time_2 = time_sec.time(1:5376,:);
% Data from Temp 6 
temp_sensor_6 = temp_data_6.Temperature(:);
time_6 = time_sec.time(1:7921,:);

temp_sensor_1 = (1.8 * temp_sensor_1) + 32; % convert from C to F
temp_sensor_2 = (1.8 * temp_sensor_2) + 32;
temp_sensor_6 = (1.8 * temp_sensor_6) + 32;
%}

%%{
figure(1);
plot(time_1, temp_sensor_1);
hold on;
plot(time_2, temp_sensor_2);
hold on;
plot(time_6, temp_sensor_6);
title('Temperature vs Time')
ylabel('Temperature ( Fahrenheit )')
xlabel('Time ( sec )')
legend('Sensor 1','Sensor 2','Sensor 6')
%}

%%{
% Sent Data from Temp 1 to ESP
sensor_1_sent = sent_sensor_1.data(:);
time_1 = time_30_sec.time(1:168,:);
% Sent Data from Temp 2 to ESP
sensor_2_sent = sent_sensor_2.data(:);
time_2 = time_30_sec.time(1:177,:);
% Sent Data from Temp 6 to ESP
sensor_6_sent = sent_sensor_6.data(:);
time_6 = time_30_sec.time(1:263,:);

sensor_1_sent = (1.8 * (sensor_1_sent/10000)) + 32;
sensor_2_sent = (1.8 * (sensor_2_sent/10000)) + 32;
sensor_6_sent = (1.8 * (sensor_6_sent/10000)) + 32;

%}

%%{
figure(2);
scatter(time_1, sensor_1_sent);
hold on;
scatter(time_2, sensor_2_sent);
hold on;
scatter(time_6, sensor_6_sent);
title('Data Received by Main ESP (Temperature vs Time)')
ylabel('Temperature ( Fahrenheit )')
xlabel('Time ( sec )')
legend('Sensor 1','Sensor 2','Sensor 6')
%}


