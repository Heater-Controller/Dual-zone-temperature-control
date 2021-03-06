%% Import data from text file
% Script for importing data from the following text file:
%
%    filename: /Users/.../testing_filter/output_data_for_test.txt
%
% Auto-generated by MATLAB on 07-Apr-2022 16:50:41

%% Set up the Import Options and import the data
opts = delimitedTextImportOptions("NumVariables", 1);

% Specify range and delimiter
opts.DataLines = [1, Inf];
opts.Delimiter = ",";

% Specify column names and types
opts.VariableNames = "output";
opts.VariableTypes = "double";

% Specify file level properties
opts.ExtraColumnsRule = "ignore";
opts.EmptyLineRule = "read";

% Import the data
output_data_for_test = readtable("/Users/.../testing_filter/window_5_data.txt", opts);


%% Clear temporary variables
clear opts