import sqlite3
import streamlit as st

# Initialize SQLite Database
conn = sqlite3.connect('movies.db', check_same_thread=False)
c = conn.cursor()

# Create table
c.execute('''
    CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY,
        title TEXT,
        director TEXT,
        year INTEGER,
        watched BOOLEAN
    )
''')
conn.commit()

st.title("Movie List App")
# Define toggle_watched function
def toggle_watched(movie_id, watched_status):
    c.execute('''
        UPDATE movies
        SET watched = ?
        WHERE id = ?
    ''', (not watched_status, movie_id))
    conn.commit()

# Define delete_movie function
def delete_movie(movie_id):
    c.execute('''
        DELETE FROM movies
        WHERE id = ?
    ''', (movie_id,))
    conn.commit()


# Layout for Search and Filters
st.subheader("Search and Filter")
col1, col2, col3, col4 = st.columns(4)
with col1:
    search_query = st.text_input("Search Movies")
with col2:
    director_filter = st.selectbox("Filter by Director", ['All'] + [x[0] for x in c.execute('SELECT DISTINCT director FROM movies').fetchall()])
with col3:
    year_filter = st.selectbox("Filter by Year", ['All'] + [x[0] for x in c.execute('SELECT DISTINCT year FROM movies').fetchall()])
with col4:
    watched_filter = st.selectbox("Filter by Watched", ['All', 'Watched', 'Not Watched'])

# Input fields for the Movie
with st.form(key='movie_form'):
    title = st.text_input("Movie Title")
    director = st.text_input("Director")
    year = st.number_input("Year of Release", min_value=1800, max_value=2100, step=1)
    watched = st.checkbox("Watched?")
    submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        # Insert form data into SQLite Database
        c.execute('''
            INSERT INTO movies (title, director, year, watched)
            VALUES (?, ?, ?, ?)
        ''', (title, director, year, watched))
        conn.commit()
        st.success("Movie added successfully!")

# Query based on filters
query = "SELECT id, title, director, year, watched FROM movies WHERE title LIKE ?"
params = [f'%{search_query}%']

if director_filter != 'All':
    query += " AND director = ?"
    params.append(director_filter)

if year_filter != 'All':
    query += " AND year = ?"
    params.append(year_filter)

if watched_filter != 'All':
    watched_value = 1 if watched_filter == 'Watched' else 0
    query += " AND watched = ?"
    params.append(watched_value)

# Displaying Movies in Columns with Update and Delete options
st.subheader("Movie List")
movies = c.execute(query, params).fetchall()
for movie in movies:
    col9, col10, col11, col12, col13, col14 = st.columns(6)
    with col9:
        st.text(f"Title: {movie[1]}")
    with col10:
        st.text(f"Director: {movie[2]}")
    with col11:
        st.text(f"Year: {movie[3]}")
    with col12:
        st.text(f"Watched: {'Yes' if movie[4] else 'No'}")
    with col13:
        if st.button("Toggle Watched", key=f"watched_{movie[0]}"):
            toggle_watched(movie[0], movie[4])
            st.experimental_rerun()
    with col14:
        if st.button("Delete", key=f"delete_{movie[0]}"):
            delete_movie(movie[0])
            st.experimental_rerun()
    st.write("---")

# Run the app: streamlit run your_script.py
