#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Base Watcher - Abstract base class for all watcher scripts.

All watchers follow this pattern:
1. Run continuously in the background
2. Monitor a specific input source (Gmail, WhatsApp, filesystem, etc.)
3. Create .md action files in the /Needs_Action folder when new items are detected
4. Track processed items to avoid duplicates
"""

import time
import logging
from pathlib import Path
from abc import ABC, abstractmethod
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class BaseWatcher(ABC):
    """
    Abstract base class for all watcher scripts.
    
    Subclasses must implement:
    - check_for_updates(): Return list of new items to process
    - create_action_file(item): Create .md file in Needs_Action folder
    """
    
    def __init__(self, vault_path: str, check_interval: int = 60):
        """
        Initialize the watcher.
        
        Args:
            vault_path: Path to the Obsidian vault root
            check_interval: Seconds between checks (default: 60)
        """
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.check_interval = check_interval
        self.logger = logging.getLogger(self.__class__.__name__)
        self.processed_ids = set()
        
        # Ensure Needs_Action directory exists
        self.needs_action.mkdir(parents=True, exist_ok=True)
        
    @abstractmethod
    def check_for_updates(self) -> list:
        """
        Check for new items to process.
        
        Returns:
            List of new items (format depends on watcher type)
        """
        pass
    
    @abstractmethod
    def create_action_file(self, item) -> Path:
        """
        Create an action file for the given item.
        
        Args:
            item: Item to create action file for
            
        Returns:
            Path to the created file
        """
        pass
    
    def run(self):
        """
        Main run loop. Continuously checks for updates and creates action files.
        
        This method runs indefinitely until interrupted (Ctrl+C).
        """
        self.logger.info(f'Starting {self.__class__.__name__}')
        self.logger.info(f'Vault path: {self.vault_path}')
        self.logger.info(f'Check interval: {self.check_interval} seconds')
        
        try:
            while True:
                try:
                    items = self.check_for_updates()
                    if items:
                        self.logger.info(f'Found {len(items)} new item(s)')
                        for item in items:
                            try:
                                filepath = self.create_action_file(item)
                                self.logger.info(f'Created action file: {filepath.name}')
                            except Exception as e:
                                self.logger.error(f'Error creating action file: {e}')
                    else:
                        self.logger.debug('No new items')
                except Exception as e:
                    self.logger.error(f'Error checking for updates: {e}')
                
                time.sleep(self.check_interval)
        except KeyboardInterrupt:
            self.logger.info(f'{self.__class__.__name__} stopped by user')
        except Exception as e:
            self.logger.error(f'Fatal error: {e}')
            raise


def load_processed_ids(cache_file: Path) -> set:
    """Load previously processed IDs from cache file."""
    if cache_file.exists():
        return set(cache_file.read_text().strip().split('\n'))
    return set()


def save_processed_ids(cache_file: Path, processed_ids: set):
    """Save processed IDs to cache file."""
    cache_file.write_text('\n'.join(processed_ids))
