# AI Employee - Bronze Tier Implementation

> **Tagline:** Your life and business on autopilot. Local-first, agent-driven, human-in-the-loop.
> **AI Engine:** Qwen Code

This is a **Bronze Tier** implementation of the Personal AI Employee Hackathon. It provides the foundational layer for an autonomous AI assistant using Qwen Code and Obsidian.

## What's Included (Bronze Tier)

✅ **Obsidian vault** with Dashboard.md and Company_Handbook.md
✅ **File System Watcher** script for monitoring drop folder
✅ **Qwen Code integration** ready (reading/writing to vault)
✅ **Basic folder structure:** /Inbox, /Needs_Action, /Done, etc.
✅ **Business Goals template** for tracking objectives

## Project Structure

```
hacathon0/
├── AI_Employee_Vault/           # Obsidian vault
│   ├── Dashboard.md             # Real-time status dashboard
│   ├── Company_Handbook.md      # Rules of Engagement
│   ├── Business_Goals.md        # Objectives and metrics
│   ├── Inbox/                   # Raw incoming items
│   ├── Needs_Action/            # Items requiring attention
│   ├── Done/                    # Completed items archive
│   ├── Plans/                   # Action plans
│   ├── Pending_Approval/        # Awaiting human approval
│   ├── Approved/                # Approved actions
│   ├── Rejected/                # Rejected actions
│   ├── Logs/                    # Activity logs
│   ├── Accounting/              # Financial records
│   ├── Briefings/               # CEO briefings
│   ├── Invoices/                # Invoice files
│   └── watchers/                # Watcher scripts
│       ├── base_watcher.py      # Base class for all watchers
│       ├── filesystem_watcher.py # File drop monitor
│       └── requirements.txt     # Python dependencies
└── drop_folder/                 # Drop files here for processing
```

## Prerequisites

| Software | Version | Purpose |
|----------|---------|---------|
| [Python](https://www.python.org/downloads/) | 3.13+ | Watcher scripts |
| [Obsidian](https://obsidian.md/download) | v1.10.6+ | Knowledge base |
| [Qwen Code](https://github.com/QwenLM/Qwen) | Latest | AI reasoning engine |
| [Node.js](https://nodejs.org/) | v24+ LTS | MCP servers (future tiers) |

## Quick Start

### Step 1: Open Vault in Obsidian

1. Open Obsidian
2. Click "Open folder as vault"
3. Select: `D:\Learning\quater-4\projects\hacathon0\AI_Employee_Vault`

### Step 2: Start the File System Watcher

Open a terminal and run:

```bash
# Navigate to watchers directory
cd D:\Learning\quater-4\projects\hacathon0\AI_Employee_Vault\watchers

# Start the watcher (checks every 30 seconds)
python filesystem_watcher.py ../ D:\Learning\quater-4\projects\hacathon0\drop_folder
```

**Keep this terminal open** - the watcher runs continuously.

### Step 3: Create Drop Folder

```bash
mkdir D:\Learning\quater-4\projects\hacathon0\drop_folder
```

### Step 4: Test the System

1. **Drop a file** into the `drop_folder` directory
2. **Wait 30 seconds** for the watcher to detect it
3. **Check** `AI_Employee_Vault/Needs_Action/` for a new action file
4. **Use Qwen Code** to process the action:

```bash
cd D:\Learning\quater-4\projects\hacathon0\AI_Employee_Vault
python orchestrator.py . --once
```

This will create a processing prompt for Qwen Code.

Then use Qwen Code to process:
```
Check the /Needs_Action folder and process any pending items.
Create a plan for handling the dropped file.
```

## Usage Guide

### How the File Watcher Works

1. **Monitor:** Watches the `drop_folder` for new files
2. **Detect:** Calculates file hash to avoid duplicates
3. **Create:** Generates an action file in `/Needs_Action`
4. **Process:** Qwen Code reads and creates action plan
5. **Complete:** Move to `/Done` when finished

### File Watcher Command Options

```bash
# Basic usage (30 second check interval)
python filesystem_watcher.py <vault_path> <drop_folder>

# Custom check interval (60 seconds)
python filesystem_watcher.py <vault_path> <drop_folder> 60

# Example with absolute paths
python filesystem_watcher.py ../ "D:\Learning\quater-4\projects\hacathon0\drop_folder" 45
```

### Running in Background (Windows)

To run the watcher continuously in the background:

**Option 1: Using PowerShell**
```powershell
Start-Process python -ArgumentList "filesystem_watcher.py ../ drop_folder" -WindowStyle Hidden
```

**Option 2: Using Task Scheduler**
1. Open Task Scheduler
2. Create Basic Task
3. Trigger: "When I log on"
4. Action: Start a program
   - Program: `python.exe`
   - Arguments: `filesystem_watcher.py ../ drop_folder`
   - Start in: `D:\Learning\quater-4\projects\hacathon0\AI_Employee_Vault\watchers`

## Qwen Code Integration

### Using the Orchestrator

The orchestrator automatically detects action files and creates processing prompts for Qwen Code.

```bash
# Run orchestrator (continuous mode, check every 60 seconds)
cd D:\Learning\quater-4\projects\hacathon0\AI_Employee_Vault
python orchestrator.py . --check-interval 60

# Run once (check and exit immediately)
python orchestrator.py . --once
```

**What the orchestrator does:**
1. Monitors `/Needs_Action/` for new action files
2. Creates `orchestrator_prompt.md` with processing instructions
3. Logs all activities to `/Logs/`
4. Updates `Dashboard.md` with pending item count

### Processing Action Files

Once action files appear in `/Needs_Action/`, use Qwen Code to process them:

```bash
cd D:\Learning\quater-4\projects\hacathon0\AI_Employee_Vault
# Use Qwen Code to process
```

**Example prompts:**
- "Check /Needs_Action and create a plan for each item"
- "Review the Company_Handbook and process pending files"
- "Update the Dashboard.md with current status"
- "Move completed items from /Needs_Action to /Done"

### Ralph Wiggum Loop (Future Tier)

For autonomous multi-step processing, implement the Ralph Wiggum pattern (Gold Tier feature).

## Testing the Implementation

### Test Checklist

- [ ] Obsidian vault opens correctly
- [ ] Dashboard.md displays properly
- [ ] Company_Handbook.md is readable
- [ ] File watcher starts without errors
- [ ] Dropping a file creates action file in /Needs_Action
- [ ] Qwen Code can read and write to vault
- [ ] Action files have correct metadata

### Expected Output

When you drop a file `report.pdf` into the drop folder:

1. Watcher logs: `New file detected: report.pdf`
2. Action file created: `Needs_Action/FILE_DROP_20260316_120000_report.pdf.md`
3. Dashboard shows: "Pending Actions: 1"

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Watcher not starting | Check Python version (3.13+ required) |
| No action file created | Verify drop folder path is correct |
| Duplicate action files | Check cache file in `watchers/.filesystem_cache` |
| Permission errors | Run terminal as administrator |
| Watcher crashes immediately | Check vault path exists and is accessible |

## Next Steps (Silver Tier)

To upgrade to Silver Tier, add:

1. **Gmail Watcher** - Monitor Gmail for important messages
2. **WhatsApp Watcher** - Detect urgent WhatsApp messages
3. **MCP Server** - Send emails automatically
4. **Approval Workflow** - Human-in-the-loop for sensitive actions
5. **Scheduled Tasks** - Daily briefings via cron/Task Scheduler

## Security Notes

⚠️ **Important Security Practices:**

- Never commit `.env` files with credentials
- Use environment variables for API keys
- Keep the vault in a secure location
- Regularly review `/Logs/` for audit trail
- Always approve sensitive actions manually

## Resources

- [Hackathon Blueprint](../Personal%20AI%20Employee%20Hackathon%200_%20Building%20Autonomous%20FTEs%20in%202026.md)
- [Obsidian Help](https://help.obsidian.md/)
- [Qwen Code Documentation](https://github.com/QwenLM/Qwen)
- [Python Documentation](https://docs.python.org/3/)

## License

This project is part of the Personal AI Employee Hackathon 0.

---

*Built with ❤️ for the AI Employee Hackathon - Bronze Tier*
