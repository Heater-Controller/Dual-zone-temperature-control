%%{
% Data from Temp 1 
temp_sensor_1 = temp_data_1.Temperature(:);
time_1 = time_sec.time(1:2040,:);
% Data from Temp 2 
temp_sensor_2 = temp_data_2.Temperature(:);
time_2 = time_sec.time(1:2040,:);
% Data from Temp 3 
temp_sensor_3 = temp_data_3.Temperature(:);
time_3 = time_sec.time(1:2040,:);
% Data from Temp 4 
temp_sensor_4 = temp_data_4.Temperature(:);
time_4 = time_sec.time(1:3630,:);
% Data from Temp 5 
temp_sensor_5 = temp_data_5.Temperature(:);
time_5 = time_sec.time(1:3690,:);
% Data from Temp 6 
temp_sensor_6 = temp_data_6.Temperature(:);
time_6 = time_sec.time(1:3690,:);

temp_sensor_1 = (1.8 * temp_sensor_1) + 32; % convert from C to F
temp_sensor_2 = (1.8 * temp_sensor_2) + 32;
temp_sensor_3 = (1.8 * temp_sensor_3) + 32;
temp_sensor_4 = (1.8 * temp_sensor_4) + 32;
temp_sensor_5 = (1.8 * temp_sensor_5) + 32;
temp_sensor_6 = (1.8 * temp_sensor_6) + 32;
%}

%{
figure(1);
plot(time_1, temp_sensor_1);
hold on;
plot(time_2, temp_sensor_2);
hold on;
plot(time_3, temp_sensor_3);
hold on;
plot(time_4, temp_sensor_4);
hold on;
plot(time_5, temp_sensor_5);
hold on;
plot(time_6, temp_sensor_6);
title('Temperature vs Time')
ylabel('Temperature ( Fahrenheit )')
xlabel('Time ( sec )')
legend('Sensor 1','Sensor 2','Sensor 3','Sensor 4','Sensor 5','Sensor 6')
%}

%%{
Tss1 = (temp_sensor_1 + temp_sensor_2 + temp_sensor_3)/3;
Tss1_time = time_sec.time(1:2040,:);

sensor_5 = temp_data_5.Temperature(1:3630,:);
sensor_6 = temp_data_6.Temperature(1:3630,:);
sensor_5 = (1.8 * sensor_5) + 32;
sensor_6 = (1.8 * sensor_6) + 32;

Tss2 = (temp_sensor_4 + sensor_5 + sensor_6)/3;
Tss2_time = time_sec.time(1:3630,:);
%}

%%{
figure(2);
plot(Tss1_time, Tss1);
hold on;
plot(Tss2_time, Tss2);
title('Temperature vs Time')
ylabel('Temperature ( Fahrenheit )')
xlabel('Time ( sec )')
legend('Special Spot 1','Special Spot 2')
%}

%%{
% Sent Data from Temp 1 to ESP
sensor_1_sent = sent_sensor_1.data(:);
time_1 = time_30_sec.time(1:67,:);
% Sent Data from Temp 2 to ESP
sensor_2_sent = sent_sensor_2.data(:);
time_2 = time_30_sec.time(1:67,:);
% Sent Data from Temp 3 to ESP
sensor_3_sent = sent_sensor_3.data(:);
time_3 = time_30_sec.time(1:67,:);
% Sent Data from Temp 4 to ESP
sensor_4_sent = sent_sensor_4.data(:);
time_4 = time_30_sec.time(1:120,:);
% Sent Data from Temp 5 to ESP
sensor_5_sent = sent_sensor_5.data(:);
time_5 = time_30_sec.time(1:122,:);
% Sent Data from Temp 6 to ESP
sensor_6_sent = sent_sensor_6.data(:);
time_6 = time_30_sec.time(1:122,:);

sensor_1_sent = (1.8 * (sensor_1_sent/10000)) + 32;
sensor_2_sent = (1.8 * (sensor_2_sent/10000)) + 32;
sensor_3_sent = (1.8 * (sensor_3_sent/10000)) + 32;
sensor_4_sent = (1.8 * (sensor_4_sent/10000)) + 32;
sensor_5_sent = (1.8 * (sensor_5_sent/10000)) + 32;
sensor_6_sent = (1.8 * (sensor_6_sent/10000)) + 32;

%}

%{
figure(3);
scatter(time_1, sensor_1_sent);
hold on;
scatter(time_2, sensor_2_sent);
hold on;
scatter(time_3, sensor_3_sent);
hold on;
scatter(time_4, sensor_4_sent);
hold on;
scatter(time_5, sensor_5_sent);
hold on;
scatter(time_6, sensor_6_sent);
title('Data Received by Main ESP (Temperature vs Time)')
ylabel('Temperature ( Fahrenheit )')
xlabel('Time ( sec )')
legend('Sensor 1','Sensor 2','Sensor 3','Sensor 4','Sensor 5','Sensor 6')
%}

ESP_Tss1 = (sensor_1_sent + sensor_2_sent + sensor_3_sent)/3;
ESP_Tss1_time = time_30_sec.time(54:120,:);

sent5 = sent_sensor_5.data(1:120,:);
sent6 = sent_sensor_6.data(1:120,:);
sent5 = (1.8 * (sent5/10000)) + 32;
sent6 = (1.8 * (sent6/10000)) + 32;

ESP_Tss2 = (sensor_4_sent + sent5 + sent6)/3;
ESP_Tss2_time = time_30_sec.time(1:120,:);

%%{
figure(4);
tiledlayout(3,1)
together = nexttile;
scatter(ESP_Tss1_time, ESP_Tss1);
hold on;
scatter(ESP_Tss2_time, ESP_Tss2);
title('Data Received by Main ESP (Temperature vs Time)')
ylabel('Temperature ( Fahrenheit )')
xlabel('Time ( sec )')
legend('Special Spot 1','Special Spot 2')

special_1 = nexttile;
scatter(ESP_Tss1_time, ESP_Tss1);
title('Special Spot 1 (Temperature vs Time)')
ylabel('Temperature ( Fahrenheit )')
xlabel('Time ( sec )')

special_2 = nexttile;
scatter(ESP_Tss2_time, ESP_Tss2);
title('Special Spot 2 (Temperature vs Time)')
ylabel('Temperature ( Fahrenheit )')
xlabel('Time ( sec )')

%}


