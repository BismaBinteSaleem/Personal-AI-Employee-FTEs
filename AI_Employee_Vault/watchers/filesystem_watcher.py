#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File System Watcher - Monitors a drop folder for new files.

This watcher monitors a designated "drop folder" for new files. When a file
is added, it creates an action file in /Needs_Action for the AI Employee
to process.

Usage:
    python filesystem_watcher.py /path/to/vault /path/to/drop/folder

For Bronze Tier: This is the simplest watcher to implement and test.
"""

import sys
import time
import logging
import hashlib
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from base_watcher import BaseWatcher

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class FileSystemWatcher(BaseWatcher):
    """
    Watcher that monitors a drop folder for new files.
    
    When a new file is detected, creates an action file in /Needs_Action
    with metadata about the file for AI processing.
    """
    
    def __init__(self, vault_path: str, drop_folder: str, check_interval: int = 30):
        """
        Initialize the file system watcher.
        
        Args:
            vault_path: Path to the Obsidian vault root
            drop_folder: Path to the folder to monitor for new files
            check_interval: Seconds between checks (default: 30)
        """
        super().__init__(vault_path, check_interval)
        self.drop_folder = Path(drop_folder)
        self.processed_files = set()
        self.cache_file = self.vault_path / 'watchers' / '.filesystem_cache'
        
        # Ensure drop folder exists
        self.drop_folder.mkdir(parents=True, exist_ok=True)
        
        # Ensure cache directory exists
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Load previously processed files
        self._load_cache()
        
        self.logger.info(f'Drop folder: {self.drop_folder}')
    
    def _load_cache(self):
        """Load previously processed file hashes from cache."""
        if self.cache_file.exists():
            self.processed_files = set(self.cache_file.read_text().strip().split('\n'))
            self.logger.info(f'Loaded {len(self.processed_files)} cached file hashes')
    
    def _save_cache(self):
        """Save processed file hashes to cache."""
        self.cache_file.write_text('\n'.join(self.processed_files))
    
    def _get_file_hash(self, filepath: Path) -> str:
        """
        Calculate MD5 hash of a file for deduplication.
        
        Args:
            filepath: Path to the file
            
        Returns:
            MD5 hash string
        """
        hash_md5 = hashlib.md5()
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def check_for_updates(self) -> list:
        """
        Check for new files in the drop folder.
        
        Returns:
            List of tuples: (filepath, file_hash)
        """
        new_files = []
        
        try:
            for filepath in self.drop_folder.iterdir():
                if filepath.is_file() and not filepath.name.startswith('.'):
                    file_hash = self._get_file_hash(filepath)
                    
                    # Check if already processed
                    if file_hash not in self.processed_files:
                        new_files.append((filepath, file_hash))
                        self.logger.debug(f'New file detected: {filepath.name}')
        except Exception as e:
            self.logger.error(f'Error scanning drop folder: {e}')
        
        return new_files
    
    def create_action_file(self, item) -> Path:
        """
        Create an action file for the dropped file.
        
        Args:
            item: Tuple of (filepath, file_hash)
            
        Returns:
            Path to the created action file
        """
        filepath, file_hash = item
        
        # Get file metadata
        stat = filepath.stat()
        file_size = stat.st_size
        modified_time = datetime.fromtimestamp(stat.st_mtime).isoformat()
        
        # Generate unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_name = filepath.name.replace(' ', '_').replace('-', '_')
        action_filename = f'FILE_DROP_{timestamp}_{safe_name}.md'
        action_filepath = self.needs_action / action_filename
        
        # Determine file type category
        file_ext = filepath.suffix.lower()
        file_type_map = {
            '.pdf': 'document',
            '.doc': 'document',
            '.docx': 'document',
            '.txt': 'text',
            '.md': 'markdown',
            '.xls': 'spreadsheet',
            '.xlsx': 'spreadsheet',
            '.csv': 'data',
            '.jpg': 'image',
            '.jpeg': 'image',
            '.png': 'image',
            '.gif': 'image',
        }
        file_type = file_type_map.get(file_ext, 'unknown')
        
        # Create action file content
        content = f'''---
type: file_drop
source: filesystem
original_name: {filepath.name}
file_size: {file_size} bytes
file_type: {file_type}
received: {datetime.now().isoformat()}
modified: {modified_time}
status: pending
priority: normal
---

# File Drop for Processing

A new file has been dropped for processing.

## File Details

- **Original Name:** `{filepath.name}`
- **File Type:** {file_type} ({file_ext})
- **Size:** {file_size:,} bytes
- **Location:** `{filepath}`
- **Received:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Suggested Actions

- [ ] Review file content
- [ ] Categorize and file appropriately
- [ ] Extract any actionable information
- [ ] Move original file to archive or delete
- [ ] Mark this task as complete

## Notes

```
Add any notes or processing instructions here
```

---
*Generated by File System Watcher v0.1*
'''
        
        # Write action file
        action_filepath.write_text(content)
        
        # Update cache
        self.processed_files.add(file_hash)
        self._save_cache()
        
        # Log the action
        self.logger.info(f'Created action file for: {filepath.name} ({file_size:,} bytes)')
        
        return action_filepath


def main():
    """Main entry point for running the watcher."""
    if len(sys.argv) < 3:
        print("Usage: python filesystem_watcher.py <vault_path> <drop_folder> [check_interval]")
        print("\nExample:")
        print("  python filesystem_watcher.py ./AI_Employee_Vault ./drop_folder")
        print("  python filesystem_watcher.py ./AI_Employee_Vault ./drop_folder 60")
        sys.exit(1)
    
    vault_path = sys.argv[1]
    drop_folder = sys.argv[2]
    check_interval = int(sys.argv[3]) if len(sys.argv) > 3 else 30
    
    watcher = FileSystemWatcher(vault_path, drop_folder, check_interval)
    watcher.run()


if __name__ == '__main__':
    main()
