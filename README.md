
This project uses UV as its python dependency manager(see: https://github.com/astral-sh/uv)

Quick installation of UV:

bash```
curl -LsSf https://astral.sh/uv/install.sh | sh
or
pip install uv
```
And restart the console afterward


Installation of the python dependencies
bash```
uv pip install -r pyproject.toml
```



Running of the code(exemple):

bash```
uv run scripts/main.py
```
