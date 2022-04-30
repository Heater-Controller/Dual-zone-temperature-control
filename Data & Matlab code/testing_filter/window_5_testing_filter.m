
%%% Sensor 1
data_start_1 = 825;
data_end_1 = 1134;
y_sensor_1_data = temp_sensor_1_data_march27.Temperature_Sensor_1(data_start_1:data_end_1,:);
x_sensor_1_data = temp_sensor_1_data_march27.Second_Sensor_1(data_start_1:data_end_1,:);
for row = 1: size(temp_sensor_1_data_march27.Second_Sensor_1(data_start_1:data_end_1,:))
    x_sensor_1_data(row) = row;
end
%%%

%%%
filtered_data = output_data_for_test.output(:);
%%%

%%{ 
figure(1);
plot(x_sensor_1_data, y_sensor_1_data)
title('Temperature vs Time')
ylabel('Temp (Celcius)')
xlabel('Time (sec)')
hold on;

window = 60;
method = 'lowess'; % 'movmedian'
plot(x_sensor_1_data, smoothdata(y_sensor_1_data,method,window))
title('Temperature vs Time')
ylabel('Temp (Celcius)')
xlabel('Time (sec)')
hold on;

plot(x_sensor_1_data(1:310,:), filtered_data)
title('Temperature vs Time')
ylabel('Temp (Celcius)')
xlabel('Time (sec)')

legend('Raw', 'Matlab Filter', 'My filter');
%}

%%{ 
figure(2);
tiledlayout(3,1);
nexttile;

plot(x_sensor_1_data, y_sensor_1_data)
title('Raw')
ylabel('Temp (Celcius)')
xlabel('Time (sec)')
hold on;
nexttile;

window = 60;
method = 'lowess'; % 'movmedian'
plot(x_sensor_1_data, smoothdata(y_sensor_1_data,method,window))
title('Matlab Filter')
ylabel('Temp (Celcius)')
xlabel('Time (sec)')
hold on;
nexttile;

plot(x_sensor_1_data(1:310,:), filtered_data)
title('My filter')
ylabel('Temp (Celcius)')
xlabel('Time (sec)')

%}
