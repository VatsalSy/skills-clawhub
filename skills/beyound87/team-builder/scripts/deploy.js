#!/usr/bin/env node
// Team Builder - OpenClaw Multi-Agent Team Deployer
// Usage: node deploy.js

const fs = require('fs');
const path = require('path');
const readline = require('readline');
const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
const ask = q => new Promise(r => rl.question(q, r));
const w = (fp, c) => { fs.mkdirSync(path.dirname(fp), { recursive: true }); fs.writeFileSync(fp, c, 'utf8'); };
const home = process.env.HOME || process.env.USERPROFILE;

// --- Multi-team support ---
const args = process.argv.slice(2);
const teamFlagIdx = args.indexOf('--team');
const teamPrefix = (teamFlagIdx !== -1 && args[teamFlagIdx + 1]) ? args[teamFlagIdx + 1] + '-' : '';

// --- Model auto-detection ---
function detectModels() {
  try {
    const confPath = path.join(home, '.openclaw', 'openclaw.json');
    const conf = JSON.parse(fs.readFileSync(confPath, 'utf8'));
    const provs = Object.keys(conf.modelProviders || {});
    return provs;
  } catch { return []; }
}
function suggestModel(type, provs) {
  const patterns = { think: /glm.?5|opus|o1|deepthink/i, exec: /glm.?4(?!.*flash)|sonnet|gpt-4/i, fast: /flash|haiku|mini/i };
  const p = patterns[type]; if (!p) return null;
  for (const k of provs) { if (p.test(k)) return k; }
  return null;
}

const ROLES = [
  { id: 'chief-of-staff', dname: 'Chief of Staff', pos: 'dispatch+strategy+efficiency', think: true },
  { id: 'data-analyst', dname: 'Data Analyst', pos: 'data+user research', think: false },
  { id: 'growth-lead', dname: 'Growth Lead', pos: 'GEO+SEO+community+social', think: true },
  { id: 'content-chief', dname: 'Content Chief', pos: 'strategy+writing+copy+i18n', think: true },
  { id: 'intel-analyst', dname: 'Intel Analyst', pos: 'competitors+market trends', think: false },
  { id: 'product-lead', dname: 'Product Lead', pos: 'product mgmt+tech architecture', think: true },
  { id: 'fullstack-dev', dname: 'Fullstack Dev', pos: 'fullstack dev+ops+ACP Claude Code', think: false },
];

// --- SOUL generators ---
function chiefSoul(name, team) {
  return `# SOUL.md - ${name} (chief-of-staff)

## Identity
- Role ID: chief-of-staff
- Position: Global dispatch + product matrix strategy + internal efficiency
- Reports to: CEO
- Bridge between CEO and ${team}

## Core Responsibilities

### Dispatch & Coordination
1. Daily morning/evening brief writing and distribution
2. Scan all agent inboxes, detect blockers and anomalies
3. Cross-team task coordination and priority sorting
4. Maintain task board (shared/kanban/)

### Matrix Strategy
5. Product matrix health assessment
6. Cross-product traffic strategy suggestions
7. Resource allocation optimization
8. Pricing strategy analysis

### Internal Efficiency
9. Workflow optimization: find bottlenecks, reduce repetition
10. Agent output quality monitoring
11. Inbox protocol compliance
12. Knowledge base governance
13. Automation suggestions
14. CEO efficiency recommendations

## Daily Flow
### Morning (cron)
1. Read shared/decisions/active.md
2. Scan all shared/inbox/to-*.md
3. Read shared/kanban/blocked.md
4. Check agent output quality
5. Write shared/briefings/morning-YYYY-MM-DD.md

### Evening (cron)
1. Summarize day output
2. Check task completion
3. Evaluate team efficiency
4. Write shared/briefings/evening-YYYY-MM-DD.md
5. Generate next day plan

### Weekly review (Friday evening appendix)
- Agent workload distribution
- Inbox response times
- Efficiency bottlenecks
- Knowledge base health

## Permissions
### Autonomous: coordinate tasks, adjust non-critical priorities, optimize processes
### Ask CEO: new product launch/shutdown, strategy changes, external publishing, spending
`;
}

function dataSoul(name) {
  return `# SOUL.md - ${name} (data-analyst)

## Identity
- Role ID: data-analyst
- Position: Data hub + user research
- Reports to: Chief of Staff

## Core Responsibilities
1. Cross-product core metrics summary (traffic, signups, active users, revenue)
2. Data anomaly detection (>20% deviation from 7-day avg = alert)
3. Funnel analysis, conversion tracking
4. User feedback collection and analysis
5. User persona maintenance -> shared/knowledge/user-personas.md

## Daily Flow
1. Read brief and inbox
2. Pull product core data
3. Scan user feedback channels
4. Anomalies -> write to chief-of-staff and product-lead

## Standards
- Note time range and data source
- YoY and MoM comparisons
- Never fabricate data
`;
}

function growthSoul(name) {
  return `# SOUL.md - ${name} (growth-lead)

## Identity
- Role ID: growth-lead
- Position: Full-channel growth (GEO + SEO + community + social)
- Reports to: Chief of Staff -> CEO

## Core Responsibilities
### GEO - AI Search Optimization (Highest Priority)
1. Monitor AI search engines (ChatGPT, Perplexity, Gemini, Google AI Overview)
2. Track product mention rate, ranking, accuracy
3. Knowledge graph maintenance (Wikipedia, Crunchbase, G2, Capterra)
4. Update shared/knowledge/geo-playbook.md

### SEO
5. Keyword research and ranking tracking
6. Technical SEO audit
7. Update shared/knowledge/seo-playbook.md

### Community + Social
8. Reddit/Product Hunt/Indie Hackers/HN engagement
9. Twitter/X, LinkedIn publishing

## Channel Priority: GEO > SEO > Community > Content > Paid ads (CEO decides)
## Principle: Provide value first, no spam
`;
}

function contentSoul(name) {
  return `# SOUL.md - ${name} (content-chief)

## Identity
- Role ID: content-chief
- Position: One-person content factory (strategy + writing + copy + i18n)
- Reports to: Chief of Staff

## Core Responsibilities
1. Content calendar and topic planning
2. Long-form: tutorials, comparisons, industry analysis (2-3/week)
3. Short copy: landing pages, CTAs, social posts
4. Multi-language localization

## Standards
- Blog: 2000-3000 words, keyword in title, FAQ section
- Copy: concise, 3-second value delivery, 2-3 A/B versions
- Translation: native level, culturally adapted
`;
}

function intelSoul(name) {
  return `# SOUL.md - ${name} (intel-analyst)

## Identity
- Role ID: intel-analyst
- Position: Competitor intel + market trends
- Reports to: Chief of Staff

## Core Responsibilities
1. Competitor product monitoring (features, pricing, funding)
2. Competitor marketing strategy analysis
3. Market trends and new player discovery
4. Competitor AI search presence

## Rhythm: Mon/Wed/Fri scans (cron). Major changes = immediate alert.

## Each Scan
1. Read shared/knowledge/competitor-map.md
2. Search competitor news
3. Update competitor-map.md
4. Alert chief-of-staff, growth-lead, product-lead on findings
`;
}

function productSoul(name) {
  return `# SOUL.md - ${name} (product-lead)

## Identity
- Role ID: product-lead
- Position: Product management + tech architecture
- Reports to: Chief of Staff -> CEO
- Direct report: fullstack-dev

## Core Responsibilities
1. Requirements pool and prioritization
2. Product roadmap
3. Tech architecture design and standards
4. Code quality oversight
5. Technical debt management

## Principles: User value first | Reuse over reinvent | MVP then iterate
`;
}

function devSoul(name) {
  return `# SOUL.md - ${name} (fullstack-dev)

## Identity
- Role ID: fullstack-dev
- Position: Fullstack engineering manager + basic ops
- Reports to: product-lead

## Core Responsibilities
1. Receive tasks from product-lead
2. Simple tasks (<60 lines): do directly
3. Medium/complex: spawn Claude Code via ACP
4. Ops: monitoring, deployment, SSL, security scans

## Coding Behavior

> **Skip this entire section if the coding-lead skill is loaded.** coding-lead takes priority.

### Task Classification
- Simple (<60 lines, single file): do directly
- Medium (2-5 files): spawn Claude Code
- Complex (architecture): plan first, then spawn

### Coding Roles (Complex Tasks Only)
- Architect, Frontend, Backend, Reviewer, QA
- Spawn role-specific Claude Code sessions for complex multi-layer tasks
- Skip roles that don't apply. Simple/medium: no roles.

### Context: gather project docs, tech-standards.md, memory before spawning
### Prompt: include path, stack, standards, history, criteria. Append linter/test + auto-notify
### Spawn: cwd=project dir, never ~/.openclaw/, parallel 2-3 max
### Review: simple=skip, medium=quick check, complex=full checklist (logic/security/perf/style/tests)
### Smart Retry: fail -> analyze -> rewrite prompt -> retry, max 3 then report
### Patterns: record successful prompts in memory, search before spawning
### Updates: notify on start/completion/error, kill runaway sessions

## Proactive Patrol
- Scan git logs and error logs when triggered by cron
- Fix simple issues, report complex ones to chief-of-staff

## Principles
- Follow shared/knowledge/tech-standards.md strictly
- Reuse over reinvention
- When in doubt, ask product-lead
`;
}

const SOUL_FN = {
  'chief-of-staff': chiefSoul,
  'data-analyst': dataSoul,
  'growth-lead': growthSoul,
  'content-chief': contentSoul,
  'intel-analyst': intelSoul,
  'product-lead': productSoul,
  'fullstack-dev': devSoul,
};

// --- Main ---
async function main() {
  console.log('\n========================================');
  console.log('  OpenClaw Team Builder v1.0');
  console.log('========================================\n');

  const teamName = await ask('Team name [Alpha Team]: ') || 'Alpha Team';

  // --- Flexible role selection (2-10) ---
  console.log('\nAvailable roles:');
  ROLES.forEach((r, i) => console.log('  ' + (i+1) + '. ' + r.dname + ' (' + r.id + ') - ' + r.pos));
  const roleInput = await ask('\nSelect roles (comma-separated numbers, or Enter for all): ');
  let selectedRoles;
  if (!roleInput.trim()) {
    selectedRoles = ROLES;
  } else {
    const indices = roleInput.split(',').map(s => parseInt(s.trim()) - 1).filter(i => i >= 0 && i < ROLES.length);
    selectedRoles = indices.map(i => ROLES[i]);
    if (selectedRoles.length < 2) { console.log('Minimum 2 roles. Using all.'); selectedRoles = ROLES; }
  }
  console.log('Selected ' + selectedRoles.length + ' roles: ' + selectedRoles.map(r => r.dname).join(', '));
  const defDir = path.join(home, '.openclaw', 'workspace-team');
  const workDir = await ask(`Workspace dir [${defDir}]: `) || defDir;
  const tz = await ask('Timezone [Asia/Shanghai]: ') || 'Asia/Shanghai';
  const mh = parseInt(await ask('Morning brief hour [8]: ') || '8');
  const eh = parseInt(await ask('Evening brief hour [18]: ') || '18');
  const provs = detectModels();
  const sugT = suggestModel('think', provs) || 'zai/glm-5';
  const sugE = suggestModel('exec', provs) || 'zai/glm-4.7';
  if (provs.length) console.log('\nDetected providers: ' + provs.join(', '));
  console.log('Suggested: thinking=' + sugT + ', execution=' + sugE);
  const tm = await ask('Thinking model [' + sugT + ']: ') || sugT;
  const em = await ask('Execution model [' + sugE + ']: ') || sugE;
  const ceoTitle = await ask('CEO title [Boss]: ') || 'Boss';

  console.log('\n--- Role names (Enter for default) ---');
  const names = {};
  for (const r of selectedRoles) {
    names[r.id] = await ask(`  ${r.id} [${r.dname}]: `) || r.dname;
  }

  const doTg = (await ask('\nSetup Telegram? (y/n) [n]: ')).toLowerCase() === 'y';
  let tgId, tgProxy, tgTokens;
  if (doTg) {
    tgId = await ask('  Telegram user ID: ');
    tgProxy = await ask('  Proxy (Enter to skip): ') || null;
    console.log('  Bot tokens (Enter to skip):');
    tgTokens = {};
    for (const r of selectedRoles) {
      const t = await ask(`    ${names[r.id]} (${r.id}): `);
      if (t) tgTokens[r.id] = t;
    }
    if (!Object.keys(tgTokens).length) tgTokens = null;
  }

  console.log('\n--- Generating ---\n');

  // Directories
  const dirs = ['shared/briefings','shared/inbox','shared/decisions','shared/kanban','shared/knowledge','shared/products'];
  ROLES.forEach(r => dirs.push(`agents/${r.id}/memory`));
  dirs.forEach(d => fs.mkdirSync(path.join(workDir, d), { recursive: true }));
  console.log('  [OK] Directories');

  // AGENTS.md
  const rows = ROLES.map(r => `| ${names[r.id]} | ${r.id} | ${r.pos} |`).join('\n');
  w(path.join(workDir, 'AGENTS.md'), `# AGENTS.md - ${teamName}

## First Instruction

You are a member of ${teamName}. Your identity.name is set in OpenClaw config.

Execute immediately:
1. Confirm your role
2. Read agents/[your-id]/SOUL.md
3. Read shared/decisions/active.md
4. Read shared/inbox/to-[your-id].md
5. Read agents/[your-id]/MEMORY.md

### Role Lookup
| Name | ID | Position |
|------|-----|----------|
${rows}

## Inbox Protocol

Write: [YYYY-MM-DD HH:MM] from:[id] priority:[high/normal/low] | To: [id] | Subject | Expected output | Deadline
Read inbox at session start. Processed items -> bottom. Urgent -> also notify chief-of-staff.

## Output: memory->agents/[id]/ | inbox->shared/inbox/ | products->shared/products/ | knowledge->shared/knowledge/ | tasks->shared/kanban/

## Prohibited: no reading other agents' private dirs, no modifying decisions/, no deleting shared/, no external publishing without CEO, no fabricating data
`);
  console.log('  [OK] AGENTS.md');

  // SOUL.md + USER.md
  w(path.join(workDir, 'SOUL.md'), `# ${teamName} Values\n\nBe genuinely helpful. Have opinions. Be resourceful. Earn trust. Keep private info private. No fabricating data.\n`);
  w(path.join(workDir, 'USER.md'), `# CEO Info\n\n- Title: ${ceoTitle}\n- Timezone: ${tz}\n- Role: SaaS product matrix entrepreneur\n`);
  console.log('  [OK] SOUL.md + USER.md');

  // Agent SOUL + MEMORY
  for (const r of selectedRoles) {
    const fn = SOUL_FN[r.id];
    const soul = r.id === 'chief-of-staff' ? fn(names[r.id], teamName) : fn(names[r.id]);
    w(path.join(workDir, `agents/${r.id}/SOUL.md`), soul);
    w(path.join(workDir, `agents/${r.id}/MEMORY.md`), `# Memory - ${names[r.id]}\n\n(New agent, no memory yet)\n`);
  }
  console.log('  [OK] 7 Agent SOUL.md + MEMORY.md');

  // Inboxes
  for (const r of selectedRoles) {
    w(path.join(workDir, `shared/inbox/to-${r.id}.md`), `# Inbox - ${names[r.id]}\n\n(No messages)\n\n## Processed\n`);
  }
  console.log('  [OK] 7 Inboxes');

  // Shared files
  w(path.join(workDir, 'shared/decisions/active.md'), `# Active Decisions\n\n> All agents read every session.\n\n## Strategy\n- Team: ${teamName}\n- Stage: Cold start\n- Focus: GEO\n\n## Channel Priority\n1. GEO > 2. SEO > 3. Community > 4. Content > 5. Paid (not yet)\n\n## CEO Decision Queue\n(None)\n\n---\n*Fill in: products, goals, resource allocation*\n`);
  w(path.join(workDir, 'shared/products/_index.md'), `# Product Matrix\n\n## Template\n- Name:\n- URL:\n- Code dir:\n- Description:\n- Target users:\n- Features:\n- Tech stack:\n- Status:\n- Keywords (GEO/SEO):\n- Competitors:\n- Differentiator:\n`);
  w(path.join(workDir, 'shared/knowledge/geo-playbook.md'), '# GEO Playbook\n\nAI search optimization strategies.\n');
  w(path.join(workDir, 'shared/knowledge/seo-playbook.md'), '# SEO Playbook\n\nTraditional SEO strategies.\n');
  w(path.join(workDir, 'shared/knowledge/competitor-map.md'), '# Competitor Map\n\n(Fill in competitors)\n');
  w(path.join(workDir, 'shared/knowledge/content-guidelines.md'), '# Content Guidelines\n\nBrand voice, standards.\n');
  w(path.join(workDir, 'shared/knowledge/user-personas.md'), '# User Personas\n\nTarget user profiles.\n');
  w(path.join(workDir, 'shared/knowledge/tech-standards.md'), `# Tech Standards\n\n## Core: KISS + SOLID + DRY. Research before modifying.\n## Red lines: no copy-paste, no breaking existing features, no blind execution.\n## Quality: methods <200 lines, files <500 lines, follow existing style.\n## Security: no hardcoded secrets, DB changes via SQL scripts.\n\n## Tech Stack Preferences (New Projects)\nNew project tech stack must be confirmed with CEO before starting.\n- Backend: PHP (Laravel/ThinkPHP preferred), Python as fallback\n- Frontend: Vue.js or React\n- Mobile: Flutter or UniApp-X\n- CSS: Tailwind CSS\n- DB: MySQL or PostgreSQL\n- Existing projects: keep current stack\n- Always propose first, get approval, then code\n\n---\n*Customize with your tech stack*\n`);
  w(path.join(workDir, 'shared/kanban/backlog.md'), '# Backlog\n\n(Product Lead maintains)\n');
  w(path.join(workDir, 'shared/kanban/in-progress.md'), '# In Progress\n\n(Agents update)\n');
  w(path.join(workDir, 'shared/kanban/blocked.md'), '# Blocked\n\n(Chief of Staff monitors)\n');
  console.log('  [OK] Shared files');

  // apply-config.js
  const wsPath = workDir.replace(/\\/g, '/').replace(home.replace(/\\/g, '/'), '~');
  const agentList = ROLES.map(r => `    { id: "${r.id}", name: "${names[r.id]}", workspace: "${wsPath}", model: { primary: "${r.think ? tm : em}" }, identity: { name: "${names[r.id]}" } }`).join(',\n');
  const allIds = ['main', ...ROLES.map(r => `"${r.id}"`)].join(', ');

  let tgBlock = '';
  if (tgTokens && tgId) {
    const tgEntries = Object.entries(tgTokens).map(([id, tk]) =>
      `  config.channels.telegram.accounts["${id}"] = { botToken: "${tk}", dmPolicy: "allowlist", allowFrom: ["${tgId}"], groupPolicy: "open", streaming: "partial" };\n  config.bindings.push({ agentId: "${id}", match: { channel: "telegram", accountId: "${id}" } });`
    ).join('\n');
    tgBlock = `
  // Telegram
  if (!config.channels) config.channels = {};
  if (!config.channels.telegram) config.channels.telegram = { enabled: true };
  if (!config.channels.telegram.accounts) config.channels.telegram.accounts = {};
  ${tgProxy ? `config.channels.telegram.proxy = "${tgProxy}";` : ''}
${tgEntries}`;
  }

  w(path.join(workDir, 'apply-config.js'), `#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const cfgPath = path.join(process.env.HOME || process.env.USERPROFILE, '.openclaw', 'openclaw.json');
const config = JSON.parse(fs.readFileSync(cfgPath, 'utf8'));

// Backup
const bak = cfgPath + '.backup-' + Date.now();
fs.writeFileSync(bak, JSON.stringify(config, null, 2));
console.log('Backup: ' + bak);

// Add agents
const newAgents = [
${agentList}
];
const existing = new Set(config.agents.list.map(a => a.id));
for (const a of newAgents) {
  if (!existing.has(a.id)) { config.agents.list.push(a); console.log('Added: ' + a.id); }
  else console.log('Exists: ' + a.id);
}

// agentToAgent
if (!config.tools) config.tools = {};
config.tools.agentToAgent = { enabled: true, allow: [${allIds}] };

// bindings
if (!config.bindings) config.bindings = [];
${tgBlock}

fs.writeFileSync(cfgPath, JSON.stringify(config, null, 2));
console.log('\\nDone! Run: openclaw gateway restart');
`);
  console.log('  [OK] apply-config.js');

  // Cron scripts
  const crons = [
    { name: 'chief-morning-brief', cron: `0 ${mh} * * *`, agent: 'chief-of-staff', deliver: '--announce', msg: 'Morning workflow: 1. Read decisions. 2. Scan inboxes. 3. Read kanban. 4. Write shared/briefings/morning-today.md. Under 500 words.' },
    { name: 'chief-evening-brief', cron: `0 ${eh} * * *`, agent: 'chief-of-staff', deliver: '--announce', msg: 'Evening workflow: 1. Scan inboxes. 2. Check task completion. 3. Write shared/briefings/evening-today.md. Under 500 words.' },
    { name: 'growth-daily-work', cron: `0 ${mh+1} * * *`, agent: 'growth-lead', deliver: '--no-deliver', msg: 'Daily growth (incl GEO): 1. Read brief+inbox. 2. GEO monitoring. 3. SEO check. 4. Community scan. 5. Write to shared/.' },
    { name: 'data-daily-pull', cron: `0 ${mh-1} * * *`, agent: 'data-analyst', deliver: '--no-deliver', msg: 'Daily data+research: 1. Check product data. 2. Scan user feedback. 3. Alert chief-of-staff on anomalies.' },
    { name: 'intel-scan', cron: `0 ${mh-1} * * 1,3,5`, agent: 'intel-analyst', deliver: '--no-deliver', msg: 'Competitor scan: 1. Read competitor-map. 2. Search news. 3. Update map. 4. Alert on findings.' },
    { name: 'content-weekly-plan', cron: `0 ${mh+1} * * 1`, agent: 'content-chief', deliver: '--no-deliver', msg: 'Weekly content plan: 1. Read decisions+inbox. 2. Plan this week content. 3. Start first piece.' },
  ];

  // PowerShell
  let ps = `# ${teamName} Cron Jobs\n\n`;
  for (const c of crons) {
    ps += `cmd /c "openclaw cron add --name \\"${c.name}\\" --cron \\"${c.cron}\\" --tz \\"${tz}\\" --session isolated --agent ${c.agent} ${c.deliver} --exact --timeout-seconds 180 --message \\"${c.msg}\\""\n\n`;
  }
  w(path.join(workDir, 'create-crons.ps1'), ps);

  // Bash
  let sh = `#!/bin/bash\n# ${teamName} Cron Jobs\n\n`;
  for (const c of crons) {
    sh += `openclaw cron add --name "${c.name}" --cron "${c.cron}" --tz "${tz}" --session isolated --agent ${c.agent} ${c.deliver} --exact --timeout-seconds 180 --message "${c.msg}"\n\n`;
  }
  w(path.join(workDir, 'create-crons.sh'), sh);
  console.log('  [OK] create-crons.ps1 + .sh');

  // README
  w(path.join(workDir, 'README.md'), `# ${teamName}

## Quick Start
1. \`node apply-config.js\` -- add agents to openclaw.json
2. Run \`create-crons.ps1\` (Windows) or \`create-crons.sh\` (Linux/Mac)
3. \`openclaw gateway restart\`
4. Fill in shared/decisions/active.md and shared/products/_index.md

## Agents
${ROLES.map(r => `- **${names[r.id]}** (${r.id}) -- ${r.pos} -- model: ${r.think ? tm : em}`).join('\n')}

## Cron Schedule
| Time | Agent | Task |
|------|-------|------|
${crons.map(c => `| ${c.cron} | ${c.agent} | ${c.name} |`).join('\n')}
`);
  console.log('  [OK] README.md');

  console.log(`\n========================================`);
  console.log(`  ${teamName} deployed to ${workDir}`);
  console.log(`  Next: node apply-config.js`);
  console.log(`========================================\n`);

  rl.close();
}

main().catch(e => { console.error(e); rl.close(); process.exit(1); });
