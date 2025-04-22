import streamlit as st
import json
import os
import pandas as pd
from fpdf import FPDF

# ---------- File Setup ----------
LIBRARY_FILE = "library.json"

def load_library():
    if os.path.exists(LIBRARY_FILE):
        with open(LIBRARY_FILE, "r") as file:
            return json.load(file)
    return []

def save_library(library):
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file, indent=4)

def add_book(library, title, author, year, genre, read):
    new_book = {
        "title": title.strip(),
        "author": author.strip(),
        "year": year,
        "genre": genre.strip(),
        "read": read
    }
    library.append(new_book)
    save_library(library)

def remove_book(library, title):
    title = title.strip().lower()
    library[:] = [book for book in library if book['title'].lower() != title]
    save_library(library)

def search_books(library, keyword, by):
    keyword = keyword.strip().lower()
    return [book for book in library if keyword in book[by].lower()]

def filter_books(library, genre=None, year=None):
    return [
        book for book in library
        if (not genre or book["genre"] == genre) and
           (not year or book["year"] == year)
    ]

def sort_books(library, sort_by, ascending=True):
    return sorted(library, key=lambda x: x[sort_by], reverse=not ascending)

# ---------- Export ----------
def export_to_csv(library):
    df = pd.DataFrame(library)
    return df.to_csv(index=False).encode('utf-8')

def export_to_pdf(library):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Personal Library", ln=True, align='C')
    pdf.ln(10)

    for i, book in enumerate(library, 1):
        pdf.multi_cell(0, 10, f"{i}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {'Read' if book['read'] else 'Unread'}")

    pdf_output = "library_export.pdf"
    pdf.output(pdf_output)
    return pdf_output

# ---------- Streamlit UI ----------
st.set_page_config(page_title="📚 Personal Library Manager", layout="centered")
st.title("📚 Personal Library Manager")

library = load_library()

tab1, tab2, tab3, tab4 = st.tabs(["➕ Add Book", "🔍 Search", "📘 All Books", "📊 Stats"])

# --- Add Book ---
with tab1:
    st.header("➕ Add a New Book")
    with st.form("add_form"):
        col1, col2 = st.columns(2)
        title = col1.text_input("Book Title")
        author = col2.text_input("Author")
        year = col1.number_input("Publication Year", min_value=0, max_value=2100, step=1)
        genre = col2.text_input("Genre")
        read = st.checkbox("Have you read this book?")
        submitted = st.form_submit_button("Add Book")
        if submitted and title and author and genre:
            add_book(library, title, author, year, genre, read)
            st.success(f"✅ '{title}' added!")

# --- Search ---
with tab2:
    st.header("🔍 Search for a Book")
    search_by = st.radio("Search by:", ["Title", "Author"], horizontal=True)
    keyword = st.text_input("Enter search term:")
    if keyword:
        results = search_books(library, keyword, search_by.lower())
        if results:
            for book in results:
                st.write(f"**{book['title']}** by *{book['author']}* ({book['year']}) - {book['genre']} - {'✅ Read' if book['read'] else '📖 Unread'}")
        else:
            st.warning("No matching books found.")

# --- All Books with Filters & Sort ---
with tab3:
    st.header("📘 All Books")

    if library:
        genres = sorted(set(book['genre'] for book in library))
        years = sorted(set(book['year'] for book in library))

        st.subheader("📂 Filter")
        col1, col2 = st.columns(2)
        selected_genre = col1.selectbox("Genre", ["All"] + genres)
        selected_year = col2.selectbox("Year", ["All"] + [str(y) for y in years])

        st.subheader("🔃 Sort")
        sort_by = st.radio("Sort by:", ["title", "year"], horizontal=True)
        ascending = st.checkbox("Sort ascending", value=True)

        # Apply filter & sort
        filtered = filter_books(
            library,
            genre=None if selected_genre == "All" else selected_genre,
            year=None if selected_year == "All" else int(selected_year)
        )
        sorted_list = sort_books(filtered, sort_by, ascending)

        for i, book in enumerate(sorted_list, 1):
            with st.expander(f"{i}. {book['title']} by {book['author']}"):
                st.write(f"**Year:** {book['year']}")
                st.write(f"**Genre:** {book['genre']}")
                st.write(f"**Status:** {'✅ Read' if book['read'] else '📖 Unread'}")
                if st.button(f"🗑 Remove '{book['title']}'", key=f"remove_{i}"):
                    remove_book(library, book['title'])
                    st.experimental_rerun()

        # Export Options
        st.subheader("📤 Export Library")
        col1, col2 = st.columns(2)
        with col1:
            csv = export_to_csv(library)
            st.download_button("⬇️ Export to CSV", csv, "library.csv", "text/csv")
        with col2:
            pdf_file = export_to_pdf(library)
            with open(pdf_file, "rb") as f:
                st.download_button("⬇️ Export to PDF", f, file_name="library.pdf")

    else:
        st.info("📭 Your library is empty.")

# --- Statistics ---
with tab4:
    st.header("📊 Library Statistics")
    total = len(library)
    read_count = sum(1 for b in library if b['read'])
    st.metric("📚 Total Books", total)
    st.metric("✅ Read", read_count)
    if total > 0:
        st.progress(read_count / total)

st.caption("💾 All changes are saved to library.json automatically.")
