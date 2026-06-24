---
# Canonical repo classification — see docs/REPO-CLASSIFICATION.md.
# This front-matter is the source of truth; GitHub topics mirror from it.
content: code
domain: dev-tooling
exposure: developer
lifecycle: inactive
---

# sonetel-python

> A simple Python wrapper / SDK for using Sonetel's REST APIs.

## What it contains
The official `sonetel` Python SDK (published to PyPI, docs on Read the Docs) wrapping Sonetel's REST API. The `sonetel/` package exposes modules for auth/token management (`auth.py`), account (`account.py`), calls/callback (`calls.py`), phone numbers (`phonenumber.py`), recordings (`recording.py`), users (`users.py`) and voice apps (`voiceapps.py`), with packaging via `setup.py`/`pyproject.toml`, MkDocs how-to/reference docs, and a `tests/` suite.

## Ownership
- **Code owner:** Aashish Joshi (aashish-joshi)

## Notes
Keep — Python SDK customers use to work with the Sonetel API (confirmed 2026-06-09).
