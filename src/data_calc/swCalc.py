import numpy as np
import math


def sw_archie(Rw, Rt, Poro, a, m, n):
    F = a / (Poro**m)
    Sw_archie = (F * Rw / Rt) ** (1 / n)
    return Sw_archie


def sw_indonesia(Rw, Rt, Poro, a, m, n, vcl, rsh):
    """
    Vectorized implementation of the Indonesia Sw calculation

    Parameters:
    -----------
    Rw, Rt, Poro, a, m, n, vcl, rsh : numpy arrays or pandas Series
        Input parameters for the Indonesia equation

    Returns:
    --------
    numpy array
        Water saturation values
    """
    # Create a mask for invalid inputs
    invalid_mask = (Rt == 0) | (rsh == 0) | (a == 0) | (n == 0)

    # Calculate terms using numpy operations
    vcl_term = np.power(vcl, 1 - (0.5 * vcl))
    poro_term = np.power(Poro, m) / (a * Rw)

    # Calculate denominator
    denominator = (vcl_term / np.sqrt(rsh)) + np.sqrt(poro_term)

    # Update invalid mask for zero denominators
    invalid_mask = invalid_mask | (denominator == 0)

    # Final calculation
    Sw_indonesia = np.power((1 / Rt) / denominator, 2 / n)

    # Apply range validation (0 to 1)
    invalid_mask = invalid_mask | (Sw_indonesia < 0) | (Sw_indonesia > 1)

    # Create result array with nan values for invalid results
    result = Sw_indonesia.copy()
    result[invalid_mask] = np.nan

    return result


def sw_waxman_vectorized(Rw, Qv, a, m, n, Temp, Rt, Phi):
    # Input validation
    invalid_mask = (Rw == 0) | (Rt == 0) | (Phi == 0) | (n == 0)

    # Initialize Sw and Swi arrays
    Sw = np.zeros_like(Rw, dtype=float)
    Swi = np.zeros_like(Rw, dtype=float)

    # Calculate Bmax and b
    Bmax = 51.31 * np.log(Temp + 460) - 317.2
    b = (1 - 0.83 / np.exp(0.5 / Rw)) * Bmax

    # Calculate F
    F = a / (Phi**m)

    # Initial Swi calculation
    Swi = (F * Rw / Rt) ** (1 / n)

    # Protect against Swi being zero in the loop
    for i in range(len(Rt)):
        if invalid_mask[i]:
            Sw[i] = np.nan
            continue

        while abs(Sw[i] - Swi[i]) > 0.01 and Swi[i] != 0:
            denominator = 1 / Rw + (b[i] * Qv[i] / Swi[i])
            if denominator == 0:
                Sw[i] = np.nan
                break
            Sw[i] = (F[i] / Rt[i] / denominator) ** (1 / n)
            Swi[i] = Sw[i]

    return Sw


def sw_waxman(Rw, Qv, a, m, n, Temp, Rt, Phi):
    try:
        # Input validation
        if Rw == 0 or Rt == 0 or Phi == 0 or n == 0:
            return np.nan

        Sw, Swi = 0.0, 0.0

        # Calculate Bmax and b
        Bmax = 51.31 * math.log(Temp + 460) - 317.2
        b = (1 - 0.83 / math.exp(0.5 / Rw)) * Bmax
        F = a / (Phi**m)

        # Initial Swi calculation
        Swi = (F * Rw / Rt) ** (1 / n)

        # Protect against Swi being zero in the loop
        while abs(Sw - Swi) > 0.01 and Swi != 0:
            denominator = 1 / Rw + (b * Qv / Swi)
            if denominator == 0:
                return np.nan

            Sw = (F / Rt / denominator) ** (1 / n)
            Swi = Sw

        return Sw

    except:
        return np.nan


def sw_simandoux(Rw, Rt, Vsh, Poro, a, m, n, Rsh):
    F = a / (Poro**m)
    X = Vsh / Rsh
    term = X**2 + (4 / a) * F * Rw / Rt
    Sw_modsim = (F * (Rw / 2) * (np.sqrt(term) - X)) ** (2 / n)

    return Sw_modsim
