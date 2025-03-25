from flask import Flask, request, send_file
import qrcode
from io import BytesIO

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QR Code Generator</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }}
        .container {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
            width: 400px;
            text-align: center;
        }}
        input {{
            width: 100%;
            padding: 10px;
            margin: 8px 0;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 16px;
        }}
        button {{
            width: 100%;
            padding: 10px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            margin-top: 10px;
        }}
        .generate-btn {{ background: #28a745; color: white; }}
        .clear-btn {{ background: #dc3545; color: white; }}
        .success-msg {{
            color: green;
            font-weight: bold;
            margin-top: 10px;
        }}
        .qr-container {{
            margin-top: 20px;
        }}
        img {{
            width: 200px;
            height: 200px;
        }}
    </style>
    <script>
        function clearFields() {{
            document.getElementById('emp_code').value = '';
            document.getElementById('emp_name').value = '';
            document.getElementById('emp_dept').value = '';
            document.getElementById('emp_desg').value = '';
            document.getElementById('qr-container').innerHTML = '';
            document.getElementById('success-msg').innerHTML = '';
        }}
    </script>
</head>
<body>
    <div class="container">
        <h2>QR Code Generator</h2>
        <form action="/" method="post">
            <input type="text" id="emp_code" name="emp_code" placeholder="Employee ID" required>
            <input type="text" id="emp_name" name="emp_name" placeholder="Employee Name" required>
            <input type="text" id="emp_dept" name="emp_dept" placeholder="Department" required>
            <input type="text" id="emp_desg" name="emp_desg" placeholder="Designation" required>
            <button type="submit" class="generate-btn">Generate QR</button>
            <button type="button" class="clear-btn" onclick="clearFields()">Clear</button>
        </form>
        <p id="success-msg" class="success-msg">{message}</p>
        <div id="qr-container">{qr_code}</div>
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    qr_code = ""
    message = ""

    if request.method == "POST":
        emp_code = request.form.get("emp_code", "")
        emp_name = request.form.get("emp_name", "")
        emp_dept = request.form.get("emp_dept", "")
        emp_desg = request.form.get("emp_desg", "")

        if not emp_code or not emp_name or not emp_dept or not emp_desg:
            return HTML_PAGE.format(qr_code="<p style='color:red;'>All fields are required!</p>", message="")

        # Store full employee details in QR code
        qr_data = f"""
        Employee ID: {emp_code}
        Name: {emp_name}
        Department: {emp_dept}
        Designation: {emp_desg}
        """
        qr = qrcode.make(qr_data)

        # Save QR to memory
        img_io = BytesIO()
        qr.save(img_io, format="PNG")
        img_io.seek(0)

        qr_code = f'<img src="/qr_code?emp_code={emp_code}&emp_name={emp_name}&emp_dept={emp_dept}&emp_desg={emp_desg}" alt="QR Code">'
        message = "✅ QR Code Generated Successfully!"

        return HTML_PAGE.format(qr_code=qr_code, message=message)

    return HTML_PAGE.format(qr_code="", message="")

@app.route("/qr_code")
def get_qr():
    emp_code = request.args.get("emp_code", "Unknown")
    emp_name = request.args.get("emp_name", "Unknown")
    emp_dept = request.args.get("emp_dept", "Unknown")
    emp_desg = request.args.get("emp_desg", "Unknown")

    # Store full employee details in QR code
    qr_data = f"""
    Employee ID: {emp_code}
    Name: {emp_name}
    Department: {emp_dept}
    Designation: {emp_desg}
    """
    qr = qrcode.make(qr_data)

    img_io = BytesIO()
    qr.save(img_io, format="PNG")
    img_io.seek(0)
    
    return send_file(img_io, mimetype="image/png")

if __name__ == "__main__":
    app.run(debug=True)