# 🎓 Student Attendance System - Vercel Deployment

**GitHub Repository:** https://github.com/yashikapanda/AI-chatbot-for-student-attendance-details

**Live Demo:** Deploy using steps below ⬇️

---

## 📦 **Project Files**

All files needed for Vercel deployment are included:

```
📁 Repository
├── 📄 api.py                           (Flask backend - main app)
├── 📄 vercel.json                      (Vercel configuration)
├── 📄 requirements.txt                 (Python dependencies)
├── 📄 README.md                        (This file)
├── 📄 VERCEL_DEPLOYMENT.md             (Detailed deployment guide)
├── 📊 New Microsoft Excel Worksheet (2).xlsx  (Student data)
└── 📁 static/
    └── 📄 index.html                   (Web UI frontend)
```

---

## 🚀 **Deploy to Vercel (3 Easy Steps)**

### **Step 1: Install Vercel CLI**
```bash
npm install -g vercel
```

### **Step 2: Login to Vercel**
```bash
vercel login
```
- Opens browser, authenticate with GitHub/Google/email

### **Step 3: Deploy from GitHub**

**Option A: Deploy from Your Machine**
```bash
git clone https://github.com/yashikapanda/AI-chatbot-for-student-attendance-details.git
cd AI-chatbot-for-student-attendance-details
vercel --prod
```

**Option B: Deploy Directly from GitHub (Easiest)**
1. Go to https://vercel.com/new
2. Click **"Import Git Repository"**
3. Paste: `https://github.com/yashikapanda/AI-chatbot-for-student-attendance-details.git`
4. Click **"Import"**
5. Click **"Deploy"**
6. Wait ~2-3 minutes ⏳
7. Get your live URL! 🎉

---

## ✅ **What Gets Deployed**

- ✅ **Flask API Backend** - Serverless Python functions
- ✅ **Web UI** - Beautiful HTML/CSS/JavaScript interface  
- ✅ **Student Data** - Excel file with all student records
- ✅ **Attendance Logic** - All chatbot features via REST API

---

## 🔐 **Login Credentials**

### Admin Access
- **Username:** `2005`
- **Password:** `Ritesh@2005`

### Student Access
- **Roll Number:** Any number from Excel file
- **Password:** `<StudentName>@2023`
  - Example: If student name is "Student_1", password is `Student_1@2023`

---

## 🎯 **Features**

✨ **Student Features:**
- View personal details
- Check attendance percentage
- See present/absent dates by subject
- View attendance charts

📊 **Admin Features:**
- View all student data
- Query any student's information
- Generate attendance reports
- See cross-subject attendance analysis

---

## 📊 **Excel File Structure**

Your Excel file must have these sheets:
- `student details` - Main student information
- `NLP` - Subject attendance data
- `IOT` - Subject attendance data
- `SE` - Subject attendance data
- `ML` - Subject attendance data
- `ELECTIVE` - Subject attendance data
- `OE` - Subject attendance data

**Column Format:**
- Roll numbers in first column
- Student names in second column
- Date columns: YYYY-MM-DD format with P (Present) or A (Absent)

---

## 🛠️ **Technology Stack**

- **Backend:** Python Flask
- **Frontend:** HTML5, CSS3, JavaScript
- **Data:** Pandas, Excel files
- **Charts:** Matplotlib
- **Hosting:** Vercel Serverless

---

## 📱 **Vercel Deploy Link**

Once deployed, your app will be available at:
```
https://your-project-name.vercel.app
```

---

## ❓ **Troubleshooting**

### "Module not found" error
- Check `requirements.txt` has all packages
- Rebuild: `vercel --prod`

### "Excel file not found"
- Excel file must be in root directory
- Filename must match exactly: `New Microsoft Excel Worksheet (2).xlsx`

### "Login not working"
- Check credentials above
- Verify Excel has correct sheet names
- Try admin login first: 2005 / Ritesh@2005

### "Page loads but no response"
- Wait 2-3 minutes for cold start
- Check Vercel deployment logs
- Refresh browser

---

## 📚 **Helpful Links**

- 🔗 Vercel Documentation: https://vercel.com/docs
- 🔗 Flask Documentation: https://flask.palletsprojects.com/
- 🔗 Python on Vercel: https://vercel.com/docs/concepts/functions/serverless-functions/python

---

## 🎉 **Your App is Ready to Deploy!**

Deploy now and start using your attendance system on Vercel! 

**Questions or issues?** Check `VERCEL_DEPLOYMENT.md` for detailed steps.

---

**Happy Deploying! 🚀**
