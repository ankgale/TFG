import { useState, useEffect } from 'react';
import { 
  RefreshCw, 
  TrendingUp, 
  TrendingDown,
  DollarSign,
  PieChart,
  Clock,
  AlertCircle
} from 'lucide-react';
import clsx from 'clsx';
import StockCard from '../components/StockCard';
import StockChart from '../components/StockChart';
import { stocksApi } from '../services/api';
import { useStockPrices } from '../hooks/useWebSocket';
import translations from '../i18n/translations';

// Sample stocks data (used when API is not available)
const sampleStocks = [
  { id: 1, symbol: 'AAPL', name: 'Apple Inc.', sector: 'Tecnología', current_price: 178.50, previous_close: 175.20, price_change: 3.30, price_change_percent: 1.88 },
  { id: 2, symbol: 'MSFT', name: 'Microsoft Corporation', sector: 'Tecnología', current_price: 378.90, previous_close: 380.50, price_change: -1.60, price_change_percent: -0.42 },
  { id: 3, symbol: 'GOOGL', name: 'Alphabet Inc.', sector: 'Tecnología', current_price: 141.25, previous_close: 139.80, price_change: 1.45, price_change_percent: 1.04 },
  { id: 4, symbol: 'JPM', name: 'JPMorgan Chase', sector: 'Finanzas', current_price: 195.40, previous_close: 193.20, price_change: 2.20, price_change_percent: 1.14 },
  { id: 5, symbol: 'V', name: 'Visa Inc.', sector: 'Finanzas', current_price: 275.80, previous_close: 278.10, price_change: -2.30, price_change_percent: -0.83 },
  { id: 6, symbol: 'JNJ', name: 'Johnson & Johnson', sector: 'Salud', current_price: 156.20, previous_close: 155.90, price_change: 0.30, price_change_percent: 0.19 },
  { id: 7, symbol: 'PG', name: 'Procter & Gamble', sector: 'Consumo', current_price: 148.75, previous_close: 149.20, price_change: -0.45, price_change_percent: -0.30 },
  { id: 8, symbol: 'XOM', name: 'Exxon Mobil', sector: 'Energía', current_price: 104.30, previous_close: 102.80, price_change: 1.50, price_change_percent: 1.46 },
  { id: 9, symbol: 'TSLA', name: 'Tesla Inc.', sector: 'Automotriz', current_price: 248.90, previous_close: 252.40, price_change: -3.50, price_change_percent: -1.39 },
  { id: 10, symbol: 'KO', name: 'Coca-Cola', sector: 'Consumo', current_price: 59.80, previous_close: 59.50, price_change: 0.30, price_change_percent: 0.50 },
];

// Sample chart data
const generateSampleChartData = (basePrice) => {
  const data = [];
  const now = new Date();
  for (let i = 30; i >= 0; i--) {
    const date = new Date(now);
    date.setDate(date.getDate() - i);
    const randomChange = (Math.random() - 0.5) * 10;
    const close = basePrice + randomChange + (30 - i) * 0.5;
    data.push({
      timestamp: date.toISOString(),
      open: close - Math.random() * 2,
      high: close + Math.random() * 3,
      low: close - Math.random() * 3,
      close: close,
      volume: Math.floor(Math.random() * 10000000) + 5000000,
    });
  }
  return data;
};

function StockSimulation() {
  const { stocks: stocksText, periods: periodsText } = translations;
  
  const [stocks, setStocks] = useState(sampleStocks);
  const [selectedStock, setSelectedStock] = useState(null);
  const [chartData, setChartData] = useState([]);
  const [chartPeriod, setChartPeriod] = useState('1mo');
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [tradeModal, setTradeModal] = useState({ open: false, type: 'buy' });
  const [tradeAmount, setTradeAmount] = useState('');
  
  // WebSocket for real-time updates
  const { stocks: wsStocks, isConnected, refreshPrices } = useStockPrices();

  // Virtual portfolio (mock data for now)
  const portfolio = {
    balance: 100000.00,
    holdings: [],
    totalValue: 100000.00,
  };

  useEffect(() => {
    async function fetchStocks() {
      try {
        // Try to initialize and fetch stocks
        await stocksApi.initializeStocks();
        await stocksApi.refreshPrices();
        const data = await stocksApi.getStocks();
        if (data && data.length > 0) {
          setStocks(data);
        }
      } catch (error) {
        console.log('Using sample stocks:', error.message);
      } finally {
        setLoading(false);
      }
    }

    fetchStocks();
  }, []);

  // Update stocks from WebSocket
  useEffect(() => {
    if (wsStocks && wsStocks.length > 0) {
      setStocks(wsStocks);
    }
  }, [wsStocks]);

  // Fetch chart data when stock is selected
  useEffect(() => {
    if (selectedStock) {
      fetchChartData(selectedStock.id, chartPeriod);
    }
  }, [selectedStock, chartPeriod]);

  async function fetchChartData(stockId, period) {
    try {
      const data = await stocksApi.getStockHistory(stockId, period);
      if (data?.history && data.history.length > 0) {
        setChartData(data.history);
      } else {
        // Use sample data
        const stock = stocks.find(s => s.id === stockId);
        setChartData(generateSampleChartData(stock?.current_price || 100));
      }
    } catch (error) {
      // Use sample data on error
      const stock = stocks.find(s => s.id === stockId);
      setChartData(generateSampleChartData(stock?.current_price || 100));
    }
  }

  const handleRefresh = async () => {
    setRefreshing(true);
    try {
      if (isConnected) {
        refreshPrices();
      } else {
        await stocksApi.refreshPrices();
        const data = await stocksApi.getStocks();
        if (data && data.length > 0) {
          setStocks(data);
        }
      }
    } catch (error) {
      console.error('Refresh failed:', error);
    } finally {
      setTimeout(() => setRefreshing(false), 1000);
    }
  };

  const handleTrade = async () => {
    const shares = parseFloat(tradeAmount);
    if (!shares || shares <= 0 || !selectedStock) return;

    try {
      await stocksApi.executeTrade(
        selectedStock.id,
        shares,
        tradeModal.type,
        null // user_id - will be set when auth is implemented
      );
      
      setTradeModal({ open: false, type: 'buy' });
      setTradeAmount('');
      // TODO: Refresh portfolio
    } catch (error) {
      console.error('Trade failed:', error);
      // TODO: Show error toast
    }
  };

  const periods = [
    { value: '1d', label: periodsText['1d'] },
    { value: '5d', label: periodsText['5d'] },
    { value: '1mo', label: periodsText['1mo'] },
    { value: '3mo', label: periodsText['3mo'] },
    { value: '1y', label: periodsText['1y'] },
  ];

  return (
    <div className="max-w-7xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            {stocksText.title}
          </h1>
        </div>
        <div className="flex items-center gap-3">
          {/* Connection status */}
          <div className={clsx(
            'flex items-center gap-2 px-3 py-1.5 rounded-full text-sm',
            isConnected ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-600'
          )}>
            <div className={clsx(
              'w-2 h-2 rounded-full',
              isConnected ? 'bg-green-500 animate-pulse' : 'bg-gray-400'
            )} />
            {isConnected ? stocksText.live : stocksText.offline}
          </div>
          
          <button
            onClick={handleRefresh}
            disabled={refreshing}
            className="btn btn-outline flex items-center gap-2"
          >
            <RefreshCw className={clsx('w-4 h-4', refreshing && 'animate-spin')} />
            {stocksText.refresh}
          </button>
        </div>
      </div>

      {/* Portfolio Summary */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div className="card">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-primary-100 rounded-xl flex items-center justify-center">
              <DollarSign className="w-5 h-5 text-primary-500" />
            </div>
            <div>
              <p className="text-sm text-gray-500">{stocksText.cashBalance}</p>
              <p className="text-xl font-bold text-gray-900">
                ${portfolio.balance.toLocaleString()}
              </p>
            </div>
          </div>
        </div>
        
        <div className="card">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-accent-100 rounded-xl flex items-center justify-center">
              <PieChart className="w-5 h-5 text-accent-500" />
            </div>
            <div>
              <p className="text-sm text-gray-500">{stocksText.portfolioValue}</p>
              <p className="text-xl font-bold text-gray-900">
                ${portfolio.totalValue.toLocaleString()}
              </p>
            </div>
          </div>
        </div>
        
        <div className="card">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-green-100 rounded-xl flex items-center justify-center">
              <TrendingUp className="w-5 h-5 text-green-500" />
            </div>
            <div>
              <p className="text-sm text-gray-500">{stocksText.totalGainLoss}</p>
              <p className="text-xl font-bold text-green-600">+$0.00</p>
            </div>
          </div>
        </div>
        
        <div className="card">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-secondary-100 rounded-xl flex items-center justify-center">
              <Clock className="w-5 h-5 text-secondary-500" />
            </div>
            <div>
              <p className="text-sm text-gray-500">{stocksText.holdings}</p>
              <p className="text-xl font-bold text-gray-900">
                {portfolio.holdings.length} {stocksText.stocks.toLowerCase()}
              </p>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Stock List */}
        <div className="lg:col-span-1">
          <div className="card p-4">
            <h2 className="text-lg font-bold text-gray-900 mb-4">{stocksText.stocks}</h2>
            
            {loading ? (
              <div className="space-y-3">
                {[1, 2, 3, 4, 5].map(i => (
                  <div key={i} className="animate-pulse">
                    <div className="h-20 bg-gray-100 rounded-xl" />
                  </div>
                ))}
              </div>
            ) : (
              <div className="space-y-3 max-h-[600px] overflow-y-auto pr-2">
                {stocks.map(stock => (
                  <StockCard
                    key={stock.id}
                    stock={stock}
                    isSelected={selectedStock?.id === stock.id}
                    onClick={() => setSelectedStock(stock)}
                  />
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Chart and Trading */}
        <div className="lg:col-span-2">
          {selectedStock ? (
            <div className="card">
              {/* Stock header */}
              <div className="flex items-start justify-between mb-6">
                <div>
                  <div className="flex items-center gap-3 mb-1">
                    <h2 className="text-2xl font-bold text-gray-900">
                      {selectedStock.symbol}
                    </h2>
                    <span className={clsx(
                      'flex items-center gap-1 px-2 py-1 rounded-lg text-sm font-medium',
                      selectedStock.price_change >= 0 
                        ? 'bg-green-100 text-green-700'
                        : 'bg-red-100 text-red-700'
                    )}>
                      {selectedStock.price_change >= 0 ? (
                        <TrendingUp className="w-4 h-4" />
                      ) : (
                        <TrendingDown className="w-4 h-4" />
                      )}
                      {selectedStock.price_change >= 0 ? '+' : ''}
                      {selectedStock.price_change_percent?.toFixed(2)}%
                    </span>
                  </div>
                  <p className="text-gray-500">{selectedStock.name}</p>
                </div>
                <div className="text-right">
                  <p className="text-3xl font-bold text-gray-900">
                    ${selectedStock.current_price?.toFixed(2)}
                  </p>
                  <p className={clsx(
                    'text-sm',
                    selectedStock.price_change >= 0 ? 'text-green-600' : 'text-red-600'
                  )}>
                    {selectedStock.price_change >= 0 ? '+' : ''}
                    ${selectedStock.price_change?.toFixed(2)} {stocksText.today}
                  </p>
                </div>
              </div>

              {/* Period selector */}
              <div className="flex gap-2 mb-4">
                {periods.map(period => (
                  <button
                    key={period.value}
                    onClick={() => setChartPeriod(period.value)}
                    className={clsx(
                      'px-3 py-1.5 rounded-lg text-sm font-medium transition-colors',
                      chartPeriod === period.value
                        ? 'bg-primary-500 text-white'
                        : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                    )}
                  >
                    {period.label}
                  </button>
                ))}
              </div>

              {/* Chart */}
              <StockChart
                data={chartData}
                symbol={selectedStock.symbol}
                isPositive={selectedStock.price_change >= 0}
              />

              {/* Trading buttons */}
              <div className="flex gap-3 mt-6 pt-6 border-t border-gray-100">
                <button
                  onClick={() => setTradeModal({ open: true, type: 'buy' })}
                  className="btn flex-1 bg-green-500 text-white hover:bg-green-600 py-3"
                >
                  {stocksText.buy}
                </button>
                <button
                  onClick={() => setTradeModal({ open: true, type: 'sell' })}
                  className="btn flex-1 bg-red-500 text-white hover:bg-red-600 py-3"
                >
                  {stocksText.sell}
                </button>
              </div>
            </div>
          ) : (
            <div className="card flex flex-col items-center justify-center h-96 text-center">
              <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mb-4">
                <TrendingUp className="w-8 h-8 text-gray-400" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                {stocksText.selectStock}
              </h3>
              <p className="text-gray-500">
                {stocksText.selectStockDesc}
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Trade Modal */}
      {tradeModal.open && selectedStock && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-white rounded-2xl p-6 w-full max-w-md mx-4">
            <h3 className="text-xl font-bold text-gray-900 mb-4">
              {tradeModal.type === 'buy' ? stocksText.buy : stocksText.sell} {selectedStock.symbol}
            </h3>
            
            <div className="mb-4">
              <p className="text-sm text-gray-500 mb-1">Precio Actual</p>
              <p className="text-2xl font-bold text-gray-900">
                ${selectedStock.current_price?.toFixed(2)}
              </p>
            </div>

            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                {stocksText.numberOfShares}
              </label>
              <input
                type="number"
                value={tradeAmount}
                onChange={(e) => setTradeAmount(e.target.value)}
                placeholder={stocksText.enterAmount}
                className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
              />
            </div>

            {tradeAmount && (
              <div className="bg-gray-50 rounded-xl p-4 mb-4">
                <div className="flex justify-between text-sm mb-2">
                  <span className="text-gray-500">{stocksText.estimatedTotal}</span>
                  <span className="font-semibold text-gray-900">
                    ${(parseFloat(tradeAmount) * selectedStock.current_price).toFixed(2)}
                  </span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-500">{stocksText.availableBalance}</span>
                  <span className="font-semibold text-gray-900">
                    ${portfolio.balance.toLocaleString()}
                  </span>
                </div>
              </div>
            )}

            <div className="flex gap-3">
              <button
                onClick={() => setTradeModal({ open: false, type: 'buy' })}
                className="btn btn-outline flex-1"
              >
                {stocksText.cancel}
              </button>
              <button
                onClick={handleTrade}
                disabled={!tradeAmount || parseFloat(tradeAmount) <= 0}
                className={clsx(
                  'btn flex-1 text-white',
                  tradeModal.type === 'buy' 
                    ? 'bg-green-500 hover:bg-green-600'
                    : 'bg-red-500 hover:bg-red-600',
                  'disabled:opacity-50 disabled:cursor-not-allowed'
                )}
              >
                {tradeModal.type === 'buy' ? stocksText.confirmBuy : stocksText.confirmSell}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Info banner */}
      <div className="mt-6 bg-accent-50 border border-accent-200 rounded-xl p-4 flex items-start gap-3">
        <AlertCircle className="w-5 h-5 text-accent-500 flex-shrink-0 mt-0.5" />
        <div>
          <p className="font-medium text-accent-700">{stocksText.paperTradingMode}</p>
          <p className="text-sm text-accent-600">
            {stocksText.paperTradingDesc}
          </p>
        </div>
      </div>
    </div>
  );
}

export default StockSimulation;
