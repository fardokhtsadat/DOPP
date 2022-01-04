# pd.set_option('display.max_rows', 500)
# pd.set_option('display.max_columns', 500)
# pd.set_option('display.max_rows', 10)
# pd.set_option('display.max_columns', 10)

# Import libraries
import pandas as pd
import numpy as np
import re


# Load data
transport_to_gdp = pd.read_csv("ModalTransportToGDP/tran_hv_pstra.tsv", sep='\s', engine='python', header=None, skipfooter=1)

# The last line of the file is corrupted, has to be loaded seperately
with open('ModalTransportToGDP/tran_hv_pstra.tsv') as f:
    for line in f:
        pass #iterate to the end
    last_line = line

last_line = re.split('\s', last_line)[:-1]

transport_to_gdp = pd.concat([transport_to_gdp, pd.DataFrame([last_line])], ignore_index=True, sort=False, axis=0)
transport_to_gdp = transport_to_gdp.drop(transport_to_gdp.index[0])

# Preprocess and extract indices as columns
unit_geo = transport_to_gdp[0].str.split(",", expand=True)


# Preprocess and assign column names
# NOTE: status variable stores the information of the data point status, i.e. is the data successfully retrieved (NaN), estimated (e), definition differs (d), not applicable (z), definition differs and estimated (de), or break in time series and estimated (be)
years = np.flip(np.arange(1990, 2020))
status = np.full((1, years.size), [str(year)+'_status' for year in years])
cols = np.empty((years.size + status.size, ), dtype=status.dtype)
cols[0::2] = years
cols[1::2] = status

# Stack the two data frames horizontally
transport_to_gdp_combined = pd.concat([unit_geo, transport_to_gdp.iloc[:,1:]], ignore_index=True, sort=False, axis=1)
transport_to_gdp_combined.columns = ['Unit', 'Location'] + cols.tolist()


# Treat missing/special values
# NOTE: If a status column contain NaNs, it actually means that there is no additional information to describe the data point, meaning that that data point is fine and can be used.
#       The NaNs are replaced with an 'ok' string, denoting that nothing is wrong with those values.
#       The actual missing values are stored as colons -> ':', will be replaced with NaNs.

#transport_to_gdp_combined.isna().any() #only status columns contain NaNs
# Replace NaNs in status column with 'ok', replace ':' with NaNs
transport_to_gdp_combined = transport_to_gdp_combined.fillna('ok').replace(':', np.nan)

#TODO: add a frequency table of the types of data there is per year per country (ok, estimated, not applicable, etc.)
transport_to_gdp_combined.to_csv("ModalTransportToGDP/GDP_all_countries_full_timeperiod_withmissingdata.csv", index=False)

# Check if there are countries/cities with no values at all.
all_rows_missing = transport_to_gdp_combined[[str(year) for year in years]].isnull().all(1)
all_rows_missing #does not affect any country

# Check for countries/cities that have at least one missing value, treat them individually.
some_rows_missing = transport_to_gdp_combined.isna().any(axis=1)

transport_to_gdp_combined[some_rows_missing] #Missing value amount varies on time and also country.

# Missing values per location, per unit
missing_years_per_location_per_unit = pd.concat([transport_to_gdp_combined[['Location', 'Unit']],
                                                 transport_to_gdp_combined.isnull().sum(axis=1)],
          axis=1).rename(columns={0:'Frequency_in_years'}).\
    sort_values(by=['Frequency_in_years', 'Location'], ascending=False)
missing_years_per_location_per_unit[missing_years_per_location_per_unit['Frequency_in_years']>0].to_csv("ModalTransportToGDP/GDP_missing_data_per_country_per_unit.csv")


# Missing values per unit, location, and year. Missing is 1 or 0.
missing_years = pd.concat([transport_to_gdp_combined[['Unit', 'Location']],
                           transport_to_gdp_combined[[str(year) for year in years]].isnull().astype(int)],
          axis=1)

missing_years_melted = missing_years.melt(['Unit', 'Location'], var_name="Year", value_name="Missing")

missing_years_melted[missing_years_melted['Missing']>0].to_csv("ModalTransportToGDP/GDP_Missing_data_perlocation_perunit_peryear.csv", index=False)


# Are there any countries that have missing values?
missing_per_year = missing_years_melted.groupby(['Location', 'Year']).sum()
# missing_per_year[(missing_per_year.Missing > 0)]
# missing_per_year[(missing_per_year.Missing == 0)]

missing_per_year.to_csv("ModalTransportToGDP/GDP_missing_data_per_location_per_year.csv")

# Extract countries that contain full data
locations_with_full_data = missing_per_year.groupby(['Location']).sum() == 0
locations_with_full_data = locations_with_full_data.index[locations_with_full_data['Missing']].to_list()


full_time_period = transport_to_gdp_combined[transport_to_gdp_combined['Location'].isin(locations_with_full_data)]
full_time_period.to_csv("ModalTransportToGDP/GDP_location_data_with_full_time_period.csv")


# Provide full dataset ready to be plotted
full_time_period[["Unit", "Location"]+[str(year) for year in years]].\
    melt(['Unit', 'Location'], var_name="Year", value_name="GDP").to_csv("ModalTransportToGDP/GDP_unit_location_year_gdp_full_time_period.csv", index=False)

transport_to_gdp_combined[["Unit", "Location"]+[str(year) for year in years]].\
    melt(['Unit', 'Location'], var_name="Year", value_name="GDP").to_csv("ModalTransportToGDP/GDP_unit_location_year_gdp_full_time_period_all_countries.csv", index=False)


