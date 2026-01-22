import { useMemo } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Area,
  AreaChart,
} from 'recharts';
import { format, parseISO } from 'date-fns';

function StockChart({ data, symbol, isPositive = true }) {
  const chartData = useMemo(() => {
    if (!data || data.length === 0) return [];
    
    return data.map((point) => ({
      ...point,
      date: typeof point.timestamp === 'string' 
        ? parseISO(point.timestamp) 
        : new Date(point.timestamp),
      price: point.close,
    }));
  }, [data]);

  const color = isPositive ? '#22c55e' : '#ef4444';
  const gradientId = `gradient-${symbol}`;

  if (chartData.length === 0) {
    return (
      <div className="h-64 flex items-center justify-center text-gray-400">
        No chart data available
      </div>
    );
  }

  const minPrice = Math.min(...chartData.map(d => d.price)) * 0.995;
  const maxPrice = Math.max(...chartData.map(d => d.price)) * 1.005;

  return (
    <div className="h-64 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={chartData} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
          <defs>
            <linearGradient id={gradientId} x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor={color} stopOpacity={0.3} />
              <stop offset="95%" stopColor={color} stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
          <XAxis
            dataKey="date"
            tickFormatter={(date) => format(date, 'MMM d')}
            stroke="#94a3b8"
            fontSize={12}
            tickLine={false}
            axisLine={false}
          />
          <YAxis
            domain={[minPrice, maxPrice]}
            tickFormatter={(value) => `$${value.toFixed(0)}`}
            stroke="#94a3b8"
            fontSize={12}
            tickLine={false}
            axisLine={false}
            width={60}
          />
          <Tooltip
            content={({ active, payload }) => {
              if (active && payload && payload.length) {
                const data = payload[0].payload;
                return (
                  <div className="bg-white shadow-lg rounded-lg p-3 border border-gray-100">
                    <p className="text-xs text-gray-500 mb-1">
                      {format(data.date, 'MMM d, yyyy')}
                    </p>
                    <p className="font-bold text-gray-900">
                      ${data.price.toFixed(2)}
                    </p>
                    <div className="text-xs text-gray-500 mt-1">
                      <p>Open: ${data.open?.toFixed(2)}</p>
                      <p>High: ${data.high?.toFixed(2)}</p>
                      <p>Low: ${data.low?.toFixed(2)}</p>
                    </div>
                  </div>
                );
              }
              return null;
            }}
          />
          <Area
            type="monotone"
            dataKey="price"
            stroke={color}
            strokeWidth={2}
            fill={`url(#${gradientId})`}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}

export default StockChart;
