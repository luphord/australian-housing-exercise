# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

from .. import paths

def encode_dates(dt):
    '''Encodes datetime values as floats expressed in year fractions.
       >>> encode_dates(pd.date_range('2017-11-01', '2018-02-01', freq='M').values)
       Float64Index([2017.945205479452, 2018.0301369863014, 2018.1150684931506], dtype='float64')
    '''
    return pd.to_timedelta(dt).total_seconds()/365/24/60/60 + 1970

def polynom(t, order=1):
    '''Returns a list of t raised to any integer power up to order.
    '''
    return [t**n for n in range(order+1)]

def polynom_regressor(order):
    '''Returns a regressor function containing a polynom of order order.
    '''
    def _regressor(t):
        return np.stack(polynom(t, order), axis=1)
    return _regressor

def cosine(t):
    '''Returns a list containing the cosine with periodicity of 1.
    '''
    return [np.cos(t*2*np.pi)]

def periodic_regressor(poly_order, add_cosine):
    '''Returns a regressor function containing a polynom of order poly_order
       and optionally a cosine function (with periodicity of 1).
    '''
    def _regressor(t):
        l = polynom(t, poly_order)
        if add_cosine:
            l.extend(cosine(t))
        return np.stack(l, axis=1)
    return _regressor

def fit_ols(time_series, regressor):
    '''OLS fit the first column of time_series on the regressor function
       applied to the float-encoded date index of the time_series
    '''
    y = time_series.iloc[:,0]
    t = encode_dates(time_series.index.values)
    return sm.OLS(y, regressor(t)).fit()

def history_and_prediction_plot(fig, time_series, model_fit, regressor, last_date='2020-07-01', freq='M', alpha=0.05):
    '''Creates a plot containing the time series history as well as prediction
       including confidence intervals for level alpha.
    '''
    t = encode_dates(time_series.index.values)
    t_range = pd.date_range(time_series.index[0], last_date, freq=freq)
    t_all = encode_dates(t_range.values)
    pred = model_fit.get_prediction(regressor(t_all))
    resf = pred.summary_frame(alpha=alpha)

    ax = fig.add_subplot(111)
    ax.set_title('New South Wales Houses Approved - History and Prediction')
    ax.grid(True)
    ax.set_xlabel('time')
    ax.set_ylabel('Number of dwelling units approved')
    ax.plot(t, time_series.iloc[:,0].values, label='history')
    ax.plot(t_all, resf['mean'], label='prediction');
    ax.plot(t_all, resf['obs_ci_lower'], linestyle='dashed', label='lower quantile');
    ax.plot(t_all, resf['obs_ci_upper'], linestyle='dashed', label='upper quantile');
    ax.legend()
    return fig, pd.DataFrame(pred.predicted_mean, index=t_range, columns=['Prediction'])
