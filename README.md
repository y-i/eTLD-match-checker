# eTLD-match-checker

## Install

- `git clone git@github.com:y-i/eTLD-match-checker.git`
- `curl https://publicsuffix.org/list/public_suffix_list.dat | sed '/^$/d' | grep -v -- "//" > list.dat`

## Test
- `pipenv install`
- `pipenv run pytest`
