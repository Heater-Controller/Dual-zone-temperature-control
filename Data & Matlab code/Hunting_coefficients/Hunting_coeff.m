
%%% Sensor 1
data_start_1 = 425;
data_end_1 = 8701;
y_sensor_1_data = temp_sensor_1_data_march27.Temperature_Sensor_1(data_start_1:data_end_1,:);
x_sensor_1_data = temp_sensor_1_data_march27.Second_Sensor_1(data_start_1:data_end_1,:);
for row = 1: size(temp_sensor_1_data_march27.Second_Sensor_1(data_start_1:data_end_1,:))
    x_sensor_1_data(row) = row;
end
%%%

%%% Sensor 2
data_start_2 = 425;
data_end_2 = 8701;
y_sensor_2_data = temp_sensor_2_data_march27.Temperature_Sensor_2(data_start_2:data_end_2,:);
x_sensor_2_data = temp_sensor_2_data_march27.Second_Sensor_2(data_start_2:data_end_2,:);
for row = 1: size(temp_sensor_2_data_march27.Second_Sensor_2(data_start_2:data_end_2,:))
    x_sensor_2_data(row) = row;
end
%%%

%%% Sensor 3
data_start_3 = 425;
data_end_3 = 8701;
y_sensor_3_data = temp_sensor_3_data_march27.Temperature_Sensor_3(data_start_3:data_end_3,:);
x_sensor_3_data = temp_sensor_3_data_march27.Second_Sensor_3(data_start_3:data_end_3,:);
for row = 1: size(temp_sensor_3_data_march27.Second_Sensor_3(data_start_3:data_end_3,:))
    x_sensor_3_data(row) = row;
end
%%%

%%% Time_Sample
time_start = 425;
time_end = 8701;
time = timesample1.Time(time_start:time_end,:);
%%%

%%{ 
figure(1);
tiledlayout(3,1);
nexttile;
plot(x_sensor_1_data, y_sensor_1_data)
title('Temperature vs Time')
ylabel('Temp (Celcius)')
xlabel('Time (sec)')
legend('Sensor 1');
hold on;
nexttile;
plot(x_sensor_2_data, y_sensor_2_data)
title('Temperature vs Time')
ylabel('Temp (Celcius)')
xlabel('Time (sec)')
legend('Sensor 2');
hold on;
nexttile;
plot(x_sensor_3_data, y_sensor_3_data)
title('Temperature vs Time')
ylabel('Temp (Celcius)')
xlabel('Time (sec)')
legend('Sensor 3');
%}

%%{ 
window = 60;
method = 'lowess'; % 'movmedian'
figure(2);
tiledlayout(3,1);
nexttile;
plot(x_sensor_1_data, smoothdata(y_sensor_1_data,method,window))
xline(1332);
xline(3492);
xline(5892);
title('Temperature vs Time')
ylabel('Temp (Celcius)')
xlabel('Time (sec)')
legend('Sensor 1');
hold on;

nexttile;
plot(x_sensor_2_data, smoothdata(y_sensor_2_data,method,window))
xline(1332);
xline(3492);
xline(5892);
title('Temperature vs Time')
ylabel('Temp (Celcius)')
xlabel('Time (sec)')
legend('Sensor 2');
hold on;

nexttile;
plot(x_sensor_3_data, smoothdata(y_sensor_3_data,method,window))
xline(1332);
xline(3492);
xline(5892);
title('Temperature vs Time')
ylabel('Temp (Celcius)')
xlabel('Time (sec)')
legend('Sensor 3');
%}

%{
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
%}

%{ 
window = 60;
method = 'lowess'; % 'movmedian'
figure(2);
plot(x_sensor_1_data, smoothdata(y_sensor_1_data,method,window))
hold on;
plot(x_sensor_2_data, smoothdata(y_sensor_2_data,method,window))
hold on;
plot(x_sensor_3_data, smoothdata(y_sensor_3_data,method,window))
title('Temperature vs Time')
ylabel('Temp (Celcius)')
xlabel('Time (sec)')
legend('Sensor 1','Sensor 2','Sensor 3');
%}