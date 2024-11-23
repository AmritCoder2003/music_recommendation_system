# Importing necessary modules for the Flask web application and data handling
from flask import Flask, render_template, request
import pickle
import pandas as pd
import difflib

# Loading the pre-saved music data and similarity matrix from pickle files
music_data = pickle.load(open('musicrec.pkl', 'rb'))
similarity = pickle.load(open('similarities.pkl', 'rb'))

# Creating a Flask application instance
app = Flask(__name__)

@app.route('/')
def home():
    # Rendering the home page (index.html) when accessing the root URL
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    if request.method == 'POST':
        # Retrieving the song name submitted via the form and processing it
        song_name = request.form['song'].strip().lower()
        
        # Finding close matches to the submitted song name with a cutoff for similarity
        close_match = difflib.get_close_matches(song_name, music_data['title'].str.lower().values, n=1, cutoff=0.7)

        if close_match:
            # If a close match is found, retrieve the matched song title
            matched_song = close_match[0]
            # Find the index of the matched song in the music data
            music_index = music_data[music_data['title'].str.lower() == matched_song].index[0]
            # Retrieve the similarity scores for the matched song
            distances = similarity[music_index]
            # Create a list of tuples (index, similarity score) and sort it in descending order
            # Exclude the first item (itself) and select the top 5 most similar songs
            music_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
            # Extract the titles of the top 5 similar songs
            recommendations = [music_data.iloc[i[0]].title for i in music_list]
            # Render the result page (result.html) with the recommendations and the original song title
            return render_template('result.html', recommendations=recommendations, song=music_data.iloc[music_index].title)
        else:
            # If no close match is found, return to the home page with an error message
            return render_template('index.html', error="Song not found. Please try another song.")
    
    # For any request method other than POST, render the home page
    return render_template('index.html')

# Running the Flask application in debug mode
if __name__ == '__main__':
    app.run(debug=True)
