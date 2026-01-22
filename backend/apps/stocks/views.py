"""
API views for Stocks app.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from decimal import Decimal

from .models import Stock, Portfolio, Transaction, Watchlist
from .serializers import (
    StockSerializer, StockListSerializer,
    PortfolioSerializer, TransactionSerializer,
    WatchlistSerializer, TradeSerializer
)
from .services import StockService
from .config import STOCK_SYMBOLS


class StockViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Stock model.
    Read-only as stocks are managed through services.
    """
    
    queryset = Stock.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return StockListSerializer
        return StockSerializer
    
    @action(detail=False, methods=['post'])
    def refresh(self, request):
        """Refresh stock prices from external API."""
        updated = StockService.update_stock_prices()
        return Response({
            'message': f'Updated {updated} stocks',
            'updated_count': updated
        })
    
    @action(detail=False, methods=['post'])
    def initialize(self, request):
        """Initialize stocks from config."""
        stocks = StockService.initialize_stocks()
        serializer = StockListSerializer(stocks, many=True)
        return Response({
            'message': f'Initialized {len(stocks)} stocks',
            'stocks': serializer.data
        })
    
    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
        """Get price history for a stock."""
        stock = self.get_object()
        period = request.query_params.get('period', '1mo')
        
        history = StockService.fetch_price_history(stock.symbol, period)
        
        return Response({
            'symbol': stock.symbol,
            'period': period,
            'history': history
        })
    
    @action(detail=True, methods=['get'])
    def quote(self, request, pk=None):
        """Get real-time quote for a stock."""
        stock = self.get_object()
        quote = StockService.get_stock_quote(stock.symbol)
        
        if quote:
            return Response(quote)
        return Response(
            {'error': 'Failed to fetch quote'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )


class PortfolioViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Portfolio model.
    """
    
    serializer_class = PortfolioSerializer
    
    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        queryset = Portfolio.objects.select_related('stock')
        
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get portfolio summary for a user."""
        user_id = request.query_params.get('user_id')
        
        if not user_id:
            return Response({
                'total_value': 0,
                'total_cost': 0,
                'total_profit_loss': 0,
                'holdings_count': 0
            })
        
        holdings = Portfolio.objects.filter(user_id=user_id).select_related('stock')
        
        total_value = sum(h.current_value for h in holdings)
        total_cost = sum(h.total_cost for h in holdings)
        
        return Response({
            'total_value': float(total_value),
            'total_cost': float(total_cost),
            'total_profit_loss': float(total_value - total_cost),
            'profit_loss_percent': float(((total_value - total_cost) / total_cost) * 100) if total_cost > 0 else 0,
            'holdings_count': holdings.count()
        })


class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Transaction model.
    """
    
    serializer_class = TransactionSerializer
    
    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        queryset = Transaction.objects.select_related('stock')
        
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        
        return queryset


class TradeView(APIView):
    """
    API endpoint for executing trades.
    """
    
    def post(self, request):
        """Execute a buy or sell trade."""
        serializer = TradeSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        user_id = data.get('user_id')
        stock_id = data['stock_id']
        shares = Decimal(str(data['shares']))
        transaction_type = data['transaction_type']
        
        try:
            stock = Stock.objects.get(id=stock_id)
        except Stock.DoesNotExist:
            return Response(
                {'error': 'Stock not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if stock.current_price <= 0:
            return Response(
                {'error': 'Stock price not available'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        total_amount = shares * stock.current_price
        
        if transaction_type == 'buy':
            result = self._execute_buy(user_id, stock, shares, total_amount)
        else:
            result = self._execute_sell(user_id, stock, shares, total_amount)
        
        if 'error' in result:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(result)
    
    def _execute_buy(self, user_id, stock, shares, total_amount):
        """Execute a buy order."""
        from apps.users.models import User
        
        # Check user balance (if user exists)
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                if user.virtual_balance < total_amount:
                    return {'error': 'Insufficient balance'}
                
                user.virtual_balance -= total_amount
                user.save()
            except User.DoesNotExist:
                pass
        
        # Update or create portfolio
        portfolio, created = Portfolio.objects.get_or_create(
            user_id=user_id,
            stock=stock,
            defaults={
                'shares': shares,
                'average_buy_price': stock.current_price
            }
        )
        
        if not created:
            # Calculate new average price
            total_shares = portfolio.shares + shares
            total_cost = (portfolio.shares * portfolio.average_buy_price) + total_amount
            portfolio.average_buy_price = total_cost / total_shares
            portfolio.shares = total_shares
            portfolio.save()
        
        # Record transaction
        transaction = Transaction.objects.create(
            user_id=user_id,
            stock=stock,
            transaction_type='buy',
            shares=shares,
            price_per_share=stock.current_price,
            total_amount=total_amount
        )
        
        return {
            'message': f'Successfully bought {shares} shares of {stock.symbol}',
            'transaction': TransactionSerializer(transaction).data,
            'portfolio': PortfolioSerializer(portfolio).data
        }
    
    def _execute_sell(self, user_id, stock, shares, total_amount):
        """Execute a sell order."""
        from apps.users.models import User
        
        # Check portfolio
        try:
            portfolio = Portfolio.objects.get(user_id=user_id, stock=stock)
        except Portfolio.DoesNotExist:
            return {'error': 'No shares to sell'}
        
        if portfolio.shares < shares:
            return {'error': f'Insufficient shares. You have {portfolio.shares}'}
        
        # Update user balance
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                user.virtual_balance += total_amount
                user.save()
            except User.DoesNotExist:
                pass
        
        # Update portfolio
        portfolio.shares -= shares
        if portfolio.shares == 0:
            portfolio.delete()
            portfolio_data = None
        else:
            portfolio.save()
            portfolio_data = PortfolioSerializer(portfolio).data
        
        # Record transaction
        transaction = Transaction.objects.create(
            user_id=user_id,
            stock=stock,
            transaction_type='sell',
            shares=shares,
            price_per_share=stock.current_price,
            total_amount=total_amount
        )
        
        return {
            'message': f'Successfully sold {shares} shares of {stock.symbol}',
            'transaction': TransactionSerializer(transaction).data,
            'portfolio': portfolio_data
        }


class WatchlistViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Watchlist model.
    """
    
    serializer_class = WatchlistSerializer
    
    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        queryset = Watchlist.objects.select_related('stock')
        
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        
        return queryset
    
    def perform_create(self, serializer):
        user_id = self.request.data.get('user_id')
        serializer.save(user_id=user_id)
