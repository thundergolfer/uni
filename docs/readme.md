## Docs

You can get a basic webserver to serve these static files by doing:

```
cd "$(git rev-parse --show-toplevel)/docs"
python3 -m http.server
```
