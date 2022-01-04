# pd.set_option('display.max_rows', 500)
# pd.set_option('display.max_columns', 500)
# pd.set_option('display.max_rows', 10)
# pd.set_option('display.max_columns', 10)

# Import libraries
import pandas as pd
import numpy as np

# Load data
modal_split = pd.read_csv("ModalSplit/tran_hv_psmod.tsv", sep='\s', engine='python', header=None)

# Preprocess and assign column names
# NOTE: status variable stores the information of the data point status, i.e. is the data successfully retrieved (NaN), estimated (e), definition differs (d), not applicable (z), definition differs and estimated (de), or break in time series and estimated (be)
years = np.flip(np.arange(1990, 2020))
status = np.full((1, years.size), [str(year)+'_status' for year in years])
cols = np.empty((years.size + status.size, ), dtype=status.dtype)
cols[0::2] = years
cols[1::2] = status
modal_split.columns = cols
modal_split = modal_split.drop(modal_split.index[0])

# Preprocess and extract indices as columns
modal_split = modal_split.rename(index={'unit,vehicle,geo\\time':'unit,vehicle,geo'})
rows = modal_split.index.str.split(",", expand=True).to_frame(index=False)
modal_split = modal_split.reset_index(drop=True)

# Stack the two data frames horizontally
modal_split_combined = pd.concat([rows, modal_split], ignore_index=True, sort=False, axis=1)
modal_split_combined.columns = ['Percentage', 'VehicleType', 'Country'] + modal_split.columns.to_list()

# Treat missing/special values
# NOTE: If a status column contain NaNs, it actually means that there is no additional information to describe the data point, meaning that that data point is fine and can be used.
#       The NaNs are replaced with an 'ok' string, denoting that nothing is wrong with those values.
#       The actual missing values are stored as colons -> ':', will be replaced with NaNs.

#modal_split_combined.isna().any() #only status columns contain NaNs
# Replace NaNs in status column with 'ok', replace ':' with NaNs
modal_split_combined = modal_split_combined.fillna('ok').replace(':', np.nan)

#TODO: add a frequency table of the types of data there is per year per country (ok, estimated, not applicable, etc.)
modal_split_combined.to_csv("ModalSplit/MODSPLIT_all_countries_full_timeperiod_withmissingdata.csv", index=False)

# Check if there are countries/cities with no values at all, remove those rows.
all_rows_missing = modal_split_combined[[str(year) for year in years]].isnull().all(1)

# Countries with no train data
modal_split_combined[all_rows_missing].to_csv("ModalSplit/MODSPLIT_countries_with_no_trains.csv", index=False)

#modal_split_combined.iloc[modal_split_combined.index[all_rows_missing].values] #Iceland, Cyprus, and Malta don't have any data for trains as it is not applicable there..
modal_split_combined = modal_split_combined.drop(modal_split_combined.index[all_rows_missing])

# Check for countries/cities that have at least one missing value, treat them individually.
some_rows_missing = modal_split_combined.isna().any(axis=1)

modal_split_combined[some_rows_missing] #Missing value amount varies on time and also country.

# Missing values per country, per vehicle type
missing_years_per_country_per_vehicletype = pd.concat([modal_split_combined[['Country', 'VehicleType']],
           modal_split_combined.isnull().sum(axis=1)],
          axis=1).rename(columns={0:'Frequency_in_years'}).\
    sort_values(by=['Frequency_in_years', 'Country'], ascending=False)
missing_years_per_country_per_vehicletype[missing_years_per_country_per_vehicletype['Frequency_in_years']>0].to_csv("ModalSplit/MODSPLIT_missing_data_per_country_per_vehicletype.csv")


# Missing values per vehicle type, country, and year. Missing is 1 or 0.
missing_years = pd.concat([modal_split_combined[['VehicleType', 'Country']],
           modal_split_combined[[str(year) for year in years]].isnull().astype(int)],
          axis=1)

missing_years_melted = missing_years.melt(['VehicleType', 'Country'], var_name="Year", value_name="Missing")

missing_years_melted[missing_years_melted['Missing']>0].to_csv("ModalSplit/MODSPLIT_missing_data_percountry_pervehicletype_peryear.csv", index=False)


# Are there any countries that have missing values only for certain vehicle types? I.e. is any frequency country per year lower than 4 but larger 0?
missing_per_year = missing_years_melted.groupby(['Country', 'Year']).sum()
# missing_per_year[(missing_per_year.Missing > 0) & (missing_per_year.Missing < 5)]
# missing_per_year[(missing_per_year.Missing > 4)]
# missing_per_year[(missing_per_year.Missing == 0)]

missing_per_year.to_csv("ModalSplit/MODSPLIT_missing_data_per_country_per_year.csv")

# Extract countries that contain full data
countries_with_full_data = missing_per_year.groupby(['Country']).sum() == 0
countries_with_full_data = countries_with_full_data.index[countries_with_full_data['Missing']].to_list()


full_time_period = modal_split_combined[modal_split_combined['Country'].isin(countries_with_full_data)]
full_time_period.to_csv("ModalSplit/MODSPLIT_country_data_with_full_time_period.csv")



# Provide full dataset ready to be plotted
full_time_period[["VehicleType", "Country"]+[str(year) for year in years]].\
    melt(['VehicleType', 'Country'], var_name="Year", value_name="Percentage").to_csv("ModalSplit/MODSPLIT_vehicletype_country_year_percentage_full_time_period_all_countries.csv", index=False)


modal_split_combined[["VehicleType", "Country"]+[str(year) for year in years]].\
    melt(['VehicleType', 'Country'], var_name="Year", value_name="Percentage").to_csv("ModalSplit/MODSPLIT_vehicletype_country_year_percentage_full_time_period_all_countries.csv", index=False)





