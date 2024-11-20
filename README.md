
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
uv pip install -r pyproject.toml
```



Running of the code(exemple):

```bash
uv run scripts/main.py
```


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
