# eTLD-match-checker

![cheker badge](https://github.com/y-i/eTLD-match-checker/actions/workflows/checker.yml/badge.svg)
[![Auto deploy to vercel](https://github.com/y-i/eTLD-match-checker/actions/workflows/deploy.yml/badge.svg)](https://github.com/y-i/eTLD-match-checker/actions/workflows/deploy.yml)

## Set up

- `git clone git@github.com:y-i/eTLD-match-checker.git`
- `curl https://publicsuffix.org/list/public_suffix_list.dat | sed '/^$/d' | grep -v -- "//" > files/list.dat`
- `pipenv install --dev`

## How to use
- `pipenv run server`
- Go to http://localhost:8000/

## Document
- [OpenAPI](http://localhost:8000/docs)
- [ReDoc](http://localhost:8000/redoc)

## Test
- `pipenv run pytest`

## Implemented
- [x] null input
- [x] Mixed case
- [x] Leading dot
- [ ] Unlisted TLD
- [ ] Listed, but non-Internet, TLD
- [x] TLD with only 1 rule
- [x] TLD with some 2-level rules
- [x] TLD with only 1 (wildcard) rule
- [x] More complex TLD
- [x] TLD with a wildcard rule and exceptions
- [x] US K12
- [x] IDN labels
- [ ] Same as above, but punycoded
