import numpy as np
import matplotlib.pyplot as plt

# asset value
def sim_value(start_val, n_sims=1000, n_years=25, mean=0.01, var=0.015, final_values=False):

    # initialize data structures
    start_arr = np.full(n_sims, fill_value=start_val)
    returns = np.random.normal(mean + 1, var, size=(n_sims, n_years))

    # calculate
    if final_values:
        final_returns = np.prod(returns, axis=1)
        final_values = np.multiply(final_returns, start_arr) # single value per sim
        return final_values
    else:
        yearly_returns = np.cumproduct(returns, axis=1)
        yearly_values = np.multiply(start_arr.reshape(-1, 1), yearly_returns) # values per year and sim
        return yearly_values


# rent income
def sim_rent(start_val, n_sims=1000, n_years=25, flat_years=5, mean=0.05, var=0.03, final_values=False):

    start_arr = np.full((n_sims, 1), fill_value=start_val)
    rent_incrs = np.random.normal(mean + 1, var, size=(n_sims, n_years // flat_years))
    rent_incrs[:, 0] = 1.0

    rent_rel = np.cumproduct(rent_incrs, axis=1)
    rent_abs = np.multiply(start_arr, rent_rel)

    rent_final = np.concatenate(
                                [np.repeat(rent_abs[:, i].reshape(-1, 1), flat_years, axis=1) for i in range(rent_abs.shape[1])], 
                                axis=1
                                )

    return rent_final

