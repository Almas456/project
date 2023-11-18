import subprocess
import traceback
from flask import Flask, render_template, request
import sys
from io import StringIO

app = Flask(__name__)

def scan_and_debug_code(code):
    # Redirect standard output to capture print statements
    original_stdout = sys.stdout
    sys.stdout = StringIO()

    try:
        # Executing the code to identify runtime errors
        exec(code)
        debug_result = "No errors found."
    except Exception as e:
        # Returning the error message
        debug_result = f"Error: {str(e)}\n{traceback.format_exc()}"
    
    # Get the content of standard output (print statements)
    captured_output = sys.stdout.getvalue()
    
    # Reset the standard output
    sys.stdout = original_stdout
    
    return captured_output, debug_result

@app.route('/', methods=['GET', 'POST'])
def index():
    scan_result = ""
    debug_result = ""

    if request.method == 'POST':
        code = request.form['code']
        scan_result, debug_result = scan_and_debug_code(code)

    return render_template('index.html', code=code, scan_result=scan_result, debug_result=debug_result)

if __name__ == "__main__":
    app.run(debug=True)



