csv = readtable("stability_measurements\stability_detection_m3_01.csv");

t = csv{:, 1} - min(csv{:, 1});
I = csv{:, 2};

% Normalize the data
I = I - min(I);
I = I / max(I);
%I = csv{:, 2};

tiledlayout(4, 1);

nexttile;
scatter(t, I, '.');
xlabel("Time [s]");
ylabel("Compensated Irradiance [W/m²]");
%title("Time Response of ICF-02 Lamp");
subtitle("Amount of datapoints: " + length(I), "Color", "#888888");
hold on;
grid on;


dI = diff(I);
dt = diff(t);
D = dI ./ dt;

windowsize = 20;
DMean = movmean(D, [windowsize - 1 0]);

nexttile
plot(t(1:end-1), D);
hold on;

nexttile;
plot(t(1:end-1), abs(DMean));
hold on;
grid on;