# LifeOS — Your Personal Command Center

A luxurious jewel-tone life organization system with built-in AI.
Available as a Python web app (deployable online) and an Android app.

---

## What's Included

```
lifeos/               ← Python web app
  app.py              ← Flask backend + AI endpoints
  templates/
    index.html        ← Full dashboard UI
  static/
    css/style.css     ← Jewel-tone luxury theme
    js/app.js         ← All interactivity
  requirements.txt
  Procfile            ← Render deployment

lifeos-android/       ← Android Kotlin app
  app/src/main/java/com/lifeos/app/
    MainActivity.kt   ← Full Jetpack Compose UI
    data/Models.kt    ← Data classes
    network/ApiClient.kt ← Retrofit API calls
    viewmodel/TaskViewModel.kt
    ui/theme/Theme.kt ← Jewel tone colors
  app/build.gradle
```

---

## Part 1: Deploy the Web App

### Step 1 — Get your Anthropic API key
1. Go to https://console.anthropic.com
2. Create an API key (starts with `sk-ant-...`)
3. Copy it — you'll need it in Step 3

### Step 2 — Push to GitHub
1. Create a free account at https://github.com
2. Create a new repository called `lifeos`
3. Upload all files in the `lifeos/` folder to it

### Step 3 — Deploy on Render (free hosting)
1. Go to https://render.com and sign up free
2. Click **New → Web Service**
3. Connect your GitHub repo `lifeos`
4. Set these values:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT`
   - **Environment:** Python 3
5. Under **Environment Variables**, add:
   - Key: `ANTHROPIC_API_KEY`
   - Value: your key from Step 1
6. Click **Create Web Service**
7. Render gives you a URL like `https://lifeos-xxxx.onrender.com`

Your web app is now live! Open it in any browser on any device.

### Running locally (optional)
```bash
cd lifeos
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your-key-here
python app.py
# Open http://localhost:5000
```

---

## Part 2: Build the Android App

### Prerequisites
- Android Studio (free) — download at https://developer.android.com/studio
- A Samsung phone or tablet with USB debugging enabled

### Step 1 — Open the project
1. Open Android Studio
2. Open the `lifeos-android/` folder as a project

### Step 2 — Set your server URL
Open `app/src/main/java/com/lifeos/app/network/ApiClient.kt`
Replace this line:
```kotlin
private const val BASE_URL = "https://your-app-name.onrender.com/"
```
With your actual Render URL from Part 1.

### Step 3 — Build & install
1. Connect your Samsung device via USB
2. Enable Developer Mode on phone: Settings → About Phone → tap Build Number 7 times
3. Enable USB Debugging: Settings → Developer Options → USB Debugging ON
4. In Android Studio, click the green ▶ Run button
5. Select your device

The app installs and runs on your phone and tablet.

---

## Features

### Web App
- ✦ Full tabbed dashboard (Urgent, Health, Kids, Home, Money, Routines, Schedule)
- ✦ Add, edit, delete tasks in any category
- ✦ Brain Dump: type or speak, AI categorizes and sorts everything
- ✦ AI Chat: ask questions, get personalized advice based on your life
- ✦ 75 Challenge daily tracker with progress bar
- ✦ Voice input (Chrome/Edge supported)
- ✦ Responsive — works on phone, tablet, and desktop browser
- ✦ Deep jewel-tone luxury theme (emerald, sapphire, gold)

### Android App
- ✦ Native Jetpack Compose UI with jewel-tone theme
- ✦ Syncs with your web app backend in real time
- ✦ Voice input via Android speech recognition
- ✦ Brain Dump with AI analysis
- ✦ Full chat with your personal AI
- ✦ Adaptive layout works on phone and tablet
- ✦ Offline-tolerant (shows cached tasks)

---

## Updating Your API Key
If you ever need to rotate your Anthropic key:
1. Go to render.com → your service → Environment
2. Update `ANTHROPIC_API_KEY`
3. Redeploy

## Adding More Tasks
- Web: click **+ Add Task** in any tab
- Android: tap the **+** FAB button
- Brain Dump: speak or type anything, AI sorts it

## Data Storage
Tasks are saved in `data/tasks.json` on the server.
On Render free tier, the file resets on redeploy — for permanent storage,
upgrade to Render's paid tier or connect a free PostgreSQL database
(ask your AI assistant to help you add SQLite or Post
