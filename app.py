"""
CLOUD FILE UPLOAD STORAGE APPS
Main Application File - Flask Backend
BCA Final Year Project
"""

# ============================================
# IMPORTS
# ============================================
from flask import (
    Flask, render_template, request, 
    redirect, url_for, flash, send_file, 
    jsonify, session
)
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import hashlib
import uuid

# ============================================
# INITIALIZATION
# ============================================
app = Flask(__name__)
app.secret_key = 'bca-project-2024-secret-key'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB
app.config['ALLOWED_EXTENSIONS'] = {
    'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif',
    'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx',
    'mp3', 'mp4', 'zip', 'rar', '7z'
}

# ============================================
# UTILITY FUNCTIONS
# ============================================

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def generate_file_id(filename):
    """Generate unique file ID"""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    unique_id = str(uuid.uuid4())[:8]
    return f"{timestamp}_{unique_id}"

def format_file_size(size):
    """Convert bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} TB"

def get_file_icon(filename):
    """Return appropriate icon for file type"""
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    
    icons = {
        # Documents
        'pdf': 'fa-file-pdf',
        'doc': 'fa-file-word', 'docx': 'fa-file-word',
        'txt': 'fa-file-alt',
        'ppt': 'fa-file-powerpoint', 'pptx': 'fa-file-powerpoint',
        'xls': 'fa-file-excel', 'xlsx': 'fa-file-excel',
        
        # Media
        'jpg': 'fa-file-image', 'jpeg': 'fa-file-image',
        'png': 'fa-file-image', 'gif': 'fa-file-image',
        'mp3': 'fa-file-audio', 'wav': 'fa-file-audio',
        'mp4': 'fa-file-video', 'avi': 'fa-file-video',
        
        # Archives
        'zip': 'fa-file-archive', 'rar': 'fa-file-archive',
        '7z': 'fa-file-archive'
    }
    
    return icons.get(ext, 'fa-file')

# ============================================
# ROUTES
# ============================================

@app.route('/')
def index():
    """Home page route"""
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    """File upload route"""
    if request.method == 'POST':
        # Check if file exists
        if 'file' not in request.files:
            flash('⚠️ No file selected!', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        
        # Check if file name is empty
        if file.filename == '':
            flash('⚠️ Please select a file!', 'error')
            return redirect(request.url)
        
        # Validate and save file
        if file and allowed_file(file.filename):
            # Secure filename
            original_filename = secure_filename(file.filename)
            
            # Generate unique filename
            file_id = generate_file_id(original_filename)
            name, ext = os.path.splitext(original_filename)
            filename = f"{file_id}_{name}{ext}"
            
            # Save file
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Get file size
            size = os.path.getsize(file_path)
            
            # Success message
            flash(f'✅ File uploaded successfully!', 'success')
            flash(f'📁 File: {original_filename}', 'info')
            flash(f'📊 Size: {format_file_size(size)}', 'info')
            
            return redirect(url_for('list_files'))
        else:
            flash('❌ File type not allowed!', 'error')
    
    return render_template('upload.html')

@app.route('/files')
def list_files():
    """List all uploaded files"""
    files = []
    
    # Check if uploads folder exists
    if os.path.exists(app.config['UPLOAD_FOLDER']):
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            if os.path.isfile(filepath):
                # Get file stats
                stat = os.stat(filepath)
                
                # Extract original filename (remove ID prefix)
                parts = filename.split('_', 2)
                if len(parts) >= 3:
                    display_name = parts[2]
                else:
                    display_name = filename
                
                # Get file ID
                file_id = parts[1] if len(parts) >= 3 else 'local'
                
                files.append({
                    'id': file_id,
                    'filename': filename,
                    'name': display_name,
                    'size': stat.st_size,
                    'size_formatted': format_file_size(stat.st_size),
                    'icon': get_file_icon(filename),
                    'created': datetime.fromtimestamp(stat.st_ctime),
                    'created_formatted': datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M'),
                    'type': 'local'
                })
    
    # Sort by date (newest first)
    files.sort(key=lambda x: x['created'], reverse=True)
    
    return render_template('files.html', files=files)

@app.route('/download/<filename>')
def download_file(filename):
    """Download file route"""
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if os.path.exists(filepath):
        # Extract original filename
        parts = filename.split('_', 2)
        if len(parts) >= 3:
            download_name = parts[2]
        else:
            download_name = filename
        
        return send_file(filepath, as_attachment=True, download_name=download_name)
    else:
        flash('❌ File not found!', 'error')
        return redirect(url_for('list_files'))

@app.route('/delete/<filename>')
def delete_file(filename):
    """Delete file route"""
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if os.path.exists(filepath):
        os.remove(filepath)
        flash('🗑️ File deleted successfully!', 'success')
    else:
        flash('❌ File not found!', 'error')
    
    return redirect(url_for('list_files'))

@app.route('/preview/<filename>')
def preview_file(filename):
    """Preview file in browser"""
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if os.path.exists(filepath):
        return send_file(filepath)
    else:
        flash('❌ File not found!', 'error')
        return redirect(url_for('list_files'))

@app.route('/api/files')
def api_files():
    """REST API endpoint for files"""
    files = []
    
    if os.path.exists(app.config['UPLOAD_FOLDER']):
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if os.path.isfile(filepath):
                stat = os.stat(filepath)
                files.append({
                    'name': filename,
                    'size': stat.st_size,
                    'created': stat.st_ctime,
                    'type': filename.rsplit('.', 1)[1].lower() if '.' in filename else 'unknown'
                })
    
    return jsonify({
        'status': 'success',
        'count': len(files),
        'files': files
    })

@app.route('/stats')
def storage_stats():
    """Get storage statistics"""
    total_size = 0
    file_count = 0
    
    if os.path.exists(app.config['UPLOAD_FOLDER']):
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if os.path.isfile(filepath):
                total_size += os.path.getsize(filepath)
                file_count += 1
    
    return jsonify({
        'total_files': file_count,
        'total_size': total_size,
        'total_size_formatted': format_file_size(total_size),
        'max_size': app.config['MAX_CONTENT_LENGTH'],
        'max_size_formatted': format_file_size(app.config['MAX_CONTENT_LENGTH'])
    })

# ============================================
# ERROR HANDLERS
# ============================================

@app.errorhandler(404)
def not_found_error(error):
    flash('🔍 Page not found!', 'error')
    return redirect(url_for('index'))

@app.errorhandler(413)
def too_large_error(error):
    flash('⚠️ File too large! Maximum size is 10MB', 'error')
    return redirect(url_for('upload_file'))

@app.errorhandler(500)
def internal_error(error):
    flash('❌ Internal server error!', 'error')
    return redirect(url_for('index'))

# ============================================
# MAIN ENTRY POINT
# ============================================

if __name__ == '__main__':
    # Create uploads folder if it doesn't exist
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
        print("📁 Created uploads folder")
    
    # Print startup banner
    print("\n" + "="*50)
    print("🚀 CLOUD FILE UPLOAD STORAGE APPS")
    print("="*50)
    print(f"📂 Upload folder: {app.config['UPLOAD_FOLDER']}")
    print(f"📊 Max file size: {format_file_size(app.config['MAX_CONTENT_LENGTH'])}")
    print(f"📝 Allowed types: {', '.join(app.config['ALLOWED_EXTENSIONS'])}")
    print(f"🌐 Server: http://localhost:5000")
    print("="*50 + "\n")
    
    # Run app
    app.run(debug=True, host='localhost', port=5000)
