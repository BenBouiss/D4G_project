# Standard imports
import logging
import uuid

# External imports
import nest_asyncio
import pandas as pd
from llama_parse import LlamaParse

import os
from dotenv import load_dotenv

class LlamaParseExtractor:
    def __init__(self, **kwargs: dict) -> None:
        """
        Builds a pdf page parser, looking for tables using
        the llama_parse library.
        The kwargs given to the constructor are directly propagated
        to the LlamaParse constructor.
        You are free to define any parameter LlamaParse recognizes
        """
        self.kwargs = kwargs
        self.type = "llama_parse"

        # Load environment variables from .env
        load_dotenv()
        # Get the API key
        api_key = os.getenv("LLAMA_CLOUD_API_KEY")
        if not api_key:
            raise ValueError("API_KEY not found in environment variables.")
        
        # llama-parse is async-first
        nest_asyncio.apply()

    def __call__(self, pdf_filepath: str) -> dict:
        logging.info("\nKicking off extraction stage...")
        logging.info(f"Extraction type: {self.type}, with params: {self.kwargs}")

        json_objs = LlamaParse(**self.kwargs).get_json_result(pdf_filepath)

        tables_list = []
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
                    tables_list.append(df)
        return tables_list