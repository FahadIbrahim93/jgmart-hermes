## Getting Started — Local Development

Prerequisites
- Python 3.11+
- Git

Create a virtual environment and install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the validation toolkit (generates `VALIDATION_REPORT.txt`)

```bash
python tests/validate_toolkit.py
```

Run tests

```bash
pytest -q
```

Run the static frontend locally (simple HTTP server)

```bash
cd src/web
python -m http.server 8000
# open http://localhost:8000 in your browser
```

Supabase setup (admin panel)
1. Create a Supabase project.
2. Run `src/web/supabase/schema.sql` and `src/web/supabase/seed.sql` in the Supabase SQL editor.
3. Update `src/web/supabase/config.js` with your Supabase URL and anon key.

See `README.md` and `docs/MASTER_INDEX.md` for full project documentation.
