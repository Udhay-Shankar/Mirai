import React, { useState, useEffect } from 'react';
import axios from 'axios';

const DatabaseMonitorDashboard = () => {
  const [healthData, setHealthData] = useState(null);
  const [connections, setConnections] = useState(null);
  const [performance, setPerformance] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [autoRefresh, setAutoRefresh] = useState(true);

  const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

  // Fetch monitoring data
  const fetchData = async () => {
    try {
      const token = localStorage.getItem('accessToken');
      const config = {
        headers: { Authorization: `Bearer ${token}` }
      };

      const [healthRes, connectRes, perfRes] = await Promise.all([
        axios.get(`${API_URL}/api/monitor/health`),
        axios.get(`${API_URL}/api/monitor/db/connections`, config),
        axios.get(`${API_URL}/api/monitor/db/performance`, config)
      ]);

      setHealthData(healthRes.data);
      setConnections(connectRes.data);
      setPerformance(perfRes.data);
      setError(null);
    } catch (err) {
      console.error('Error fetching monitoring data:', err);
      setError(err.response?.data?.detail || 'Failed to fetch monitoring data');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();

    // Auto-refresh every 5 seconds
    let interval;
    if (autoRefresh) {
      interval = setInterval(fetchData, 5000);
    }

    return () => {
      if (interval) clearInterval(interval);
    };
  }, [autoRefresh]);

  const getStatusColor = (status) => {
    switch (status) {
      case 'healthy':
      case 'good':
        return 'text-green-500';
      case 'warning':
        return 'text-yellow-500';
      case 'critical':
      case 'unhealthy':
        return 'text-red-500';
      default:
        return 'text-gray-500';
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-900">
        <div className="text-white text-xl">Loading monitoring data...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      {/* Header */}
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Database Monitor</h1>
        <div className="flex gap-4 items-center">
          <label className="flex items-center gap-2 cursor-pointer">
            <input
              type="checkbox"
              checked={autoRefresh}
              onChange={(e) => setAutoRefresh(e.target.checked)}
              className="w-4 h-4"
            />
            <span>Auto-refresh (5s)</span>
          </label>
          <button
            onClick={fetchData}
            className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg transition"
          >
            Refresh Now
          </button>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-600/20 border border-red-600 rounded-lg p-4 mb-6">
          <p className="text-red-300">{error}</p>
        </div>
      )}

      {/* Health Status */}
      {healthData && (
        <div className="bg-gray-800 rounded-lg p-6 mb-6 border border-gray-700">
          <h2 className="text-xl font-semibold mb-4">System Health</h2>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <span className="text-gray-400">Overall Status:</span>
              <span className={`ml-2 font-bold ${getStatusColor(healthData.status)}`}>
                {healthData.status.toUpperCase()}
              </span>
            </div>
            <div>
              <span className="text-gray-400">Database:</span>
              <span className={`ml-2 font-bold ${getStatusColor(healthData.database === 'connected' ? 'healthy' : 'unhealthy')}`}>
                {healthData.database.toUpperCase()}
              </span>
            </div>
          </div>
        </div>
      )}

      {/* Connection Stats */}
      {connections && (
        <div className="bg-gray-800 rounded-lg p-6 mb-6 border border-gray-700">
          <h2 className="text-xl font-semibold mb-4">Database Connections</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            <div className="text-center">
              <div className="text-3xl font-bold text-blue-400">{connections.total_connections}</div>
              <div className="text-gray-400 text-sm mt-1">Total</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-green-400">{connections.active_connections}</div>
              <div className="text-gray-400 text-sm mt-1">Active</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-gray-400">{connections.idle_connections}</div>
              <div className="text-gray-400 text-sm mt-1">Idle</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-yellow-400">{connections.waiting_connections}</div>
              <div className="text-gray-400 text-sm mt-1">Waiting</div>
            </div>
          </div>
          {connections.longest_connection_seconds > 0 && (
            <div className="mt-4 text-sm text-gray-400">
              Longest connection: {Math.round(connections.longest_connection_seconds)}s
            </div>
          )}
        </div>
      )}

      {/* Cache Hit Ratio */}
      {performance?.cache_hit_ratio && (
        <div className="bg-gray-800 rounded-lg p-6 mb-6 border border-gray-700">
          <h2 className="text-xl font-semibold mb-4">Cache Performance</h2>
          <div className="flex items-center gap-4">
            <div className="flex-1">
              <div className="flex justify-between mb-2">
                <span>Cache Hit Ratio</span>
                <span className={`font-bold ${getStatusColor(performance.cache_hit_ratio.status)}`}>
                  {performance.cache_hit_ratio.cache_hit_ratio_percent}%
                </span>
              </div>
              <div className="w-full bg-gray-700 rounded-full h-4">
                <div
                  className={`h-4 rounded-full ${
                    performance.cache_hit_ratio.status === 'good' ? 'bg-green-500' :
                    performance.cache_hit_ratio.status === 'warning' ? 'bg-yellow-500' : 'bg-red-500'
                  }`}
                  style={{ width: `${performance.cache_hit_ratio.cache_hit_ratio_percent}%` }}
                ></div>
              </div>
              <div className="mt-2 text-sm text-gray-400">
                Target: &gt; 99% (Disk reads: {performance.cache_hit_ratio.heap_blocks_read})
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Long Running Queries */}
      {performance?.long_running_queries && performance.long_running_queries.length > 0 && (
        <div className="bg-gray-800 rounded-lg p-6 mb-6 border border-gray-700">
          <h2 className="text-xl font-semibold mb-4 text-red-400">
            ⚠️ Long Running Queries
          </h2>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="text-left border-b border-gray-700">
                  <th className="pb-2">PID</th>
                  <th className="pb-2">Duration</th>
                  <th className="pb-2">User</th>
                  <th className="pb-2">State</th>
                  <th className="pb-2">Query</th>
                </tr>
              </thead>
              <tbody>
                {performance.long_running_queries.map((query, idx) => (
                  <tr key={idx} className="border-b border-gray-700/50">
                    <td className="py-2">{query.pid}</td>
                    <td className="py-2 text-red-400">{Math.round(query.duration_seconds)}s</td>
                    <td className="py-2">{query.user}</td>
                    <td className="py-2">{query.state}</td>
                    <td className="py-2 text-sm font-mono text-gray-400">
                      {query.query.substring(0, 100)}...
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Query Performance */}
      {performance?.query_performance && performance.query_performance.length > 0 && (
        <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
          <h2 className="text-xl font-semibold mb-4">Slowest Queries</h2>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="text-left border-b border-gray-700">
                  <th className="pb-2">Query</th>
                  <th className="pb-2">Calls</th>
                  <th className="pb-2">Avg Time</th>
                  <th className="pb-2">Max Time</th>
                  <th className="pb-2">Rows</th>
                </tr>
              </thead>
              <tbody>
                {performance.query_performance.slice(0, 10).map((query, idx) => (
                  <tr key={idx} className="border-b border-gray-700/50">
                    <td className="py-2 text-sm font-mono">{query.query_preview}</td>
                    <td className="py-2">{query.calls}</td>
                    <td className="py-2">{query.mean_exec_time_ms.toFixed(2)}ms</td>
                    <td className="py-2 text-red-400">{query.max_exec_time_ms.toFixed(2)}ms</td>
                    <td className="py-2">{query.rows_affected}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Timestamp */}
      <div className="text-center text-gray-500 text-sm mt-6">
        Last updated: {new Date().toLocaleTimeString()}
      </div>
    </div>
  );
};

export default DatabaseMonitorDashboard;
