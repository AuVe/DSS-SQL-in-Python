# -*- coding: utf-8 -*-
import dataiku
import pandas as pd, numpy as np
from dataiku import pandasutils as pdu

# Import the class that allows us to execute SQL on the Studio connections
from dataiku.core.sql import SQLExecutor2

# Read recipe inputs
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
            from sfo_prepared
            group by "Aircraft Manufacturer"
            order by count desc limit 5
    """)

# The "query_to_df" method returns a Pandas dataframe that
# contains the manufacturers

cases = []

for (row_index, manufacturer, count) in mf_manufacturers.itertuples():
    cases.append(
    """SUM (case when "Aircraft Manufacturer" = '%s'
            then "Total Landed Weight" else 0 end)
        as "weight_%s"
        """ % (manufacturer, manufacturer))
    
final_query = """select "Activity Period", "Operating Airline",
        COUNT(*) as airline_count, %s
        from sfo_prepared
        group by "Activity Period", "Operating Airline"
        """ % (",".join(cases))

print final_query

result = executor.query_to_df(final_query)

output_dataset = dataiku.Dataset("sfo_pivot")
output_dataset.write_with_schema(result)