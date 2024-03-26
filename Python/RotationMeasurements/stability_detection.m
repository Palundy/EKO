csv = readtable("stability_measurements\stability_detection_m1_01.csv");

t = csv{:, 1} - min(csv{:, 1});
I = csv{:, 2};


tiledlayout(2, 1);

nexttile;
scatter(t, I, '.');
xlabel("Time [s]");
ylabel("Compensated Irradiance [W/m²]");
subtitle("Amount of datapoints: " + length(I), "Color", "#888888");
hold on;
grid on;

% Calculate the derivatives
%       backward difference method
D = ( I(2:end) - I(1:end-1) ) ./ ( t(2:end) - t(1:end-1) );

Frac = I * 0.001;

nexttile
plot(t(1:end-1), D);
xlabel("Time [s]");
ylabel("Change in Irradiance [(W/m²)/s]");
hold on;
plot(t, Frac);
grid on;
hold on;