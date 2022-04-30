% Sent Data from Temp 1 to ESP
sensor_1_sent = sent_data_1.ESP(:);
time_1 = time_sample.time_sec(1:102,:);

% Sent Data from Temp 1 to ESP
sensor_2_sent = sent_data_2.ESP(:);
time_2 = time_sample.time_sec(1:102,:);

% Sent Data from Temp 1 to ESP
sensor_3_sent = sent_data_3.ESP(595:693,:);
time_3 = time_sample.time_sec(1:99,:);


%%{
figure(1);
plot(time_1, sensor_1_sent);
hold on;
plot(time_2, sensor_2_sent);
hold on;
plot(time_3, sensor_3_sent);
title('Temperature vs Time')
ylabel('Temperature (Celcius)')
xlabel('Time (30 sec)')
legend('Sensor 1','Sensor 2','Sensor 3')
%}