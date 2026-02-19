"""
Test script for Phase 1 processing logic.
Run with: python api/test_processing.py
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from processing import analyze_entries

# Sample test data - simulating a week of manual entries
test_entries = [
    {"date": "2024-01-15", "app": "Instagram", "time_minutes": 120, "pickups": 15},
    {"date": "2024-01-15", "app": "TikTok", "time_minutes": 90, "pickups": 20},
    {"date": "2024-01-15", "app": "Gmail", "time_minutes": 30, "pickups": 5},
    {"date": "2024-01-15", "app": "Netflix", "time_minutes": 60, "pickups": 2},
    
    {"date": "2024-01-16", "app": "Instagram", "time_minutes": 150, "pickups": 18},
    {"date": "2024-01-16", "app": "Twitter", "time_minutes": 45, "pickups": 12},
    {"date": "2024-01-16", "app": "Slack", "time_minutes": 60, "pickups": 8},
    {"date": "2024-01-16", "app": "Spotify", "time_minutes": 120, "pickups": 3},
    
    {"date": "2024-01-17", "app": "YouTube", "time_minutes": 180, "pickups": 10},
    {"date": "2024-01-17", "app": "Reddit", "time_minutes": 90, "pickups": 25},
    {"date": "2024-01-17", "app": "Notion", "time_minutes": 45, "pickups": 4},
    
    # Testing auto-categorization (no category provided)
    {"date": "2024-01-18", "app": "WhatsApp", "time_minutes": 60, "pickups": 8},
    {"date": "2024-01-18", "app": "UnknownApp", "time_minutes": 30, "pickups": 2},  # Should categorize as "Other"
    
    # Testing manual category override
    {"date": "2024-01-19", "app": "CustomApp", "time_minutes": 45, "category": "Productivity", "pickups": 5},
]

if __name__ == "__main__":
    print("=" * 60)
    print("Testing Phase 1: Data Processing Engine")
    print("=" * 60)
    
    result = analyze_entries(test_entries)
    
    print("\n📊 METRICS:")
    print(f"Total Screen Time: {result['metrics']['total_screen_time_hours']} hours")
    print(f"Doomscroll Hours (Social Media): {result['metrics']['doomscroll_hours']} hours")
    print(f"Total Pickups: {result['metrics']['total_pickups']}")
    print(f"Avg Pickups/Day: {result['metrics']['avg_pickups_per_day']}")
    print(f"Days Tracked: {result['metrics']['days_tracked']}")
    
    print("\n📱 CATEGORY BREAKDOWN:")
    for category, hours in result['metrics']['category_breakdown'].items():
        print(f"  {category}: {hours} hours")
    
    print("\n🏆 TOP APPS:")
    for app, hours in list(result['metrics']['top_apps'].items())[:5]:
        print(f"  {app}: {hours} hours")
    
    print("\n📅 DAILY TOTALS (first 3 days):")
    for day in result['metrics']['daily_totals'][:3]:
        print(f"  {day['date']}: {day['time_hours']:.2f} hours, {day['pickups']} pickups")
    
    print("\n" + "=" * 60)
    print("🔍 CHRONIC ONLINE SCORE")
    print("=" * 60)
    chronic = result['chronic_score']
    print(f"Score: {chronic['score']}/100")
    print(f"Level: {chronic['level']}")
    print(f"Description: {chronic['description']}")
    print(f"\nBreakdown:")
    print(f"  - Daily Screen Time: {chronic['breakdown']['avg_hours_per_day']} hours/day (contributed {chronic['breakdown']['time_score']} points)")
    print(f"  - Social Media: {chronic['breakdown']['doomscroll_percentage']}% of total time (contributed {chronic['breakdown']['doomscroll_score']} points)")
    print(f"  - Pickup Frequency: {result['metrics']['avg_pickups_per_day']} pickups/day (contributed {chronic['breakdown']['pickup_score']} points)")
    
    print("\n" + "=" * 60)
    print("💡 PERSONALIZED TIPS")
    print("=" * 60)
    for i, tip in enumerate(result['tips'][:5], 1):  # Show top 5 tips
        priority_emoji = "🔴" if tip['priority'] == 'high' else "🟡" if tip['priority'] == 'medium' else "🟢"
        print(f"\n{i}. {priority_emoji} [{tip['priority'].upper()}] {tip['title']}")
        print(f"   {tip['description']}")
    
    print("\n✅ Processed entries:", result['processed_entries_count'])
    print("=" * 60)
