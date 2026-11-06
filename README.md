# NYC restaurant inspections

An exploratory pandas analysis of the included historical NYC restaurant
inspection extract. `Restaurants Project.ipynb` explores chains, cuisine,
boroughs and violation descriptions. `inspection_summary.py` provides a
reproducible, lightweight command-line summary.

## Run the summary

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python inspection_summary.py
python inspection_summary.py NYC_Restaurants.csv --borough Brooklyn --top 10
python -m unittest discover -s tests -v
```

The script reads a CSV without modifying it and prints JSON, including record
count, distinct CAMIS identifiers, inspection date range, missing-data counts,
and the most common violation descriptions by **row**. Borough filtering is
case-insensitive. An unknown borough is an error. This repository does not
contain an Excel data source.

The notebook now reads the included CSV locally; it additionally requires
Jupyter and plotting dependencies. It is the original exploratory analysis,
not the same algorithm as the CLI: in particular, it constructs a name/address
key for restaurants, whereas the CLI counts CAMIS identifiers.

## Interpretation

The extract covers inspections from November 2014 through January 2015, not
current restaurant conditions. Rows can represent multiple violations for a
single inspection; row counts are not counts of restaurants or inspections.
Violation frequency is not an adjusted risk measure, and comparisons can be
affected by inspection frequency, missing records, and data definitions.
