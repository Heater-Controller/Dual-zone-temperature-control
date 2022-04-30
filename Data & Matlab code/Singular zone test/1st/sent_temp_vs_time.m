% Sent Data from Temp 1 to ESP
sensor_1_sent = sent_data_1.ESP(:);
time_1 = time_sample.time_sec(1:592,:);

% Sent Data from Temp 1 to ESP
sensor_2_sent = sent_data_2.ESP(:);
time_2 = time_sample.time_sec(1:587,:);

% Sent Data from Temp 1 to ESP
sensor_3_sent = sent_data_3.ESP(:);
time_3 = time_sample.time_sec(1:499,:);


%%{
figure(1);
plot(time_1, sensor_1_sent);
hold on;
plot(time_2, sensor_2_sent);
hold on;
plot(time_3, sensor_3_sent);
title('Temperature vs Time')
ylabel('Temperature (Celcius)')
xlabel('Time (sec)')
legend('Sensor_1','Sensor_2','Sensor_3')
%}