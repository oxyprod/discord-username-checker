import itertools
import requests
import time
from typing import List
import json

class DiscordUsernameChecker:
    """Search for available 4-character Discord usernames"""
    
    def __init__(self, delay: float = 1.0, timeout: int = 10):
        """
        Initialize the Discord username checker
        
        Args:
            delay: Delay between requests in seconds (to avoid rate limiting)
            timeout: Request timeout in seconds
        """
        self.delay = delay
        self.timeout = timeout
        self.available_usernames = []
        self.checked_count = 0
        self.session = requests.Session()
        
    def generate_4char_usernames(self) -> List[str]:
        """Generate all possible 4-character combinations"""
        # Characters allowed in Discord usernames (alphanumeric + underscore)
        characters = 'abcdefghijklmnopqrstuvwxyz0123456789_'
        
        print("Generating all 4-character username combinations...")
        usernames = [''.join(combo) for combo in itertools.product(characters, repeat=4)]
        print(f"Generated {len(usernames)} combinations to check")
        return usernames
    
    def check_username_available(self, username: str) -> bool:
        """
        Check if a Discord username is available
        
        Args:
            username: The username to check
            
        Returns:
            True if available, False otherwise
        """
        try:
            # Discord API endpoint to check username availability
            url = f"https://discordapp.com/api/v6/users/{username}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = self.session.get(url, headers=headers, timeout=self.timeout)
            
            # 404 means username doesn't exist (available)
            # 200 means username is taken
            if response.status_code == 404:
                return True
            elif response.status_code == 429:
                # Rate limited - wait and retry
                print("Rate limited! Waiting 60 seconds...")
                time.sleep(60)
                return self.check_username_available(username)
            
            return False
            
        except requests.exceptions.RequestException as e:
            print(f"Error checking {username}: {e}")
            return False
    
    def search_available(self, limit: int = None, save_to_file: str = None):
        """
        Search for available Discord usernames
        
        Args:
            limit: Maximum number of usernames to check (None = all)
            save_to_file: Optional file to save available usernames
        """
        usernames = self.generate_4char_usernames()
        
        if limit:
            usernames = usernames[:limit]
        
        print(f"\nStarting search for available usernames (checking {len(usernames)} combinations)...")
        print("This may take a while. Press Ctrl+C to stop.\n")
        
        try:
            for i, username in enumerate(usernames, 1):
                self.checked_count = i
                
                if self.check_username_available(username):
                    self.available_usernames.append(username)
                    print(f"✓ AVAILABLE: {username} [{i}/{len(usernames)}]")
                
                if i % 100 == 0:
                    print(f"Progress: {i}/{len(usernames)} checked, {len(self.available_usernames)} available")
                
                time.sleep(self.delay)
        
        except KeyboardInterrupt:
            print("\n\nSearch stopped by user.")
        
        self.print_results(save_to_file)
    
    def print_results(self, save_to_file: str = None):
        """Print and optionally save results"""
        print("\n" + "="*50)
        print(f"SEARCH COMPLETE")
        print("="*50)
        print(f"Total checked: {self.checked_count}")
        print(f"Available usernames found: {len(self.available_usernames)}")
        
        if self.available_usernames:
            print("\nAvailable usernames:")
            for username in self.available_usernames:
                print(f"  • {username}")
            
            if save_to_file:
                with open(save_to_file, 'w') as f:
                    json.dump(self.available_usernames, f, indent=2)
                print(f"\nResults saved to {save_to_file}")
        else:
            print("\nNo available usernames found.")


if __name__ == "__main__":
    # Example usage
    checker = DiscordUsernameChecker(delay=2.0)  # 2 second delay between requests
    
    # Search with a limit for testing (remove or increase for full search)
    # checker.search_available(limit=1000, save_to_file="available_usernames.json")
    
    # For full search (warning: this will take a very long time)
    checker.search_available(save_to_file="available_usernames.json")
