
# 🎬 Movie Picker

Welcome to **Movie Picker** — a simple, clean Python app that randomly picks a movie from a curated list of the greatest films of all time — **or** lets you pick a movie based on the genres you're feeling!

Built to be fast, beautiful, and customizable to your own movie collection.

---

## 🚀 Features

- 🎥 Pick a completely **random movie**.
- 🎭 Pick a **movie by genres** (e.g., "Animation, Adventure", "Drama, Romance").
- 🎨 **Colorful terminal output** for a better experience.
- 🔁 **Pick multiple movies** in one session with an "ask again" loop.
- 📝 Easy to **expand** — add your own movies from Plex or anywhere else!

---

## 📂 Project Structure

```
/MoviePicker
    /lists
        standardized_movies.json   # Master movie list (fully filled out)
    /scripts
        merge_movies.py             # (optional) Merge lists
        fill_missing_data.py        # (optional) Fill missing movie info
    moviepicker.py                   # Main app file
    README.md                        # You're reading it!
```

---

## 🛠️ Installation

1. **Clone or download** this project into a folder.
2. **Install Python libraries** (only one needed):

```bash
pip install colorama
```

3. That's it — you're ready to go!

---

## 🎯 How to Use

1. Open a terminal inside the `/MoviePicker` folder.
2. Run the app:

```bash
python3 moviepicker.py
```

3. Choose an option:
   - `1` → Pick a completely random movie from the list.
   - `2` → Pick a movie that matches genres you enter (e.g., "Animation, Family", "Drama, War").

4. After each pick, you can choose to pick another movie or exit.

Example:

```
🎥 Welcome to Movie Picker!

1. Pick a completely random movie
2. Pick a movie by genre(s)

Choose an option (1 or 2): 2

🎬 What genres are you feeling? (comma-separated, e.g., 'Drama, Adventure')
> Animation, Family

🎬 Your Movie Pick!
Title    : Spirited Away
Year     : 2001
Director : Hayao Miyazaki
Genres   : Animation, Adventure, Family

🔁 Pick another movie? (y/n):
```

---

## 📦 Dependencies

- Python 3.x
- [`colorama`](https://pypi.org/project/colorama/)

Install with:

```bash
pip install colorama
```

---

## 💡 Future Ideas (Optional Expansions)

- 🎞️ Import your own Plex/Tiny Media Manager movie list!
- 🔎 Filter by **year** (e.g., "Movies from the 90s").
- 💾 Save history of picked movies.
- 🎨 Fancy UI using `rich` for animations.
- 🌐 Web version using Flask (future idea).

---

## 🤝 Contributing

Feel free to fork and improve!  
Add more lists, genres, or features!

---

## 📝 License

This project is open-source and free to use.  
Created for fun, movies, and random exploration. 🎬

---
