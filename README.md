# Telegram Summary Bot With MiniApp Control Panel

## Minimal local bot setup

This repository includes a minimal Python Telegram bot you can run locally or deploy as a long-running worker. The script supports:

- `/start` health check
- `/help` command list
- `/summary <text>` to summarize provided text
- `/summary` to summarize recent text messages seen in the current chat

The current summarizer is intentionally local and dependency-light. It creates a short extractive summary from the first few sentences and does not require an AI API key.

### 1. Create a Telegram bot token

1. Open Telegram and message [@BotFather](https://t.me/BotFather).
2. Run `/newbot`.
3. Follow the prompts and copy the bot token.
4. For group summaries, ask BotFather for `/setprivacy` and disable privacy mode so the bot can read group messages.

### 2. Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` and replace `TELEGRAM_BOT_TOKEN` with your real token.

Start the bot:

```bash
python bot.py
```

Open Telegram, message your bot, and run:

```text
/start
/summary This is a long message. It has several sentences. The bot returns a short summary.
```

### 3. Environment variables

| Variable | Required | Default | Description |
| --- | --- | --- | --- |
| `TELEGRAM_BOT_TOKEN` | Yes | None | Token from BotFather. |
| `LOG_LEVEL` | No | `INFO` | Python logging level. |
| `POLL_TIMEOUT` | No | `30` | Telegram long-poll timeout in seconds. |
| `MAX_STORED_MESSAGES` | No | `100` | Recent messages retained per chat for `/summary`. |
| `SUMMARY_SENTENCES` | No | `5` | Maximum sentences returned by the local summarizer. |

### 4. Deploy with Docker

Build the image:

```bash
docker build -t telegram-summary-bot .
```

Run it:

```bash
docker run --env-file .env --restart unless-stopped telegram-summary-bot
```

### 5. Deploy on Render, Railway, Fly.io, or similar

Use the repository as a worker/background service, not a web service.

General settings:

- Build command: `pip install -r requirements.txt`
- Start command: `python bot.py`
- Environment variable: `TELEGRAM_BOT_TOKEN=<your BotFather token>`

If the platform supports Procfile workers, this repository includes:

```text
worker: python bot.py
```

### 6. Deploy on a VPS with systemd

Clone the repository on your server, create `.env`, install dependencies, then create `/etc/systemd/system/telegram-summary-bot.service`:

```ini
[Unit]
Description=Telegram Summary Bot
After=network.target

[Service]
WorkingDirectory=/opt/telegram-summary-bot
EnvironmentFile=/opt/telegram-summary-bot/.env
ExecStart=/opt/telegram-summary-bot/.venv/bin/python /opt/telegram-summary-bot/bot.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Enable and start it:

```bash
sudo systemctl daemon-reload
sudo systemctl enable telegram-summary-bot
sudo systemctl start telegram-summary-bot
sudo systemctl status telegram-summary-bot
```

### 7. Security notes

- Never commit `.env` or your real Telegram token.
- Rotate the token in BotFather if it is exposed.
- Use one running instance per bot token when using long polling.

_Powerful AI-powered manager for Telegram channels and groups, Summarize and query channel and group chats. No limits. No coding. Just results.
Best MiniApp for businesses, marketers, and agencies who want to grow rapidly on Telegram and effortlessly manage their Channels and Groups via a single Dashboard.
The Ultimate Telegram Channel & Group Manager._

[@InDMDevBots](https://t.me/InDMDevBots)

<img width="627" height="1280" alt="image" src="https://github.com/user-attachments/assets/d18f182b-2dbc-4628-afeb-2bff87dd9a04" />

<img width="629" height="1280" alt="image" src="https://github.com/user-attachments/assets/a6bc3b79-7d17-43d6-af89-f8861e29bfc9" />

 ━━━━━━━━━━━━━━━━━━

📢 Channel & Group Management:

      - ✅ Manage unlimited channels & groups from one panel.
      - ✅ Organize with custom categories.
      - ✅ Per-channel settings & configurations.


👥 Member Management:

      - ✅ Advanced search, filter & bulk operations.
      - ✅ CSV export & member categories.
      - ✅ Track activity, joins, leaves & growth.



📣 Smart Broadcasting:

      - ✅  Broadcast to channels OR direct-message users
      - ✅ 7 audience segments (All, VIP, Premium, Active, New, By Channel & more)
      - ✅ Full media support — photos, videos, documents, polls


📅 Scheduled Posts:

      - ✅ Schedule any message type to any channel
      - ✅ Retry logic & engagement tracking
      - ✅ Pin, unpin & auto-delete support


🤖 Custom Bot Commands:

      - ✅ Create unlimited custom bot responses
      - ✅ Admin-only commands & usage statistics
      - ✅ Dynamic placeholders ({name}, {username}, {channel}...)


👋 Auto Messages:

      • Welcome & goodbye messages
      • New month, new year & birthday greetings
      • Fully customizable with placeholders


🛡️ Moderation Suite:

      - ✅ Prohibited words filter with auto-actions
      - ✅ Custom auto-moderation rules
      - ✅ Warning system & CAPTCHA verification for new members


📋 Join Requests & Invite Links:

      - ✅ Manage & auto-approve join requests
      - ✅ Track invite link performance
      - ✅ Custom approval workflows


📨 Contact Lists & Campaigns:

      - ✅ Import contacts & organize into lists
      - ✅ Bulk & drip campaign modes
      - ✅ Bot mode (20 msg/sec) & Business mode via Telegram Business API


📝 Templates & Media Library:

      - ✅ Save & reuse message templates
      - ✅ Centralized media library
      - ✅ Quick access across all features


📊 Analytics & Reports:

      - ✅ Member growth & engagement charts
      - ✅ Daily breakdown & trend analysis
      - ✅ Exportable reports


🧠 AI-Powered (Gemini + ChatGPT):

      - ✅ Chat summarization
      - ✅ AI Q&A from channel history
      - ✅ Smart content insights


👨‍💼 Admin Management:

      - ✅ 3 roles: Super Admin, Admin, Moderator
      - ✅ Granular permissions per admin
      - ✅ Two-Factor Authentication (2FA) & full audit log


💾 Backup & Restore:

      - ✅ One-click JSON/SQL export
      - ✅ Full database restore
      - ✅ Never lose your data


🔒 Enterprise-Grade Security:

      - ✅ CSRF, XSS & SQL injection protection
      - ✅ Rate limiting & account lockout
      - ✅ IP tracking & session management


🌍 15 Languages Built-in:

      - ✅ English, Arabic, Chinese, German, Spanish, French, Indonesian, Italian, Japanese, Georgian, Korean, Portuguese, Romanian, Russian, Turkish
      - ✅ Full RTL support
      - ✅ Auto-detects user language


📱 Progressive Web App (PWA):

      - ✅ Install on any device like a native app
      - ✅ Offline support
      - ✅ Home screen shortcuts


⚙️ Zero Dependencies:

      - ✅ No Composer, no Node.js, no frameworks
      - ✅ Works on any shared hosting (cPanel, Hostinger, Plesk)
      - ✅ PHP 7.4+ & MySQL — that's all you need
      - ✅ 5-minute setup wizard


 ━━━━━━━━━━━━━━━━━━

✨ TelePilot — Everything you need to run your Telegram channels and groups like a pro.
