from flask import Flask, render_template

# Create Flask app
app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Run server
if __name__ == '__main__':
    app.run(debug=True)(debug=True)