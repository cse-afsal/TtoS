# 🎙️ TtoS — Text to Speech

A clean, fast, and free **Text-to-Speech web app** powered by [Google TTS (gTTS)](https://gtts.readthedocs.io/) and Flask. Paste any text, choose a language and regional accent, and download a high-quality **MP3 file** in seconds — no sign-up required.

---

## ✨ Features

- 🌍 **16 languages** — English, Spanish, French, German, Italian, Portuguese, Russian, Japanese, Korean, Chinese (Simplified), Arabic, Hindi, Dutch, Swedish, Polish, Turkish
- 🗣️ **5 regional accents** — United States, United Kingdom, Australia, India, Canada
- 🐢 **Slow speech mode** — Reduces playback speed for clearer pronunciation
- ⚡ **Instant MP3 download** — Audio generated and delivered in under 5 seconds
- 💰 **Completely free** — No API keys, no accounts, no rate limits
- 📱 **Responsive UI** — Works on desktop and mobile

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/ttos.git
cd ttos

# 2. Create and activate a virtual environment (recommended)
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

### Run Locally

```bash
python app.py
```

Open your browser at **http://localhost:5000**.

---

## 📂 Project Structure

```
ttos/
├── app.py              # Flask app — routes, HTML template, TTS logic
├── main.py             # Quick standalone gTTS script (for testing)
├── requirements.txt    # Python dependencies
├── vercel.json         # Vercel deployment configuration
└── api/
    └── index.py        # Vercel serverless entry point
```

---

## 🌐 Deploying to Vercel

This project is pre-configured for [Vercel](https://vercel.com) via `vercel.json`.

```bash
# Install the Vercel CLI
npm install -g vercel

# Deploy
vercel
```

All requests are routed to `api/index.py`, which imports the Flask app from `app.py`.

> **Note:** Vercel's Python runtime has a 50 MB deployment limit. The `gTTS` package is lightweight and works within this limit.

---

## 🛠️ Tech Stack

| Layer      | Technology                          |
|------------|-------------------------------------|
| Backend    | Python · Flask · flask-cors         |
| TTS Engine | Google Text-to-Speech (gTTS)        |
| Frontend   | Vanilla HTML · CSS · JavaScript     |
| Fonts      | Inter (Google Fonts)                |
| Deployment | Vercel (serverless)                 |

---

## 📦 Dependencies

```
Flask>=3.0.0
flask-cors>=4.0.0
gTTS>=2.5.0
```

---

## 📖 API Reference

### `POST /generate`

Converts text to speech and returns an MP3 file.

**Request Body (JSON):**

| Field  | Type    | Description                              |
|--------|---------|------------------------------------------|
| `text` | string  | The text to convert (max 5,000 chars)    |
| `lang` | string  | Language code (e.g. `"en"`, `"fr"`)      |
| `tld`  | string  | Accent TLD (e.g. `"com"`, `"co.uk"`)     |
| `slow` | boolean | `true` for slower speech                 |

**Response:** `audio/mpeg` — downloadable MP3 file.

---

## 🗺️ Supported Languages

| Code    | Language             |
|---------|----------------------|
| `en`    | English              |
| `es`    | Spanish              |
| `fr`    | French               |
| `de`    | German               |
| `it`    | Italian              |
| `pt`    | Portuguese           |
| `ru`    | Russian              |
| `ja`    | Japanese             |
| `ko`    | Korean               |
| `zh-CN` | Chinese (Simplified) |
| `ar`    | Arabic               |
| `hi`    | Hindi                |
| `nl`    | Dutch                |
| `sv`    | Swedish              |
| `pl`    | Polish               |
| `tr`    | Turkish              |

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

---

## 🙏 Acknowledgements

- [gTTS](https://github.com/pndurette/gTTS) — Google Text-to-Speech Python library
- [Flask](https://flask.palletsprojects.com/) — Lightweight Python web framework
- [Vercel](https://vercel.com/) — Serverless deployment platform
