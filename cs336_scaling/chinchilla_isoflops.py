import numpy as np
from scipy.optimize import curve_fit
import pandas as pd
import matplotlib.pyplot as plt

def func(x, a, b, c):
    return a * x**b + c

if __name__ == '__main__':
    data_path = r'data/isoflops_curves.json'
    data = pd.read_json(data_path)

    min_indices = data.groupby('compute_budget')['final_loss'].idxmin()
    result = data.loc[min_indices]

    print(result)

    p0 = [1.0, 0.5, 1e8]
    popt, pcov = curve_fit(func, result['compute_budget'], result['parameters'], 
                           p0=p0, maxfev=10000)
    print(popt)
    x = data['compute_budget'].unique()
    x = np.append(x, 1e23)
    x = np.append(x, 1e24)
    y = func(x, *popt)

    plt.scatter(result['compute_budget'], result['parameters'])
    plt.plot(x, y)
    plt.xlabel('compute_budget')
    plt.ylabel('parameters')
    plt.show()