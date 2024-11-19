pdf_filepath = "../data/bilan-social.pdf"

###################################################################################
################################# CAMELOT #########################################
###################################################################################
# import camelot

# tables = camelot.read_pdf(pdf_filepath, pages="all", flavor="lattice")
# for i, table in enumerate(tables):
#     table.to_csv(f"table_{i}.csv")

###################################################################################
################################# LLAMA_PARSE #####################################
###################################################################################
import os
from dotenv import load_dotenv

import logging
import uuid

# External imports
import nest_asyncio
import pandas as pd
from llama_parse import LlamaParse

# Load environment variables from .env
load_dotenv()

# Get the API key
api_key = os.getenv("LLAMA_CLOUD_API_KEY")

if not api_key:
    raise ValueError("API_KEY not found in environment variables.")

# Standard imports

json_objs = LlamaParse().get_json_result(pdf_filepath)

tables = []
for page in json_objs[0]["pages"]:
    for item in page["items"]:
        if item["type"] == "table":
            # If the number of columns in the header row is greater than the data rows
            header_length = len(item["rows"][0])

            for i in range(1, len(item["rows"])):
                while len(item["rows"][i]) < header_length:
                    item["rows"][i].append("No Extract ")
                while len(item["rows"][i]) > header_length:
                    item["rows"][0].append("No Extract ")
                    header_length = len(item["rows"][0])

            df = pd.DataFrame(item["rows"][1:], columns=item["rows"][0])
            tables.append(df)
for i, table in enumerate(tables):
    table.to_csv(f"table_{i}.csv")



###################################################################################
################################## TABULA #########################################
###################################################################################
# from tabula import read_pdf

# df = read_pdf(pdf_filepath, pages="all")
# print(df)