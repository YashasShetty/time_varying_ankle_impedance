import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt

hs_i = []

def second_order_model(params, t, delta_t):
    I, B, K = params
    omega_n = np.sqrt(K / I)
    zeta = B / (2 * np.sqrt(I * K))
    h_model = np.exp(-zeta * omega_n * t) * np.sin(omega_n * np.sqrt(1 - zeta**2) * t)
    return h_model

def compute_h_s_hat_i(z, u, M1, M2, delta_t, N_w, i):
    h_s_hat_i = np.zeros_like(u)
    for j in range(i - int(N_w/2), i + int(N_w/2) + 1):
        if 1 <= j <= len(u):
            h_hat_j = compute_h_hat_i(u, z, j, M1, M2, delta_t)
            if j == i - int(N_w/2):
                h_s_hat_i = h_hat_j
            else:
                h_s_hat_i += h_hat_j
    h_s_hat_i /= N_w
    hs_i.append(h_s_hat_i)

    return h_s_hat_i

def compute_h_hat_i(u, z, i, M1, M2, delta_t):
    Phi_uu_hat_i = compute_auto_correlation_matrix(u, i, M1, M2)
    phi_zu_hat_i = compute_cross_correlation(z, u, i, M1, M2)
    h_hat_i, _, _, _ = np.linalg.lstsq(Phi_uu_hat_i, phi_zu_hat_i, rcond=None)
    return (1 / delta_t) * h_hat_i

def compute_cross_correlation(z, u, i, M1, M2):
    phi_zu_hat_i = np.zeros(M2 - M1 + 1)
    for k in range(M1, M2 + 1):
        index = i - k
        if 1 <= index <= len(u):
            phi_zu_hat_i[k - M1] = z[i-1] * u[index-1]
    return phi_zu_hat_i

def compute_auto_correlation_matrix(u, i, M1, M2):
    Phi_uu_hat_i = np.zeros((M2 - M1 + 1, M2 - M1 + 1))
    for m in range(M1, M2 + 1):
        for n in range(M2 - M1 + 1):
            Phi_uu_hat_i[m - M1, n] = compute_auto_correlation(u, i, m, n)
    return Phi_uu_hat_i

def compute_auto_correlation(u, i, j, k):
    phi_uu_hat = 0
    if i - j >= 1 and i - k >= 1:
        phi_uu_hat += u[i - j - 1] * u[i - k - 1]
    return phi_uu_hat

def fit_second_order_model(u, z, M1, M2, delta_t, N_w, i):
    h_s_hat_i = compute_h_s_hat_i(z, u, M1, M2, delta_t, N_w, i)

    # Generate the entire range of indices for t
    t = np.arange(1, len(h_s_hat_i) + 1)

    def model_function(params):
        return np.mean((second_order_model(params, t, delta_t) - h_s_hat_i)**2)

    initial_guess = np.array([1.0, 1.0, 1.0])
    fitted_params = minimize(model_function, initial_guess).x

    I_star_i, B_star_i, K_star_i = fitted_params

    # Adjust the range of indices for the model response
    h_model = second_order_model(fitted_params, t, delta_t)

    return I_star_i, B_star_i, K_star_i, h_model

u = np.array([-5.91370912, -6.14645549, -6.35498157, -6.53982496, -6.70152327, -6.8406141, -6.95763507, -7.05312379, -7.12761786, -7.18165489, -7.21577248, -7.23050826, -7.22639981, -7.20398476, -7.16380072, -7.10638528, -7.03227606, -6.94201066, -6.8361267, -6.71516177, -6.5796535, -6.43013949, -6.26715734, -6.09124467, -5.90293908, -5.70277817, -5.49129957, -5.26904087, -5.03653969, -4.79433363, -4.54296031, -4.28295732, -4.01486227, -3.73921279, -3.45654646, -3.16740091, -2.87231374, -2.57182256, -2.26646497, -1.95677858, -1.64330101, -1.32656986, -1.00712274, -0.68549725, -0.36223101, -0.03786162, 0.28707331, 0.61203617, 0.93648935, 1.25989525, 1.58171626, 1.90141476, 2.21845315, 2.53229383, 2.84239918, 3.14823159, 3.44925347, 3.74492719, 4.03471515, 4.31807975, 4.59448337, 4.86338842, 5.12425727, 5.37655232, 5.61973596, 5.85327059, 6.0766186, 6.28924237, 6.4906043, 6.68016679, 6.85739222, 7.02174299, 7.17268148, 7.3096701, 7.43217123, 7.53964726, 7.63156058, 7.70737359, 7.76654869, 7.80854825, 7.83283468, 7.83887036, 7.82611768, 7.79403905, 7.74209685, 7.66975347, 7.5764713, 7.46171274, 7.32494018, 7.165616, 6.98320261, 6.7771624, 6.54695774, 6.29205105, 6.0119047, 5.7059811, 5.37374263, 5.01465168, 4.62817065, 4.21376193, 3.77088791, 3.29901098, 2.79759354, 2.26609797, 1.70398667, 1.11072203, 0.48576644, -0.1714177, -0.86136801, -1.58462209])

z = np.array([-0.116328103, -0.132347511, -0.148525838, -0.164461687, -0.17973988, -0.193953439, -0.206728703, -0.217750801, -0.22678336, -0.233683161, -0.238405023, -0.240996396, -0.241585494, -0.240362639, -0.237561236, -0.233436671, -0.228249042, -0.222248153, -0.215661131, -0.208684574, -0.201480019, -0.194172192, -0.186849538, -0.179568576, -0.17235774, -0.165224183, -0.158159881, -0.151147389, -0.144165424, -0.137191833, -0.130207427, -0.123196156, -0.116148077, -0.109057957, -0.101926668, -0.094759618, -0.087566052, -0.080357833, -0.073148219, -0.065948897, -0.058770333, -0.051620204, -0.04450322, -0.037421648, -0.030375488, -0.023364042, -0.016385218, -0.009436398, -0.002514966, 0.00438187, 0.011257598, 0.018116404, 0.024963, 0.031803839, 0.038645724, 0.045497553, 0.052369094, 0.059271163, 0.066215448, 0.073213984, 0.08027881, 0.087421612, 0.094653904, 0.101986328, 0.109429349, 0.116992737, 0.124685562, 0.132514629, 0.140484298, 0.148593522, 0.156834976, 0.165192434, 0.173639209, 0.182136921, 0.190634982, 0.199069894, 0.2073656, 0.215434528, 0.223178814, 0.230491874, 0.237262587, 0.243377213, 0.248724459, 0.253197738, 0.256700408, 0.259146817, 0.260465617, 0.26059802, 0.259497799, 0.257130413, 0.253471616, 0.248507276, 0.242231637, 0.234646269, 0.225759197, 0.215583503, 0.204137854, 0.191447196, 0.17754502, 0.162475811, 0.146299403, 0.129096216, 0.110971961, 0.092063753, 0.072545164, 0.052630587, 0.032576628, 0.012682286, -0.006715239, -0.025246821])

M1 = 0
M2 = 1
delta_t = 1
N_w = 4

I = []
B = []
K = []
h = []

for i_value in range(5, 100):
    I_star, B_star, K_star, h_model = fit_second_order_model(u, z, M1, M2, delta_t, N_w, i_value)
    I_star = I_star * -0.05
    B_star = B_star * 0.4
    K_star = K_star * -10
    I.append(I_star)
    B.append(B_star)
    K.append(K_star)
    h.append(h_model)

# Function to convert array of array to an array
def extractor(a):
  extract = []
  for i in range(0,len(a)):
    a1 = a[i]
    for j in range(0,1):
      a2 = a1[0]
      extract.append(a2)
      extract1 = np.array([extract])
  return extract1

def accomodator(a,b):
  c =[]
  for i in range(0,len(a)):
    c1 = a[i] - b
    c.append(c1)
  return c


