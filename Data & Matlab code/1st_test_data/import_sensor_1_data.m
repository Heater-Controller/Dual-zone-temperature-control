%% Import data from text file
% Script for importing data from the following text file:
%
%    filename: /Users/.../march_21st_data/temp_data_1_march_21.txt
%
% Auto-generated by MATLAB on 05-Apr-2022 17:37:39

%% Set up the Import Options and import the data
opts = delimitedTextImportOptions("NumVariables", 2);

% Specify range and delimiter
opts.DataLines = [2, Inf];
opts.Delimiter = ",";

% Specify column names and types
opts.VariableNames = ["Temperature_Sensor_1", "Second_Sensor_1"];
opts.VariableTypes = ["double", "double"];

% Specify file level properties
opts.ExtraColumnsRule = "ignore";
opts.EmptyLineRule = "read";

% Import the data
temp_sensor_1_data_march21 = readtable("/Users/.../march_21st_data/temp_data_1_march_21.txt", opts);


%% Clear temporary variables
clear opts