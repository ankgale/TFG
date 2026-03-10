import { useState, useEffect } from 'react';
import { ArrowUpRight, ArrowDownRight, Clock, Loader2 } from 'lucide-react';
import clsx from 'clsx';
import { stocksApi } from '../services/api';
import { useAuth } from '../contexts/AuthContext';
import translations from '../i18n/translations';

function TransactionHistory() {
  const { isAuthenticated } = useAuth();
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchTransactions() {
      if (!isAuthenticated) {
        setLoading(false);
        return;
      }
      try {
        const data = await stocksApi.getTransactions();
        setTransactions(data?.results ?? data ?? []);
      } catch (err) {
        console.log('Failed to fetch transactions:', err.message);
      } finally {
        setLoading(false);
      }
    }
    fetchTransactions();
  }, [isAuthenticated]);

  const formatDate = (iso) => {
    if (!iso) return '';
    const d = new Date(iso);
    return d.toLocaleDateString('es-ES', {
      day: '2-digit',
      month: 'short',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 mb-1">
            Historial de Operaciones
          </h1>
          <p className="text-gray-500">
            {transactions.length} operaciones registradas
          </p>
        </div>
        <div className="w-14 h-14 bg-primary-100 rounded-2xl flex items-center justify-center">
          <Clock className="w-7 h-7 text-primary-500" />
        </div>
      </div>

      {!isAuthenticated ? (
        <div className="card text-center py-16 text-gray-400">
          Inicia sesión para ver tu historial de operaciones.
        </div>
      ) : loading ? (
        <div className="flex flex-col items-center justify-center py-20">
          <Loader2 className="w-10 h-10 text-primary-500 animate-spin mb-3" />
          <p className="text-sm text-gray-500">{translations.common.loading}</p>
        </div>
      ) : transactions.length === 0 ? (
        <div className="card text-center py-16 text-gray-400">
          No has realizado ninguna operación todavía.
        </div>
      ) : (
        <div className="space-y-3">
          {transactions.map((tx) => {
            const isBuy = tx.transaction_type === 'buy';
            return (
              <div key={tx.id} className="card flex items-center gap-4">
                <div
                  className={clsx(
                    'w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0',
                    isBuy ? 'bg-green-100' : 'bg-red-100'
                  )}
                >
                  {isBuy ? (
                    <ArrowDownRight className="w-5 h-5 text-green-600" />
                  ) : (
                    <ArrowUpRight className="w-5 h-5 text-red-600" />
                  )}
                </div>

                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <span className="font-semibold text-gray-900">
                      {tx.stock_symbol || tx.stock?.symbol || '—'}
                    </span>
                    <span
                      className={clsx(
                        'text-xs font-medium px-2 py-0.5 rounded-full',
                        isBuy
                          ? 'bg-green-100 text-green-700'
                          : 'bg-red-100 text-red-700'
                      )}
                    >
                      {isBuy ? 'Compra' : 'Venta'}
                    </span>
                  </div>
                  <p className="text-xs text-gray-400 mt-0.5">
                    {formatDate(tx.executed_at)}
                  </p>
                </div>

                <div className="text-right flex-shrink-0">
                  <p className="font-semibold text-gray-900">
                    {tx.shares} acc. × ${parseFloat(tx.price_per_share).toFixed(2)}
                  </p>
                  <p
                    className={clsx(
                      'text-sm font-medium',
                      isBuy ? 'text-green-600' : 'text-red-600'
                    )}
                  >
                    {isBuy ? '-' : '+'}${parseFloat(tx.total_amount).toLocaleString()}
                  </p>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

export default TransactionHistory;
