import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import json
import time

class LinkedInScheduler:
    """Advanced content scheduling system for LinkedIn posts"""
    
    def __init__(self, db_path: str = "content_library.db"):
        self.db_path = db_path
        self.init_scheduler_tables()
    
    def init_scheduler_tables(self):
        """Initialize scheduler database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scheduled_posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_id INTEGER,
                scheduled_time TIMESTAMP NOT NULL,
                status TEXT DEFAULT 'pending',
                platform TEXT DEFAULT 'linkedin',
                auto_hashtags BOOLEAN DEFAULT TRUE,
                optimal_time_adjusted BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                published_at TIMESTAMP,
                error_message TEXT,
                FOREIGN KEY (post_id) REFERENCES posts (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS posting_schedule (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                day_of_week INTEGER,
                time_slot TEXT,
                frequency TEXT DEFAULT 'weekly',
                is_active BOOLEAN DEFAULT TRUE,
                performance_score REAL DEFAULT 0.0
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def schedule_post(self, post_id: int, scheduled_time: datetime, 
                     auto_optimize: bool = True) -> int:
        """Schedule a post for future publishing"""
        
        # Optimize timing if requested
        if auto_optimize:
            scheduled_time = self._optimize_posting_time(scheduled_time)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO scheduled_posts (post_id, scheduled_time, optimal_time_adjusted)
            VALUES (?, ?, ?)
        ''', (post_id, scheduled_time, auto_optimize))
        
        schedule_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return schedule_id
    
    def get_scheduled_posts(self, days_ahead: int = 7) -> List[Dict]:
        """Get posts scheduled for the next N days"""
        end_date = datetime.now() + timedelta(days=days_ahead)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT sp.id, sp.post_id, sp.scheduled_time, sp.status, 
                   p.content, p.content_type, p.topic
            FROM scheduled_posts sp
            JOIN posts p ON sp.post_id = p.id
            WHERE sp.scheduled_time <= ? AND sp.status = 'pending'
            ORDER BY sp.scheduled_time ASC
        ''', (end_date,))
        
        scheduled_posts = []
        for row in cursor.fetchall():
            scheduled_posts.append({
                'schedule_id': row[0],
                'post_id': row[1],
                'scheduled_time': row[2],
                'status': row[3],
                'content': row[4][:100] + "..." if len(row[4]) > 100 else row[4],
                'content_type': row[5],
                'topic': row[6]
            })
        
        conn.close()
        return scheduled_posts
    
    def _optimize_posting_time(self, requested_time: datetime) -> datetime:
        """Optimize posting time based on engagement data"""
        
        # Optimal times for LinkedIn (based on industry research)
        optimal_times = {
            0: [],  # Sunday - limited posting
            1: [9, 10, 11, 13],  # Monday
            2: [8, 9, 10, 12, 15],  # Tuesday - best day
            3: [9, 10, 14],  # Wednesday
            4: [8, 9, 11, 16],  # Thursday
            5: [9, 13],  # Friday
            6: [10]  # Saturday - limited
        }
        
        weekday = requested_time.weekday()
        optimal_hours = optimal_times.get(weekday, [9, 10, 11])
        
        # If requested time is already optimal, keep it
        if requested_time.hour in optimal_hours:
            return requested_time
        
        # Otherwise, adjust to nearest optimal time
        if optimal_hours:
            nearest_hour = min(optimal_hours, key=lambda x: abs(x - requested_time.hour))
            optimized_time = requested_time.replace(hour=nearest_hour, minute=0, second=0)
            return optimized_time
        
        return requested_time
    
    def get_optimal_schedule_suggestions(self) -> Dict:
        """Get personalized schedule suggestions"""
        return {
            "high_engagement_times": [
                {"day": "Tuesday", "time": "9:00 AM", "engagement_boost": "+25%"},
                {"day": "Tuesday", "time": "12:00 PM", "engagement_boost": "+20%"},
                {"day": "Wednesday", "time": "10:00 AM", "engagement_boost": "+18%"},
                {"day": "Thursday", "time": "9:00 AM", "engagement_boost": "+22%"}
            ],
            "recommended_frequency": "3-4 posts per week",
            "best_content_mix": {
                "Thought Leadership": "40%",
                "Professional Updates": "30%", 
                "Industry Insights": "20%",
                "Personal Stories": "10%"
            }
        }

class ContentCalendar:
    """Visual content calendar for planning and organizing posts"""
    
    def __init__(self, db_path: str = "content_library.db"):
        self.db_path = db_path
        self.scheduler = LinkedInScheduler(db_path)
    
    def get_calendar_data(self, year: int, month: int) -> Dict:
        """Get calendar data for a specific month"""
        
        # Get scheduled posts for the month
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = datetime(year, month + 1, 1) - timedelta(days=1)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT DATE(sp.scheduled_time) as date, COUNT(*) as post_count,
                   GROUP_CONCAT(p.content_type) as content_types
            FROM scheduled_posts sp
            JOIN posts p ON sp.post_id = p.id
            WHERE DATE(sp.scheduled_time) BETWEEN ? AND ?
            GROUP BY DATE(sp.scheduled_time)
        ''', (start_date.date(), end_date.date()))
        
        calendar_data = {}
        for row in cursor.fetchall():
            calendar_data[row[0]] = {
                'post_count': row[1],
                'content_types': row[2].split(',') if row[2] else []
            }
        
        conn.close()
        return calendar_data
    
    def suggest_content_gaps(self, days_ahead: int = 30) -> List[Dict]:
        """Identify gaps in content calendar and suggest content"""
        
        # Get current scheduled posts
        scheduled = self.scheduler.get_scheduled_posts(days_ahead)
        scheduled_dates = [datetime.fromisoformat(post['scheduled_time']).date() 
                          for post in scheduled]
        
        # Identify gaps (days without posts)
        gaps = []
        current_date = datetime.now().date()
        
        for i in range(days_ahead):
            check_date = current_date + timedelta(days=i)
            
            # Skip weekends for business content
            if check_date.weekday() < 5 and check_date not in scheduled_dates:
                gaps.append({
                    'date': check_date,
                    'suggested_content': self._suggest_content_for_date(check_date),
                    'optimal_time': self._get_optimal_time_for_date(check_date)
                })
        
        return gaps[:10]  # Return top 10 gaps
    
    def _suggest_content_for_date(self, date) -> str:
        """Suggest content type based on day of week"""
        content_by_day = {
            0: "Motivational Monday - Career advice or inspiration",
            1: "Thought Leadership Tuesday - Industry insights", 
            2: "Wisdom Wednesday - Professional tips and best practices",
            3: "Throwback Thursday - Lessons learned or case studies",
            4: "Feature Friday - Team spotlights or achievements"
        }
        
        return content_by_day.get(date.weekday(), "Professional update or industry news")
    
    def _get_optimal_time_for_date(self, date) -> str:
        """Get optimal posting time for a specific date"""
        optimal_times = {
            0: "9:00 AM",  # Monday
            1: "10:00 AM",  # Tuesday
            2: "9:00 AM",   # Wednesday  
            3: "11:00 AM",  # Thursday
            4: "9:00 AM"    # Friday
        }
        
        return optimal_times.get(date.weekday(), "9:00 AM")

class PerformanceTracker:
    """Track and analyze post performance metrics"""
    
    def __init__(self, db_path: str = "content_library.db"):
        self.db_path = db_path
        self.init_performance_tables()
    
    def init_performance_tables(self):
        """Initialize performance tracking tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS post_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_id INTEGER,
                metric_date DATE,
                views INTEGER DEFAULT 0,
                likes INTEGER DEFAULT 0,
                comments INTEGER DEFAULT 0,
                shares INTEGER DEFAULT 0,
                clicks INTEGER DEFAULT 0,
                engagement_rate REAL DEFAULT 0.0,
                reach INTEGER DEFAULT 0,
                FOREIGN KEY (post_id) REFERENCES posts (id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS performance_insights (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                insight_type TEXT,
                insight_data TEXT,
                confidence_score REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def track_post_performance(self, post_id: int, metrics: Dict):
        """Record performance metrics for a post"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        engagement_rate = 0
        if metrics.get('views', 0) > 0:
            total_engagement = metrics.get('likes', 0) + metrics.get('comments', 0) + metrics.get('shares', 0)
            engagement_rate = (total_engagement / metrics.get('views', 1)) * 100
        
        cursor.execute('''
            INSERT INTO post_metrics 
            (post_id, metric_date, views, likes, comments, shares, clicks, engagement_rate, reach)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            post_id, datetime.now().date(),
            metrics.get('views', 0), metrics.get('likes', 0), 
            metrics.get('comments', 0), metrics.get('shares', 0),
            metrics.get('clicks', 0), engagement_rate, metrics.get('reach', 0)
        ))
        
        conn.commit()
        conn.close()
    
    def get_performance_summary(self, days: int = 30) -> Dict:
        """Get performance summary for the last N days"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        start_date = datetime.now().date() - timedelta(days=days)
        
        cursor.execute('''
            SELECT 
                COUNT(*) as total_posts,
                AVG(views) as avg_views,
                AVG(likes) as avg_likes,
                AVG(comments) as avg_comments,
                AVG(shares) as avg_shares,
                AVG(engagement_rate) as avg_engagement_rate
            FROM post_metrics 
            WHERE metric_date >= ?
        ''', (start_date,))
        
        result = cursor.fetchone()
        
        summary = {
            'total_posts': result[0] or 0,
            'avg_views': round(result[1] or 0, 1),
            'avg_likes': round(result[2] or 0, 1),
            'avg_comments': round(result[3] or 0, 1),
            'avg_shares': round(result[4] or 0, 1),
            'avg_engagement_rate': round(result[5] or 0, 2)
        }
        
        conn.close()
        return summary
    
    def generate_performance_insights(self) -> List[Dict]:
        """Generate AI-powered performance insights"""
        
        # Mock insights - in production, this would use ML analysis
        insights = [
            {
                "type": "timing",
                "message": "Your Tuesday posts get 40% more engagement than other days",
                "confidence": 0.85,
                "action": "Schedule more content for Tuesdays"
            },
            {
                "type": "content",
                "message": "Thought Leadership posts perform 25% better than other content types",
                "confidence": 0.78,
                "action": "Increase thought leadership content to 40% of your posts"
            },
            {
                "type": "hashtags",
                "message": "Posts with 3-5 hashtags get optimal engagement",
                "confidence": 0.92,
                "action": "Use 3-5 relevant hashtags per post"
            },
            {
                "type": "length",
                "message": "Medium-length posts (300-600 chars) have highest engagement",
                "confidence": 0.81,
                "action": "Focus on medium-length content for better reach"
            }
        ]
        
        return insights
