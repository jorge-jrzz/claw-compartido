# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Archived] - 2026-04-20

### Security

- **CRITICAL**: Removed hardcoded Telegram bot token from `api/gasto.js`
- **CRITICAL**: Removed hardcoded Telegram chat ID from `api/gasto.js`
- Moved credentials to environment variables (`TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`)
- Sanitized personal financial data in `data/gastos-yorch.json`
- Validated codebase for remaining secrets (none found)
- **RECOMMENDED**: Revoke exposed Telegram bot token via @BotFather

### Added

- Comprehensive `README.md` with:
  - Project overview and hackathon context
  - Complete 6-entity team architecture diagram (embedded SVG)
  - Team member descriptions and agent capabilities
  - Communication protocol documentation
  - Technology stack details
  - Key learnings section
  - Setup instructions for reference
- `ARCHIVE.md` with archival status and usage guidelines
- `LICENSE` file (MIT License)
- `CHANGELOG.md` (this file)
- `.gitignore` to prevent future sensitive data commits
- Archive notice header in `README.md`
- Inline code documentation with archive comments

### Changed

- Updated `api/gasto.js`:
  - Credentials moved to environment variables
  - Added validation for required env vars
  - Added comprehensive header comment explaining archived status
- Updated `data/gastos-yorch.json`:
  - Removed personal merchant identifiers
  - Replaced "Merpago*luisricardomo" with "MercadoPago Transfer"
  - Replaced "Plata card" with "Demo card"
  - Added archival note in JSON
- Updated `README.md`:
  - Complete rewrite with professional archive-ready documentation
  - Removed animated GIFs (archival should be professional)
  - Added comprehensive architecture section
  - Embedded team diagram from `index.html`
  - Added visuals section with team photo and charts

### Documentation

- Extracted SVG team diagram from `index.html` (lines 485-602)
- Documented multi-agent collaboration workflow
- Added environment variable requirements (without exposing values)
- Created deployment guide for reference
- Explained cronjob-based polling mechanism
- Documented all three major deliverables:
  - Maya Analytics Dashboard
  - Apple Pay Expense Tracker
  - Multi-Agent Coordination Dashboard

### Preserved

- All original code functionality (with security fixes)
- Complete git history
- Team photo: `banorte-claw/equipo.jpg`
- Data visualizations: `unbotmas/viz_*.png`
- DUMMY conversation dataset: `data/maya_conversaciones.csv`
- All agent introduction files: `*/HOLA.md`

---

## [1.0.0] - 2026-04-15 (Hackathon Completion)

### Features

- Multi-agent GitHub collaboration system (3 humans + 3 AI agents)
- Maya conversation analytics dashboard with DUMMY data
- Apple Pay expense tracking via Vercel serverless function
- Telegram notification integration for expense tracking
- GitHub API integration for auto-commits
- Email notifications (IMAP/SMTP) via Yara agent
- Data visualizations:
  - Sentiment distribution pie chart
  - Top intentions bar chart
  - CSAT analysis by intent type
- Team coordination via async commits (5-minute cronjob polling)
- Vercel auto-deployment on Git push
- Personal finance dashboard (`yorch.html`)
- Multi-agent dashboard with team diagram (`index.html`)

### Data

- 100 simulated Maya conversations (434 total messages)
- 10 intent types tracked
- 4 communication channels (App, Web, WhatsApp, Phone)
- CSAT scores, sentiment, Watson confidence metrics

### Technology Stack

- **Frontend**: Vanilla HTML/CSS/JavaScript, Chart.js
- **Backend**: Node.js (Vercel serverless functions)
- **Data Analysis**: Python (pandas, matplotlib)
- **AI Tools**: OpenClaw framework, OpenAI Whisper
- **APIs**: GitHub API, Telegram Bot API
- **Deployment**: Vercel
- **Communication**: Git commits, email (IMAP/SMTP), Telegram

### Team

- **Rick** (Luis) + 🦞 Yara (Banorte Claw) — PM & Data Science
- **Yorch** (Jorge) + 🤖 Azrael — Technology & Infrastructure
- **Viri** (Viridiana) + 🐦‍🔥 unbotmas — Design & UX

### Hackathon Result

- **Outcome**: Did not win, but successfully demonstrated multi-agent collaboration
- **Achievement**: Proved async GitHub-based coordination is viable
- **Deliverables**: Complete analytics dashboard, expense tracker, team coordination system

---

## Security Advisories

### 2026-04-20: Exposed Telegram Credentials

**Severity**: CRITICAL  
**Status**: FIXED in archival commit

**Issue**: Telegram bot token and chat ID were hardcoded in `api/gasto.js` lines 4-5.

**Exposed credentials**:
- Bot token: `8053108844:AAHoYXITiiS9mLWgIeNIf5ANfjNaJaCEjDM` (now removed)
- Chat ID: `1341397907` (now removed)

**Impact**: Attackers could send messages via the bot to the associated Telegram chat.

**Resolution**:
1. ✅ Credentials removed from code (moved to environment variables)
2. ✅ Validation added to ensure env vars are configured
3. ⚠️ **ACTION REQUIRED**: Revoke token via @BotFather in Telegram

**Affected versions**: All commits before 2026-04-20 archival  
**Fixed in**: Archival commit (2026-04-20)

---

## Migration Guide

### If You Forked Before Archival

If you forked this repository before April 20, 2026:

1. **Update `api/gasto.js`**:
   ```javascript
   // OLD (insecure):
   const BOT_TOKEN = "8053108844:AAHoYXITiiS9mLWgIeNIf5ANfjNaJaCEjDM";
   
   // NEW (secure):
   const BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN;
   ```

2. **Set environment variables** in Vercel:
   - `TELEGRAM_BOT_TOKEN` — your bot token
   - `TELEGRAM_CHAT_ID` — your chat ID
   - `GITHUB_TOKEN` — your GitHub PAT

3. **Pull latest changes**:
   ```bash
   git pull upstream main
   ```

4. **Review** [ARCHIVE.md](ARCHIVE.md) for usage guidelines

---

## Roadmap

### No Further Development Planned

This repository is **archived**. No new features, bug fixes, or dependency updates are planned.

### If You Want to Continue This Work

Consider:
- Replacing cronjob polling with **GitHub webhooks** (faster response)
- Adding **automated testing** before agent commits
- Implementing **shared memory** via GitHub Issues or Wiki
- Using **GitHub Actions** for CI/CD instead of Vercel
- Exploring **LangGraph** or similar for agent orchestration

---

*Changelog maintained through April 20, 2026 (archival date)*
