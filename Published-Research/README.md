# Published-Research

Rails travel-log site for **throwingstarfish.studio** — adventure artifacts at home, Research-Bot reports as **field notes**.

## What this is (ELI5)

`Research-Bot/` is where agents write long, self-contained HTML research papers.

`Published-Research/` is the **public Rails site** that will run on the VPS. It is *not* where research gets written. Bio, decisions, and the app live here; report bodies stay in `Research-Bot/` (phase 2 will scan that folder).

## Phase status

| Phase | What | Status |
|-------|------|--------|
| 1 | Scaffold Rails: home, bio, field-notes list, report show (stub catalog) | **Done in this pass** |
| 2 | Wire real `Research-Bot/**/*.html` catalog + slug rules | Not started |
| 3 | VPS nginx + Puma + TLS | Not started |
| 4 | Auto-deploy on merge to `main` | Not started |

Phase 1 uses two sample HTML files under `sample_reports/` so you can click Home → Field notes → Report before the real catalog exists.

## Docs

| Doc | Role |
|-----|------|
| [`dev-decisions.md`](dev-decisions.md) | Binding human answers |
| [`master-plan.md`](master-plan.md) | Approved execution brief |
| [`bio.md`](bio.md) | About / home voice |
| [`dev-log.md`](dev-log.md) | What changed |

## Run locally (laptop / this machine)

```bash
cd Published-Research
bundle config set --local path 'vendor/bundle'   # once
bundle install
bin/rails server
```

Open:

- http://127.0.0.1:3000/ — home
- http://127.0.0.1:3000/bio — bio from `bio.md`
- http://127.0.0.1:3000/field-notes — stub field notes
- http://127.0.0.1:3000/research/mesa-dusk-walk — report in site chrome
- http://127.0.0.1:3000/research/mesa-dusk-walk/raw — bare HTML document

## Publish / smoke-test on the VPS (phase 1 manual)

Steady-state will be **automatic on merge to `main`** (phase 4). Until then, use these commands to get the site answering on the VPS so you can test pages (stubs, not the Research-Bot catalog yet).

### 1. One-time packages (Ubuntu-ish VPS)

```bash
sudo apt update
sudo apt install -y ruby ruby-dev ruby-bundler build-essential zlib1g-dev libyaml-dev libssl-dev git
```

### 2. Get the code

```bash
# pick a home for the monorepo, e.g.:
cd /var/www
sudo git clone https://github.com/Curtis-Mortensen/curtis-curiosities.git
sudo chown -R "$USER":"$USER" curtis-curiosities
cd curtis-curiosities
```

If the repo is already cloned, pull the branch or `main` after merge:

```bash
cd /var/www/curtis-curiosities
git fetch origin
git checkout main
git pull origin main
```

### 3. Install gems + secret

```bash
cd /var/www/curtis-curiosities/Published-Research
bundle config set --local path 'vendor/bundle'
bundle install
# generate once; save this value (systemd/env file later in phase 3/4)
bin/rails secret
```

### 4. Start Puma for a smoke test (no nginx/TLS yet)

```bash
cd /var/www/curtis-curiosities/Published-Research

export RAILS_ENV=production
export SECRET_KEY_BASE='paste-the-secret-from-step-3-here'
export FORCE_SSL=false   # required until phase 3 puts TLS on nginx

bin/rails server -b 0.0.0.0 -p 3000
```

Visit `http://YOUR_VPS_IP:3000/` and click through home, bio, field notes, and a report.

Stop the server with `Ctrl+C` when finished. Phase 3 will add nginx, HTTPS, and a systemd service; phase 4 removes the need to SSH for routine publishes.

### Firewall note

If the page does not load from your laptop, allow port 3000 temporarily (`ufw allow 3000/tcp` or your cloud security-group rule). Close that port again once nginx (phase 3) listens on 80/443 only.

## Relationship to other folders

- **Report HTML source of truth:** `Research-Bot/` (served directly starting phase 2; no copies)
- **This folder:** site identity, Rails app, bio, decisions
- Do not pull stacks from other monorepo projects
