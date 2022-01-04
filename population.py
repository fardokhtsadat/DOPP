# pd.set_option('display.max_rows', 500)
# pd.set_option('display.max_columns', 500)
# pd.set_option('display.max_rows', 10)
# pd.set_option('display.max_columns', 10)

# Import libraries
import pandas as pd
import numpy as np
import re

### Loop the data lines
with open("Population/tgs00096.tsv", 'r') as temp_f:
    # get No of columns in each line
    col_count = [ len(re.split('\s', l)) for l in temp_f.readlines() ]

### Generate column names  (names will be 0, 1, 2, ..., maximum columns - 1)
column_names = [i for i in range(0, max(col_count) - 1)]

# Load data
population = pd.read_csv("Population/tgs00096.tsv", sep='\s', engine='python', header=None, names=column_names)
population = population.drop(population.index[0])

# Preprocess and extract indices as columns
unit_geo = population[0].str.split(",", expand=True)
# Remove third and fourth letter from country information, so it could be connected with other country codes
unit_geo.iloc[:,3] = unit_geo.iloc[:,3].str[:2]


# Preprocess and assign column names
# NOTE: status variable stores the information of the data point status, i.e. is the data successfully retrieved (NaN), estimated (e), definition differs (d), not applicable (z), definition differs and estimated (de), or break in time series and estimated (be)
years = np.flip(np.arange(2009, 2021))
status = np.full((1, years.size), [str(year)+'_status' for year in years])
cols = np.empty((years.size + status.size, ), dtype=status.dtype)
cols[0::2] = years
cols[1::2] = status

# Stack the two data frames horizontally
population_combined = pd.concat([unit_geo, population.iloc[:,1:]], ignore_index=True, sort=False, axis=1)
population_combined.columns = ['Unit', 'Age', 'Sex', 'Location'] + cols.tolist()


# Treat missing/special values
# NOTE: If a status column contain NaNs, it actually means that there is no additional information to describe the data point, meaning that that data point is fine and can be used.
#       The NaNs are replaced with an 'ok' string, denoting that nothing is wrong with those values.
#       The actual missing values are stored as colons -> ':', will be replaced with NaNs.

#population_combined.isna().any() #only status columns contain NaNs
# Replace NaNs in status column with 'ok', replace ':' with NaNs
population_combined = population_combined.fillna('ok').replace(':', np.nan)

#TODO: add a frequency table of the types of data there is per year per country (ok, estimated, not applicable, etc.)
population_combined.to_csv("Population/POP_all_countries_full_timeperiod_withmissingdata.csv", index=False)

# Check if there are countries/cities with no values at all.
all_rows_missing = population_combined[[str(year) for year in years]].isnull().all(1)
all_rows_missing #does not affect any country

# Check for countries/cities that have at least one missing value, treat them individually.
some_rows_missing = population_combined.isna().any(axis=1)

population_combined[some_rows_missing] #Missing value amount varies on time and also country.

# Missing values per location, per unit
missing_years_per_location_per_unit = pd.concat([population_combined[['Location', 'Unit']],
                                                 population_combined.isnull().sum(axis=1)],
          axis=1).rename(columns={0:'Frequency_in_years'}).\
    sort_values(by=['Frequency_in_years', 'Location'], ascending=False)
missing_years_per_location_per_unit[missing_years_per_location_per_unit['Frequency_in_years']>0].to_csv("Population/POP_missing_data_per_country_per_unit.csv")


# Missing values per unit, location, and year. Missing is 1 or 0.
missing_years = pd.concat([population_combined[['Unit', 'Location']],
                           population_combined[[str(year) for year in years]].isnull().astype(int)],
          axis=1)

missing_years_melted = missing_years.melt(['Unit', 'Location'], var_name="Year", value_name="Missing")

missing_years_melted[missing_years_melted['Missing']>0].to_csv("Population/POP_Missing_data_perlocation_perunit_peryear.csv", index=False)


# Are there any countries that have missing values?
missing_per_year = missing_years_melted.groupby(['Location', 'Year']).sum()
# missing_per_year[(missing_per_year.Missing > 0)]
# missing_per_year[(missing_per_year.Missing == 0)]

missing_per_year.to_csv("Population/POP_missing_data_per_location_per_year.csv")

# Extract countries that contain full data
locations_with_full_data = missing_per_year.groupby(['Location']).sum() == 0
locations_with_full_data = locations_with_full_data.index[locations_with_full_data['Missing']].to_list()


full_time_period = population_combined[population_combined['Location'].isin(locations_with_full_data)]
full_time_period.to_csv("Population/POP_location_data_with_full_time_period.csv")


# Provide full dataset ready to be plotted
full_time_period[["Unit", "Location"]+[str(year) for year in years]].\
    melt(['Unit', 'Location'], var_name="Year", value_name="Count").to_csv("Population/POP_unit_location_year_POP_full_time_period.csv", index=False)

population_combined[["Unit", "Location"]+[str(year) for year in years]].\
    melt(['Unit', 'Location'], var_name="Year", value_name="Count").to_csv("Population/POP_unit_location_year_POP_full_time_period_all_countries.csv", index=False)


