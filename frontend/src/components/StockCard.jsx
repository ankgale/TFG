import { TrendingUp, TrendingDown, Minus } from 'lucide-react';
import clsx from 'clsx';

function StockCard({ stock, onClick, isSelected = false }) {
  const priceChange = stock.price_change || 0;
  const priceChangePercent = stock.price_change_percent || 0;
  const isPositive = priceChange > 0;
  const isNegative = priceChange < 0;

  const TrendIcon = isPositive ? TrendingUp : isNegative ? TrendingDown : Minus;

  return (
    <div
      onClick={onClick}
      className={clsx(
        'card cursor-pointer transition-all duration-200',
        isSelected 
          ? 'ring-2 ring-primary-500 border-primary-200' 
          : 'hover:shadow-md hover:border-gray-200',
      )}
    >
      <div className="flex items-start justify-between mb-2">
        <div>
          <h3 className="font-bold text-lg text-gray-900">{stock.symbol}</h3>
          <p className="text-sm text-gray-500 truncate max-w-[150px]">{stock.name}</p>
        </div>
        <div className={clsx(
          'flex items-center gap-1 px-2 py-1 rounded-lg text-sm font-medium',
          isPositive && 'bg-green-100 text-green-700',
          isNegative && 'bg-red-100 text-red-700',
          !isPositive && !isNegative && 'bg-gray-100 text-gray-600'
        )}>
          <TrendIcon className="w-4 h-4" />
          <span>{isPositive ? '+' : ''}{priceChangePercent.toFixed(2)}%</span>
        </div>
      </div>

      <div className="flex items-end justify-between">
        <div>
          <p className="text-2xl font-bold text-gray-900">
            ${stock.current_price?.toFixed(2) || '0.00'}
          </p>
          <p className={clsx(
            'text-sm',
            isPositive && 'text-green-600',
            isNegative && 'text-red-600',
            !isPositive && !isNegative && 'text-gray-500'
          )}>
            {isPositive ? '+' : ''}${priceChange.toFixed(2)}
          </p>
        </div>
        <div className="text-right text-xs text-gray-400">
          <p>{stock.sector}</p>
        </div>
      </div>
    </div>
  );
}

export default StockCard;
