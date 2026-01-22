"""
WebSocket consumers for real-time stock data.
"""

import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .services import StockService
from .config import UPDATE_INTERVAL


class StockPriceConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for real-time stock price updates.
    Clients can subscribe to receive price updates every UPDATE_INTERVAL seconds.
    """
    
    async def connect(self):
        """Handle WebSocket connection."""
        self.room_group_name = 'stock_prices'
        self.update_task = None
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Send initial stock data
        await self.send_stock_prices()
        
        # Start periodic updates
        self.update_task = asyncio.create_task(self.periodic_update())
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection."""
        # Cancel periodic updates
        if self.update_task:
            self.update_task.cancel()
        
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        """Handle incoming WebSocket messages."""
        try:
            data = json.loads(text_data)
            action = data.get('action')
            
            if action == 'get_prices':
                await self.send_stock_prices()
            elif action == 'get_history':
                symbol = data.get('symbol')
                period = data.get('period', '1mo')
                await self.send_stock_history(symbol, period)
            elif action == 'refresh':
                await self.refresh_prices()
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'error': 'Invalid JSON'
            }))
    
    async def periodic_update(self):
        """Periodically send stock price updates."""
        while True:
            await asyncio.sleep(UPDATE_INTERVAL)
            await self.send_stock_prices()
    
    async def send_stock_prices(self):
        """Fetch and send current stock prices."""
        stocks = await self.get_stocks_from_db()
        
        await self.send(text_data=json.dumps({
            'type': 'prices',
            'data': stocks
        }))
    
    async def send_stock_history(self, symbol: str, period: str):
        """Fetch and send stock price history."""
        history = await database_sync_to_async(
            StockService.fetch_price_history
        )(symbol, period)
        
        await self.send(text_data=json.dumps({
            'type': 'history',
            'symbol': symbol,
            'period': period,
            'data': history
        }))
    
    async def refresh_prices(self):
        """Refresh prices from external API and send update."""
        await database_sync_to_async(StockService.update_stock_prices)()
        await self.send_stock_prices()
    
    @database_sync_to_async
    def get_stocks_from_db(self):
        """Get all stocks from database."""
        from .models import Stock
        stocks = Stock.objects.all()
        
        return [
            {
                'id': stock.id,
                'symbol': stock.symbol,
                'name': stock.name,
                'sector': stock.sector,
                'current_price': float(stock.current_price),
                'previous_close': float(stock.previous_close),
                'day_high': float(stock.day_high),
                'day_low': float(stock.day_low),
                'volume': stock.volume,
                'price_change': float(stock.price_change),
                'price_change_percent': float(stock.price_change_percent),
                'last_updated': stock.last_updated.isoformat() if stock.last_updated else None,
            }
            for stock in stocks
        ]
    
    async def stock_price_update(self, event):
        """Handle stock price update from channel layer."""
        await self.send(text_data=json.dumps({
            'type': 'prices',
            'data': event['data']
        }))
