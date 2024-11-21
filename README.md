
This project uses UV as its python dependency manager(see: https://github.com/astral-sh/uv)

Quick installation of UV:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
or
pip install uv
```
And restart the console afterward


Installation of the python dependencies
```bash
uv venv

uv pip install -r pyproject.toml
```



Running of the code(exemple):

```bash
uv run src/main.py
```

------------------------
Launching the posgressql DB from the docker-compose.yaml


```bash
sudo docker compose up
```

Initialising the DB with the data present in the data folder

```bash
uv run src/db/init_database.py
```

------------------------

Using the Streamlit dashbord

```bash
streamlit run src/data_viz/dashbord_skript.py
```

**_NOTE:_**: this requires the UV environnement to be activated to do so run


```bash
source activate .venv/bin/activate
```

The postgresql database must also be running in order for the streamlit dashboard to work


------------------------

Using superset

Superset requires node version >= 16.20 

```bash
sudo apt install nodejs
```

Clone the superset git repo outside of this repo

```bash
git clone --depth=1 https://github.com/apache/superset.git
```

Then launch the superset instance by moving to the created repo building the docker compose

```bash
sudo docker compose -f docker-compose-image-tag.yml up
```

Default address and ports: http://127.0.0.1:8088
With Username and password both = "admin"

------------------------

Project structure

```md
data
└── Folder containing csv used by src.db and pdf files to be used by src.data_extractor

src
├── data_extractor
│   └── Include scripts to extract tables from a given pdf file
│     
├── data_viz
│   └── Frontend scripts utilizing streamlit to display database information to the user
│ 
└── db
    └── Contains script to initialize the database and add informations to it
```

    


