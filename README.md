# VyaparSaathi Voice OS

VyaparSaathi is a Marathi/Hindi/Hinglish/English voice-first inventory and
sales system for MSME shopkeepers. React runs the dashboard, FastAPI executes
commands, and SQLite stores products and transactions locally.

## What works

- Add/edit/delete products from the Inventory screen
- Create sales orders and automatically reduce stock
- Calculate sale amount and gross profit
- Persist products and transactions after restarting the server
- Show daily sales, profit, low-stock products, and dashboard totals
- Execute typed regional-language commands without an API key
- Record real voice commands when `GEMINI_API_KEY` or `OPENAI_API_KEY` is set

## First-time setup (CachyOS / fish)

Open terminal 1:

```fish
cd ~/Desktop/2026_TEAM_GENESIS/backend
python -m venv venv
source venv/bin/activate.fish
pip install -r requirements.txt
cp .env.example .env
python scripts/seed_demo_data.py
uvicorn app.main:app --reload
```

Open terminal 2:

```fish
cd ~/Desktop/2026_TEAM_GENESIS/Frontend
cp .env.example .env
npm install
npm run dev
```

Open `http://localhost:5173`. Demo login:

- Email: `owner@vyaparsaathi.in`
- Password: `demo123`

Backend API docs are available at `http://localhost:8000/docs`.

## Enable real microphone commands

Typed commands work without any AI key. For recorded audio, edit
`backend/.env` and set one of these:

```env
GEMINI_API_KEY=your_gemini_key
# OR
OPENAI_API_KEY=your_openai_key
```

Never commit `.env` to GitHub. Restart FastAPI after changing it.

## Commands to demonstrate

```text
Add 20 Dettol Soap, buying price 18, selling price 22
Sell 3 Dettol Soap
डेटॉल साबणाचे तीन नग विकले
डेटॉल साबणाचे वीस नग स्टॉकमध्ये जोडा
आजची विक्री आणि नफा सांगा
कमी स्टॉक दाखवा
```

For a brand-new product, buying price and selling price are required. For an
existing product, a stock-add command only needs product name and quantity.

## Tests

```fish
cd backend
source venv/bin/activate.fish
pytest -q

cd ../Frontend
npm run build
```
