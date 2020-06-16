import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor


def main():
    """ Func description
    """
    r'''
    # Little ML example

    This is written in ```markdown``` and is latex friendly.

    Here is the equation to predict:
    $$y = 3x\sin\left(\frac{\pi}{20}\right) + \varepsilon$$;

    ML model is re-run in real-time as no. of samples changes (test set is 20%
    of full datasets).
    '''
    # Interactive
    n_samples = st.slider(r'Dataset size', 100, 500, 100)

    # Generate data
    sigma = 40
    X = np.random.uniform(0, 100, n_samples)
    y = 3*X*np.sin(X*np.pi/20) + np.random.normal(0, sigma, n_samples) + 100
    raw = pd.DataFrame(np.transpose([X.flatten(), y]), columns=['x', 'y'])

    # Train/test split
    raw['Type'] = 'Train'
    raw['Type'].iloc[np.int(n_samples*4/5):] = 'Test'

    # Fit model
    regr = GaussianProcessRegressor(alpha=0.05)
    regr.fit(raw.loc[raw['Type'] == 'Train', 'x'].values.reshape(-1, 1),
             raw.loc[raw['Type'] == 'Train', 'y'].values.reshape(-1, 1))

    # Predict line shape
    max_X_test = raw.loc[raw['Type'] == 'Test', 'x'].max()
    x_span = np.linspace(0, max_X_test, 50)
    y_fit = regr.predict(x_span.reshape(-1, 1))
    df = pd.DataFrame(np.transpose([x_span, y_fit.flatten()]),
                      columns=['x', 'y'])

    # Plot
    line = alt.Chart(df).mark_line().encode(
        x='x',
        y='y',
    )
    scatter = alt.Chart(raw).mark_point().encode(
        x='x',
        y='y',
        color='Type',
    )
    plot = (line + scatter).properties(width=700).interactive()
    st.write(plot)
    '''
    More markdown here.

    Here is a live update of the model predictions:
    '''
    st.dataframe(df)


if __name__ == "__main__":
    main()
