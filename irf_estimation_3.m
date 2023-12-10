
% True parameter values
true_m = 2.0;
true_b = 0.5;
true_k = 3.0;
K = 1.0;

% Generate synthetic experimental data
time_steps = linspace(0, 5, 100);
force_input = sin(time_steps);  % Example force input
true_response = K ./ (true_m * time_steps.^2 + true_b * time_steps + true_k);

% Add some random noise to simulate measurement errors
noise = 0.1 * randn(size(true_response));
observed_data = true_response + noise;

% Define the objective function (mean squared error)
objective = @(params) mean((observed_data - K ./ (params(1) * time_steps.^2 + params(2) * time_steps + params(3))).^2);

% Initial guess for parameters
initial_guess = [1.0, 0.2, 2.0];

% Use fminsearch for parameter estimation
estimated_params = fminsearch(objective, initial_guess);

% Display results
disp('True Parameters:');
disp(['Inertia (m): ', num2str(true_m)]);
disp(['Viscosity (b): ', num2str(true_b)]);
disp(['Stiffness (k): ', num2str(true_k)]);
disp(' ');
disp('Estimated Parameters:');
disp(['Inertia (m): ', num2str(estimated_params(1))]);
disp(['Viscosity (b): ', num2str(estimated_params(2))]);
disp(['Stiffness (k): ', num2str(estimated_params(3))]);

% Example usage:

% Sample IRF data
t = 0:0.01:0.08; % Time vector
theta_measured = [0 0.01 0.018 0.024 0.028 0.026 0.02 0.012 0.002]; % Hypothetical measured joint angles

% Add some noise to simulate measurement errors
noise = 0.005 * randn(size(theta_measured));
theta_measured_with_noise = theta_measured + noise;

% Assign the IRF data to the variable irf_data
h = theta_measured_with_noise;

% Now you can use irf_data in your code

% Load the IRF data (replace 'irf_data.mat' with your actual file)
% load('irf_data.mat'); % Assuming 'h' is the variable representing IRF data



% Example usage:

% Define other variables (replace with actual values)
I_Abot = 0.1; % Abot inertia
B_Abot = 0.2; % Abot viscosity
K_Abot = 0.1; % Abot stiffness

% Smooth the IRF data
i = 1; % Choose an appropriate index for smoothing
w = 10; % Window size for smoothing
h_s = smooth_irf(h, i, w);

% Estimate the best fit IRF model parameters
[I_star, B_star, K_star] = estimate_irf_model_parameters(h_s);

% Calculate the ankle parameters
[I_Ankle_star, B_Ankle_star, K_Ankle_star] = calculate_ankle_parameters(I_star, B_star, K_star, I_Abot, B_Abot, K_Abot);


% Calculate the smoothed IRF estimates (h_s(i))
function h_s = smooth_irf(h, i, w)
  N_w = length(h(max(1,i-floor(w/2)):min(length(h),i+floor(w/2))));
  h_s = 1/N_w * sum(h(max(1,i-floor(w/2)):min(length(h),i+floor(w/2))));
end

% Estimate the best fit IRF model parameters (I*(i), B*(i), K*(i))
function [I_star, B_star, K_star] = estimate_irf_model_parameters(h_s)
  % Use an unconstrained nonlinear optimization method (Nelder-Mead simplex method)
  [I_star, B_star, K_star] = fminsearch(@(params) mean((h_s - calculate_irf_model(params)).^2), [0, 0, 0]);
end

% Calculate the ankle parameters (I_Ankle*(i), B_Ankle*(i), K_Ankle*(i))
function [I_Ankle_star, B_Ankle_star, K_Ankle_star] = calculate_ankle_parameters(I_star, B_star, K_star, I_Abot, B_Abot, K_Abot)
  I_Ankle_star = I_star(1) - I_Abot;
  B_Ankle_star = B_star - B_Abot;
  K_Ankle_star = K_star - K_Abot;
end

% Calculate the IRF of the model (h_model(i))
function h_model = calculate_irf_model(params)
  % Define or load the data needed for the model (e.g., I, B, K)
  I = params(1);
  B = params(2);
  K = params(3);
  
  % Simulate the response of the rotational system
  t = 0:0.01:0.08; % Define time vector
  theta_model = zeros(size(t));
  dtheta_dt = zeros(size(t));
  
  % Initial conditions
  theta_model(1) = 0;
  dtheta_dt(1) = 0;
  
  % Simulate model using Euler's method
  for i = 2:length(t)
    dt = t(i) - t(i-1);
    
    dtheta_dt(i) = (-B*dtheta_dt(i-1) - K*theta_model(i-1))/I;
    theta_model(i) = theta_model(i-1) + dt*dtheta_dt(i-1);
  end
  
  % Calculate the impulse response function
  h_model = theta_model;
end

