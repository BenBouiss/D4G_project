# pdf_filepath = "../data/bilan-social.pdf.md"
import pathlib
pdf_filepath = pathlib.Path("../data/bilan-social.pdf")
###################################################################################
################################# CAMELOT #########################################
###################################################################################
# import camelot

# tables = camelot.read_pdf(pdf_filepath, pages="all", flavor="lattice")
# for i, table in enumerate(tables):
#     table.to_csv(f"table_{i}.csv")


import pandas as pd
from io import StringIO
import unstructured
from unstructured.partition.pdf import partition_pdf

class Unstructured:

    def __init__(self, **kwargs: dict) -> dict:
        self.kwargs = kwargs


    def __call__(self, pdf_filepath: str) -> list:    
        elements = partition_pdf(
            pdf_filepath,
            infer_table_structure=True,
            strategy="hi_res",
            **self.kwargs
        )
        tables_list = [el for el in elements if isinstance(el, unstructured.documents.elements.Table) ] # el.category == "Table"
        tables_list = [
            pd.read_html(StringIO(t.metadata.text_as_html))[0] for t in tables_list
        ]

        return tables_list
