# Splight Push Components

Automatically find and publish all components in your repository.

## Description

This action will find the Splight Component configuration file ("spec.json") present in your repository, and push the component using the [Splight CLI](https://pypi.org/project/splight-cli/).

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
        splight_access_id: ${{ secrets.MY_SECRET_ACCESS_ID }} # Your credentials as action secrets
        splight_secret_key: ${{ secrets.MY_SECRET_KEY }}
```

## Development
```bash
pip install pre-commit
pre-commit install-hooks
```

