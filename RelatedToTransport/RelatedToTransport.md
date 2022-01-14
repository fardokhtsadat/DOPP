### Overview

This note provides a summary on the second round of preprocessing steps that were taken. 

After the second meeting, we concluded that: 
1. More data is needed to analyze potential relationships
2. The datasets have to be joined together, so they can be compared. 

Those two points are now covered with the second round of preprocessing. Mainly, a new folder "RelatedToTransport" was created, which keeps EUROSTATS datasets with the respective preprocessed CSV file. The approach now is that instead of keeping one dataset for every folder, we try to group the dataset according to a "topic", like in this case "RelatedToTransport". Related to transport means that it contains all datasets that can be taken from EUROSTATS that could benefit our analysis in regard to Transportation in any way. The goal is then to create other folders that will cover different topics, such as demographic related datasets, or environmental related datasets, and so on. 

### What files to focus on

Beside this Markdown file, you only need to focus on the .CSV and .TSV files. The .TSV files are the original datasets. The filenames correspond to the topic that can be found when downloading the dataset from EUROSTAT. We moved away from keeping the original filename (e.g. "sdg_200_21.tsv"), because it is harder to understand for what that dataset is really used. Instead, we use the dataset-title from EUROSTAT to provide a better overview of the data (e.g. "Co2Emissions.tsv").

If you want to seperately load and analyze each of the datasets, simply load the .CSV file. If you would like to study the combined datasets, you can find it in "All_data_outer_join_by_country_and_year.csv" and "All_data_inner_join_by_country_and_year.csv". Note that an outer join was used to join the data, meaning that there will be entries with NaNs, but it will contain all of the original processed datapoints. If you would like to work with the smallest subset / the intersection of all datasets, you can use the dataset joined using the inner join. 

### Regarding the CSV file structure of the combined datasets

As long as we want to distinguish among different datasets, the column names of each dataset have a prefix attached to it. This is important, because several datasets have a column named "Unit", and were renamed to e.g. "ModalSplit_Unit", etc. to avoid duplicate column names. 

### Regarding the processing script

The preprocessing script was adjusted now to cover the aspects we discussed in the second meeting. There is only a single script "related_to_transport.py", which can be executed using:

```bash
python3 related_to_transport.py --path_to_config related_to_transport.json
```

The ```related_to_transport.json``` is a configuration file that stores all configurations for every dataset. Like this, we were able to generalize the preprocessing steps into single functions, instead of having one script per dataset. **This script replaces the older preprocessing scripts.**

### The outline of the pre-processing at the moment

The new pre-processing pipeline loads the configuration from the JSON file, and executes the pipeline for every dataset. Depending on each dataset then, the preprocessing will e.g. process grouping variables, melt/pivot some of the columns, remove missing values, etc. 

 

