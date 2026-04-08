# 🚀 Vercel Deployment Guide - Student Attendance System

## Files Structure (Ready to Deploy)

```
your-project/
├── api.py                                         (Flask backend)
├── vercel.json                                    (Vercel config)
├── requirements.txt                               (Python dependencies)
├── New Microsoft Excel Worksheet (2).xlsx         (Student data)
└── static/
    └── index.html                                 (Frontend UI)
```

## ✅ Deployment Steps

### 1️⃣ **Install Vercel CLI**
```bash
npm install -g vercel
```

### 2️⃣ **Login to Vercel**
```bash
vercel login
```
- Opens browser, sign in with GitHub/Google/email

### 3️⃣ **Prepare Your Project**
Create a folder with all files:
```bash
mkdir my-attendance-app
cd my-attendance-app

# Copy these files into this folder:
# - api.py
# - vercel.json
# - requirements.txt
# - New Microsoft Excel Worksheet (2).xlsx
# - static/index.html
```

### 4️⃣ **Deploy to Vercel**
```bash
vercel --prod
```

- Select your project name
- Choose framework: **Other**
- Allow Vercel to proceed

### 5️⃣ **Wait for Deployment**
- Build logs will appear
- Once complete, you get a **Production URL**

---

## 🎯 Your Live App Will Be At:
```
https://your-project-name.vercel.app
```

---

## 📋 Quick Checklist

- [ ] Files organized in correct structure
- [ ] All 5 files present (api.py, vercel.json, requirements.txt, Excel, index.html)
- [ ] Vercel CLI installed
- [ ] Vercel account created
- [ ] Run `vercel --prod`
- [ ] Access your URL

---

## ⚙️ How It Works on Vercel

✅ **Flask API** runs on Vercel serverless functions
✅ **HTML/CSS/JS** frontend loaded from static files
✅ **Excel data** served with the app
✅ **Easy to update** - just push, redeploy

---

## 🔧 Troubleshooting

**"Excel file not found" error:**
- Make sure Excel file is in the root directory
- Check filename exactly matches: `New Microsoft Excel Worksheet (2).xlsx`

**"API not responding":**
- Check Vercel deployment logs
- Verify all files uploaded
- Wait 2-3 minutes for cold start

**Login doesn't work:**
- Admin: ID: 2005, Password: Ritesh@2005
- Check Excel has correct sheet names

---

## 📞 Need Help?
- Vercel Docs: https://vercel.com/docs
- Flask Docs: https://flask.palletsprojects.com/
- Python on Vercel: https://vercel.com/docs/concepts/functions/serverless-functions/python

---

**Your app is now Vercel-ready! 🎉**
