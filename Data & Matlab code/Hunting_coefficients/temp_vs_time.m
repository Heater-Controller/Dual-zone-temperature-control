%%% Sensor 1
y_sensor_1_data = temp_sensor_1_data_march27.Temperature_Sensor_1(2:end,:);
x_sensor_1_data = temp_sensor_1_data_march27.Second_Sensor_1(2:end,:);
for row = 1: size(temp_sensor_1_data_march27.Second_Sensor_1(2:end,:))
    x_sensor_1_data(row) = row;
end
%%%

%%% Sensor 2
y_sensor_2_data = temp_sensor_2_data_march27.Temperature_Sensor_2(2:end,:);
x_sensor_2_data = temp_sensor_2_data_march27.Second_Sensor_2(2:end,:);
for row = 1: size(temp_sensor_2_data_march27.Second_Sensor_2(2:end,:))
    x_sensor_2_data(row) = row;
end
%%%

%%% Sensor 3
y_sensor_3_data = temp_sensor_3_data_march27.Temperature_Sensor_3(2:end,:);
x_sensor_3_data = temp_sensor_3_data_march27.Second_Sensor_3(2:end,:);
for row = 1: size(temp_sensor_3_data_march27.Second_Sensor_3(2:end,:))
    x_sensor_3_data(row) = row;
end
%%%


figure(1);
plot(x_sensor_1_data, y_sensor_1_data)
hold on;
plot(x_sensor_2_data, y_sensor_2_data)
hold on;
plot(x_sensor_3_data, y_sensor_3_data)
title('Temperature vs Time')
ylabel('Temp (Celcius)')
xlabel('Time (sec)')
legend('Sensor 1','Sensor 2','Sensor 3');