# 📚 Personal Library Manager

Easily track and manage your personal book collection with this interactive and user-friendly Streamlit app.

---

## ✨ Features

- ➕ **Add New Books** – Store title, author, year, genre, and reading status.
- 🔍 **Search** – Find books by title or author.
- 📂 **Filter & Sort** – Organize your collection by genre, year, or title.
- 🗑 **Remove Books** – Delete any book from your collection.
- 📤 **Export** – Download your library as a CSV or PDF.
- 📊 **Statistics** – View total books and reading progress.
- 💾 **Data Saved Automatically** – Changes persist in a local `library.json` file.

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/personal-library-manager.git
cd personal-library-manager
```

### 2. Install Dependencies
```bash
pip install streamlit pandas fpdf
```

### 3. Run the App
```bash
streamlit run app.py
```

---

## 🗂️ Project Structure

```
personal-library-manager/
│
├── app.py                # Main Streamlit app
├── library.json          # Data file (auto-generated)
├── library_export.pdf    # PDF export (auto-generated)
└── README.md             # Project documentation
```


---

## 🔐 Notes

- All book entries are saved locally in `library.json`.
- PDF and CSV exports are generated from your current data.
- No internet or cloud service is required – all data stays on your machine.

---

## 💡 Future Enhancements (Ideas)

- 📅 Reading schedule planner
- 📈 Graphs for genres and yearly reading trends
- ☁️ Cloud backup and sync support
- 🔐 Login system for multi-user use

---

## 🧑‍💻 Author

Built using [Streamlit](https://streamlit.io/).  


---
