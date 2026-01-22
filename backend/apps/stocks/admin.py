"""
Admin configuration for Stocks app.
"""

from django.contrib import admin
from .models import Stock, StockPriceHistory, Portfolio, Transaction, Watchlist


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    """Admin for Stock model."""
    
    list_display = ['symbol', 'name', 'sector', 'current_price', 'price_change_display', 'last_updated']
    list_filter = ['sector']
    search_fields = ['symbol', 'name']
    readonly_fields = ['last_updated']
    
    def price_change_display(self, obj):
        change = obj.price_change_percent
        sign = '+' if change >= 0 else ''
        return f'{sign}{change:.2f}%'
    price_change_display.short_description = 'Change %'


@admin.register(StockPriceHistory)
class StockPriceHistoryAdmin(admin.ModelAdmin):
    """Admin for StockPriceHistory model."""
    
    list_display = ['stock', 'timestamp', 'close_price', 'volume']
    list_filter = ['stock']
    date_hierarchy = 'timestamp'


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    """Admin for Portfolio model."""
    
    list_display = ['user', 'stock', 'shares', 'average_buy_price', 'current_value_display']
    list_filter = ['stock']
    search_fields = ['user__username', 'stock__symbol']
    
    def current_value_display(self, obj):
        return f'${obj.current_value:,.2f}'
    current_value_display.short_description = 'Current Value'


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """Admin for Transaction model."""
    
    list_display = ['user', 'stock', 'transaction_type', 'shares', 'price_per_share', 'total_amount', 'executed_at']
    list_filter = ['transaction_type', 'stock', 'executed_at']
    search_fields = ['user__username', 'stock__symbol']
    date_hierarchy = 'executed_at'


@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    """Admin for Watchlist model."""
    
    list_display = ['user', 'stock', 'added_at']
    list_filter = ['stock']
    search_fields = ['user__username', 'stock__symbol']
