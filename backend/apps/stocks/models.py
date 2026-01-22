"""
Stock models for FinLearn.
Paper trading simulation with real stock data.
"""

from django.db import models
from django.conf import settings
from decimal import Decimal


class Stock(models.Model):
    """
    Stock information and latest price data.
    """
    
    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=200)
    sector = models.CharField(max_length=100, blank=True)
    
    # Latest price data (updated periodically)
    current_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    previous_close = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    day_high = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    day_low = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    volume = models.BigIntegerField(default=0)
    market_cap = models.BigIntegerField(default=0)
    
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'stocks'
        ordering = ['symbol']
    
    def __str__(self):
        return f"{self.symbol} - {self.name}"
    
    @property
    def price_change(self) -> Decimal:
        """Calculate price change from previous close."""
        if self.previous_close == 0:
            return Decimal('0')
        return self.current_price - self.previous_close
    
    @property
    def price_change_percent(self) -> Decimal:
        """Calculate percentage price change."""
        if self.previous_close == 0:
            return Decimal('0')
        return ((self.current_price - self.previous_close) / self.previous_close) * 100


class StockPriceHistory(models.Model):
    """
    Historical price data for charts.
    """
    
    stock = models.ForeignKey(
        Stock,
        on_delete=models.CASCADE,
        related_name='price_history'
    )
    
    timestamp = models.DateTimeField()
    open_price = models.DecimalField(max_digits=12, decimal_places=2)
    high_price = models.DecimalField(max_digits=12, decimal_places=2)
    low_price = models.DecimalField(max_digits=12, decimal_places=2)
    close_price = models.DecimalField(max_digits=12, decimal_places=2)
    volume = models.BigIntegerField(default=0)
    
    class Meta:
        db_table = 'stock_price_history'
        ordering = ['-timestamp']
        unique_together = ['stock', 'timestamp']
    
    def __str__(self):
        return f"{self.stock.symbol} @ {self.timestamp}"


class Portfolio(models.Model):
    """
    User's stock portfolio for paper trading.
    """
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='portfolio',
        null=True,  # Nullable for now (no auth yet)
        blank=True
    )
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    
    shares = models.DecimalField(max_digits=12, decimal_places=4, default=0)
    average_buy_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'portfolios'
        unique_together = ['user', 'stock']
    
    def __str__(self):
        return f"{self.user} - {self.stock.symbol}: {self.shares} shares"
    
    @property
    def current_value(self) -> Decimal:
        """Calculate current value of holdings."""
        return self.shares * self.stock.current_price
    
    @property
    def total_cost(self) -> Decimal:
        """Calculate total cost of holdings."""
        return self.shares * self.average_buy_price
    
    @property
    def profit_loss(self) -> Decimal:
        """Calculate profit/loss."""
        return self.current_value - self.total_cost
    
    @property
    def profit_loss_percent(self) -> Decimal:
        """Calculate profit/loss percentage."""
        if self.total_cost == 0:
            return Decimal('0')
        return (self.profit_loss / self.total_cost) * 100


class Transaction(models.Model):
    """
    Record of all buy/sell transactions.
    """
    
    TRANSACTION_TYPES = [
        ('buy', 'Buy'),
        ('sell', 'Sell'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='transactions',
        null=True,  # Nullable for now (no auth yet)
        blank=True
    )
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    
    transaction_type = models.CharField(max_length=4, choices=TRANSACTION_TYPES)
    shares = models.DecimalField(max_digits=12, decimal_places=4)
    price_per_share = models.DecimalField(max_digits=12, decimal_places=2)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    
    executed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'transactions'
        ordering = ['-executed_at']
    
    def __str__(self):
        return f"{self.transaction_type.upper()} {self.shares} {self.stock.symbol} @ ${self.price_per_share}"


class Watchlist(models.Model):
    """
    User's watchlist for tracking stocks.
    """
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='watchlist',
        null=True,  # Nullable for now (no auth yet)
        blank=True
    )
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'watchlists'
        unique_together = ['user', 'stock']
    
    def __str__(self):
        return f"{self.user} watching {self.stock.symbol}"
