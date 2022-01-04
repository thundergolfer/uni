---
---
## Spam / A plan for spam, web UI

### Run

```
cd "$(git rev-parse --show-toplevel)/machine_learning/applications/spam/a_plan_for_spam/web/public"
python3 -m http.server
```

Then navigate to http://localhost:8000

Note that webserver is needed to be run on localhost to avoid CORS issues loading the Javascript.
