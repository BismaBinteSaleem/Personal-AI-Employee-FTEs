#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Orchestrator for AI Employee - Qwen Code Integration

This script orchestrates the AI Employee system by:
1. Monitoring watcher processes
2. Triggering Qwen Code to process action files
3. Managing the overall workflow

Usage:
    python orchestrator.py <vault_path> [options]

Example:
    python orchestrator.py ./AI_Employee_Vault --check-interval 60
"""

import argparse
import subprocess
import sys
import time
import logging
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('Orchestrator')


class Orchestrator:
    """
    Orchestrates the AI Employee workflow with Qwen Code.
    
    Responsibilities:
    - Monitor watcher processes
    - Trigger Qwen Code when action files are detected
    - Update dashboard status
    - Log all orchestration activities
    """
    
    def __init__(self, vault_path: str, check_interval: int = 60):
        """
        Initialize the orchestrator.
        
        Args:
            vault_path: Path to the Obsidian vault
            check_interval: Seconds between checks (default: 60)
        """
        self.vault_path = Path(vault_path)
        self.check_interval = check_interval
        self.needs_action = self.vault_path / 'Needs_Action'
        self.done = self.vault_path / 'Done'
        self.logs = self.vault_path / 'Logs'
        self.dashboard = self.vault_path / 'Dashboard.md'
        self.last_processed = {}  # Track processed files
        
        # Ensure directories exist
        for directory in [self.needs_action, self.done, self.logs]:
            directory.mkdir(parents=True, exist_ok=True)
        
        logger.info(f'Vault path: {self.vault_path}')
        logger.info(f'Check interval: {check_interval} seconds')
    
    def get_pending_actions(self) -> list:
        """
        Get list of pending action files.
        
        Returns:
            List of Path objects for pending action files
        """
        try:
            return [
                f for f in self.needs_action.iterdir()
                if f.is_file() and f.suffix == '.md'
            ]
        except Exception as e:
            logger.error(f'Error reading Needs_Action folder: {e}')
            return []
    
    def log_action(self, action_type: str, details: str, status: str = 'info'):
        """
        Log an action to the logs folder.
        
        Args:
            action_type: Type of action (e.g., 'file_processed', 'qwen_triggered')
            details: Details of the action
            status: Status level (info, success, error)
        """
        today = datetime.now().strftime('%Y-%m-%d')
        log_file = self.logs / f'{today}.jsonl'
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action_type': action_type,
            'details': details,
            'status': status
        }
        
        with open(log_file, 'a', encoding='utf-8') as f:
            import json
            f.write(json.dumps(log_entry) + '\n')
        
        logger.info(f'Logged: {action_type} - {details}')
    
    def update_dashboard(self, pending_count: int, completed_today: int = 0):
        """
        Update the Dashboard.md with current status.
        
        Args:
            pending_count: Number of pending action files
            completed_today: Number of items completed today
        """
        if not self.dashboard.exists():
            logger.warning('Dashboard.md not found')
            return
        
        try:
            content = self.dashboard.read_text(encoding='utf-8')
            
            # Update pending count
            if 'Pending Actions |' in content:
                old_line = [l for l in content.split('\n') if 'Pending Actions |' in l][0]
                new_line = f'| Pending Actions | {pending_count} | {"✅ Clear" if pending_count == 0 else "⚠️ Pending"} |'
                content = content.replace(old_line, new_line)
            
            # Update timestamp
            content = content.replace(
                'last_updated: 2026-03-16T00:00:00Z',
                f'last_updated: {datetime.now().isoformat()}Z'
            )
            
            self.dashboard.write_text(content, encoding='utf-8')
            logger.debug(f'Dashboard updated: {pending_count} pending')
            
        except Exception as e:
            logger.error(f'Error updating dashboard: {e}')
    
    def trigger_qwen_code(self, action_files: list):
        """
        Trigger Qwen Code to process action files.
        
        This method prepares a prompt for Qwen Code and can either:
        1. Output instructions for manual Qwen Code usage
        2. Call Qwen Code API if available
        
        Args:
            action_files: List of action file paths to process
        """
        logger.info(f'Triggering Qwen Code for {len(action_files)} action file(s)')
        
        # Create a processing prompt
        prompt = f"""
# AI Employee Task Processing Request

**Time:** {datetime.now().isoformat()}

**Pending Action Files:**
"""
        for action_file in action_files:
            prompt += f"\n- `{action_file.name}`"
        
        prompt += """

## Instructions for Qwen Code

1. Read each action file in /Needs_Action/
2. Review Company_Handbook.md for rules and guidelines
3. Review Business_Goals.md for priorities
4. Create a plan for each action item in /Plans/
5. If approval is needed, create file in /Pending_Approval/
6. If auto-approved, process and move to /Done/
7. Update Dashboard.md with results
8. Log all actions to /Logs/

## Example Processing Flow

```
For each action file:
  1. Read the file content and metadata
  2. Determine action type from frontmatter
  3. Check Company_Handbook.md for rules
  4. Create plan in /Plans/
  5. Execute or request approval
  6. Move to /Done/ when complete
```

**Start processing now.**
"""
        
        # Save the prompt to a file for Qwen Code to read
        prompt_file = self.vault_path / 'orchestrator_prompt.md'
        prompt_file.write_text(prompt, encoding='utf-8')
        
        self.log_action(
            'qwen_triggered',
            f'Created processing prompt for {len(action_files)} files',
            'success'
        )
        
        # Output instructions for user
        print("\n" + "="*60)
        print("QWEN CODE PROCESSING REQUIRED")
        print("="*60)
        print(f"\n{len(action_files)} action file(s) need processing.")
        print(f"\nPrompt saved to: {prompt_file}")
        print("\nTo process with Qwen Code:")
        print(f"  1. Navigate to: {self.vault_path}")
        print("  2. Run Qwen Code with this prompt:")
        print("     'Read orchestrator_prompt.md and process all action files'")
        print("\n" + "="*60 + "\n")
    
    def mark_as_processed(self, action_file: Path):
        """
        Mark an action file as processed (move to Done).
        
        Args:
            action_file: Path to the action file
        """
        try:
            dest = self.done / action_file.name
            action_file.rename(dest)
            logger.info(f'Moved {action_file.name} to /Done/')
            self.log_action('file_completed', str(action_file.name), 'success')
        except Exception as e:
            logger.error(f'Error moving file to Done: {e}')
    
    def run(self):
        """
        Main orchestration loop.
        
        Continuously monitors for action files and triggers Qwen Code.
        """
        logger.info('Starting Orchestrator')
        logger.info('Press Ctrl+C to stop')
        
        try:
            while True:
                # Get pending actions
                pending = self.get_pending_actions()
                
                if pending:
                    logger.info(f'Found {len(pending)} pending action(s)')
                    
                    # Update dashboard
                    self.update_dashboard(len(pending))
                    
                    # Trigger Qwen Code
                    self.trigger_qwen_code(pending)
                    
                    # Note: In automatic mode, Qwen Code would process
                    # and move files to /Done/. For now, we track manually.
                else:
                    logger.debug('No pending actions')
                    self.update_dashboard(0)
                
                # Wait before next check
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            logger.info('Orchestrator stopped by user')
        except Exception as e:
            logger.error(f'Fatal error: {e}')
            raise


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='AI Employee Orchestrator - Qwen Code Integration'
    )
    parser.add_argument(
        'vault_path',
        type=str,
        help='Path to the Obsidian vault'
    )
    parser.add_argument(
        '--check-interval', '-i',
        type=int,
        default=60,
        help='Seconds between checks (default: 60)'
    )
    parser.add_argument(
        '--once',
        action='store_true',
        help='Run once and exit (no loop)'
    )
    
    args = parser.parse_args()
    
    vault = Path(args.vault_path)
    if not vault.exists():
        logger.error(f'Vault path does not exist: {vault}')
        sys.exit(1)
    
    if args.once:
        # Run once mode
        orchestrator = Orchestrator(str(vault))
        pending = orchestrator.get_pending_actions()
        if pending:
            orchestrator.trigger_qwen_code(pending)
        else:
            logger.info('No pending actions')
    else:
        # Continuous mode
        orchestrator = Orchestrator(str(vault), args.check_interval)
        orchestrator.run()


if __name__ == '__main__':
    main()
