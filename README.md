# FinLearn - Duolingo-Style Financial Education App

A production-ready template for a gamified financial education platform featuring interactive learning modules and a stock market simulation.

## Features

- **Learning Modules**: Duolingo-style lessons with interactive quizzes
- **Gamification**: XP points, levels, streaks, and achievements
- **Stock Market Simulation**: Paper trading with real-time stock data
- **Real-time Updates**: WebSocket support for live stock prices
- **Modern UI**: Beautiful, responsive Duolingo-inspired design
- **Spanish UI**: All user-facing text in Spanish (code remains in English)

## Tech Stack

### Backend
- **Django 5.x** - Web framework
- **Django REST Framework** - API development
- **Django Channels** - WebSocket support for real-time features
- **SQLite** (development) / **PostgreSQL** (production)
- **yfinance** - Stock market data

### Frontend
- **React 18** - UI library
- **Vite** - Build tool and dev server
- **TailwindCSS** - Styling
- **Recharts** - Stock charts
- **React Router** - Navigation
- **Lucide React** - Icons

## Project Structure

```
tfg/
├── backend/
│   ├── config/                 # Django project configuration
│   │   ├── settings.py         # Main settings
│   │   ├── urls.py             # Root URL configuration
│   │   ├── asgi.py             # ASGI config (WebSocket support)
│   │   └── wsgi.py             # WSGI config
│   ├── apps/
│   │   ├── users/              # User management & gamification
│   │   │   ├── models.py       # User, Achievement models
│   │   │   ├── views.py        # User API endpoints
│   │   │   ├── serializers.py  # DRF serializers
│   │   │   └── urls.py         # URL routing
│   │   ├── lessons/            # Learning content
│   │   │   ├── models.py       # Module, Lesson, Quiz models
│   │   │   ├── views.py        # Lessons API endpoints
│   │   │   ├── serializers.py  # DRF serializers
│   │   │   └── urls.py         # URL routing
│   │   └── stocks/             # Stock simulation
│   │       ├── models.py       # Stock, Portfolio, Transaction models
│   │       ├── views.py        # Stocks API endpoints
│   │       ├── services.py     # Stock data fetching (yfinance)
│   │       ├── consumers.py    # WebSocket consumers
│   │       ├── routing.py      # WebSocket routing
│   │       └── config.py       # Tracked stocks configuration
│   ├── requirements.txt        # Python dependencies
│   └── manage.py               # Django CLI
├── frontend/
│   ├── src/
│   │   ├── components/         # Reusable UI components
│   │   │   ├── Layout.jsx      # Main layout with sidebar
│   │   │   ├── Sidebar.jsx     # Navigation sidebar
│   │   │   ├── ModuleCard.jsx  # Learning module card
│   │   │   ├── StockCard.jsx   # Stock display card
│   │   │   └── StockChart.jsx  # Price chart component
│   │   ├── pages/              # Page components
│   │   │   ├── Dashboard.jsx   # Learning modules dashboard
│   │   │   ├── LessonDetail.jsx # Lesson content & quiz
│   │   │   └── StockSimulation.jsx # Trading simulation
│   │   ├── services/           # API services
│   │   │   └── api.js          # Backend API client
│   │   ├── hooks/              # Custom React hooks
│   │   │   └── useWebSocket.js # WebSocket hook for real-time data
│   │   ├── App.jsx             # Main app component
│   │   ├── main.jsx            # Entry point
│   │   └── index.css           # Global styles
│   ├── package.json            # Node dependencies
│   ├── vite.config.js          # Vite configuration
│   ├── tailwind.config.js      # Tailwind configuration
│   └── index.html              # HTML template
└── README.md
```

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- npm or pnpm

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser** (optional, for admin access):
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

   The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory** (in a new terminal):
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start the development server**:
   ```bash
   npm run dev
   ```

   The app will be available at `http://localhost:5173`

## API Endpoints

### Lessons API (`/api/lessons/`)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/modules/` | GET | List all modules |
| `/modules/{id}/` | GET | Get module details |
| `/modules/{id}/lessons/` | GET | Get lessons for a module |
| `/lessons/` | GET | List all lessons |
| `/lessons/{id}/` | GET | Get lesson details with quizzes |
| `/lessons/{id}/start/` | POST | Mark lesson as started |
| `/lessons/{id}/complete/` | POST | Mark lesson as completed |
| `/quizzes/{id}/answer/` | POST | Submit quiz answer |
| `/progress/summary/` | GET | Get progress summary |

### Stocks API (`/api/stocks/`)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/stocks/` | GET | List all stocks |
| `/stocks/{id}/` | GET | Get stock details |
| `/stocks/{id}/history/` | GET | Get price history |
| `/stocks/{id}/quote/` | GET | Get real-time quote |
| `/stocks/initialize/` | POST | Initialize stocks from config |
| `/stocks/refresh/` | POST | Refresh all stock prices |
| `/portfolio/` | GET | Get user portfolio |
| `/portfolio/summary/` | GET | Get portfolio summary |
| `/trade/` | POST | Execute buy/sell trade |
| `/transactions/` | GET | Get transaction history |
| `/watchlist/` | GET, POST, DELETE | Manage watchlist |

### Users API (`/api/users/`)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | List users |
| `/{id}/` | GET | Get user details |
| `/{id}/progress/` | GET | Get user progress |
| `/{id}/add_xp/` | POST | Add XP to user |
| `/achievements/` | GET | List achievements |
| `/user-achievements/` | GET | Get user achievements |

### WebSocket

| Endpoint | Description |
|----------|-------------|
| `ws://localhost:8000/ws/stocks/` | Real-time stock price updates |

**WebSocket Messages:**
```javascript
// Request current prices
{ "action": "get_prices" }

// Request price history
{ "action": "get_history", "symbol": "AAPL", "period": "1mo" }

// Refresh prices from API
{ "action": "refresh" }
```

## Configuration

### Changing Tracked Stocks

Edit `backend/apps/stocks/config.py`:

```python
TRACKED_STOCKS = [
    ('AAPL', 'Apple Inc.', 'Technology'),
    ('MSFT', 'Microsoft Corporation', 'Technology'),
    # Add or modify stocks here
]
```

After changing, run:
```bash
python manage.py shell
>>> from apps.stocks.services import StockService
>>> StockService.initialize_stocks()
>>> StockService.update_stock_prices()
```

### Environment Variables

Create a `.env` file in the backend directory:

```bash
# Django Settings
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

## Database Models

### Users App

- **User**: Extended Django user with XP, level, streak, virtual balance
- **Achievement**: Unlockable achievements with conditions
- **UserAchievement**: Many-to-many tracking unlocked achievements

### Lessons App

- **Module**: Learning modules containing lessons
- **Lesson**: Individual lessons with content and quizzes
- **Quiz**: Multiple choice questions
- **QuizOption**: Answer options for quizzes
- **UserLessonProgress**: Track user progress through lessons
- **UserModuleProgress**: Track user progress through modules

### Stocks App

- **Stock**: Stock information and latest prices
- **StockPriceHistory**: Historical price data
- **Portfolio**: User stock holdings
- **Transaction**: Buy/sell transaction records
- **Watchlist**: User stock watchlist

## Development

### Running Tests

```bash
# Backend
cd backend
python manage.py test

# Frontend
cd frontend
npm run lint
```

### Building for Production

```bash
# Frontend build
cd frontend
npm run build

# The build output will be in frontend/dist/
```

## Internationalization (i18n)

The app UI is in **Spanish** while all code remains in **English**. Translations are managed in a single file:

```
frontend/src/i18n/translations.js
```

### Translation Structure

```javascript
import translations from '../i18n/translations';

// Access translations
const { dashboard, stocks, lesson } = translations;

// Use in components
<h1>{dashboard.title}</h1>  // "Módulos de Aprendizaje"
```

### Adding/Modifying Translations

Edit `frontend/src/i18n/translations.js`:

```javascript
const translations = {
  dashboard: {
    title: 'Módulos de Aprendizaje',
    // Add more translations here
  },
  // ...
};
```

### Adding Another Language

To add support for multiple languages:

1. Create language-specific files (e.g., `es.js`, `en.js`)
2. Create a language context/provider
3. Switch translations based on user preference

## Future Enhancements

- [ ] User authentication (JWT/Session)
- [ ] Social features (leaderboards, friends)
- [ ] More lesson types (video, interactive exercises)
- [ ] Advanced trading features (limit orders, stop-loss)
- [ ] Portfolio analytics and performance tracking
- [ ] Mobile-responsive improvements
- [ ] Push notifications for streaks and achievements
- [ ] Docker containerization
- [ ] CI/CD pipeline

## License

This project is for educational purposes. Stock data is provided by Yahoo Finance through the yfinance library.

---

Built with Django + React for the TFG project.
