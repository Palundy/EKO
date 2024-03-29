csv = readtable("measurements/measurement_quick_scan_23.csv");

pos_abs = csv{:, 1};
pos_rel = csv{:, 2};
I = csv{:, 3};


% Convert the relative rotation to angle in radians
FULL_ROTATION = 51200 * -5;
angles = (pos_rel / FULL_ROTATION) * -2 * pi;


% Map the radial points
% into cartesian points
r = 10.5; % cm. Radius from center to dome-center
x = r * cos(angles);
y = r * sin(angles);


% Set the thresholds for the optimal irradiance range 
lower_threshold = 775; % W/m²
upper_threshold = 825; % W/m²

% Retrieve the points that are within the optimum range
opt_irr_indices = find(I >= lower_threshold & I <= upper_threshold);
o_x = x(opt_irr_indices);
o_y = y(opt_irr_indices);
o_I = I(opt_irr_indices);
o_a = angles(opt_irr_indices);

% For each point in the optimal range determine the 
% dI/dθ by using the finite difference method (central)
derivatives = zeros(length(I), 1);
d_theta = angles(2) - angles(1); % Angle step size

for i = 1:length(I) - 1
    % Calculate the derivative
    derivatives(i) = ( I(i + 1) - I(i) ) / d_theta;
end
o_deriv = derivatives(opt_irr_indices);

polarplot(angles, I);
figure;


% Check which derivatives fall within 2sigma from the mean
sigma = std(o_deriv);
valid_indices = find(abs(o_deriv - mean(o_deriv)) <= 2 * sigma);

% Calculate the mean derivative from the valid points
mean_derivative = mean(o_deriv(valid_indices));
% Now we take the absolute value, because the polarity of the derivative
% is not of very much value
mean_derivative = abs(mean_derivative);

disp("The mean dI/dθ is: " + mean_derivative + "W/m² per rad");
disp("Or: " + mean_derivative/(360 / 2*pi) + "W/m² per °");


% What could be interesting to know
% is the ratio between irradiance and the derivative on each point
deriv_ratio = abs(I) ./ derivatives;



figure;
scatter3(x, y, I);
hold on;
scatter3(o_x, o_y, o_I);
hold on;
scatter3(x(1), y(1), I(1), 'x');
hold on
scatter3(x(end), y(end), I(end), 'square');
hold off;

%figure;
%scatter3(x, y, deriv_ratio);
