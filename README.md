# Am I Chronically Online? 📱

A web application that analyzes daily screen time habits through manual data entry, calculating key metrics like total screen time, "doomscroll" hours, and pickup frequency.

## Tech Stack

- **Backend:** Python 3.9+, FastAPI, Pandas, NumPy
- **Frontend:** Next.js (React), Tailwind CSS, Recharts, Lucide React
- **Deployment:** Vercel (Serverless functions)

## Project Structure

```
am-i-chronically-online/
├── api/                    # Python FastAPI serverless functions
│   ├── index.py           # FastAPI endpoints (Phase 2) ✅
│   ├── processing.py      # Data processing engine (Phase 1) ✅
│   ├── test_processing.py # Test script for Phase 1
│   └── test_api.py        # Test script for Phase 2
├── app/                    # Next.js app directory (Phase 3) ✅
│   ├── layout.tsx          # Root layout
│   ├── page.tsx            # Main page
│   └── globals.css         # Global styles
├── components/             # React components
│   ├── DataEntryForm.tsx   # Manual data entry form
│   ├── Dashboard.tsx       # Main dashboard
│   ├── ChronicScoreCard.tsx # Score display
│   ├── MetricsCards.tsx    # Metrics overview
│   ├── ChartsSection.tsx   # Recharts visualizations
│   └── TipsSection.tsx      # Tips display
├── types/                  # TypeScript type definitions
│   └── index.ts
├── public/                 # Static assets
├── requirements.txt        # Python dependencies
├── package.json           # Node.js dependencies ✅
├── vercel.json            # Vercel configuration ✅
└── README.md
```

## Phase 1: Data Engine ✅

The processing engine (`api/processing.py`) handles:
- **Auto-categorization:** Automatically categorizes apps based on name patterns (Social Media, Productivity, Entertainment, etc.)
- **Manual categorization:** Users can override with their own category
- **Metrics calculation:** 
  - Total screen time (hours/minutes)
  - Doomscroll hours (Social Media category sum)
  - Pickup frequency (total and average per day)
  - Category breakdown
  - Daily/weekly trends
  - Top apps by usage
- **Chronic Online Score (0-100):** 
  - Weighted scoring based on daily screen time, social media ratio, and pickup frequency
  - Levels: Casually Online, Moderately Online, Pretty Online, Very Online, Chronically Online
  - Includes detailed breakdown of scoring factors
- **Personalized Tips:** 
  - Actionable recommendations based on usage patterns
  - Prioritized by urgency (high/medium/low)
  - Covers specific apps, categories, and general digital wellness strategies

### Testing Phase 1

```bash
# Install dependencies
pip install -r requirements.txt

# Run test script
python api/test_processing.py
```

## Phase 2: API Layer ✅

The FastAPI application (`api/index.py`) provides REST endpoints:

- **POST `/api/entries`**: Submit daily screen time entries (returns analytics immediately)
- **GET `/api/analytics`**: Get analytics for all stored entries
- **DELETE `/api/entries`**: Clear all entries (for testing/resetting)
- **GET `/`**: Health check endpoint

### Features:
- **Pydantic validation**: Automatic request/response validation with clear error messages
- **CORS enabled**: Ready for frontend integration
- **In-memory storage**: Simple storage that can be easily replaced with a database
- **Vercel-ready**: Configured for serverless deployment with Mangum adapter

### Testing Phase 2

```bash
# Install dependencies (if not already done)
pip install -r requirements.txt

# Start the API server
uvicorn api.index:app --reload --port 8000

# In another terminal, run the test script
python api/test_api.py

# Or test manually with curl:
curl -X POST http://localhost:8000/api/entries \
  -H "Content-Type: application/json" \
  -d '{
    "entries": [
      {"date": "2024-01-20", "app": "Instagram", "time_minutes": 120, "pickups": 15}
    ]
  }'

# Get analytics
curl http://localhost:8000/api/analytics
```

### API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Data Entry Format

Each entry should be a dictionary with:
```python
{
    "date": "2024-01-15",           # Required: YYYY-MM-DD
    "app": "Instagram",              # Required: App name
    "time_minutes": 120,             # Required: Time spent in minutes
    "category": "Social Media",      # Optional: Auto-categorized if not provided
    "pickups": 15                    # Optional: Number of times app was opened
}
```

## Phase 3: Frontend & Deploy ✅

The Next.js frontend provides a complete user interface:

### Features:
- **Data Entry Form**: Manual entry with date picker, app name, time, category selector, and pickups
- **Chronic Score Display**: Large, color-coded score card with breakdown
- **Metrics Cards**: Quick overview of key statistics
- **Interactive Charts** (Recharts):
  - Daily screen time trends (line chart)
  - Category breakdown (pie chart)
  - Top apps by usage (bar chart)
- **Personalized Tips**: Prioritized recommendations with visual indicators
- **Real-time Updates**: Dashboard refreshes automatically after submitting entries

### Running the Frontend

```bash
# Install Node.js dependencies
npm install

# Start the Next.js development server
npm run dev

# The app will be available at http://localhost:3000
```

### Development Setup

1. **Start the API server** (in one terminal):
   ```bash
   uvicorn api.index:app --reload --port 8000
   ```

2. **Start the Next.js frontend** (in another terminal):
   ```bash
   npm run dev
   ```

3. **Open your browser**: http://localhost:3000

### Environment Variables

Create a `.env.local` file (optional for local development):
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

For production on Vercel, the API URL will be automatically set to your Vercel deployment URL.

### Deployment to Vercel

1. **Install Vercel CLI** (if not already installed):
   ```bash
   npm i -g vercel
   ```

2. **Deploy**:
   ```bash
   vercel
   ```

   Or connect your GitHub repository to Vercel for automatic deployments.

3. **Configure Environment Variables** in Vercel dashboard:
   - Set `NEXT_PUBLIC_API_URL` to your Vercel API URL (e.g., `https://your-project.vercel.app`)

The `vercel.json` is already configured to handle both Next.js frontend and Python API serverless functions.

## Project Complete! 🎉

All three phases are complete:
- ✅ Phase 1: Data Engine (Pandas processing)
- ✅ Phase 2: API Layer (FastAPI)
- ✅ Phase 3: Frontend & Deploy (Next.js + Vercel)