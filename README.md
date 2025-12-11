# PortTracker

PortTracker is a containerized web application that helps users track their stock holdings.

This repository contains:

- A Flask backend (`backend/`)
- SQLite database integration (`portfolio.db` at runtime)
- Alpha Vantage API integration for live stock prices
- Docker support (`Dockerfile`, `docker-compose.yml`)
- Project documentation in LaTeX under `docs/`

## User Manual (LaTeX)

The full README / User Manual for this project is written in LaTeX:

- `docs/README_UserManual.tex`

Please compile it with `pdflatex` to generate the PDF version, or view the source directly in the repo.

Jira project for this application:

https://calstatela-cs3338-fall-2025.atlassian.net/jira/software/projects/POR/boards/67

## Run Instructions (Quick View)

```bash
git clone https://github.com/Woestee/porttracker.git
cd porttracker

# create a .env file in the project root:
# FLASK_SECRET_KEY=dev-secret
# FLASK_APP=app.py
# FLASK_RUN_HOST=0.0.0.0
# PORT=5000
# ALPHA_VANTAGE_API_KEY=YOUR_ALPHA_VANTAGE_KEY_HERE

docker-compose up

Then open: http://localhost:5000
