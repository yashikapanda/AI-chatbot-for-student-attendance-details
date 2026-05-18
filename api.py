from flask import Flask, jsonify, request, send_from_directory
import pandas as pd
import matplotlib.pyplot as plt
import os
import json
from io import BytesIO
import base64

app = Flask(__name__, static_folder='static', static_url_path='')

# Load Excel data
file_path = "New Microsoft Excel Worksheet (2).xlsx"
if not os.path.exists(file_path):
    file_path = r"C:\Users\lenovo\Downloads\New Microsoft Excel Worksheet (2).xlsx"

try:
    student_df = pd.read_excel(file_path, sheet_name="student details")
    subjects = ["All", "NLP", "IOT", "SE", "ML", "ELECTIVE", "OE"]
    
    subject_data = {}
    for sub in subjects:
        if sub != "All":
            subject_data[sub] = pd.read_excel(file_path, sheet_name=sub)
    print("✅ Excel file loaded successfully")
except Exception as e:
    print(f"❌ Error loading Excel: {e}")
    student_df = None

def find_student(query, roll_input_str):
    if roll_input_str is not None and str(roll_input_str).strip() != "":
        try:
            potential_roll = int(str(roll_input_str).strip())
            if potential_roll in student_df["roll no"].values:
                return potential_roll
        except ValueError:
            pass

    query = query.lower()
    for _, row in student_df.iterrows():
        name = str(row["name"]).lower()
        roll = row["roll no"]
        if name in query or str(roll) in query:
            return int(roll)
    return None

def get_student_details(roll):
    data = student_df[student_df["roll no"] == roll]
    if len(data) == 0:
        return "❌ Student not found"
    return str(data.to_dict("records")[0])

def attendance_percentage(roll, subject):
    df = subject_data[subject]
    student_row = df[df["roll no"] == roll]
    if len(student_row) == 0:
        return "❌ No Data", 0, 0
    
    student_row = student_row.iloc[0]
    p, a = 0, 0
    for col in df.columns:
        if str(col).startswith("20"):
            if student_row[col] == "P":
                p += 1
            elif student_row[col] == "A":
                a += 1
    
    total = p + a
    if total == 0:
        return "No Attendance Data", 0, 0
    
    percent = (p / total) * 100
    return f"📊 Attendance Percentage = {round(percent, 2)} %", p, a

def get_attendance_dates(roll, subject, mode="both"):
    df = subject_data[subject]
    student_row = df[df["roll no"] == roll]
    if len(student_row) == 0:
        return "❌ No Data", "❌ No Data", 0, 0
    
    student_row = student_row.iloc[0]
    present, absent = [], []
    
    for col in df.columns:
        if str(col).startswith("20"):
            if student_row[col] == "P":
                present.append(str(col)[:10])
            elif student_row[col] == "A":
                absent.append(str(col)[:10])
    
    present_str = f"✅ Present Dates:\n{present}" if present else "✅ No Present Dates Found"
    absent_str = f"❌ Absent Dates:\n{absent}" if absent else "❌ No Absent Dates Found"
    
    if mode == "present":
        return present_str, "", len(present), len(absent)
    elif mode == "absent":
        return "", absent_str, len(present), len(absent)
    else:
        return present_str, absent_str, len(present), len(absent)

def generate_attendance_chart(roll, subject):
    _, present_count, absent_count = attendance_percentage(roll, subject)
    if present_count == 0 and absent_count == 0:
        return None
    
    labels = ['Present', 'Absent']
    sizes = [present_count, absent_count]
    colors = ['#4CAF50', '#F44336']
    
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
    ax.axis('equal')
    plt.title(f'Attendance for Roll No: {roll}, Subject: {subject}')
    
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode()
    plt.close(fig)
    
    return f"data:image/png;base64,{img_base64}"

# API Routes
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/login', methods=['POST'])
def login_api():
    data = request.json
    roll_no = data.get('roll_no', 0)
    password = data.get('password', '')
    
    # Admin login
    if roll_no == 2005 and password == "Ritesh@2005":
        return jsonify({"success": True, "type": "admin", "message": "Admin Login Successful"})
    
    # Student login
    student = student_df[student_df["roll no"] == roll_no]
    if student.empty:
        return jsonify({"success": False, "message": "Invalid Roll Number"}), 400
    
    student_name = student.iloc[0]["name"]
    expected_password = f"{student_name}@2023"
    
    if password == expected_password:
        return jsonify({"success": True, "type": "student", "name": student_name, "roll": roll_no})
    
    return jsonify({"success": False, "message": "Invalid Password"}), 400

@app.route('/api/query', methods=['POST'])
def query_api():
    data = request.json
    query = data.get('query', '')
    subject = data.get('subject', 'All')
    roll_no = data.get('roll_no', 0)
    is_admin = data.get('is_admin', False)
    
    student_roll = find_student(query, roll_no if is_admin else roll_no)
    
    if student_roll is None:
        return jsonify({"error": "Student not found"}), 400
    
    response = {}
    query_lower = query.lower()
    
    if "detail" in query_lower:
        response['details'] = get_student_details(student_roll)
    
    if "percent" in query_lower or "percentage" in query_lower:
        if subject != "All":
            percentage_result, p, a = attendance_percentage(student_roll, subject)
            response['percentage'] = percentage_result
            response['present_count'] = p
            response['absent_count'] = a
            chart = generate_attendance_chart(student_roll, subject)
            if chart:
                response['chart'] = chart
    
    if "present" in query_lower and subject != "All":
        present_dates, _, _, _ = get_attendance_dates(student_roll, subject, "present")
        response['present_dates'] = present_dates
    
    if "absent" in query_lower and subject != "All":
        _, absent_dates, _, _ = get_attendance_dates(student_roll, subject, "absent")
        response['absent_dates'] = absent_dates
    
    if ("date" in query_lower or "attendance" in query_lower) and subject != "All":
        if "present" not in query_lower and "absent" not in query_lower:
            present_dates, absent_dates, _, _ = get_attendance_dates(student_roll, subject, "both")
            response['present_dates'] = present_dates
            response['absent_dates'] = absent_dates
    
    if "chart" in query_lower and subject != "All":
        response['chart'] = generate_attendance_chart(student_roll, subject)
    
    return jsonify(response)

@app.route('/api/students', methods=['GET'])
def get_students():
    data = student_df.to_dict(orient='records')
    return jsonify(data)

@app.route('/api/subjects', methods=['GET'])
def get_subjects():
    return jsonify(subjects)

if __name__ == '__main__':
    app.run(debug=False)
