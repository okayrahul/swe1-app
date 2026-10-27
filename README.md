# Django Polls

[![Build Status](https://app.travis-ci.com/okayrahul/swe1-app.svg?branch=main)](https://app.travis-ci.com/github/okayrahul/swe1-app)
[![Coverage Status](https://coveralls.io/repos/github/okayrahul/swe1-app/badge.svg?branch=main)](https://coveralls.io/github/okayrahul/swe1-app?branch=main)

An individual Django polls application deployed to AWS Elastic Beanstalk.

## Assignment links

- [GitHub repository](https://github.com/okayrahul/swe1-app)
- [Travis CI dashboard](https://app.travis-ci.com/github/okayrahul/swe1-app)
- [Deployed polls application](http://rahul-swe1-app-env.eba-2syr3zrb.us-east-1.elasticbeanstalk.com/polls/)
- [Coveralls report](https://coveralls.io/github/okayrahul/swe1-app?branch=main)

## Run locally

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000/polls/.

## Run the CI checks locally

```powershell
python -m black --check .
python -m flake8 .
python manage.py check
python manage.py makemigrations --check --dry-run
python -m coverage run manage.py test --noinput
python -m coverage report
```

Use `python -m black .` to fix formatting before committing. Flake8 uses an
88-character line limit. The application wrapper intentionally re-exports
`application`, so only that file's F401 warning is excluded.

## Continuous integration and deployment

Travis CI runs formatting, lint, Django checks, and tests for GitHub pushes and
pull requests when this repository is enabled in Travis. Coverage.py measures
the tests, and Coveralls receives the report after the checks pass.

A successful push build on `main` deploys through Travis's Elastic Beanstalk
provider. Pull request builds and other branches do not deploy. Deployment waits
for AWS to finish updating the existing environment.

See [CI account setup](docs/CI_SETUP.md) for the required service connections,
deployment secrets, branch protection, and verification steps.
