import streamlit as st
import pickle
import pandas as pd
import numpy as np

# Function to load data from pickle files
def load_data(file_path):
    return pickle.load(open(file_path, 'rb'))

# Function to preprocess data for display
def preprocess_data(popular_df):
    book_data = {
        'book_name': list(popular_df['Book-Title'].values),
        'author': list(popular_df['Book-Author'].values),
        'image': list(popular_df['Image-URL-M'].values),
        'votes': list(popular_df['Total-Rating'].values),
        'rating': list(round(popular_df['Avg-Rating'], 2).values)
    }
    return book_data

# Function for recommendation
def recommend_books(user_input, pt, books, similarity_scores):
    user_input = user_input.lower()
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    recommendations = []
    for i in similar_items:
        book_info = books[books['Book-Title'] == pt.index[i[0]]].drop_duplicates('Book-Title').iloc[0]
        recommendations.append({
            'book_name': book_info['Book-Title'],
            'author': book_info['Book-Author'],
            'image': book_info['Image-URL-M']
        })

    return recommendations


def main():
    # Load data
    popular_df = load_data('./Data/popular_books.pkl')
    pt = load_data('./Data/pt.pkl')
    books = load_data('./Data/books.pkl')
    similarity_scores = load_data('./Data/similarity_scores.pkl')

    # Preprocess data
    book_data = preprocess_data(popular_df)

    # Set page configuration
    st.set_page_config(page_title="Book Recommendation", page_icon="📚", layout="wide")

    # Main title
    st.title('Book Recommendation System')

    # User input for book search
    user_input = st.text_input('Please type a book to get recommendations')

    # Show recommendations when button is clicked
    if st.button('Show Recommendation'):
        st.header(f'Recommendations for the book: {user_input}')
        recommendations = recommend_books(user_input, pt, books, similarity_scores)
        cols = st.columns(4)
        for i, rec in enumerate(recommendations):
            with cols[i % 4]:
                st.image(rec['image'])
                st.write(rec['book_name'])
                st.write(rec['author'])

    # Separator lines
    st.markdown('---')

    # Top rated books section
    st.title('Top rated books')
    cols = st.columns(4)
    for i in range(len(book_data['book_name'])):
        with cols[i % 4]:
            st.image(book_data['image'][i])
            st.write(book_data['book_name'][i])
            st.write(book_data['author'][i])
            
if __name__ == "__main__":
    main()
