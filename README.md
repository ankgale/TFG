# FinLearn — Duolingo-Style Financial Education

A production-ready **bachelor’s thesis (TFG)** project: a gamified financial learning platform with interactive modules, gamification, and a stock market paper-trading simulation. The **end-user UI is in Spanish**; code and API-facing identifiers stay in **English**.

## Features

- **Learning modules** — lessons with quizzes and per-module progress
- **Gamification** — XP, levels, streaks, achievements, and a daily challenge
- **Stock simulation** — paper trading with live-style quotes via **yfinance**
- **Real-time updates** — WebSockets for price refresh
- **Auth** — registration, login, and **DRF token** authentication (`Authorization: Token …`)
- **App routes** — dashboard, module/lesson flow, trading sim, achievements, transaction history, profile, leaderboard, login/register

## Tech stack

### Backend
- **Django 5.2** — web framework
- **Django REST Framework** — REST API, pagination
- **DRF token auth** and **SessionAuthentication**
- **Django Channels** + **Daphne** — WebSockets; default **in-memory** channel layer (use **Redis** in production)
- **django-cors-headers** — CORS to the Vite dev origin
- **SQLite** in development; **PostgreSQL** dependency included for production-style setups
- **yfinance** — market data

### Frontend
- **React 18** + **Vite 5**
- **TailwindCSS 3**
- **React Router 6**
- **Recharts** — charts
- **Lucide React** — icons
- **date-fns**, **clsx**
- User-visible strings: `frontend/src/i18n/translations.js`

## Repository layout

```
tfg/
├── backend/
│   ├── config/                 # settings, urls, asgi, wsgi
│   ├── apps/
│   │   ├── users/              # user model, auth, achievements, leaderboard, daily challenge
│   │   ├── lessons/            # modules, lessons, quizzes, progress
│   │   └── stocks/             # stocks, portfolio, trades, watchlist, websockets
│   ├── requirements.txt
│   └── manage.py
├── frontend/
│   ├── src/
│   │   ├── components/         # Layout, Sidebar, cards, StockChart, ProtectedRoute, …
│   │   ├── pages/              # Dashboard, ModuleDetail, LessonDetail, StockSimulation, …
│   │   ├── contexts/           # AuthContext
│   │   ├── services/           # api.js (HTTP + token)
│   │   ├── hooks/              # useWebSocket
│   │   ├── i18n/
│   │   ├── App.jsx, main.jsx, index.css
│   ├── vite.config.js          # proxy /api and /ws to the backend
│   ├── package.json
│   └── index.html
└── README.md
```

## Quick start

**Requirements:** Python 3.10+, Node.js 18+, and npm (or pnpm).

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser   # optional, for /admin
python manage.py runserver
```

API base: `http://127.0.0.1:8000/`. With this setup, `runserver` serves the ASGI app (Channels). For production, you typically run an ASGI server (e.g. Daphne) and set **Redis**-backed `CHANNEL_LAYERS` instead of the in-memory layer.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

App URL: `http://127.0.0.1:5173`. The Vite dev server **proxies** `/api` and `/ws` to port 8000, so the React client uses relative URLs like `/api/...` without a separate `VITE_*` base URL in development.

A production `npm run build` outputs to `frontend/dist/`. In a real deployment, host the frontend and API under one origin, or set an explicit API base URL and update **CORS** in `config/settings.py`.

## API (accurate DRF paths)

All routes are prefixed as shown. Trailing slashes follow Django/DRF defaults.

### Users — `/api/users/`

| Path | Method | Description |
|------|--------|-------------|
| `register/` | POST | Create account |
| `login/` | POST | Returns auth token |
| `logout/` | POST | Log out |
| `change-password/` | POST | Change password |
| `profile/` | GET, PUT/PATCH | Update profile (authenticated) |
| `leaderboard/` | GET | Leaderboard |
| `daily-challenge/` | GET | Daily challenge |
| `profiles/` | GET | List user profiles |
| `profiles/{id}/` | GET, … | Profile detail |
| `profiles/{id}/progress/` | GET | Level, XP, streak, etc. |
| `profiles/{id}/add_xp/` | POST | Add XP (body: `amount`) |
| `achievements/` | GET | All achievements |
| `user-achievements/` | GET | Unlocked achievements |

Send `Authorization: Token <key>` for authenticated requests after login.

### Lessons — `/api/lessons/`

| Path | Method | Description |
|------|--------|-------------|
| `modules/` | GET | Published modules |
| `modules/{id}/` | GET | Module detail |
| `modules/{id}/lessons/` | GET | Lessons in a module |
| `lessons/` | GET | Lessons (optional `?module_id=`) |
| `lessons/{id}/` | GET | Lesson with quizzes (detail serializer) |
| `lessons/{id}/quizzes/` | GET | Quizzes for that lesson |
| `lessons/{id}/start/` | POST | Start lesson (auth required) |
| `lessons/{id}/complete/` | POST | Complete lesson (e.g. `score`) |
| `quizzes/{id}/` | GET | Quiz detail |
| `quizzes/{id}/answer/` | POST | Check answer (`option_id`) |
| `progress/` | GET | User module progress rows |
| `progress/summary/` | GET | Overall summary |
| `progress/completed_lessons/` | GET | Completed lesson IDs |
| `progress/module_progress/` | GET | Per-module progress map |

### Stocks — `/api/stocks/`

Because the router registers the `Stock` view on the basename `stocks`, the collection URL is **`/api/stocks/stocks/`** (repeated `stocks` segment).

| Path | Method | Description |
|------|--------|-------------|
| `stocks/stocks/` | GET | List stocks |
| `stocks/stocks/{id}/` | GET | Stock detail |
| `stocks/stocks/initialize/` | POST | Seed from config |
| `stocks/stocks/refresh/` | POST | Refresh prices from API |
| `stocks/stocks/{id}/history/` | GET | History (`?period=1mo`, etc.) |
| `stocks/stocks/{id}/quote/` | GET | Current quote |
| `stocks/portfolio/` | GET | Holdings |
| `stocks/portfolio/summary/` | GET | Portfolio summary |
| `stocks/transactions/` | GET | Trades list |
| `stocks/watchlist/` | GET, POST, … | Watchlist CRUD (per user) |
| `stocks/trade/` | POST | Buy/sell (`stock_id`, `shares`, `transaction_type`) |

### WebSocket

- **URL:** `ws://localhost:8000/ws/stocks/` (Vite’s dev server proxies `/ws` to the same path on the backend; see `frontend/vite.config.js` and `apps/stocks/routing.py`)

Example message shapes (match your consumer):

```javascript
{ "action": "get_prices" }
{ "action": "get_history", "symbol": "AAPL", "period": "1mo" }
{ "action": "refresh" }
```

## Configuration

### Tracked tickers

Edit `backend/apps/stocks/config.py` (`TRACKED_STOCKS`), then in Django shell:

```python
from apps.stocks.services import StockService
StockService.initialize_stocks()
StockService.update_stock_prices()
```

### Environment (backend)

Create `backend/.env` as needed, for example:

```bash
DJANGO_SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

Adjust `CORS_ALLOWED_ORIGINS` and the database in `config/settings.py` for staging/production.

## Data model (overview)

- **users** — `User` (XP, level, streak, virtual balance), `Achievement`, `UserAchievement`, …
- **lessons** — `Module`, `Lesson`, `Quiz`, `QuizOption`, lesson and module progress
- **stocks** — `Stock`, price history, `Portfolio`, `Transaction`, `Watchlist`

## Development

```bash
# Backend
cd backend && python manage.py test

# Frontend
cd frontend && npm run lint
```

`requirements.txt` also includes **Black**, **Ruff**, **mypy**, **flake8**, and **pre-commit** for local quality checks if you add a pre-commit config.

## i18n (frontend)

Spanish UI strings live in `frontend/src/i18n/translations.js` and are imported as nested objects (e.g. `translations.dashboard.title`).

## Roadmap / ideas

- Tighten default DRF permissions (`IsAuthenticated` where appropriate) and admin-only endpoints
- Broader social features (friends, shared challenges) beyond the leaderboard
- More lesson types (video, interactive drills)
- Advanced sim features (e.g. limit orders), richer portfolio analytics
- Push notifications for streaks/achievements
- Docker and CI/CD

## License and data

Educational use. Market data is retrieved via the **yfinance** library; Yahoo Finance terms and limitations apply to delayed or live data.

---

Built with **Django + React** for the TFG.
