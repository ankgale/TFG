import { useState, useEffect, useCallback, useRef } from 'react';

/**
 * Custom hook for WebSocket connections.
 * Handles connection, reconnection, and message handling.
 */
export function useWebSocket(url) {
  const [isConnected, setIsConnected] = useState(false);
  const [lastMessage, setLastMessage] = useState(null);
  const [error, setError] = useState(null);
  const wsRef = useRef(null);
  const reconnectTimeoutRef = useRef(null);
  const reconnectAttempts = useRef(0);
  const maxReconnectAttempts = 5;

  const connect = useCallback(() => {
    try {
      // Use the full WebSocket URL
      const wsUrl = url.startsWith('ws') ? url : `ws://${window.location.host}${url}`;
      wsRef.current = new WebSocket(wsUrl);

      wsRef.current.onopen = () => {
        setIsConnected(true);
        setError(null);
        reconnectAttempts.current = 0;
        console.log('WebSocket connected');
      };

      wsRef.current.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          setLastMessage(data);
        } catch (e) {
          console.error('Failed to parse WebSocket message:', e);
        }
      };

      wsRef.current.onerror = (event) => {
        console.error('WebSocket error:', event);
        setError('Connection error');
      };

      wsRef.current.onclose = () => {
        setIsConnected(false);
        console.log('WebSocket disconnected');

        // Attempt reconnection
        if (reconnectAttempts.current < maxReconnectAttempts) {
          reconnectAttempts.current += 1;
          const delay = Math.min(1000 * Math.pow(2, reconnectAttempts.current), 30000);
          console.log(`Reconnecting in ${delay}ms (attempt ${reconnectAttempts.current})`);
          
          reconnectTimeoutRef.current = setTimeout(() => {
            connect();
          }, delay);
        }
      };
    } catch (e) {
      console.error('Failed to create WebSocket:', e);
      setError('Failed to connect');
    }
  }, [url]);

  const disconnect = useCallback(() => {
    if (reconnectTimeoutRef.current) {
      clearTimeout(reconnectTimeoutRef.current);
    }
    if (wsRef.current) {
      wsRef.current.close();
    }
  }, []);

  const sendMessage = useCallback((message) => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(message));
    } else {
      console.warn('WebSocket is not connected');
    }
  }, []);

  useEffect(() => {
    connect();

    return () => {
      disconnect();
    };
  }, [connect, disconnect]);

  return {
    isConnected,
    lastMessage,
    error,
    sendMessage,
    reconnect: connect,
  };
}

/**
 * Hook specifically for stock price updates.
 */
export function useStockPrices() {
  const { isConnected, lastMessage, error, sendMessage, reconnect } = useWebSocket('/ws/stocks/');
  const [stocks, setStocks] = useState([]);

  useEffect(() => {
    if (lastMessage?.type === 'prices') {
      setStocks(lastMessage.data);
    }
  }, [lastMessage]);

  const refreshPrices = useCallback(() => {
    sendMessage({ action: 'refresh' });
  }, [sendMessage]);

  const getHistory = useCallback((symbol, period = '1mo') => {
    sendMessage({ action: 'get_history', symbol, period });
  }, [sendMessage]);

  return {
    stocks,
    isConnected,
    error,
    refreshPrices,
    getHistory,
    reconnect,
    lastMessage,
  };
}

export default useWebSocket;
