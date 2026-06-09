# TODO - Framework hardening validation

- [ ] Add missing Django deployment hardening settings in ihatetobudget/settings.py:
  - SECURE_HSTS_SECONDS
  - SECURE_SSL_REDIRECT
  - SESSION_COOKIE_SECURE
  - CSRF_COOKIE_SECURE
  - Ensure DEBUG is not enabled for deployment checks
  - Ensure SECRET_KEY is strong when checking deploy (or avoid using insecure dev secret)
- [ ] Rerun: `pipenv run python manage.py check --deploy` and confirm it reports: `System check identified no issues (0 silenced).`

