filename = "measurements/plane_measurements/measurement_height_scan";
csv = readtable(filename + ".csv");


% Defining the offsets
intensity_offset = 4.1330695152282715;

x_offset = 3.5; %cm
y_offset = 4.0; %cm
granularity = 1; %cm

lower_threshold_intensity = 650; % W/m^2
higher_threshold_intensity = 800; % W/m^2


% Retrieve and transform the coordinates
coordinates = csv{:, 1:2};

% Retrieve the intensity and remove the offset
compensated_intensity = csv{:, 3} - intensity_offset;
% Find all the intensity indices that are greater than the threshold
threshold_indices = compensated_intensity >= higher_threshold_intensity;

x = coordinates(:, 1) + x_offset;
y = (coordinates(:, 2) / 10) + y_offset;
z = compensated_intensity;

% Prepare the meshgrid
[xq, yq] = meshgrid(min(x):0.1:max(x), min(y):0.1:max(y));

% Interpolate the data to smoothen it out (with cubic function)
zq = griddata(x, y, z, xq, yq, 'cubic');




% Create the mesh plot
figure; % Create new figure
mesh(xq, yq, zq); % Create the mesh
hold on;
contour3(xq, yq, zq, 50, 'LineColor', 'k'); % Create the contour for extra depth
hold on
%scatter3(x, y, z, ".", 'MarkerEdgeColor', '#000'); % Create the scatter to show the dataset
hold on
%scatter3(x(threshold_indices), y(threshold_indices), z(threshold_indices));
colorbar % Add colorbar for more accurate readings

% Set the appearance and texts of the figure
xlim([0 42]);
ylim([0 42]);
xlabel('x [cm]');
ylabel('y [cm]');
zlabel('Compensated Irradiance [W/m²]');
title('Gaussian Interpolation of Irradiance');
subtitle("Amount of datapoints: "+length(compensated_intensity), 'Color', '#787777')

% Save the figure
savefig(gcf, "figures/" + filename + "_3D.fig");
hold off;




% Create the second figure
% that shows the 2D contour with the
% scatter plot that shows the coordinates of
% the points where the intensity is greater than the threshold
figure;
contour(xq, yq, zq); % Create the 2D contour
hold on;
scatter(x, y, '.', 'MarkerEdgeColor', '#dcdcdc'); % Create the scatter plot to show the dataset
hold on;
scatter(x(threshold_indices), y(threshold_indices), "o", "MarkerEdgeColor","blue"); % Show the points that are within the threshold
hold on;
scatter(21, 21, 'x', 'MarkerEdgeColor', 'red'); % Show the midpoint of the bench
colorbar

% Set the appearance and texts for the figure
xlim([0 42]);
ylim([0 42]);
xlabel('x[cm]');
ylabel('y [cm]');
title('Gaussische Interpolatie van Lichtintensiteit');
subtitle("Granulariteit: "+granularity+" cm, Aantal meetpunten: "+length(compensated_intensity), 'Color', '#787777')

% Save the figure
savefig(gcf, "figures/" + filename + "_2D.fig");
hold off;




% Berekenen hoeveel de lamp verschoven moet worden, zodat
% de maximum van de lichtbundel in het midden valt
max_intensity = (compensated_intensity == max(compensated_intensity));
max_x = x(max_intensity);
max_y = y(max_intensity);



