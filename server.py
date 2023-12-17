from flask import Flask
app = Flask(__name__)

@app.route('/run-script', methods=['GET'])
def run_script():
    # Execute your Python script here
    # Example: Call a Python function or run a script
    result = "Python script executed successfully"
    return result

if __name__ == '__main__':
    app.run(debug=True)
