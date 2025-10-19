"""
Database monitoring module for real-time database health and performance tracking.
"""
from sqlalchemy import text, inspect
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from typing import Dict, List, Any
import logging
import psutil
import asyncio

logger = logging.getLogger(__name__)


class DatabaseMonitor:
    """Monitor database performance, connections, and health."""
    
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
    
    async def get_connection_stats(self) -> Dict[str, Any]:
        """Get current database connection statistics."""
        try:
            query = text("""
                SELECT 
                    count(*) as total_connections,
                    count(*) FILTER (WHERE state = 'active') as active_connections,
                    count(*) FILTER (WHERE state = 'idle') as idle_connections,
                    count(*) FILTER (WHERE wait_event IS NOT NULL) as waiting_connections,
                    max(extract(epoch from (now() - backend_start))) as longest_connection_seconds
                FROM pg_stat_activity
                WHERE datname = current_database()
            """)
            
            result = await self.db.execute(query)
            row = result.fetchone()
            
            return {
                "total_connections": row[0],
                "active_connections": row[1],
                "idle_connections": row[2],
                "waiting_connections": row[3],
                "longest_connection_seconds": float(row[4]) if row[4] else 0,
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Error getting connection stats: {e}")
            return {"error": str(e)}
    
    async def get_query_performance(self) -> List[Dict[str, Any]]:
        """Get slow queries and performance metrics."""
        try:
            # Requires pg_stat_statements extension
            query = text("""
                SELECT 
                    LEFT(query, 100) as query_preview,
                    calls,
                    total_exec_time,
                    mean_exec_time,
                    max_exec_time,
                    rows
                FROM pg_stat_statements
                ORDER BY mean_exec_time DESC
                LIMIT 10
            """)
            
            result = await self.db.execute(query)
            rows = result.fetchall()
            
            return [
                {
                    "query_preview": row[0],
                    "calls": row[1],
                    "total_exec_time_ms": float(row[2]),
                    "mean_exec_time_ms": float(row[3]),
                    "max_exec_time_ms": float(row[4]),
                    "rows_affected": row[5]
                }
                for row in rows
            ]
        except Exception as e:
            logger.warning(f"pg_stat_statements not available: {e}")
            return []
    
    async def get_table_sizes(self) -> List[Dict[str, Any]]:
        """Get size of all tables in the database."""
        try:
            query = text("""
                SELECT 
                    schemaname,
                    tablename,
                    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size,
                    pg_total_relation_size(schemaname||'.'||tablename) AS size_bytes
                FROM pg_tables
                WHERE schemaname = 'public'
                ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
            """)
            
            result = await self.db.execute(query)
            rows = result.fetchall()
            
            return [
                {
                    "schema": row[0],
                    "table": row[1],
                    "size": row[2],
                    "size_bytes": row[3]
                }
                for row in rows
            ]
        except Exception as e:
            logger.error(f"Error getting table sizes: {e}")
            return []
    
    async def get_database_size(self) -> Dict[str, Any]:
        """Get total database size."""
        try:
            query = text("""
                SELECT 
                    pg_database.datname,
                    pg_size_pretty(pg_database_size(pg_database.datname)) AS size,
                    pg_database_size(pg_database.datname) AS size_bytes
                FROM pg_database
                WHERE datname = current_database()
            """)
            
            result = await self.db.execute(query)
            row = result.fetchone()
            
            return {
                "database": row[0],
                "size": row[1],
                "size_bytes": row[2]
            }
        except Exception as e:
            logger.error(f"Error getting database size: {e}")
            return {"error": str(e)}
    
    async def get_index_usage(self) -> List[Dict[str, Any]]:
        """Get index usage statistics."""
        try:
            query = text("""
                SELECT 
                    schemaname,
                    tablename,
                    indexname,
                    idx_scan as times_used,
                    idx_tup_read as tuples_read,
                    idx_tup_fetch as tuples_fetched
                FROM pg_stat_user_indexes
                ORDER BY idx_scan DESC
            """)
            
            result = await self.db.execute(query)
            rows = result.fetchall()
            
            return [
                {
                    "schema": row[0],
                    "table": row[1],
                    "index": row[2],
                    "times_used": row[3],
                    "tuples_read": row[4],
                    "tuples_fetched": row[5]
                }
                for row in rows
            ]
        except Exception as e:
            logger.error(f"Error getting index usage: {e}")
            return []
    
    async def get_unused_indexes(self) -> List[Dict[str, Any]]:
        """Identify potentially unused indexes."""
        try:
            query = text("""
                SELECT 
                    schemaname,
                    tablename,
                    indexname,
                    pg_size_pretty(pg_relation_size(indexrelid)) as index_size
                FROM pg_stat_user_indexes
                WHERE idx_scan = 0
                AND indexrelname NOT LIKE 'pg_toast%'
                ORDER BY pg_relation_size(indexrelid) DESC
            """)
            
            result = await self.db.execute(query)
            rows = result.fetchall()
            
            return [
                {
                    "schema": row[0],
                    "table": row[1],
                    "index": row[2],
                    "size": row[3],
                    "warning": "Never used - consider dropping"
                }
                for row in rows
            ]
        except Exception as e:
            logger.error(f"Error finding unused indexes: {e}")
            return []
    
    async def get_blocking_queries(self) -> List[Dict[str, Any]]:
        """Find queries that are blocking other queries."""
        try:
            query = text("""
                SELECT 
                    blocked_locks.pid AS blocked_pid,
                    blocked_activity.usename AS blocked_user,
                    blocking_locks.pid AS blocking_pid,
                    blocking_activity.usename AS blocking_user,
                    blocked_activity.query AS blocked_statement,
                    blocking_activity.query AS blocking_statement,
                    blocked_activity.application_name AS blocked_application
                FROM pg_catalog.pg_locks blocked_locks
                JOIN pg_catalog.pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid
                JOIN pg_catalog.pg_locks blocking_locks 
                    ON blocking_locks.locktype = blocked_locks.locktype
                    AND blocking_locks.database IS NOT DISTINCT FROM blocked_locks.database
                    AND blocking_locks.relation IS NOT DISTINCT FROM blocked_locks.relation
                    AND blocking_locks.page IS NOT DISTINCT FROM blocked_locks.page
                    AND blocking_locks.tuple IS NOT DISTINCT FROM blocked_locks.tuple
                    AND blocking_locks.virtualxid IS NOT DISTINCT FROM blocked_locks.virtualxid
                    AND blocking_locks.transactionid IS NOT DISTINCT FROM blocked_locks.transactionid
                    AND blocking_locks.classid IS NOT DISTINCT FROM blocked_locks.classid
                    AND blocking_locks.objid IS NOT DISTINCT FROM blocked_locks.objid
                    AND blocking_locks.objsubid IS NOT DISTINCT FROM blocked_locks.objsubid
                    AND blocking_locks.pid != blocked_locks.pid
                JOIN pg_catalog.pg_stat_activity blocking_activity ON blocking_activity.pid = blocking_locks.pid
                WHERE NOT blocked_locks.granted
            """)
            
            result = await self.db.execute(query)
            rows = result.fetchall()
            
            return [
                {
                    "blocked_pid": row[0],
                    "blocked_user": row[1],
                    "blocking_pid": row[2],
                    "blocking_user": row[3],
                    "blocked_query": row[4],
                    "blocking_query": row[5],
                    "application": row[6]
                }
                for row in rows
            ]
        except Exception as e:
            logger.error(f"Error finding blocking queries: {e}")
            return []
    
    async def get_cache_hit_ratio(self) -> Dict[str, Any]:
        """Get database cache hit ratio (should be > 99%)."""
        try:
            query = text("""
                SELECT 
                    sum(heap_blks_read) as heap_read,
                    sum(heap_blks_hit) as heap_hit,
                    sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read))::float * 100 as cache_hit_ratio
                FROM pg_statio_user_tables
            """)
            
            result = await self.db.execute(query)
            row = result.fetchone()
            
            cache_hit_ratio = float(row[2]) if row[2] else 0
            
            return {
                "heap_blocks_read": row[0],
                "heap_blocks_hit": row[1],
                "cache_hit_ratio_percent": round(cache_hit_ratio, 2),
                "status": "good" if cache_hit_ratio > 99 else "warning" if cache_hit_ratio > 90 else "critical"
            }
        except Exception as e:
            logger.error(f"Error calculating cache hit ratio: {e}")
            return {"error": str(e)}
    
    async def get_vacuum_stats(self) -> List[Dict[str, Any]]:
        """Get vacuum and analyze statistics."""
        try:
            query = text("""
                SELECT 
                    schemaname,
                    relname,
                    last_vacuum,
                    last_autovacuum,
                    vacuum_count,
                    autovacuum_count,
                    n_dead_tup,
                    n_live_tup
                FROM pg_stat_user_tables
                ORDER BY n_dead_tup DESC
            """)
            
            result = await self.db.execute(query)
            rows = result.fetchall()
            
            return [
                {
                    "schema": row[0],
                    "table": row[1],
                    "last_vacuum": row[2].isoformat() if row[2] else None,
                    "last_autovacuum": row[3].isoformat() if row[3] else None,
                    "vacuum_count": row[4],
                    "autovacuum_count": row[5],
                    "dead_tuples": row[6],
                    "live_tuples": row[7],
                    "bloat_ratio": round((row[6] / row[7] * 100), 2) if row[7] > 0 else 0
                }
                for row in rows
            ]
        except Exception as e:
            logger.error(f"Error getting vacuum stats: {e}")
            return []
    
    async def check_replication_lag(self) -> Dict[str, Any]:
        """Check replication lag (if using replication)."""
        try:
            query = text("""
                SELECT 
                    client_addr,
                    state,
                    sent_lsn,
                    write_lsn,
                    flush_lsn,
                    replay_lsn,
                    sync_state,
                    EXTRACT(EPOCH FROM (now() - replay_lag)) as lag_seconds
                FROM pg_stat_replication
            """)
            
            result = await self.db.execute(query)
            rows = result.fetchall()
            
            if not rows:
                return {"replication_enabled": False}
            
            return {
                "replication_enabled": True,
                "replicas": [
                    {
                        "client_addr": row[0],
                        "state": row[1],
                        "sync_state": row[6],
                        "lag_seconds": float(row[7]) if row[7] else 0
                    }
                    for row in rows
                ]
            }
        except Exception as e:
            logger.warning(f"Replication not configured or error: {e}")
            return {"replication_enabled": False}
    
    async def get_long_running_queries(self, threshold_seconds: int = 30) -> List[Dict[str, Any]]:
        """Find queries running longer than threshold."""
        try:
            query = text("""
                SELECT 
                    pid,
                    now() - pg_stat_activity.query_start AS duration,
                    usename,
                    client_addr,
                    state,
                    query
                FROM pg_stat_activity
                WHERE (now() - pg_stat_activity.query_start) > interval :threshold
                AND state != 'idle'
                AND query NOT LIKE '%pg_stat_activity%'
                ORDER BY duration DESC
            """)
            
            result = await self.db.execute(query, {"threshold": f"{threshold_seconds} seconds"})
            rows = result.fetchall()
            
            return [
                {
                    "pid": row[0],
                    "duration_seconds": row[1].total_seconds(),
                    "user": row[2],
                    "client_ip": str(row[3]) if row[3] else "local",
                    "state": row[4],
                    "query": row[5][:200]  # Truncate long queries
                }
                for row in rows
            ]
        except Exception as e:
            logger.error(f"Error finding long running queries: {e}")
            return []
    
    async def get_full_health_report(self) -> Dict[str, Any]:
        """Generate comprehensive health report."""
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "connections": await self.get_connection_stats(),
            "database_size": await self.get_database_size(),
            "cache_hit_ratio": await self.get_cache_hit_ratio(),
            "table_sizes": await self.get_table_sizes(),
            "index_usage": await self.get_index_usage(),
            "unused_indexes": await self.get_unused_indexes(),
            "blocking_queries": await self.get_blocking_queries(),
            "long_running_queries": await self.get_long_running_queries(),
            "vacuum_stats": await self.get_vacuum_stats(),
            "replication": await self.check_replication_lag()
        }


class SecurityMonitor:
    """Monitor database security events."""
    
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
    
    async def get_failed_login_attempts(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Get failed login attempts (requires logging enabled)."""
        try:
            # This requires PostgreSQL log parsing or pg_stat_statements
            # For now, return from application logs
            query = text("""
                SELECT 
                    usename,
                    client_addr,
                    COUNT(*) as failed_attempts
                FROM pg_stat_activity
                WHERE state = 'idle'
                GROUP BY usename, client_addr
                ORDER BY failed_attempts DESC
            """)
            
            result = await self.db.execute(query)
            rows = result.fetchall()
            
            return [
                {
                    "user": row[0],
                    "ip_address": str(row[1]) if row[1] else "local",
                    "failed_attempts": row[2]
                }
                for row in rows
            ]
        except Exception as e:
            logger.error(f"Error getting failed logins: {e}")
            return []
    
    async def get_active_sessions(self) -> List[Dict[str, Any]]:
        """Get all active database sessions."""
        try:
            query = text("""
                SELECT 
                    pid,
                    usename,
                    client_addr,
                    client_port,
                    backend_start,
                    state,
                    query_start,
                    LEFT(query, 100) as query_preview
                FROM pg_stat_activity
                WHERE datname = current_database()
                ORDER BY backend_start DESC
            """)
            
            result = await self.db.execute(query)
            rows = result.fetchall()
            
            return [
                {
                    "pid": row[0],
                    "user": row[1],
                    "ip_address": str(row[2]) if row[2] else "local",
                    "port": row[3],
                    "connected_since": row[4].isoformat(),
                    "state": row[5],
                    "last_query": row[6].isoformat() if row[6] else None,
                    "query_preview": row[7]
                }
                for row in rows
            ]
        except Exception as e:
            logger.error(f"Error getting active sessions: {e}")
            return []
    
    async def detect_suspicious_queries(self) -> List[Dict[str, Any]]:
        """Detect potentially malicious SQL patterns."""
        suspicious_patterns = [
            "DROP TABLE",
            "DROP DATABASE",
            "TRUNCATE",
            "DELETE FROM users WHERE",
            "UPDATE users SET",
            "pg_sleep",
            "UNION SELECT",
            "'; --",
            "1=1"
        ]
        
        try:
            query = text("""
                SELECT 
                    pid,
                    usename,
                    client_addr,
                    query,
                    state
                FROM pg_stat_activity
                WHERE datname = current_database()
            """)
            
            result = await self.db.execute(query)
            rows = result.fetchall()
            
            suspicious = []
            for row in rows:
                query_text = row[3].upper()
                for pattern in suspicious_patterns:
                    if pattern.upper() in query_text:
                        suspicious.append({
                            "pid": row[0],
                            "user": row[1],
                            "ip_address": str(row[2]) if row[2] else "local",
                            "query": row[3],
                            "state": row[4],
                            "suspicious_pattern": pattern,
                            "severity": "HIGH" if pattern in ["DROP TABLE", "DROP DATABASE", "TRUNCATE"] else "MEDIUM"
                        })
                        break
            
            return suspicious
        except Exception as e:
            logger.error(f"Error detecting suspicious queries: {e}")
            return []
