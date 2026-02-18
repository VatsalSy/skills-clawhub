# ClawHub Upload Checklist — Funky Fund Flamingo

Use this **before** packaging/uploading to ClawHub.

## Pre-upload checklist

- [x] **SKILL.md frontmatter** uses `metadata.clawdbot` (not `openclaw`); includes `homepage`, `files`, `requires.env`
- [x] **SKILL.md content** includes: External Endpoints, Security & Privacy, Model Invocation Note, Trust Statement
- [x] **package.json** has `openclaw` block (skill, triggers, capabilities, files) and `homepage`
- [x] **.clawhub/origin.json** present (registry + slug)
- [x] **README.md** has install (ClawHub + manual), usage, env table, safety
- [x] **LICENSE** in repo (MIT)
- [ ] **homepage** in SKILL.md: set to your GitHub repo URL when you have one (currently `https://clawhub.ai`)
- [ ] **Test locally**: `node index.js --help` and `node index.js run --dry-run`

## What to include in the ClawHub zip

- `SKILL.md`, `README.md`, `ADL.md`, `VFM.md`, `TREE.md`
- `package.json`, `package-lock.json`
- `index.js`, `evolve.js`, and other `.js` entry/helpers
- `agents/*.yaml`
- `funky-fund-flamingo-master-directive.yaml` (and `.json` if used)
- `.clawhub/origin.json`

## What to exclude from the ClawHub zip

- `.git/`, `.gitignore`
- `LICENSE` (keep in GitHub only if you use a separate repo)
- `.env`, `.env.*`, any secrets
- `node_modules/` (list deps in package.json; install on use)
- `*.log`, `.memory/`, `evolution_history*.md` (local run artifacts)

## After upload

- Skill may be in review (審核中) for a bit; re-check ClawHub later.
- Install test: `clawhub install <your-org>/funky-fund-flamingo` (replace with your ClawHub author/slug if different).

---

*Dolla, dolla bill y'all. 🦩*
