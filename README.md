# Splight Push Components

Automatically find all components in your repository and update them.

## Description

This action will look up all the Splight Components configuration files ("spec.json") present in your repository, and push each component using the [Splight CLI](https://pypi.org/project/splight-cli/).

## Usage

```yml
name: Example usage
on:
  push:
    branches:
      - mybranch
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - uses: splightcomponents/splight-push-component@master # Or any other branch/tag
      with:
        splight_access_id: ${{ secrets.MY_SECRET_ACCESS_ID }}
        splight_secret_key: ${{ secrets.MY_SECRET_KEY }}
```

## Development
```bash
pip install pre-commit
pre-commit install-hooks
```

