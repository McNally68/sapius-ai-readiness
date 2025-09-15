#!/usr/bin/env python3
"""
Simple AI Strategy Framework Resource Updater
Updates the AI Strategy Framework page with current timestamp and resource summary
"""

import os
from datetime import datetime

def update_strategy_page():
    """Update the AI Strategy Framework page with current timestamp"""
    
    current_time = datetime.now().strftime('%B %d, %Y at %I:%M %p')
    
    # Read the current template
    template_path = 'templates/ai_strategy_framework.html'
    
    if not os.path.exists(template_path):
        print(f"Template file not found: {template_path}")
        return False
        
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update the last updated timestamp
        old_timestamp_line = 'Last Updated: December 15, 2024 at 10:00 PM<br><br>'
        new_timestamp_line = f'Last Updated: {current_time}<br><br>'
        
        updated_content = content.replace(old_timestamp_line, new_timestamp_line)
        
        # If the old timestamp wasn't found, look for any timestamp pattern
        if updated_content == content:
            import re
            timestamp_pattern = r'Last Updated: [^<]+<br><br>'
            updated_content = re.sub(timestamp_pattern, new_timestamp_line, content)
        
        # Write the updated content back
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
            
        print(f"AI Strategy Framework page updated successfully at {current_time}")
        return True
        
    except Exception as e:
        print(f"Error updating AI Strategy Framework page: {e}")
        return False

def create_scheduler_script():
    """Create a Windows Task Scheduler batch script"""
    
    batch_content = f'''@echo off
cd /d "{os.getcwd()}"
python update_strategy_resources.py
echo AI Strategy Framework updated on %date% at %time%
'''
    
    with open('update_strategy_daily.bat', 'w') as f:
        f.write(batch_content)
    
    print("Created update_strategy_daily.bat for Windows Task Scheduler")
    print("To set up daily automation:")
    print("1. Open Windows Task Scheduler")
    print("2. Create Basic Task")
    print("3. Set trigger to Daily at 10:00 PM")
    print(f"4. Set action to run: {os.getcwd()}\\update_strategy_daily.bat")

if __name__ == "__main__":
    print("AI Strategy Framework Resource Updater")
    print("=" * 50)
    
    # Update the page immediately
    success = update_strategy_page()
    
    if success:
        # Create scheduler script
        create_scheduler_script()
        print("\nSetup complete! AI Strategy Framework resources are ready.")
        print(f"View at: http://localhost:5001/resources/ai-strategy-framework")
    else:
        print("\nSetup failed. Please check the error messages above.")