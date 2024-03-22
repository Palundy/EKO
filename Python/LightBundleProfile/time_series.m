csv = readtable("measurements\time_series_measurements\time_measurement.csv");

t = csv{:, 2};
I = csv{:, 3};
I = I / max(I);

scatter(t, I, '.');
xlabel("Time [s]");
ylabel("Compensated Irradiance [W/m²]");
title("Time Response of ICF-02 Lamp");
subtitle("Amount of datapoints: " + length(I), "Color", "#888888");

% Find time at which the irradiance stabilizes within 2%
% of it's steady-state value
indices = find(I >= max(I) * 0.98);

t_filtered = t(indices);
I_filtered = I(indices);
disp(t_filtered(1));

hold on;
grid on;
xline(t_filtered(1));



dI = diff(I);
dt = diff(t);
D = dI ./ dt;

DMean = movmean(D, 40);

figure;
plot(t(1:end-1), abs(D));
hold on;
plot(t(1:end-1), DMean);

hold on;
grid on;
xline(t_filtered(1));