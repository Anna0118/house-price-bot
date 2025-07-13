# 🏠 House Price Bot

A lightweight bot for fetching, filtering, and posting Taiwan real estate transaction data to a Discord channel. This bot automatically downloads government-provided Excel files, filters specific regions (e.g., 苗栗縣、高雄市), and publishes a summarized embed message with the full report attached.

---

## 📦 Features

- 📥 Automatically downloads the latest real estate transaction files from [實價登錄服務網](https://plvr.land.moi.gov.tw/).
- 🔍 Filters specified townships per region.
- 🧾 Outputs cleaned Excel reports.
- 🤖 Posts summaries to a specified Discord channel via rich embed messages.
- ✅ Handles Discord limitations (e.g., max 25 fields per embed).
- 🔄 Runs on scheduled update dates (e.g., 1st, 11th, and 21st of each month).

---

## 🧰 Requirements

- Python 3.8+
- [Discord bot token](https://discord.com/developers/applications)
- `DISCORD_CHANNEL_ID` and `DISCORD_TOKEN` set in `.env` file

---

## 🔧 Installation

```bash
git clone https://github.com/Anna0118/house-price-bot.git
cd house-price-bot
python3 -m venv venv
source venv/bin/activate   # Or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

---

## ⚙️ Configuration

1. Create a `.env` file in the root folder:

```env
DISCORD_TOKEN=your_discord_bot_token
DISCORD_CHANNEL_ID=your_channel_id
```

2. In `process_data.py`, edit the `TARGET_FILES` dictionary to specify which regions and townships to include:

```python
TARGET_FILES = {
    "k_lvr_land_b.xls": ["頭份市", "竹南鎮"],  # Miaoli
    "e_lvr_land_b.xls": ["苓雅區", "前鎮區"],  # Kaohsiung
}
```

---

## 📦 How to Run

```bash
python callbot.py
```

The bot will:

- Download the latest `.xls` data
- Filter records based on township names
- Create a cleaned Excel report
- Send a Discord embed summary + the full report

---

## 🚀 GitHub Actions

This project supports scheduled auto-runs using GitHub Actions.

Make sure you add the following repository secrets:

- `DISCORD_TOKEN`
- `DISCORD_CHANNEL_ID`

You can customize the workflow in `.github/workflows/bot.yml`.