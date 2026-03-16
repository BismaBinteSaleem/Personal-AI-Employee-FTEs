# Project Context: Personal AI Employee Hackathon

## Project Overview

This is a **hackathon project** focused on building a "Digital FTE" (Full-Time Equivalent) — an autonomous AI employee powered by **Qwen Code** and **Obsidian**. The project creates a local-first, agent-driven automation system that proactively manages personal and business affairs 24/7.

### Core Architecture

| Layer | Component | Purpose |
|-------|-----------|---------|
| **Brain** | Qwen Code | Reasoning engine for decision-making |
| **Memory/GUI** | Obsidian (Markdown) | Dashboard and long-term knowledge base |
| **Senses** | Python Watcher Scripts | Monitor Gmail, WhatsApp, filesystems |
| **Hands** | MCP Servers | External actions (email, browser automation, payments) |
| **Persistence** | Ralph Wiggum Loop | Keeps agent working until tasks complete |

### Key Concepts

- **Watcher Pattern**: Lightweight Python scripts run continuously, monitoring inputs and creating actionable `.md` files in `/Needs_Action` folders
- **Human-in-the-Loop**: Sensitive actions require approval via file movement (`/Pending_Approval` → `/Approved`)
- **Ralph Wiggum Loop**: A Stop hook pattern that intercepts Claude's exit and re-injects prompts until tasks are complete

## Directory Structure

```
hacathon0/
├── Personal AI Employee Hackathon 0_ Building Autonomous FTEs in 2026.md  # Main blueprint document
├── skills-lock.json              # Skill version tracking
├── QWEN.md                       # This context file
├── .qwen/
│   └── skills/
│       └── browsing-with-playwright/  # Browser automation skill
│           ├── SKILL.md          # Skill documentation and usage guide
│           ├── references/
│           │   └── playwright-tools.md  # Complete MCP tool reference
│           └── scripts/
│               ├── mcp-client.py # Universal MCP client (HTTP + stdio)
│               ├── start-server.sh   # Start Playwright MCP server
│               ├── stop-server.sh    # Stop server gracefully
│               └── verify.py         # Verify server is running
└── .git/
```

## Available Skills

### browsing-with-playwright

Browser automation using Playwright MCP for web interactions.

**Server Management:**
```bash
# Start server (port 8808)
bash .qwen/skills/browsing-with-playwright/scripts/start-server.sh

# Stop server (closes browser gracefully)
bash .qwen/skills/browsing-with-playwright/scripts/stop-server.sh

# Verify server is running
python .qwen/skills/browsing-with-playwright/scripts/verify.py
```

**Key Tools Available:**
- `browser_navigate` - Navigate to URLs
- `browser_snapshot` - Capture accessibility snapshot (preferred over screenshots)
- `browser_click`, `browser_type`, `browser_fill_form` - Element interaction
- `browser_take_screenshot` - Capture screenshots
- `browser_evaluate` - Execute JavaScript
- `browser_run_code` - Run complex Playwright code snippets
- `browser_wait_for` - Wait for text/time conditions

**Usage Pattern:**
```bash
# Call tools via mcp-client.py
python .qwen/skills/browsing-with-playwright/scripts/mcp-client.py \
  call -u http://localhost:8808 \
  -t browser_navigate \
  -p '{"url": "https://example.com"}'
```

## MCP Client Usage

The bundled `mcp-client.py` supports both HTTP and stdio transports:

```bash
# List tools from HTTP server
python mcp-client.py list --url http://localhost:8808

# Call a tool
python mcp-client.py call --url http://localhost:8808 --tool browser_click \
  --params '{"element": "Submit", "ref": "e42"}'

# List tools from stdio server
python mcp-client.py list --stdio "npx -y @modelcontextprotocol/server-github"

# Emit tool schemas as markdown
python mcp-client.py emit --url http://localhost:8808
```

## Hackathon Tiers

| Tier | Description | Estimated Time |
|------|-------------|----------------|
| **Bronze** | Foundation: Obsidian vault, one watcher, basic Claude integration | 8-12 hours |
| **Silver** | Functional: Multiple watchers, MCP servers, approval workflows | 20-30 hours |
| **Gold** | Autonomous: Full integration, Odoo accounting, Ralph Wiggum loop | 40+ hours |
| **Platinum** | Production: Cloud deployment, domain specialization, A2A upgrade | 60+ hours |

## Key Files

| File | Purpose |
|------|---------|
| `Personal AI Employee Hackathon 0_...md` | Complete architectural blueprint with templates, code examples, and implementation guides |
| `.qwen/skills/browsing-with-playwright/SKILL.md` | Browser automation skill documentation |
| `.qwen/skills/browsing-with-playwright/references/playwright-tools.md` | Complete reference for all 22 Playwright MCP tools |
| `.qwen/skills/browsing-with-playwright/scripts/mcp-client.py` | Universal MCP client for tool invocation |
| `AI_Employee_Vault/orchestrator.py` | Qwen Code orchestrator for processing action files |
| `AI_Employee_Vault/watchers/filesystem_watcher.py` | File system watcher for drop folder monitoring |

## Qwen Code Integration

### Using the Orchestrator

The orchestrator monitors for action files and triggers Qwen Code processing:

```bash
# Run orchestrator (continuous mode, check every 60 seconds)
python AI_Employee_Vault/orchestrator.py ./AI_Employee_Vault --check-interval 60

# Run once (check and exit)
python AI_Employee_Vault/orchestrator.py ./AI_Employee_Vault --once
```

### Processing with Qwen Code

When the orchestrator detects pending actions:
1. Creates `orchestrator_prompt.md` with processing instructions
2. Outputs instructions for Qwen Code usage
3. Logs all activities to `/Logs/`

**Manual Qwen Code Processing:**
```bash
cd AI_Employee_Vault
# Read the prompt file and process
# Qwen Code will handle the action files
```

## Development Notes

- **OS**: Windows (win32)
- **Python**: 3.13+ required
- **Node.js**: v24+ LTS for MCP servers
- **Browser**: Playwright requires browser installation (`browser_install` tool)

## Common Workflows

### Browser Form Submission
1. Navigate: `browser_navigate`
2. Snapshot: `browser_snapshot` (get element refs)
3. Fill: `browser_fill_form` or `browser_type`
4. Submit: `browser_click`
5. Wait: `browser_wait_for`
6. Verify: `browser_take_screenshot`

### Data Extraction
1. Navigate to page
2. Get snapshot (contains text content)
3. Use `browser_evaluate` for complex extraction
4. Process results

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Server not responding | Run `verify.py`, then restart with `start-server.sh` |
| Element not found | Run `browser_snapshot` first to get current refs |
| Click fails | Try `browser_hover` before `browser_click` |
| Form not submitting | Use `"submit": true` with `browser_type` |
