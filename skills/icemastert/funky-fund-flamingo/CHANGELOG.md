# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.35] - 2026-02-18

### Added

- ClawHub-ready packaging: `.clawhub/origin.json`, `metadata.clawdbot` in SKILL.md
- OpenClaw skill manifest in `package.json` (triggers, capabilities, files)
- SKILL.md sections required for ClawHub: External Endpoints, Security & Privacy, Model Invocation Note, Trust Statement
- README: ClawHub install instructions, badge, env table, safety rails
- LICENSE (MIT)
- CHANGELOG.md (this file)

### Changed

- SKILL.md, TREE.md, VFM.md, ADL.md, and agent YAMLs rewritten with Funky Fund Flamingo cash-money vibe
- README paths and copy aligned with `funky-fund-flamingo` (no evolver references)

### Notes

- Master directive still has `clawhub_publish_forbidden: true` for the **persist** step (evolution must not auto-publish to ClawHub). Manual upload by the publisher is allowed and supported by this packaging.
