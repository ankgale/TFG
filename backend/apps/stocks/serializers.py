"""
Serializers for Stocks app.
"""

from rest_framework import serializers
from .models import Stock, StockPriceHistory, Portfolio, Transaction, Watchlist


class StockSerializer(serializers.ModelSerializer):
    """Serializer for Stock model."""
    
    price_change = serializers.ReadOnlyField()
    price_change_percent = serializers.ReadOnlyField()
    
    class Meta:
        model = Stock
        fields = [
            'id', 'symbol', 'name', 'sector',
            'current_price', 'previous_close', 'day_high', 'day_low',
            'volume', 'market_cap', 'price_change', 'price_change_percent',
            'last_updated'
        ]


class StockListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for stock lists."""
    
    price_change = serializers.ReadOnlyField()
    price_change_percent = serializers.ReadOnlyField()
    
    class Meta:
        model = Stock
        fields = [
            'id', 'symbol', 'name', 'sector',
            'current_price', 'price_change', 'price_change_percent'
        ]


class StockPriceHistorySerializer(serializers.ModelSerializer):
    """Serializer for StockPriceHistory model."""
    
    class Meta:
        model = StockPriceHistory
        fields = [
            'timestamp', 'open_price', 'high_price',
            'low_price', 'close_price', 'volume'
        ]


class PortfolioSerializer(serializers.ModelSerializer):
    """Serializer for Portfolio model."""
    
    stock = StockListSerializer(read_only=True)
    stock_id = serializers.PrimaryKeyRelatedField(
        queryset=Stock.objects.all(),
        source='stock',
        write_only=True
    )
    current_value = serializers.ReadOnlyField()
    total_cost = serializers.ReadOnlyField()
    profit_loss = serializers.ReadOnlyField()
    profit_loss_percent = serializers.ReadOnlyField()
    
    class Meta:
        model = Portfolio
        fields = [
            'id', 'user', 'stock', 'stock_id',
            'shares', 'average_buy_price',
            'current_value', 'total_cost', 'profit_loss', 'profit_loss_percent',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'average_buy_price']


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for Transaction model."""
    
    stock = StockListSerializer(read_only=True)
    stock_id = serializers.PrimaryKeyRelatedField(
        queryset=Stock.objects.all(),
        source='stock',
        write_only=True
    )
    
    class Meta:
        model = Transaction
        fields = [
            'id', 'user', 'stock', 'stock_id',
            'transaction_type', 'shares', 'price_per_share',
            'total_amount', 'executed_at'
        ]
        read_only_fields = ['user', 'price_per_share', 'total_amount', 'executed_at']


class WatchlistSerializer(serializers.ModelSerializer):
    """Serializer for Watchlist model."""
    
    stock = StockListSerializer(read_only=True)
    stock_id = serializers.PrimaryKeyRelatedField(
        queryset=Stock.objects.all(),
        source='stock',
        write_only=True
    )
    
    class Meta:
        model = Watchlist
        fields = ['id', 'user', 'stock', 'stock_id', 'added_at']
        read_only_fields = ['user']


class TradeSerializer(serializers.Serializer):
    """Serializer for executing trades."""
    
    stock_id = serializers.IntegerField()
    shares = serializers.DecimalField(max_digits=12, decimal_places=4)
    transaction_type = serializers.ChoiceField(choices=['buy', 'sell'])
    user_id = serializers.IntegerField(required=False, allow_null=True)
