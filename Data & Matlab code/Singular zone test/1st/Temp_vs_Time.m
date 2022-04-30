% Data from Temp 1 
temp_sensor_1 = temp_data_1.Temperature(:);
time_1 = time_sample.time_sec(1:17760,:);
% Data from Temp 2 
temp_sensor_2 = temp_data_2.Temperature(:);
time_2 = time_sample.time_sec(1:17610,:);
% Data from Temp 3 
temp_sensor_3 = temp_data_3.Temperature(:);
time_3 = time_sample.time_sec(1:14974,:);

%%{
figure(1);
plot(time_1, temp_sensor_1);
hold on;
plot(time_2, temp_sensor_2);
hold on;
plot(time_3, temp_sensor_3);
title('Temperature vs Time')
ylabel('Temperature (Celcius)')
xlabel('Time (sec)')
legend('Sensor_1','Sensor_2','Sensor_3')
%}