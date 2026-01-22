"""
URL configuration for Stocks app.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    StockViewSet, PortfolioViewSet, TransactionViewSet,
    WatchlistViewSet, TradeView
)

router = DefaultRouter()
router.register(r'stocks', StockViewSet, basename='stock')
router.register(r'portfolio', PortfolioViewSet, basename='portfolio')
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'watchlist', WatchlistViewSet, basename='watchlist')

urlpatterns = [
    path('', include(router.urls)),
    path('trade/', TradeView.as_view(), name='trade'),
]
