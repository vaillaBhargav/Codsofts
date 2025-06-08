from flask import Flask, render_template, request
import requests

app = Flask(__name__, static_folder='static')
app.secret_key = 'your_secret_key'

OMDB_API_KEY = '857fea31'

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html', movie=None, error=None)

@app.route('/search', methods=['POST'])
def search():
    movie_title = request.form['movie']
    url = f"https://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={movie_title}&type=movie"
    
    try:
        response = requests.get(url)
        data = response.json()

        if data.get('Response') == 'False':
            return render_template('index.html', movie=None, error=data.get('Error', 'Movie not found.'))
        return render_template('index.html', movie=data, error=None)

    except requests.exceptions.RequestException as e:
        return render_template('index.html', movie=None, error="API Error: " + str(e))

# This is required for Vercel
if __name__ == '__main__':
    app.run(debug=True)
else:
    # This is needed for Vercel's serverless environment
    import sys
    from flask import Flask as flask_app
    app = flask_app(__name__)