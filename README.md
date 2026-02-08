# 📁 Cloud File Storage System - BCA Final Year Project

## 📌 Project Overview
A web-based cloud file storage system that allows users to upload, store, and manage files in the cloud. This project demonstrates practical implementation of cloud computing concepts for BCA students.

## 🎯 Features
- ✅ **File Upload** - Upload files to cloud storage with drag & drop support
- ✅ **Cloud Storage** - Files stored in Google Drive (real cloud storage)
- ✅ **File Management** - View, organize, and manage uploaded files
- ✅ **Download Anywhere** - Access files from any device with internet
- ✅ **Responsive Design** - Works on desktop, tablet, and mobile
- ✅ **User Authentication** - Secure Google OAuth authentication
- ✅ **File Type Validation** - Supports multiple file formats
- ✅ **Progress Indicators** - Real-time upload progress

## 🛠️ Technology Stack
- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Cloud Storage**: Google Drive API
- **Authentication**: Google OAuth 2.0
- **Database**: Local file system + Cloud storage

## 📁 Project Structure
```
cloud-file-storage/
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── credentials.json          # Google Drive API credentials (add manually)
├── token.json               # Authentication token (auto-generated)
├── uploads/                  # Local cache folder (auto-created)
├── static/
│   ├── css/
│   │   └── style.css        # All CSS styles
│   └── js/
│       └── script.js        # Frontend JavaScript
└── templates/
    ├── base.html            # Base template
    ├── index.html           # Home page
    ├── upload.html          # File upload page
    └── files.html           # File listing page
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Google Account (for Drive API)
- VS Code or any code editor

### Step 1: Clone/Create Project
```bash
# Create project folder
mkdir cloud-file-storage
cd cloud-file-storage

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### Step 2: Install Dependencies
```bash
pip install flask google-auth-httplib2 google-auth-oauthlib google-api-python-client python-dotenv werkzeug
```

### Step 3: Setup Google Drive API
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project: `BCA-Cloud-Storage`
3. Enable **Google Drive API**
4. Create OAuth 2.0 credentials (Desktop app type)
5. Download `credentials.json` and place in project root

### Step 4: Run the Application
```bash
python app.py
```
Open browser: http://localhost:5000

## 📱 How to Use

### 1. First-time Setup
1. Open http://localhost:5000
2. Click "Connect Google Drive"
3. Sign in with Google account
4. Grant permissions to the app

### 2. Upload Files
1. Click "Upload" in navigation
2. Drag & drop files or click to browse
3. Select file (max 10MB)
4. Click "Upload to Google Drive"
5. File will be stored in your Google Drive

### 3. Manage Files
1. Click "Files" to view all uploaded files
2. Download files using download button
3. Delete files when no longer needed
4. View files in Google Drive

### 4. Access from Anywhere
1. Files are stored in your Google Drive
2. Access from any device:
   - Computer: http://localhost:5000
   - Mobile: Use Google Drive app
   - Any browser: drive.google.com

## 🔧 Project Configuration

### File Size Limits
- Maximum file size: 10MB
- Can be modified in `app.py`

### Supported File Types
- Documents: .txt, .pdf, .doc, .docx
- Images: .jpg, .png, .gif, .jpeg
- Spreadsheets: .xls, .xlsx
- Presentations: .ppt, .pptx
- Media: .mp3, .mp4
- Archives: .zip, .rar

### Storage Locations
- **Primary**: Google Drive (cloud)
- **Fallback**: Local `uploads/` folder
- **Cache**: Temporary local storage

## 🎓 Learning Outcomes
This project helps understand:
1. **Cloud Computing Basics** - How cloud storage works
2. **API Integration** - Working with Google Drive API
3. **Web Development** - Full-stack Flask application
4. **Authentication** - OAuth 2.0 implementation
5. **File Handling** - Upload/download operations
6. **Responsive Design** - Mobile-friendly interface

## 📊 For BCA Project Report

### Include These Sections:
1. **Introduction** - Cloud computing concepts
2. **Literature Review** - Existing cloud storage systems
3. **System Design** - Architecture diagram
4. **Implementation** - Code explanation
5. **Results & Screenshots** - Application screenshots
6. **Conclusion** - Learning outcomes
7. **Future Enhancements** - Additional features

### Important Screenshots:
1. Home page with cloud status
2. Google authentication screen
3. File upload interface
4. File listing page
5. Google Drive with uploaded files
6. Mobile view of application

## 🚀 Deployment Options

### Option 1: PythonAnywhere (Free)
1. Create account on pythonanywhere.com
2. Upload all project files
3. Configure WSGI file
4. Add credentials.json
5. Run application

### Option 2: Heroku
```bash
# Add Procfile
web: python app.py

# Add runtime.txt
python-3.9.0

# Deploy
git push heroku main
```

### Option 3: Local Network
```bash
# Run on local network
python app.py --host=0.0.0.0 --port=5000
```
Access from other devices: http://your-ip:5000

## 🔍 Testing the Application

### Test Cases:
1. **File Upload Test**
   - Upload small file (<1MB)
   - Upload large file (~10MB)
   - Try invalid file type
   - Test drag & drop

2. **Cloud Integration Test**
   - Verify files appear in Google Drive
   - Check authentication flow
   - Test download functionality

3. **User Interface Test**
   - Test on different browsers
   - Test mobile responsiveness
   - Check error messages

## ⚠️ Troubleshooting

### Common Issues:

**1. "credentials.json not found"**
```bash
# Download credentials.json from Google Cloud Console
# Place in project root folder
```

**2. "This app isn't verified"**
- Click "Advanced" → "Go to App (unsafe)"
- This is normal for development apps

**3. Port already in use**
```bash
# Change port in app.py
app.run(debug=True, port=5001)
```

**4. Import errors**
```bash
# Reinstall requirements
pip install -r requirements.txt
```

**5. Authentication errors**
```bash
# Delete token.json and reconnect
rm token.json
# Then restart app
```

## 📈 Future Enhancements
1. **User Registration** - Multiple user accounts
2. **File Sharing** - Share files with others
3. **File Preview** - Preview images/PDFs
4. **Search Functionality** - Search files by name
5. **Folder Management** - Create folders in cloud
6. **Progress Bar** - Real upload progress
7. **Dark Mode** - UI theme toggle
8. **Admin Panel** - For managing users

## 📚 Resources & References

### Documentation:
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Google Drive API](https://developers.google.com/drive/api)
- [Python Documentation](https://docs.python.org/)

### Learning Resources:
- [Cloud Computing Basics](https://aws.amazon.com/what-is-cloud-computing/)
- [OAuth 2.0 Explained](https://oauth.net/2/)
- [Web Development Guide](https://developer.mozilla.org/)

### Useful Tools:
- [Google Cloud Console](https://console.cloud.google.com/)
- [VS Code](https://code.visualstudio.com/)
- [Postman](https://www.postman.com/) (API testing)

## 👨‍💻 Developer Information

**Project**: BCA Final Year Project - Cloud File Storage System  
**Category**: Cloud Computing  
**Complexity**: Beginner to Intermediate  
**Duration**: 4-6 weeks  
**Technology**: Python, Flask, Google Drive API  

## 📄 License
This project is for educational purposes. Free to use and modify for academic projects.

## 🙏 Acknowledgments
- Google Drive API team
- Flask development community
- Open-source contributors
- College faculty guidance

---

## 📞 Contact & Support

For project assistance:
- **College Faculty**: Consult your project guide
- **Classmates**: Collaborative learning
- **Online Forums**: Stack Overflow, GitHub Discussions

**Remember**: This is a learning project. Focus on understanding concepts rather than just copying code. Happy coding! 🚀

---
*Last Updated: [Current Date]*  
*Project Status: Complete & Functional*
