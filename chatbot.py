import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt
import os

print("✅ Imports successful")
file_path = r"C:\Users\lenovo\Downloads\New Microsoft Excel Worksheet (2).xlsx"
print(f"📂 Loading Excel file from: {file_path}")
print(f"📂 File exists: {os.path.exists(file_path)}")
student_df = pd.read_excel(file_path, sheet_name="student details")
print("✅ Excel file loaded")

subjects = ["All","NLP","IOT","SE","ML","ELECTIVE","OE"]

subject_data = {}
for sub in subjects:
    if sub != "All":
        subject_data[sub] = pd.read_excel(file_path, sheet_name=sub)

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

        if name in query:
            return int(roll)

        if str(roll) in query:
            return int(roll)
    return None

def get_student_details(roll):
    data = student_df[student_df["roll no"] == roll]
    if len(data) == 0:
        return "❌ Student not found"
    return str(data.to_dict("records")[0])

def get_attendance_dates(roll, subject, mode="both"):
    df = subject_data[subject]
    student_row = df[df["roll no"] == roll]

    if len(student_row) == 0:
        return "❌ No Data", "❌ No Data", 0, 0

    student_row = student_row.iloc[0]

    present = []
    absent = []

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

def attendance_percentage(roll, subject):
    df = subject_data[subject]
    student_row = df[df["roll no"] == roll]

    if len(student_row) == 0:
        return "❌ No Data", 0, 0

    student_row = student_row.iloc[0]

    p = 0
    a = 0

    for col in df.columns:
        if str(col).startswith("20"):
            if student_row[col] == "P":
                p += 1
            elif student_row[col] == "A":
                a += 1

    total = p + a

    if total == 0:
        return "No Attendance Data", 0, 0

    percent = (p/total)*100

    return f"📊 Attendance Percentage = {round(percent,2)} %", p, a

def generate_attendance_chart(roll, subject):
    _, present_count, absent_count = attendance_percentage(roll, subject)

    if present_count == 0 and absent_count == 0:
        return None

    labels = ['Present', 'Absent']
    sizes = [present_count, absent_count]
    colors = ['#4CAF50', '#F44336']

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
    ax1.axis('equal')
    plt.title(f'Attendance for Roll No: {roll}, Subject: {subject}')

    chart_path = f"attendance_chart_{roll}_{subject}.png"
    plt.savefig(chart_path)
    plt.close(fig1)
    return chart_path

def generate_all_subject_attendance_chart(roll):
    percentages = []
    subject_names = []
    for sub_name in subjects:
        if sub_name == "All":
            continue
        percent_result, _, _ = attendance_percentage(roll, sub_name)
        if percent_result != "No Attendance Data" and "❌ No Data" not in percent_result:
            percentage_value = float(percent_result.split('=')[1].strip().replace('%', ''))
            percentages.append(percentage_value)
            subject_names.append(sub_name)

    if not percentages:
        return None

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(subject_names, percentages, color='skyblue')
    ax.set_xlabel('Subject')
    ax.set_ylabel('Attendance Percentage (%)')
    ax.set_title(f'Attendance Percentage for Roll No: {roll} Across All Subjects')
    ax.set_ylim(0, 100)
    plt.xticks(rotation=45, ha='right')

    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval + 1, round(yval, 2), ha='center', va='bottom')

    plt.tight_layout()
    chart_path = f"all_subject_attendance_chart_{roll}.png"
    plt.savefig(chart_path)
    plt.close(fig)
    return chart_path

def get_roll_suggestions(partial_roll_str):
    if not partial_roll_str or not str(partial_roll_str).strip():
        return gr.update(choices=[], visible=False)

    partial_roll_str = str(partial_roll_str).strip()

    try:
        if int(partial_roll_str) in student_df["roll no"].values:
            return gr.update(choices=[], visible=False)
    except ValueError:
        pass

    all_rolls_str = student_df["roll no"].astype(str)
    suggestions = [
        roll for roll in all_rolls_str
        if roll.startswith(partial_roll_str)
    ]
    return gr.update(choices=suggestions, visible=True)

def admin_login(username, password):
    ADMIN_ID = 2005
    ADMIN_PASSWORD = "Ritesh@2005"
    if username == ADMIN_ID and password == ADMIN_PASSWORD:
        return True
    return False

def chatbot_enhanced(query, roll_input_chatbot_ui_str, subject, logged_in_roll_state, is_admin_logged_in_state):
    effective_roll_for_query = None

    if is_admin_logged_in_state:
        student_roll_to_query = find_student(query, roll_input_chatbot_ui_str)
    else:
        student_roll_to_query = find_student(query, str(logged_in_roll_state))

    if student_roll_to_query is None or student_roll_to_query == 0:
        if is_admin_logged_in_state:
            return "❌ Admin: Please provide a valid Roll Number in the 'Enter Roll Number (Admin Only)' field or in your query.", "", "", "", None, gr.update(visible=False), 0, 0, gr.update(visible=True), ""
        else:
            return "❌ Student: You can only query your own data. Your roll number could not be determined. Please ensure you are logged in.", "", "", "", None, gr.update(visible=False), 0, 0, gr.update(visible=True), ""

    student_roll = student_roll_to_query

    details = ""
    percentage_str = ""
    present_dates = ""
    absent_dates = ""
    present_count = 0
    absent_count = 0
    chart = None

    query_lower = query.lower()

    ask_for_details = "detail" in query_lower
    ask_for_percentage = "percent" in query_lower or "percentage" in query_lower
    ask_for_present_dates_explicit = "present" in query_lower
    ask_for_absent_dates_explicit = "absent" in query_lower
    ask_for_general_attendance = "date" in query_lower or "attendance" in query_lower
    ask_for_all_subject_attendance = "all subject attendance" in query_lower

    is_all_subjects_percentage_query = (subject == "All" and ask_for_percentage)

    show_subject_dropdown = True

    if ask_for_details:
        details = get_student_details(student_roll)

    if ask_for_all_subject_attendance or is_all_subjects_percentage_query:
        all_attendance_summary = f"Attendance Summary for Roll No: {student_roll}\n\n"
        for sub_name in subjects:
            if sub_name == "All":
                continue
            percent_result, p_count, a_count = attendance_percentage(student_roll, sub_name)
            all_attendance_summary += f"- {sub_name}: {percent_result} (Present: {p_count}, Absent: {a_count})\n"
        percentage_str = all_attendance_summary
        present_dates = ""
        absent_dates = ""
        chart = generate_all_subject_attendance_chart(student_roll)
    elif subject == "All":
        if ask_for_percentage or ask_for_present_dates_explicit or ask_for_absent_dates_explicit or ask_for_general_attendance:
            percentage_str = "❌ Please select a specific subject from the dropdown for this type of attendance query."
            present_dates = ""
            absent_dates = ""
            chart = None
    else:
        if ask_for_percentage or ask_for_present_dates_explicit or ask_for_absent_dates_explicit or ask_for_general_attendance:
            percentage_result, p_count, a_count = attendance_percentage(student_roll, subject)
            present_count = p_count
            absent_count = a_count

            if ask_for_percentage:
                percentage_str = percentage_result

            if ask_for_present_dates_explicit:
                present_dates, _, _, _ = get_attendance_dates(student_roll, subject, "present")

            if ask_for_absent_dates_explicit:
                _, absent_dates, _, _ = get_attendance_dates(student_roll, subject, "absent")

            if ask_for_general_attendance and not (ask_for_present_dates_explicit or ask_for_absent_dates_explicit):
                present_dates, absent_dates, _, _ = get_attendance_dates(student_roll, subject, "both")

            if present_count > 0 or absent_count > 0:
                chart = generate_attendance_chart(student_roll, subject)

    if not ask_for_details and not ask_for_percentage and not ask_for_present_dates_explicit and not ask_for_absent_dates_explicit and not ask_for_general_attendance and not ask_for_all_subject_attendance and not is_all_subjects_percentage_query:
        return "💬 Ask about details / percentage / present dates / absent dates / all subject attendance", "", "", "", None, gr.update(visible=False), 0, 0, gr.update(visible=True), str(student_roll)

    chart_visibility_update = gr.update(visible=True) if chart else gr.update(visible=False)

    return details, percentage_str, present_dates, absent_dates, chart, chart_visibility_update, present_count, absent_count, gr.update(visible=show_subject_dropdown), str(student_roll)

def login(roll_no, password):
    student = student_df[student_df["roll no"] == roll_no]

    if student.empty:
        return False

    student_name = student.iloc[0]["name"]

    expected_password = f"{student_name}@2023"

    return password == expected_password


def login_interface(roll_input_val, password_val):
    if login(roll_input_val, password_val):
        student_name = student_df[student_df["roll no"] == roll_input_val].iloc[0]["name"]
        return (
            f"Login Successful! Welcome, {student_name}!",
            gr.update(visible=False),
            gr.update(visible=True),
            gr.update(selected='Attendance Chatbot'),
            roll_input_val,
            False,
            gr.update(visible=False),
            gr.update(visible=True),
            gr.update(visible=False),
            gr.update(visible=False)
        )
    elif admin_login(roll_input_val, password_val):
        return (
            "Admin Login Successful!",
            gr.update(visible=False),
            gr.update(visible=True),
            gr.update(selected='Student Data'),
            roll_input_val,
            True,
            gr.update(visible=True),
            gr.update(visible=True),
            gr.update(visible=True),
            gr.update(visible=True)
        )
    else:
        return (
            "Login Failed: Invalid Roll Number/Admin ID or Password.",
            gr.update(visible=True),
            gr.update(visible=False),
            gr.update(selected='Student Login'),
            0,
            False,
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False)
        )

def logout():
    return (
        "Logged out successfully.",
        gr.update(visible=True),
        gr.update(visible=False),
        gr.update(selected='Student Login'),
        0,
        False,
        gr.update(visible=False),
        gr.update(visible=False),
        gr.update(visible=False),
        gr.update(visible=False)
    )


with gr.Blocks() as demo:
    gr.Markdown("# 🎓 Student Attendance System")

    logged_in_roll = gr.State(value=0)
    is_admin_logged_in = gr.State(value=False)

    with gr.Group(visible=False) as app_interface_group:
        with gr.Row():
            gr.Markdown("## Welcome to the Student Attendance Portal!")
            logout_button = gr.Button("Logout", visible=False, scale=0)

        with gr.Tabs() as main_tabs:
            with gr.TabItem("Student Data", visible=False) as student_data_tab_item:
                gr.Dataframe(value=student_df, label="Student Details Data")
            with gr.TabItem("Attendance Chatbot") as chatbot_tab_item:
                with gr.Column():
                    gr.Markdown("### Ask about Student Attendance and Details")
                    query_input = gr.Textbox(label="Ask Question (e.g., 'details of Student_1', 'percentage of Student_2', 'present dates for 20232003', 'all subject attendance for Student_1')")
                    roll_input_chatbot_ui = gr.Textbox(label="Enter Roll Number (Admin Only)", value="", visible=False)
                    roll_suggestions_dropdown = gr.Dropdown(label="Suggested Roll Numbers", choices=[], visible=False, interactive=True)

                    subject_dropdown = gr.Dropdown(subjects, label="Select Subject", value="All")
                    submit_button = gr.Button("Get Info")

                with gr.Column():
                    student_details_output = gr.Textbox(label="Student Details", interactive=False)
                    attendance_percentage_output = gr.Textbox(label="Attendance Percentage", interactive=False)
                    present_dates_output = gr.Textbox(label="Present Dates", interactive=False)
                    absent_dates_output = gr.Textbox(label="Absent Dates", interactive=False)
                    attendance_chart_output = gr.Image(label="Attendance Chart", type="filepath", interactive=False, height=300)

                roll_input_chatbot_ui.change(
                    fn=get_roll_suggestions,
                    inputs=[roll_input_chatbot_ui],
                    outputs=[roll_suggestions_dropdown],
                    queue=False
                )

                roll_suggestions_dropdown.select(
                    fn=lambda x: gr.update(value=x) if x else "",
                    inputs=[roll_suggestions_dropdown],
                    outputs=[roll_input_chatbot_ui],
                    queue=False
                )

                submit_button.click(
                    fn=chatbot_enhanced,
                    inputs=[
                        query_input,
                        roll_input_chatbot_ui,
                        subject_dropdown,
                        logged_in_roll,
                        is_admin_logged_in
                    ],
                    outputs=[
                        student_details_output,
                        attendance_percentage_output,
                        present_dates_output,
                        absent_dates_output,
                        attendance_chart_output,
                        attendance_chart_output,
                        gr.State(),
                        gr.State(),
                        subject_dropdown,
                        roll_input_chatbot_ui
                    ]
                )

    with gr.TabItem("Student Login") as login_tab_item:
        with gr.Column() as login_column:
            gr.Markdown("### Student/Admin Login")
            login_roll_input = gr.Number(label="Roll Number / Admin ID", precision=0)
            login_password_input = gr.Textbox(label="Password", type="password")
            login_button = gr.Button("Login")
            login_status_output = gr.Textbox(label="Login Status", interactive=False)

        login_button.click(
            fn=login_interface,
            inputs=[login_roll_input, login_password_input],
            outputs=[
                login_status_output,
                login_column,
                app_interface_group,
                main_tabs,
                logged_in_roll,
                is_admin_logged_in,
                student_data_tab_item,
                logout_button,
                roll_input_chatbot_ui,
                roll_suggestions_dropdown
            ]
        )

    logout_button.click(
        fn=logout,
        inputs=[],
        outputs=[
            login_status_output,
            login_column,
            app_interface_group,
            main_tabs,
            logged_in_roll,
            is_admin_logged_in,
            student_data_tab_item,
            logout_button,
            roll_input_chatbot_ui,
            roll_suggestions_dropdown
        ]
    )

demo.launch(share=True)