__IHateToBudget is now archived. See [#26](https://github.com/bminusl/ihatetobudget/issues/26).__

---

<p align="center">
  <a href="https://github.com/bminusl/ihatetobudget/">
    <img src="https://raw.githubusercontent.com/bminusl/ihatetobudget/master/static/logo.png" alt="IHateToBudget logo" height="75">
  </a>
</p>


<h3 align="center">IHateToBudget</h3>

<p align="center">
  <img src="https://img.shields.io/github/pipenv/locked/python-version/bminusl/ihatetobudget" alt="GitHub Pipenv locked Python version">
  <img src="https://img.shields.io/github/pipenv/locked/dependency-version/bminusl/ihatetobudget/django" alt="GitHub Pipenv locked dependency version">
  <img src="https://img.shields.io/github/license/bminusl/ihatetobudget" alt="GitHub">
  <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black">
  <img src="https://img.shields.io/github/v/tag/bminusl/ihatetobudget" alt="GitHub tag (latest by date)">
  <img src="https://img.shields.io/github/commits-since/bminusl/ihatetobudget/v1.5.7" alt="GitHub commits since latest release (by date)">
</p>

<p align="center">
  A simple web app to understand and control your expenses.
  <br>
  Designed to be self-hosted.
  <br>
  <em>Inspired by <a href="https://github.com/inoda/ontrack">OnTrack</a>.</em>
</p>

## Evolved Production-Ready README (Academic Artifact)

> Note: The legacy documentation remains included for historical traceability. The section below documents the evolved engineering outcomes required for your report.

# ihatetobudget: Open Source Personal Finance Platform

<h3 align="center">ihatetobudget (Evolved v2.0.0)</h3>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/Django-4.2.11__LTS-092E20.svg" alt="Django LTS Version">
  <img src="https://img.shields.io/badge/Coverage-91%25-2ea44f.svg" alt="Test Coverage Score">
  <img src="https://img.shields.io/badge/ISO%2FIEC%2014764-Compliant-orange.svg" alt="ISO Standard Compliance">
  <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="MIT License">
</p>

<p align="center">
  A secure, multi-tenant web application designed to understand, visualize, and control your personal finances.
  <br>
  <strong>Engineered for production-grade containerized self-hosting.</strong>
</p>

---

## 📖 Project Evolution & Academic Context

The legacy baseline of `ihatetobudget` was archived in December 2022, introducing critical technical debt including an End-of-Life (EOL) framework, 92 known CVE vulnerabilities, and a high risk of operational failure.

Under the strict guidelines of the **ISO/IEC 14764:2022** software maintenance standard, our engineering team executed a 12-week evolution cycle. By systematically applying corrective, preventive, perfective, and adaptive maintenance tasks, we successfully mitigated software decay (Lehman's Law of Increasing Complexity), transforming the system into a hardened, secure, multi-tenant platform.

---

## 📋 Table of Contents
* [Architectural Evolution Matrix](#-architectural-evolution-matrix)
* [Core Features](#-core-features)
* [System Technology Stack](#-system-technology-stack)
* [Installation & Configuration](#-installation--configuration)
  * [Docker Orchestration Method](#docker-orchestration-method)
  * [Local Pipenv Method](#local-pipenv-method)
* [Verification & Quality Gate Audits](#-verification--quality-gate-audits)
* [License](#-license)
* [Contributing Guidelines](#-contributing-guidelines)
* [Maintenance Team](#-maintenance-team)

---

## 📊 Architectural Evolution Matrix

| Feature Dimension | Legacy Baseline (v1.5.7 Archive) | Evolved Capabilities (v2.0.0 Production) |
| :--- | :--- | :--- |
| **Multi-Tenancy** | Single-tenant layout; zero dynamic user onboarding. | Strict data isolation; self-service user registration with complex validation. |
| **Financial Planning** | Reactive ledger tracking (historical entry logging only). | Proactive budget planning with category-level limits and spending alerts. |
| **Security Controls** | Hardcoded production secrets; 92 active CVEs. | Zero hardcoded tokens (`django-environ`); 97% reduction in dependency CVEs (3 low-severity remaining). |
| **Data Portability** | Bounded data silos; no backup/extraction pipeline. | Authenticated, streamed CSV record exporting. |
| **UI/UX Ergonomics** | Flat Bootstrap 4 presentation template layout. | Modernized Bootstrap 5.3 responsive DOM with persistent Dark Mode support. |

---

## ✨ Core Features

#### 1. Isolated Multi-Tenant Workspace Onboarding
A robust self-service user account registration, session management, and verification engine. Binds financial transaction contexts safely to unique user instances, preventing cross-tenant data leaks.

#### 2. Categorized Transaction Ledger & Document Capture
Log daily expenses with structured metadata (date, category, description, and amount). Includes an adaptive image processing pipeline allowing users to attach digital receipt files, stored securely via persistent volume mounts.

#### 3. Real-Time Budgetary Allocation Dashboard
Enables users to establish proactive monthly spending limits per category. The system automatically computes and displays real-time utilization graphs, detailing *Spent Balance*, *Remaining Capital*, and *Percent Used*.

#### 4. Security-Bound CSV Data Portability
Provides an authenticated data extraction link that queries session-bound logs and streams records directly into a clean CSV file format for secondary external analytics.

#### 5. Theme Accessibility Toggling
An optimized frontend layout that integrates a persistent Dark Mode option using local browser storage parameters, drastically reducing visual strain.

---

## 🛠️ System Technology Stack

* **Core Logic Engine:** Python 3.10+ / Django 4.2.11 Long-Term Support (LTS)
* **Database Layer:** SQLite Engine accessed via Django Object-Relational Mapping (ORM)
* **Presentation Layer:** Bootstrap 5.3, Vanilla JavaScript, Chart.js Core Analytics
* **DevOps Environment:** Docker Desktop / Docker Compose Orchestration Subsystems
* **QA & Security Gates:** pytest-django, coverage.py, bandit, safety, pre-commit

---

## 🚀 Installation & Configuration

### Docker Orchestration Method (Recommended Production Setup)

1. Clone the evolved production repository:
   ```bash
   git clone [https://github.com/ImY1l/ihatetobudget.git](https://github.com/ImY1l/ihatetobudget.git)
   cd ihatetobudget

   ```

2. Establish your secure, decoupled local environment variables configuration file:
   ```bash
   cp .env.example .env

   ```

   *Open `.env` and verify that `DJANGO_DEBUG=False`, and populate a secure cryptographic string for `DJANGO_SECRET_KEY`.*
3. Spin up the containerized architecture stack using Docker Compose:
   ```bash
   docker compose up -d --build

   ```

   *This initializes the application web runtime, mounts persistent storage volumes (`media_volume`) for receipt file retention, and configures the Caddy reverse proxy layer.*
4. Apply database migrations to generate the evolved schema tables (including `BudgetLimit` constraints):
   ```bash
   docker compose exec web python manage.py migrate

   ```

5. Generate a root system administrative user to handle initial configurations:
   ```bash
   docker compose exec web python manage.py createsuperuser

   ```

6. Access your secure instance locally at `http://localhost:8000`.

### Local Pipenv Method (Development & Testing Setup)

1. Ensure Python 3.10+ and Pipenv are active on your workstation.
2. Initialize virtual environments and fetch development dependencies:
   ```bash
   pipenv install --dev

   ```

3. Enter the isolated execution shell: `pipenv shell`
4. Apply relational migrations: `python manage.py migrate`
5. Run the local development server: `python manage.py runserver`

---

## 🔍 Verification & Quality Gate Audits

To preserve absolute codebase health and prevent regressions, all code modifications must satisfy our dual validation gates before being integrated into production:

### 1. Security Header & Deployment Integrity Check
Validate framework hardening settings by executing:

```bash
python manage.py check --deploy

```

*Expected Output:* `System check identified no issues (0 silenced)`. This confirms that all deployment misconfigurations (such as unhandled HSTS parameters or unsecure cookies) are fully resolved.

### 2. Automated Regression Testing Suite
Run our comprehensive test net to ensure the application hits our **91% perfective coverage score**:

```bash
pytest --cov=sheets --cov-report=term-missing

```

---

## 📄 License

This evolved personal accounting platform is distributed under the **MIT License**. See the `LICENSE` file for full text parameters.

---

## 🤝 Contributing Guidelines

Contributions must follow a strict, risk-mitigated workflow to maintain code quality. Please review our formal [Contributing Manual](https://www.google.com/search?q=CONTRIBUTING.md) to understand branch naming conventions (`feat/adaptive-`, `fix/corrective-`), mandatory pre-commit hooks integration (`bandit`, `safety`, `flake8`, `black`), and pull request verification expectations.

---

## 👥 Maintenance Team

* **Mohammed Yousef Mohammed ABDULKAREM** (ID: 1221305727) — Preventive Refactoring & Budget Module
* **Mohammed AAMENA Mohammed Abdulkarem** (ID: 1221305728) — Corrective Maintenance & Infrastructure Hardening
* **FARAH HANIM BINTI MOHD ZAMRI** (ID: 1221305625) — Perfective Testing QA Gates, Authentication, & UI Theme Engine

---

*Developed for CSE6364 Software Evolution & Maintenance under the supervision of Dr. Dr. Zuriani Hayati Binti Abdullah at Multimedia University.*

---

## Table of contents
* [About](#About)
* [Features](#Features)
* [Installation & Configuration](#installation--configuration)
  * [Docker method](#docker-method)
* [Updating](#updating)
  * [Docker method](#docker-method-1)
* [License](#license)
* [Contributing](#contributing)
* [Developer documentation](#developer-documentation)
  * [The development environment](#the-development-environment)
    * [Set up](#set-up)
    * [Usage](#usage)
  * [Code quality](#code-quality)
  * [Testing](#testing)




## About

[![Mentioned in Awesome Selfhosted](https://awesome.re/mentioned-badge.svg)](https://github.com/awesome-selfhosted/awesome-selfhosted)

It is important to control your budget and know where your money goes. I've tried lots of different apps and methods, but none have really convinced me. So I designed and developed IHateToBudget, a simple and efficient application that meets my needs.

And it's also available for you.

## Features

A basic authorization system exists but this application is not intended to be hosted on a public network (yet?). It is designed to be self-hosted locally (e.g. on a Raspberry Pi) and used by a few users within the same household.

#### 1. Categories

Define categories, and their color.

![Categories](./screenshots/categories.png)

#### 2. Sheet

Add dated and categorized expenses. They are automatically grouped by month (i.e. sheet).

![Sheet](./screenshots/sheet.png)

#### 3. Overview

Analyze the overall statistics.

![Overview](./screenshots/overview.png)

#### 4. History

Explore and filter all expenses.

![History](./screenshots/history.png)

## Installation & Configuration

### Docker method

**The following instructions are guidelines. You're free to adapt these to your needs.**

1. Install [Docker](https://www.docker.com/) and [docker-compose](https://docs.docker.com/compose/), if you haven't already.

2. Clone the repository:

   ```bash
   git clone https://github.com/bminusl/ihatetobudget.git
   cd ihatetobudget
   ```

3. Create a copy of:

   * `docker-compose.yml.example` as `docker-compose.yml`
   * `docker-compose.env.example` as `docker-compose.env`
   * `Caddyfile.example` as `Caddyfile`

   ```bash
   cp docker-compose.yml.example docker-compose.yml
   cp docker-compose.env.example docker-compose.env
   cp Caddyfile.example Caddyfile
   ```

   Note: Making copies ensures that you can `git pull` (or equivalent) to receive updates without risking merge conflicts with upstream changes.

4. Edit `docker-compose.env` and adapt the following environment variables:

   * `DJANGO_SECRET_KEY`: This is the secret key used by Django.

      See [https://docs.djangoproject.com/en/3.1/ref/settings/#std:setting-SECRET_KEY](https://docs.djangoproject.com/en/3.1/ref/settings/#std:setting-SECRET_KEY) for more information.

   **Currency formatting**

   In IHateToBudget, money is represented by positive decimals of the form "xxxxxxxx.yy". The user is free to change the formatting to use the currency of their choice, by setting the following environment variables:

   * `CURRENCY_GROUP_SEPARATOR`: A single character which separates the whole number into groups of 3 digits.<sup>1</sup>
   * `CURRENCY_DECIMAL_SEPARATOR`: A single character that separates the whole part from the decimal part.<sup>1</sup>
   * `CURRENCY_PREFIX`: A string placed in front of the number.<sup>1</sup>
   * `CURRENCY_SUFFIX`: A string placed behind the number.<sup>1</sup>

   By default, it formats money as French euros. For instance, here's how to format as US dollars:

   ```
   CURRENCY_GROUP_SEPARATOR=,
   CURRENCY_DECIMAL_SEPARATOR=.
   CURRENCY_PREFIX=$
   CURRENCY_SUFFIX=
   ```

   ---

   <sup>1</sup>: Note: If it contains spaces, make sure to use [non-breaking spaces](https://en.wikipedia.org/wiki/Non-breaking_space). This is simply to prevent visual "glitches".

5. Run `docker-compose up -d`. This will build the main image, and create and start the necessary containers.

6. Start cron inside the container:

   ```bash
   docker-compose exec ihatetobudget service cron start
   ```

7. To be able to login, you will need a (super) user. To create it, execute the following commands:

   ```bash
   docker-compose run --rm ihatetobudget pipenv run python manage.py migrate
   docker-compose run --rm ihatetobudget pipenv run python manage.py createsuperuser
   ```

   This will prompt you to set a username, an optional e-mail address and finally a password.

8. You should now be able to visit your [IHateToBudget instance](http://127.0.0.1:80) at `http://127.0.0.1:80`. You can login with the username and password you just created.

## Updating

### Docker method

**The following instructions are guidelines. You're free to adapt these to your needs.**

1. Navigate to the root of the repository.

2. Run `docker-compose down -v`. This will stop all containers.

   Note: Volumes are also removed (`-v`), see [why](https://github.com/bminusl/ihatetobudget/commit/d893f01e223909df80f80d9187c355091b18c6e8).

3. **Create a backup of the database**—just in case—, e.g. run `cp db.sqlite3 db.sqlite3.bak`.

4. Upgrade the codebase to the desired revision, e.g. run `git pull`.

5. Rebuild the image:

   ```bash
   docker-compose build
   ```

6. Migrate the database:

   ```bash
   docker-compose run --rm ihatetobudget pipenv run python manage.py migrate
   ```

   This action will synchronize the database state with the current set of models and migrations.

7. Run `docker-compose up -d`. This will create and start the necessary containers.

8. Start cron inside the container:

   ```bash
   docker-compose exec ihatetobudget service cron start
   ```


## License

Distributed under the GPLv3 License. See `COPYING` for more information.


## Contributing

I maintain this project primarily for my own use. If you can think of any relevant changes that should be incorporated into the code, you can contribute by opening an issue or submitting a pull request.

See the [Developer documentation](#developer-documentation) section below for more information.

## Developer documentation

**_This section is WIP_**

### The development environment

#### Set up

1. Install [Pipenv](https://pypi.org/project/pipenv/), if you haven't already.

   Pipenv is used to manage dependencies and the virtual environment.
   Note: IHateToBudget currently targets **Python 3.8**, so **make sure it is installed too**.

2. Set up the virtual environment by executing the following command:

   ```bash
   pipenv install --dev
   ```

   This action will install both develop and default packages.

#### Usage

When you start a new development session, run the following command:

```bash
pipenv shell
```

This action spawns a shell within the virtualenv.


---

**You should now be able to work.**

Since IHateToBudget is primarily a Django project, you should read [Django's documentation](https://docs.djangoproject.com/en/3.1/) if you are not familiar with it already.

### Code quality

[`pre-commit`](https://pypi.org/project/pre-commit/) hooks are used to keep the code clean, namely:
* [`black`](https://pypi.org/project/black/)
* [`flake8`](https://pypi.org/project/flake8/)
* [`isort`](https://pypi.org/project/isort/)

Execute the following command to run pre-commit against all files:

```bash
pre-commit run --all-files
```

### Testing

* To run tests, execute the following command:

  ```bash
  python manage.py test
  ```

* Alternatively, [`coverage`](https://pypi.org/project/coverage/) can be used to measure code coverage:

  ```bash
  coverage run --source='.' manage.py test
  ```
