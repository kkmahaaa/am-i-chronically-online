"""
Data processing engine for screen time analysis.
Processes daily manual entries and calculates key metrics using Pandas for efficient vectorized operations.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional
from datetime import datetime, timedelta


# App name patterns for auto-categorization
# Using dictionary for O(1) lookup - more efficient than regex for simple pattern matching
CATEGORY_PATTERNS = {
    "Social Media": [
        "instagram", "facebook", "twitter", "x.com", "tiktok", "snapchat",
        "linkedin", "reddit", "pinterest", "whatsapp", "telegram", "discord",
        "youtube", "twitch", "messenger", "wechat", "line", "viber"
    ],
    "Productivity": [
        "gmail", "outlook", "slack", "notion", "trello", "asana", "todoist",
        "calendar", "notes", "reminders", "evernote", "onenote", "google docs",
        "sheets", "drive", "dropbox", "zoom", "teams", "meet"
    ],
    "Entertainment": [
        "netflix", "spotify", "apple music", "disney", "hulu", "prime video",
        "hbo", "paramount", "peacock", "crunchyroll", "plex", "vudu"
    ],
    "Gaming": [
        "game", "play", "roblox", "minecraft", "fortnite", "pubg", "cod",
        "among us", "candy crush", "clash", "pokemon go"
    ],
    "News": [
        "news", "cnn", "bbc", "reuters", "nytimes", "washington post",
        "the guardian", "bloomberg", "wsj", "economist"
    ],
    "Shopping": [
        "amazon", "ebay", "etsy", "shopify", "wish", "alibaba", "target",
        "walmart", "best buy", "zara", "nike", "adidas"
    ],
    "Health & Fitness": [
        "fitness", "workout", "myfitnesspal", "strava", "nike run", "fitbit",
        "apple health", "calm", "headspace", "meditation", "yoga"
    ],
    "Education": [
        "coursera", "udemy", "khan academy", "duolingo", "quizlet", "ted",
        "skillshare", "masterclass", "edx"
    ]
}


def auto_categorize_app(app_name: str) -> str:
    """
    Auto-categorize app based on name patterns.
    Uses case-insensitive matching for robustness.
    
    Why: Vectorized string operations in Pandas are faster than Python loops,
    but for single lookups, simple string matching is sufficient and readable.
    """
    app_lower = app_name.lower()
    
    for category, patterns in CATEGORY_PATTERNS.items():
        for pattern in patterns:
            if pattern in app_lower:
                return category
    
    return "Other"


def process_entries(entries: List[Dict]) -> pd.DataFrame:
    """
    Convert list of daily entries into a cleaned Pandas DataFrame.
    
    Why Pandas: Vectorized operations are 10-100x faster than Python loops
    for data transformations, filtering, and aggregations.
    
    Args:
        entries: List of dicts with keys: date, app, time_minutes, category (optional), pickups (optional)
    
    Returns:
        Cleaned DataFrame with standardized columns
    """
    if not entries:
        return pd.DataFrame()
    
    # Convert to DataFrame - Pandas handles type inference efficiently
    df = pd.DataFrame(entries)
    
    # Standardize date column
    df['date'] = pd.to_datetime(df['date'])
    
    # Ensure time_minutes is numeric (handle string inputs)
    df['time_minutes'] = pd.to_numeric(df['time_minutes'], errors='coerce')
    
    # Auto-categorize if category is missing
    # Using .apply() here because we need the app name for each row
    # Vectorization would require pre-computed lookup, which is overkill for this
    df['category'] = df.apply(
        lambda row: row['category'] if pd.notna(row.get('category')) else auto_categorize_app(row['app']),
        axis=1
    )
    
    # Fill missing pickups with 0 (assume 1 pickup if time > 0 but pickups not specified)
    df['pickups'] = df.get('pickups', pd.Series([0] * len(df)))
    df['pickups'] = df['pickups'].fillna(0).astype(int)
    # If time > 0 but pickups = 0, assume at least 1 pickup
    df.loc[(df['time_minutes'] > 0) & (df['pickups'] == 0), 'pickups'] = 1
    
    # Convert time to hours for easier interpretation
    df['time_hours'] = df['time_minutes'] / 60.0
    
    # Remove any rows with invalid data
    df = df.dropna(subset=['date', 'app', 'time_minutes'])
    
    return df


def calculate_chronic_score(metrics: Dict) -> Dict:
    """
    Calculate a "Chronic Online" score (0-100) based on usage patterns.
    
    Scoring factors:
    - Average daily screen time (0-40 points): Based on hours per day
    - Doomscroll ratio (0-30 points): Social media as % of total time
    - Pickup frequency (0-30 points): How often they check their phone
    
    Why: Weighted scoring allows us to capture multiple dimensions of "chronic online" behavior,
    not just total time. Someone with moderate time but high pickups is still chronically online.
    
    Args:
        metrics: Dictionary from calculate_metrics()
    
    Returns:
        Dictionary with score, level, and description
    """
    if metrics['days_tracked'] == 0:
        return {
            "score": 0,
            "level": "Unknown",
            "description": "No data available",
            "breakdown": {}
        }
    
    avg_hours_per_day = metrics['total_screen_time_hours'] / metrics['days_tracked']
    doomscroll_ratio = (metrics['doomscroll_hours'] / metrics['total_screen_time_hours']) * 100 if metrics['total_screen_time_hours'] > 0 else 0
    
    # Factor 1: Daily screen time (0-40 points)
    # Benchmarks: <2h = 0, 2-4h = 10, 4-6h = 20, 6-8h = 30, 8h+ = 40
    if avg_hours_per_day < 2:
        time_score = 0
    elif avg_hours_per_day < 4:
        time_score = 10
    elif avg_hours_per_day < 6:
        time_score = 20
    elif avg_hours_per_day < 8:
        time_score = 30
    else:
        time_score = 40
    
    # Factor 2: Doomscroll ratio (0-30 points)
    # Benchmarks: <20% = 0, 20-40% = 10, 40-60% = 20, 60%+ = 30
    if doomscroll_ratio < 20:
        doomscroll_score = 0
    elif doomscroll_ratio < 40:
        doomscroll_score = 10
    elif doomscroll_ratio < 60:
        doomscroll_score = 20
    else:
        doomscroll_score = 30
    
    # Factor 3: Pickup frequency (0-30 points)
    # Benchmarks: <50/day = 0, 50-100 = 10, 100-150 = 20, 150+ = 30
    avg_pickups = metrics['avg_pickups_per_day']
    if avg_pickups < 50:
        pickup_score = 0
    elif avg_pickups < 100:
        pickup_score = 10
    elif avg_pickups < 150:
        pickup_score = 20
    else:
        pickup_score = 30
    
    total_score = time_score + doomscroll_score + pickup_score
    
    # Determine level
    if total_score < 20:
        level = "Casually Online"
        description = "You have a healthy relationship with your devices! Keep it up."
    elif total_score < 40:
        level = "Moderately Online"
        description = "You're spending a reasonable amount of time online. Some small adjustments could help."
    elif total_score < 60:
        level = "Pretty Online"
        description = "You're spending quite a bit of time on your devices. Consider setting some boundaries."
    elif total_score < 80:
        level = "Very Online"
        description = "You're spending a lot of time online. It might be time to reassess your digital habits."
    else:
        level = "Chronically Online"
        description = "You're spending excessive time online. Consider implementing significant changes to your digital routine."
    
    return {
        "score": total_score,
        "level": level,
        "description": description,
        "breakdown": {
            "time_score": time_score,
            "doomscroll_score": doomscroll_score,
            "pickup_score": pickup_score,
            "avg_hours_per_day": round(avg_hours_per_day, 2),
            "doomscroll_percentage": round(doomscroll_ratio, 1)
        }
    }


def generate_tips(metrics: Dict, df: pd.DataFrame) -> List[Dict]:
    """
    Generate personalized tips based on user's usage patterns.
    
    Why: Personalized tips are more actionable than generic advice.
    We analyze their specific patterns (top apps, categories, pickups) to provide targeted suggestions.
    
    Args:
        metrics: Dictionary from calculate_metrics()
        df: Processed DataFrame
    
    Returns:
        List of tip dictionaries with title, description, and priority
    """
    tips = []
    
    if df.empty:
        return tips
    
    avg_hours_per_day = metrics['total_screen_time_hours'] / metrics['days_tracked'] if metrics['days_tracked'] > 0 else 0
    doomscroll_hours = metrics['doomscroll_hours']
    doomscroll_percentage = (doomscroll_hours / metrics['total_screen_time_hours']) * 100 if metrics['total_screen_time_hours'] > 0 else 0
    
    # Tip 1: High overall screen time
    if avg_hours_per_day >= 6:
        tips.append({
            "title": "Set Daily Screen Time Limits",
            "description": f"You're averaging {avg_hours_per_day:.1f} hours per day. Try setting a daily limit (e.g., 4-5 hours) and use your phone's built-in screen time controls to enforce it.",
            "priority": "high",
            "category": "general"
        })
    
    # Tip 2: High doomscroll hours
    if doomscroll_percentage >= 40:
        tips.append({
            "title": "Reduce Social Media Consumption",
            "description": f"Social media accounts for {doomscroll_percentage:.0f}% of your screen time ({doomscroll_hours:.1f} hours). Try: (1) Delete apps from your home screen, (2) Set app timers, (3) Use grayscale mode to reduce appeal.",
            "priority": "high",
            "category": "social_media"
        })
    
    # Tip 3: High pickup frequency
    if metrics['avg_pickups_per_day'] >= 100:
        tips.append({
            "title": "Reduce Phone Pickups",
            "description": f"You're picking up your phone {metrics['avg_pickups_per_day']:.0f} times per day on average. Try: (1) Turn off non-essential notifications, (2) Keep your phone in another room, (3) Use 'Do Not Disturb' during focused work.",
            "priority": "high",
            "category": "pickups"
        })
    
    # Tip 4: Specific top app
    if metrics.get('top_apps'):
        top_app = list(metrics['top_apps'].keys())[0]
        top_hours = list(metrics['top_apps'].values())[0]
        if top_hours >= 2:
            tips.append({
                "title": f"Limit Time on {top_app}",
                "description": f"You spend {top_hours:.1f} hours per day on {top_app}. Consider setting a daily limit for this app specifically, or try replacing some of this time with offline activities.",
                "priority": "medium",
                "category": "specific_app"
            })
    
    # Tip 5: Evening/night usage (if we had time-of-day data, but for now general)
    if avg_hours_per_day >= 4:
        tips.append({
            "title": "Create Phone-Free Zones",
            "description": "Designate certain times or places as phone-free: (1) First hour after waking, (2) During meals, (3) One hour before bed. This helps break the constant checking habit.",
            "priority": "medium",
            "category": "boundaries"
        })
    
    # Tip 6: High social media but low productivity
    social_hours = metrics.get('category_breakdown', {}).get('Social Media', 0)
    productivity_hours = metrics.get('category_breakdown', {}).get('Productivity', 0)
    if social_hours > 0 and productivity_hours > 0:
        if social_hours > productivity_hours * 2:
            tips.append({
                "title": "Balance Entertainment with Productivity",
                "description": f"You spend {social_hours:.1f} hours on social media vs {productivity_hours:.1f} hours on productivity. Try the '2-minute rule': when you open a social app, spend 2 minutes on a productive task first.",
                "priority": "medium",
                "category": "balance"
            })
    
    # Tip 7: General mindfulness tip
    tips.append({
        "title": "Practice Mindful Phone Use",
        "description": "Before picking up your phone, ask yourself: 'What do I need to do?' If you can't answer, put it down. This simple pause can prevent mindless scrolling.",
        "priority": "low",
        "category": "mindfulness"
    })
    
    # Tip 8: Track and review
    tips.append({
        "title": "Review Your Progress Weekly",
        "description": "Set aside 10 minutes each week to review your screen time data. Notice patterns: Are you using your phone more when stressed? Bored? Use this awareness to make intentional changes.",
        "priority": "low",
        "category": "tracking"
    })
    
    # Sort by priority (high -> medium -> low)
    priority_order = {"high": 0, "medium": 1, "low": 2}
    tips.sort(key=lambda x: priority_order.get(x['priority'], 3))
    
    return tips


def calculate_metrics(df: pd.DataFrame) -> Dict:
    """
    Calculate key metrics from processed entries.
    
    Why NumPy/Pandas: Aggregations like sum(), mean(), groupby() are highly optimized
    in C under the hood, making them much faster than Python loops.
    
    Args:
        df: Processed DataFrame from process_entries()
    
    Returns:
        Dictionary with calculated metrics
    """
    if df.empty:
        return {
            "total_screen_time_hours": 0.0,
            "total_screen_time_minutes": 0.0,
            "doomscroll_hours": 0.0,
            "total_pickups": 0,
            "avg_pickups_per_day": 0.0,
            "days_tracked": 0,
            "category_breakdown": {},
            "daily_totals": [],
            "weekly_totals": []
        }
    
    # Total screen time (using vectorized sum - much faster than loop)
    total_minutes = df['time_minutes'].sum()
    total_hours = total_minutes / 60.0
    
    # Doomscroll hours (Social Media category)
    # Using boolean indexing - vectorized and fast
    social_media_df = df[df['category'] == 'Social Media']
    doomscroll_hours = social_media_df['time_hours'].sum()
    
    # Pickup frequency
    total_pickups = int(df['pickups'].sum())
    unique_days = df['date'].nunique()
    avg_pickups_per_day = total_pickups / unique_days if unique_days > 0 else 0.0
    
    # Category breakdown (using groupby - optimized aggregation)
    category_breakdown = df.groupby('category')['time_hours'].sum().to_dict()
    
    # Daily totals (for trend visualization)
    daily_totals = df.groupby('date').agg({
        'time_hours': 'sum',
        'pickups': 'sum'
    }).reset_index()
    daily_totals['date'] = daily_totals['date'].dt.strftime('%Y-%m-%d')
    daily_totals = daily_totals.to_dict('records')
    
    # Weekly totals (group by week)
    df['week'] = df['date'].dt.to_period('W')
    weekly_totals = df.groupby('week').agg({
        'time_hours': 'sum',
        'pickups': 'sum'
    }).reset_index()
    weekly_totals['week'] = weekly_totals['week'].astype(str)
    weekly_totals = weekly_totals.rename(columns={'week': 'period'}).to_dict('records')
    
    # Top apps by time
    top_apps = df.groupby('app')['time_hours'].sum().sort_values(ascending=False).head(10)
    top_apps_dict = top_apps.to_dict()
    
    return {
        "total_screen_time_hours": round(total_hours, 2),
        "total_screen_time_minutes": int(total_minutes),
        "doomscroll_hours": round(doomscroll_hours, 2),
        "total_pickups": total_pickups,
        "avg_pickups_per_day": round(avg_pickups_per_day, 2),
        "days_tracked": unique_days,
        "category_breakdown": {k: round(v, 2) for k, v in category_breakdown.items()},
        "daily_totals": daily_totals,
        "weekly_totals": weekly_totals,
        "top_apps": {k: round(v, 2) for k, v in top_apps_dict.items()}
    }


def analyze_entries(entries: List[Dict]) -> Dict:
    """
    Main entry point: process entries and calculate all metrics.
    
    Args:
        entries: List of daily screen time entries
    
    Returns:
        Complete analytics dictionary with metrics, chronic score, and tips
    """
    df = process_entries(entries)
    metrics = calculate_metrics(df)
    chronic_score = calculate_chronic_score(metrics)
    tips = generate_tips(metrics, df)
    
    return {
        "metrics": metrics,
        "chronic_score": chronic_score,
        "tips": tips,
        "processed_entries_count": len(df)
    }
