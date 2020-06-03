import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
import os


def main():
    # Grab macro data
    df = load_data()
    macro_short_names = list(df.iloc[0, 1:])
    # Conversion of short name to column name
    short_long_dict = dict(zip(macro_short_names, df.columns[1:]))
    df = df.iloc[3:, :]
    # Employment by sector data
    emp_df = load_emp_data()
    # Trade data
    t_df = load_trade_data()
    # Set widths of charts
    widths = 700
    '''
    # A millenium of macroeconomic data

    Thomas and Dimdale (2017) have painstakingly put together a dataset
    that covers a millenium of UK macroeconomic data (some series go back as
    far as 1209!). It can be found [here](https://www.bankofengland.co.uk/statistics/research-datasets),
    at the page of Bank of England research datasets. In this
    [streamlit](https://www.streamlit.io/) app, I've put together
    a few of the highlights.

    ## Macroeconomic aggregates
    since 1695.
    '''
    # User choice: macro short name
    y_axis_short = st.selectbox("Choose a macro variable to display",
                                macro_short_names,
                                index=len(macro_short_names)-1)
    # Convert to column name
    y_axis = short_long_dict[y_axis_short]
    # User choice: scale
    logscale = st.checkbox("Log scale", False)
    scale = alt.Scale(type='linear')
    if logscale:
        scale = alt.Scale(type='log', clamp=True)
    # Plot
    visualize_line(df, 'Year', y_axis, scale, widths)
    '''
    Source: see Thomas (2017) headline series for full list of sources.

    ## Employment by sector
    Over the 20th century.
    '''
    sectors = list(emp_df['Sector'].unique())
    multiselection = st.multiselect("Select:",
                                    sectors,
                                    default=sectors)
    subdf = emp_df[emp_df['Sector'].isin(multiselection)]
    visualize_bar(subdf, widths)
    '''
    Source: Broadberry et al. (2015), Feinstein (1972) and ONS (various publications).


    ## Trade
    Of the United Kingdom with other regions.
    '''
    visualize_line_facet(t_df)
    '''
    Source: Mitchell (1988) and Thomas (2017) - see page A41 of v3.1.

    ### Sources
    To cite the millenium of macro data, please use:
    ```
    @misc{thomas2017millennium,
    title={A Millennium of UK Macroeconomic Data: Bank of England OBRA Dataset},
    author={Thomas, R and Dimsdale, N},
    year={2017},
    publisher={Bank of England}
    }
    ```
    Other sources:
    ```
    @book{broadberry2015british,
    title={British economic growth, 1270--1870},
    author={Broadberry, S and Campbell, Bruce MS and Klein, Alexander and Overton, Mark and van Leeuwen, Bas},
    year={2015},
    publisher={Cambridge University Press}
    }

    @book{feinstein1972national,
    title={National income, expenditure and output of the United Kingdom 1855-1965},
    author={Feinstein, Charles Hilliard},
    volume={6},
    year={1972},
    publisher={Cambridge University Press}
    }

    @book{mitchell1988british,
    title={British historical statistics},
    author={Mitchell, Brian R and MITCHELL, BRIAN S},
    year={1988},
    publisher={CUP Archive}
    }
    ```



    The code for this app is available at:

    [https://github.com/aeturrell/millennium-app]
    (https://github.com/aeturrell/millennium-app)
    '''


@st.cache
def load_data():
    df = pd.read_csv(os.path.join('data', 'millen_data.csv'), header=None)
    df = df.dropna(axis=0).reset_index(drop=True)
    new_names = ['Year'] + [x+' (' + y + ')'
                            for x, y in zip(df.iloc[1, 1:], df.iloc[2, 1:])]
    df = df.rename(columns=dict(zip(range(len(df.columns)),
                                    new_names)))
    return df


@st.cache
def load_emp_data():
    df = pd.read_csv(os.path.join('data', 'employment_sector.csv'))
    df = df.iloc[1:, :]
    df = df.loc[df['Year'] > '1920']
    df = pd.melt(df, id_vars='Year',
                 value_vars=df.columns[1:])
    df = df.rename(columns={'variable': 'Sector',
                            'value': 'Employment (thousands)'})
    return df


@st.cache
def load_trade_data():
    df = pd.read_csv(os.path.join('data', 'trade_by_region.csv'),
                     header=[0, 1])
    df = pd.melt(df, id_vars=[('Region', 'Year')], var_name=['Region', 'Type'],
                 value_name='£mn')
    df = df.rename(columns={df.columns[0]: 'Year'})
    df['Type'] = df['Type'].str.strip()
    df['Year'] = pd.to_datetime(df['Year'], format='%Y')
    countries_to_keep = ['Europe + North Africa total',
                         'Australia+New Zealand',
                         'North America (USA+Canada)',
                         'Asia',
                         'West Indies',
                         'Turkey and Middle East']
    df = df[df['Region'].isin(countries_to_keep)]
    return df


def visualize_line(df, x_axis, y_axis, scale, widths):
    graph = alt.Chart(df).mark_line(strokeWidth=4).encode(
        x=x_axis+':T',
        y=alt.Y(y_axis+':Q', scale=scale),
        tooltip=[y_axis]
    ).properties(width=widths).interactive()
    st.write(graph)


def visualize_bar(df, widths):
    graph = alt.Chart(df).mark_bar().encode(
        x='Year:T',
        y=df.columns[-1]+':Q',
        color='Sector',
        tooltip=['Sector', df.columns[-1]]
    ).properties(width=widths).interactive()
    st.write(graph)


def visualize_line_facet(df):
    graph = alt.Chart(df).mark_line().encode(
        x='Year:T',
        y=alt.Y('£mn:Q', scale=alt.Scale(type='log', clamp=True)),
        color='Type',
        facet=alt.Facet('Region:O', columns=3),
    ).properties(
        width=175,
        height=150
    )
    st.write(graph)


if __name__ == "__main__":
    main()
