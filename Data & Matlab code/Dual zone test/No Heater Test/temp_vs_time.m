% Data from Temp 1 
temp_sensor_1 = temp_data_1.Temperature(:);
time_1 = time_sec.time(1:6391,:);
% Data from Temp 2 
temp_sensor_2 = temp_data_2.Temperature(:);
time_2 = time_sec.time(1:6390,:);
% Data from Temp 3 
temp_sensor_3 = temp_data_3.Temperature(:);
time_3 = time_sec.time(1:6390,:);

temp_sensor_1 = (1.8 * temp_sensor_1) + 32;
temp_sensor_2 = (1.8 * temp_sensor_2) + 32;
temp_sensor_3 = (1.8 * temp_sensor_3) + 32;

%%{
figure(1);
plot(time_1, temp_sensor_1);
hold on;
plot(time_2, temp_sensor_2);
hold on;
plot(time_3, temp_sensor_3);
title('Temperature vs Time')
ylabel('Temperature ( Fahrenheit )')
xlabel('Time ( sec )')
legend('Sensor 1','Sensor 2','Sensor 3')
%}

sensor_1 = temp_data_1.Temperature(1:6390,:);
Tss1 = (sensor_1 + temp_sensor_2 + temp_sensor_3)/3;
Tss1_time = time_sec.time(1:6390,:);

%%{
figure(2);
plot(Tss1_time, Tss1);
title('Temperature vs Time')
ylabel('Temperature ( Fahrenheit )')
xlabel('Time ( sec )')
legend('Special Spot 1')
%}

%%{
% Sent Data from Temp 1 to ESP
sensor_1_sent = sent_sensor_1.data(:);
time_1 = time_30_sec.time(1:212,:);

% Sent Data from Temp 1 to ESP
sensor_2_sent = sent_sensor_2.data(:);
time_2 = time_30_sec.time(1:212,:);

% Sent Data from Temp 1 to ESP
sensor_3_sent = sent_sensor_3.data(:);
time_3 = time_30_sec.time(1:212,:);

sensor_1_sent = (1.8 * (sensor_1_sent/10000)) + 32;
sensor_2_sent = (1.8 * (sensor_2_sent/10000)) + 32;
sensor_3_sent = (1.8 * (sensor_3_sent/10000)) + 32;

%}

%%{
figure(3);
scatter(time_1, sensor_1_sent);
hold on;
scatter(time_2, sensor_2_sent);
hold on;
scatter(time_3, sensor_3_sent);
title('Data Received by Main ESP (Temperature vs Time)')
ylabel('Temperature ( Fahrenheit )')
xlabel('Time ( sec )')
legend('Sensor 1','Sensor 2','Sensor 3')
%}

ESP_Tss1 = (sensor_1_sent + sensor_2_sent + sensor_3_sent)/3;
ESP_Tss1_time = time_30_sec.time(1:212,:);

%%{
figure(4);
scatter(ESP_Tss1_time, ESP_Tss1);
title('Data Received by Main ESP (Temperature vs Time)')
ylabel('Temperature ( Fahrenheit )')
xlabel('Time ( sec )')
legend('Special Spot 1')
%}

%{
figure(5);
plot(time_1, sensor_1_sent);
hold on;
plot(time_2, sensor_2_sent);
hold on;
plot(time_3, sensor_3_sent);
title('Data Received by Main ESP (Temperature vs Time)')
ylabel('Temperature ( Fahrenheit )')
xlabel('Time ( sec )')
legend('Sensor 1','Sensor 2','Sensor 3')
%}