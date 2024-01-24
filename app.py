import sqlite3
import streamlit as st

# Initialize SQLite Database
conn = sqlite3.connect('todo.db', check_same_thread=False)
c = conn.cursor()

# Create table
c.execute('''
    CREATE TABLE IF NOT EXISTS todo (
        id INTEGER PRIMARY KEY,
        name TEXT,
        description TEXT,
        is_done BOOLEAN
    )
''')
conn.commit()

# Streamlit App
st.title("Todo List App")

# Input fields for the Todo
with st.form(key='todo_form'):
    name = st.text_input("Todo Name")
    description = st.text_area("Description")
    is_done = st.checkbox("Done?")
    submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        # Insert form data into SQLite Database
        c.execute('''
            INSERT INTO todo (name, description, is_done)
            VALUES (?, ?, ?)
        ''', (name, description, is_done))
        conn.commit()
        st.success("Todo added successfully!")

# Displaying Todos in Columns
st.subheader("Todo List")
todos = c.execute('SELECT name, description, is_done FROM todo').fetchall()
for todo in todos:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.text(f"Name: {todo[0]}")
    with col2:
        st.text(f"Description: {todo[1]}")
    with col3:
        st.text(f"Done: {'Yes' if todo[2] else 'No'}")
    st.write("---")

# Run the app: streamlit run your_script.py
