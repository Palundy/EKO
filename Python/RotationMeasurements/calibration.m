csv = readtable("calibration_data_1710510798.csv");

% Retrieve measurement numbers
index = csv{:, 1};

% Retrieve all the seperate measurements
for j = 1:(index(end) + 1)

    % Retrieve the indices for the given measurements
    indices = find(index == j-1);

    % Assign the values to the given index
    t{j} = csv{indices, 2};
    t{j} = t{j} - t{j}(1); % Make the time relative instead of absolute
    
    pos{j} = csv{indices, 3};
    ref_irr{j} = csv{indices, 4};
    test_irr{j} = csv{indices, 5};
end



% Create a tiled layout to show measurements
t1 = tiledlayout(3, 1);
ylabel(t1, "Comp. Irradiance [W/m²]");

nexttile;
scatter(t{1}, ref_irr{1}, 'DisplayName', 'Reference');
hold on;
scatter(t{1}, test_irr{1}, 'DisplayName', 'Test');
title("Shaded measurements");
xlabel("t [s]");
legend()
grid on;

nexttile;
scatter(t{2}, ref_irr{2}, 'DisplayName', 'Reference');
hold on;
scatter(t{3}, test_irr{3}, 'DisplayName', 'Test');
title("Position A measurements");
xlabel("t [s]");
legend()
grid on;

nexttile;
scatter(t{3}, ref_irr{3}, 'DisplayName', 'Reference');
hold on;
scatter(t{2}, test_irr{2}, 'DisplayName', 'Test');
title("Position B measurements")
xlabel("t [s]");
legend()
grid on;



% Create new figure
% which shows how similar the same position - same sensor measurements are
figure;
t2 = tiledlayout(2, 1);
ylabel(t2, "Ratio");



% Calculate the difference of the means of the datasets
% that were recorded in the same time
%   these will be used to correct the dataset of the reference sensor
%   so that the datasets are on the same level
diff_1 = mean(ref_irr{2}) - mean(test_irr{2});

%    Calculate the ratio between the corrected dataset
ratio_1 = (ref_irr{2} - diff_1) ./ test_irr{2};

% Calculate the standard deviation of the ratios
std_1 = std(ratio_1);

nexttile;
scatter(t{2}, ratio_1, 'DisplayName', "σ = " + std_1);
title("Ratio Ref/Test - Position A");
xlabel("t [s]");
ylim([0.995 1.005]);
legend()
grid on;


% Calculate the difference of the means of the datasets
% that were recorded in the same time
%   these will be used to correct the dataset of the reference sensor
%   so that the datasets are on the same level
diff_2 = mean(ref_irr{4}) - mean(test_irr{4});

%    Calculate the ratio between the corrected dataset
ratio_2 = (ref_irr{4} - diff_2) ./ test_irr{4};

% Calculate the standard deviation of the ratios
std_2 = std(ratio_2);

nexttile;
scatter(t{4}, ratio_2, 'DisplayName', "σ = " + std_2);
title("Ratio Ref/Test - Position B");
xlabel("t [s]");
ylim([0.995 1.005]);
legend()
grid on;

