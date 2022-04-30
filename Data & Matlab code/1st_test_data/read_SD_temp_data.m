%%% Sensor 1
y_sensor_1_data = temp_sensor_1_data_march21.Temperature_Sensor_1(:);
x_sensor_1_data = temp_sensor_1_data_march21.Second_Sensor_1(:);
for row = 1: size(temp_sensor_1_data_march21.Second_Sensor_1(:))
    x_sensor_1_data(row) = row;
end
%%%

%%% Sensor 2
y_sensor_2_data = temp_sensor_2_data_march21.Temperature_Sensor_2(:);
x_sensor_2_data = temp_sensor_2_data_march21.Second_Sensor_2(:);
for row = 1: size(temp_sensor_2_data_march21.Second_Sensor_2(:))
    x_sensor_2_data(row) = row;
end
%%%

figure(1);
plot(x_sensor_1_data, y_sensor_1_data)
hold on;
plot(x_sensor_2_data, y_sensor_2_data)
title('Temperature vs Time')
ylabel('Temp (Celcius)')
xlabel('Time (sec)')