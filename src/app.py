from flask import Flask, render_template

app = Flask(__name__)
# Autosave
app.debug = True

@app.route('/')
def index():
  return render_template('home.html')

# Starts Flask App
if __name__ == '__main__':
  app.run()