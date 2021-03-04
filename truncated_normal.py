import numpy as np
import scipy.stats as stats
import scipy.optimize

def truncated_mean_std(mu, sigma, lower, upper):
    alpha = (lower - mu)/sigma
    beta = (upper - mu)/sigma
    d_pdf = (stats.norm.pdf(alpha) - stats.norm.pdf(beta))
    wd_pdf = (alpha * stats.norm.pdf(alpha) - beta * stats.norm.pdf(beta))
    d_cdf = stats.norm.cdf(beta) - stats.norm.cdf(alpha)
    mu_trunc = mu + sigma * (d_pdf / d_cdf)
    var_trunc = sigma**2 * (1 + wd_pdf / d_cdf - (d_pdf/d_cdf)**2)
    std_trunc = var_trunc**0.5
    return mu_trunc, std_trunc

def trunc_samples(mu, sigma, lower, upper, num_samples=1000):
    n = stats.truncnorm((lower - mu) / sigma, (upper - mu) / sigma, loc=mu, scale=sigma)
    samples = n.rvs(num_samples)
    return samples

def corrector(mu, sigma, lower, upper):
    target = np.array([mu, sigma])
    result = scipy.optimize.minimize(
        lambda x: ((target - truncated_mean_std(x[0], x[1], lower, upper))**2).sum(),
        x0=[mu, sigma])
    return result.x

# some tests
# sample = trunc_samples(mu=2, sigma=1, lower=0, upper=100, num_samples=100_000_000)
# print(sample.min())
# print(sample.max())
# print(sample.mean())
# print(sample.var())
