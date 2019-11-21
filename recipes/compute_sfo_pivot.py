# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Import the class that allows us to execute SQL on the Studio connections
from dataiku.core.sql import SQLExecutor2

# Get a handle on the input dataset
sfo_prepared = dataiku.Dataset("sfo_prepared")

# We create an executor. We pass to it the dataset instance. This way, the
# executor  knows which SQL database should be targeted
executor = SQLExecutor2(dataset=sfo_prepared)

# Get the 5 most frequent manufacturers by total landing count
# (over the whole period)
mf_manufacturers = executor.query_to_df(
    """
    select      "Aircraft Manufacturer" as manufacturer,
                sum("Landing Count") as count
            from "sfo_prepared"
            group by "Aircraft Manufacturer"
            order by count desc limit 5
    """)

# The "query_to_df" method returns a Pandas dataframe that
# contains the manufacturers


print mf_manufacturers

output_dataset = dataiku.Dataset("sfo_pivot")
output_dataset.write_with_schema(mf_manufacturers)
