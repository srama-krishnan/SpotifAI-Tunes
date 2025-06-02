# 🎵 AI-Generated Spotify Playlist Creator

This project auto-generates custom Spotify playlists based on natural language prompts using OpenAI's GPT and Spotify's API. Whether it's *"High-energy Tamil hits"* or *"Lo-fi late night tracks"*, this tool curates the perfect set of songs for your mood or theme.

---

## 💡 How It Works

1. You give a prompt like: `Happy and energetic songs for dancing`.
2. GPT generates a JSON list of songs and artists.
3. Using the Spotify API, the script finds tracks and creates a **private playlist** on your Spotify account.

---

## 📸 Demo Snapshots

### ✅ Prompt Output and Song Detection (Console)
![image](https://github.com/user-attachments/assets/43a5e588-778e-4a95-9921-dc8c33369eee)
![image](https://github.com/user-attachments/assets/57e39b08-2e33-4566-9d07-a9dadb679437)


### 🎧 Playlist Created on Spotify
![image](https://github.com/user-attachments/assets/d7d0cda5-1066-45fc-b9ca-619aa293cf93)
![image](https://github.com/user-attachments/assets/a27643ff-008a-4602-b0f6-51902d05a89b)


---

## 🔧 Requirements

- Python 3.8 or higher
- OpenAI Python SDK (>=1.0.0)
- Spotipy
- python-dotenv

Install using:
```
pip install -r requirements.txt
```
---

## 🔐 Setup

Create a `.env` file in the root directory and add:

```
APIKEY=your-openai-api-key
SPOCLIENT_ID=your-spotify-client-id
SPOCLIENT_SECRET=your-spotify-client-secret
```

Create your Spotify app here: https://developer.spotify.com/dashboard

In your app settings, add the redirect URI:
`http://localhost:9999`

---

## ▶️ Run the Script

Usage:

"use triple quotes here"
python app.py -p "High energy Tamil workout playlist" -n 10
"use triple quotes here"

- `-p` : Prompt (theme or vibe)
- `-n` : Number of songs (2 to 12 recommended)

The script prints a playlist link after creation.

---

## 🛠 Features

- GPT-powered song and artist matching
- Spotify API-based playlist generation
- Region + language agnostic (works for Hindi, Tamil, English etc.)
- JSON-based clean responses
- CLI-ready for automation or scripting

---

## ⚠️ Notes

- Ensure that your Spotify app allows private playlist access.
- The `.env` file must never be pushed to public repositories.

---

## 📄 License

MIT License © 2025 Ramakrishnan Subramani (srama-krishnan)

---

Made with 💚 using Python, GPT, and Spotify
