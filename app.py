from flask_mail import Mail
from werkzeug.utils import secure_filename
import os
from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
import socket
from textblob import TextBlob
from nltk.corpus import sentiwordnet as swn
from datetime import datetime
import re

# ────────────────────────────────────────────────
#  Configuration
# ────────────────────────────────────────────────

app = Flask(__name__)
app.secret_key = 'your_secret_key'

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# MySQL Configuration
app.config['MYSQL_HOST']     = 'localhost'
app.config['MYSQL_USER']     = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB']       = 'fraudapps_db'   # ← updated DB name as per your latest context

mysql = MySQL(app)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def index():
    search_query = request.form.get('search_query', '')
    cur = mysql.connection.cursor()

    if search_query:
        cur.execute('''
            SELECT a.app_id, a.application_name, a.description, a.rating, a.category, 
                   a.app_image, AVG(r.sentiment_score) as sentiment_score, a.status
            FROM applications a
            LEFT JOIN reviews r ON a.app_id = r.app_id
            WHERE a.application_name LIKE %s OR a.description LIKE %s
            GROUP BY a.app_id
            ORDER BY sentiment_score DESC
        ''', ('%' + search_query + '%', '%' + search_query + '%'))
    else:
        cur.execute('''
            SELECT a.app_id, a.application_name, a.description, a.rating, a.category, 
                   a.app_image, AVG(r.sentiment_score) as sentiment_score, a.status
            FROM applications a
            LEFT JOIN reviews r ON a.app_id = r.app_id
            GROUP BY a.app_id
            ORDER BY sentiment_score DESC
        ''')

    applications = cur.fetchall()
    cur.close()

    return render_template('index.html', applications=applications)

# ────────────────────────────────────────────────
#  Admin Login
# ────────────────────────────────────────────────

@app.route('/adminlogin', methods=['GET', 'POST'])
def login():
    error = None
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM admin WHERE username = %s AND password = %s', (username, password))
        admin = cur.fetchone()
        cur.close()
        
        if admin:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            error = 'Invalid credentials. Please try again.'
    
    return render_template('admin_login.html', error=error)


# ────────────────────────────────────────────────
#  Admin Dashboard
# ────────────────────────────────────────────────

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin_logged_in' not in session or not session['admin_logged_in']:
        return redirect(url_for('login'))
    
    cur = mysql.connection.cursor()

    cur.execute("SELECT COUNT(*) FROM applications")
    total_applications = cur.fetchone()[0]

    cur.execute("SELECT * FROM reviews WHERE is_fake = 1")
    fake_reviews = cur.fetchall()

    cur.close()

    return render_template(
        'admin/admin_dashboard.html',
        total_applications=total_applications,
        fake_reviews=fake_reviews
    )


@app.route('/admin/delete_fake_review/<int:review_id>', methods=['POST'])
def delete_fake_review(review_id):
    if 'admin_logged_in' not in session or not session['admin_logged_in']:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM reviews WHERE review_id = %s', (review_id,))
    mysql.connection.commit()
    cur.close()

    flash('Review deleted successfully', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/reviews', methods=['GET'])
def admin_reviews():
    if 'admin_logged_in' not in session or not session['admin_logged_in']:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute('''
        SELECT review_id, user_id, app_id, review_text, sentiment_score, 
               ip_address, created_at, is_fake, sentiment_label 
        FROM reviews 
        ORDER BY created_at DESC
    ''')
    reviews = cur.fetchall()
    cur.close()

    return render_template('admin/admin_reviews.html', reviews=reviews)


# ────────────────────────────────────────────────
#  Admin — Add / View / Edit / Delete Applications
# ────────────────────────────────────────────────

@app.route('/admin/add_application', methods=['GET', 'POST'])
def add_application():
    if 'admin_logged_in' not in session or not session['admin_logged_in']:
        return redirect(url_for('login'))

    if request.method == 'POST':
        application_name = request.form['application_name']
        link             = request.form['link']
        description      = request.form['description']
        rating           = request.form.get('rating', 0.0)
        category         = request.form['category']
        app_image        = None

        if 'app_image' in request.files:
            file = request.files['app_image']
            if file.filename != '':
                if allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    app_image = file_path.replace('\\', '/')

        cur = mysql.connection.cursor()
        cur.execute(
            """INSERT INTO applications 
               (application_name, link, description, rating, category, app_image) 
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (application_name, link, description, rating, category, app_image)
        )
        mysql.connection.commit()
        cur.close()

        flash('Application added successfully!', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('admin/add_application.html')


@app.route('/admin/applications', methods=['GET'])
def view_applications():
    if 'admin_logged_in' not in session or not session['admin_logged_in']:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    # Fetching all columns including the new 'status' column
    cur.execute("SELECT app_id, application_name, link, description, rating, category, app_image, status FROM applications")
    apps = cur.fetchall()
    cur.close()

    applications_data = [
        {
            'app_id':           row[0],
            'application_name': row[1],
            'link':             row[2],
            'description':      row[3],
            'rating':           row[4],
            'category':         row[5],
            'app_image':        row[6],
            'status':           row[7]  # enum('genuine', 'fraud')
        }
        for row in apps
    ]

    return render_template('admin/view_applications.html', applications=applications_data)

@app.route('/admin/toggle_app_status/<int:app_id>', methods=['POST'])
def toggle_app_status(app_id):
    if 'admin_logged_in' not in session or not session['admin_logged_in']:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT status FROM applications WHERE app_id = %s", (app_id,))
    current_status = cur.fetchone()[0]
    
    # Toggle logic for ENUM
    new_status = 'fraud' if current_status == 'genuine' else 'genuine'
    
    cur.execute("UPDATE applications SET status = %s WHERE app_id = %s", (new_status, app_id))
    mysql.connection.commit()
    cur.close()
    
    flash(f"Application identity updated to {new_status.upper()}", "info")
    return redirect(url_for('view_applications'))



@app.route('/admin/edit_application/<int:app_id>', methods=['GET', 'POST'])
def edit_application(app_id):
    if 'admin_logged_in' not in session or not session['admin_logged_in']:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()

    if request.method == 'POST':
        application_name = request.form['application_name']
        link             = request.form['link']
        description      = request.form['description']
        rating           = request.form.get('rating', 0.0)
        category         = request.form['category']
        app_image        = None

        if 'app_image' in request.files:
            file = request.files['app_image']
            if file.filename != '':
                if allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    app_image = file_path.replace('\\', '/')

        if app_image:
            cur.execute(
                """UPDATE applications 
                   SET application_name=%s, link=%s, description=%s, rating=%s, category=%s, app_image=%s 
                   WHERE app_id=%s""",
                (application_name, link, description, rating, category, app_image, app_id)
            )
        else:
            cur.execute(
                """UPDATE applications 
                   SET application_name=%s, link=%s, description=%s, rating=%s, category=%s 
                   WHERE app_id=%s""",
                (application_name, link, description, rating, category, app_id)
            )

        mysql.connection.commit()
        cur.close()

        flash('Application updated successfully!', 'success')
        return redirect(url_for('view_applications'))

    cur.execute("SELECT * FROM applications WHERE app_id = %s", (app_id,))
    app_row = cur.fetchone()
    cur.close()

    if not app_row:
        flash('Application not found', 'error')
        return redirect(url_for('view_applications'))

    app_data = {
        'app_id':           app_row[0],
        'application_name': app_row[1],
        'link':             app_row[2],
        'description':      app_row[3],
        'rating':           app_row[4],
        'category':         app_row[5],
        'app_image':        app_row[6]
    }

    return render_template('admin/edit_application.html', application=app_data)


@app.route('/admin/delete_application/<int:app_id>', methods=['GET'])
def delete_application(app_id):
    if 'admin_logged_in' not in session or not session['admin_logged_in']:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM applications WHERE app_id = %s", (app_id,))
    mysql.connection.commit()
    cur.close()

    flash('Application deleted successfully!', 'success')
    return redirect(url_for('view_applications'))


# ────────────────────────────────────────────────
#  User Registration & Login
# ────────────────────────────────────────────────

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email    = request.form['email']
        password = request.form['password']
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", 
                    (username, email, password))
        mysql.connection.commit()
        cur.close()
        
        flash('Registration successful. You can now login.', 'success')
        return redirect(url_for('user_login'))
    
    return render_template('register.html')


@app.route('/user/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        user = cur.fetchone()
        cur.close()
        
        if user:
            session['user_id']   = user[0]
            session['username']  = user[1]
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password. Please try again.', 'error')
    
    return render_template('login.html')


# ────────────────────────────────────────────────
#  User Dashboard
# ────────────────────────────────────────────────

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('user_login'))

    username = session.get('username')
    search_query = request.form.get('search_query', '')

    cur = mysql.connection.cursor()

    if search_query:
        cur.execute('''
            SELECT a.app_id, a.application_name, a.description, a.rating, a.category, 
                   a.app_image, AVG(r.sentiment_score) as sentiment_score, a.status
            FROM applications a
            LEFT JOIN reviews r ON a.app_id = r.app_id
            WHERE a.application_name LIKE %s OR a.description LIKE %s
            GROUP BY a.app_id
            ORDER BY sentiment_score DESC
        ''', ('%' + search_query + '%', '%' + search_query + '%'))
    else:
        cur.execute('''
            SELECT a.app_id, a.application_name, a.description, a.rating, a.category, 
                   a.app_image, AVG(r.sentiment_score) as sentiment_score, a.status
            FROM applications a
            LEFT JOIN reviews r ON a.app_id = r.app_id
            GROUP BY a.app_id
            ORDER BY sentiment_score DESC
        ''')

    applications = cur.fetchall()
    cur.close()

    if not applications:
        flash("No applications available matching your search criteria.", 'info')

    return render_template('dashboard.html', username=username, applications=applications)


# ────────────────────────────────────────────────
#  Review an Application
# ────────────────────────────────────────────────

@app.route('/application/<int:app_id>/review', methods=['GET', 'POST'])
def review_application(app_id):
    if 'user_id' not in session:
        return redirect(url_for('user_login'))
    
    user_id = session.get('user_id')
    
    cur = mysql.connection.cursor()
    
    # Fetch application with status
    cur.execute('''
        SELECT app_id, application_name, link, description, rating, category, 
               app_image, status
        FROM applications 
        WHERE app_id = %s
    ''', (app_id,))
    application = cur.fetchone()
    
    if not application:
        flash("Application not found.", "danger")
        cur.close()
        return redirect(url_for('dashboard'))
    
    # Fetch reviews
    cur.execute('''
        SELECT r.*, u.username 
        FROM reviews r
        LEFT JOIN users u ON r.user_id = u.id
        WHERE r.app_id = %s 
        ORDER BY r.created_at DESC
    ''', (app_id,))
    reviews = cur.fetchall()
    
    if request.method == 'POST':
        review_text = request.form['review_text'].strip()
        
        if not review_text:
            flash("Review cannot be empty.", "warning")
        else:
            ip_address = socket.gethostbyname(socket.gethostname())
            
            sentiment_score, sentiment_label = get_sentiment_score(review_text)
            
            is_fake = has_fake_review(user_id, app_id)
            if is_fake:
                flash("You've already posted too many reviews for this application. Review flagged as fake.", 'warning')
            
            cur.execute(
                '''INSERT INTO reviews 
                   (user_id, app_id, review_text, sentiment_score, sentiment_label, ip_address, is_fake) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                (user_id, app_id, review_text, sentiment_score, sentiment_label, ip_address, is_fake)
            )
            mysql.connection.commit()
            
            flash("Your review has been submitted successfully.", "success")
            
            # Refresh reviews
            cur.execute('''
                SELECT r.*, u.username 
                FROM reviews r
                LEFT JOIN users u ON r.user_id = u.id
                WHERE r.app_id = %s 
                ORDER BY r.created_at DESC
            ''', (app_id,))
            reviews = cur.fetchall()
    
    cur.close()
    
    return render_template('review_application.html', 
                         application=application, 
                         reviews=reviews)


def get_sentiment_score(review_text):
    """
    Use SentiWordNet to analyze sentiment of the review and return the sentiment score and label.
    """
    analysis = TextBlob(review_text)
    polarity = analysis.sentiment.polarity  # Polarity from -1 to 1 (not currently used but available)

    sentiment_score = 0.0
    word_results = []
    total_synsets_count = 0

    print(f"\nAnalyzing review text: \"{review_text}\"\n")

    for word in review_text.split():
        synsets = list(swn.senti_synsets(word))
        if not synsets:
            print(f"Word: '{word}' → No SentiWordNet synsets found. Skipping.\n")
            continue

        print(f"Word: '{word}'")
        for syn in synsets:
            pos = syn.pos_score()
            neg = syn.neg_score()
            obj = syn.obj_score()
            word_sentiment = pos - neg

            sentiment_score += word_sentiment
            total_synsets_count += 1
            word_results.append((word, syn.synset.name(), pos, neg, obj, word_sentiment))

            print(f"  Synset: {syn.synset.name()}")
            print(f"    Pos Score: {pos}")
            print(f"    Neg Score: {neg}")
            print(f"    Obj Score: {obj}")
            print(f"    Word Sentiment (pos - neg): {word_sentiment}")

        print()

    if total_synsets_count > 0:
        avg_sentiment_score = sentiment_score / total_synsets_count
    else:
        avg_sentiment_score = 0.0

    # Assign sentiment label based on thresholds you provided
    if avg_sentiment_score > 0.1:
        sentiment_label = 'Positive'
    elif avg_sentiment_score < -0.1:
        sentiment_label = 'Negative'
    else:
        sentiment_label = 'Neutral'

    # Print the final calculation table
    print("Final Calculation Table:")
    print(f"{'Word':<12} {'Synset':<20} {'PosScore':<10} {'NegScore':<10} {'ObjScore':<10} {'WordScore':<15}")
    print("-" * 80)
    for result in word_results:
        word, synset_name, pos, neg, obj, word_sentiment = result
        print(f"{word:<12} {synset_name:<20} {pos:<10.2f} {neg:<10.2f} {obj:<10.2f} {word_sentiment:<15.2f}")

    print(f"\nFinal Sentiment Score (average over all synsets): {avg_sentiment_score:.3f}")
    print(f"Final Sentiment Label: {sentiment_label}\n")

    return avg_sentiment_score, sentiment_label


def has_fake_review(user_id, app_id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT COUNT(*) FROM reviews WHERE user_id = %s AND app_id = %s', (user_id, app_id))
    count = cur.fetchone()[0]
    cur.close()
    return count >= 3


# ────────────────────────────────────────────────
#  Profile Management
# ────────────────────────────────────────────────

@app.route('/update_profile', methods=['GET', 'POST'])
def update_profile():
    if 'user_id' not in session:
        return redirect(url_for('user_login'))

    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name  = request.form['last_name']
        email      = request.form['email']
        password   = request.form['password']

        profile_picture = None
        if 'profile_picture' in request.files:
            file = request.files['profile_picture']
            if file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                profile_picture = file_path.replace('\\', '/')

        cur = mysql.connection.cursor()
        cur.execute(
            """UPDATE users 
               SET first_name=%s, last_name=%s, email=%s, password=%s, profile_picture=%s 
               WHERE id=%s""",
            (first_name, last_name, email, password, profile_picture, session['user_id'])
        )
        mysql.connection.commit()
        cur.close()

        flash('Profile updated successfully!', 'success')
        return redirect(url_for('view_profile'))

    return render_template('update_profile.html')


@app.route('/view_profile')
def view_profile():
    if 'user_id' not in session:
        return redirect(url_for('user_login'))
    
    cur = mysql.connection.cursor()
    cur.execute('SELECT username, password, first_name, last_name, email, profile_picture FROM users WHERE id = %s', 
                (session['user_id'],))
    user = cur.fetchone()
    cur.close()
    
    if user:
        user_data = {
            'username':       user[0],
            'password':       user[1],
            'first_name':     user[2],
            'last_name':      user[3],
            'email':          user[4],
            'profile_picture': user[5].replace('\\', '/') if user[5] else None
        }
        return render_template('view_profile.html', user=user_data)
    
    flash('User not found', 'error')
    return redirect(url_for('dashboard'))


# ────────────────────────────────────────────────
#  Logout Routes
# ────────────────────────────────────────────────

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('index'))


@app.route('/user/logout')
def user_logout():
    session.clear()
    return redirect(url_for('index'))


# ────────────────────────────────────────────────
#  USER FEEDBACK
# ────────────────────────────────────────────────

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if 'user_id' not in session:
        flash('Please login to submit feedback', 'warning')
        return redirect(url_for('user_login'))

    user_id = session['user_id']

    cur = mysql.connection.cursor()

    if request.method == 'POST':
        feedback_text = request.form.get('feedback_text', '').strip()
        if not feedback_text:
            flash('Feedback cannot be empty', 'danger')
        elif len(feedback_text) > 2000:
            flash('Feedback is too long (max 2000 characters)', 'danger')
        else:
            cur.execute("""
                INSERT INTO feedback (user_id, feedback_text, status)
                VALUES (%s, %s, 'pending')
            """, (user_id, feedback_text))
            mysql.connection.commit()
            flash('Thank you! Your feedback has been submitted.', 'success')

    # Show user's own feedback
    cur.execute("""
        SELECT feedback_id, feedback_text, status, created_at, updated_at
        FROM feedback
        WHERE user_id = %s
        ORDER BY created_at DESC
    """, (user_id,))
    user_feedback = cur.fetchall()

    cur.close()

    return render_template('feedback.html', feedback_list=user_feedback)


# ────────────────────────────────────────────────
#  ADMIN - VIEW & MANAGE ALL FEEDBACK
# ────────────────────────────────────────────────

@app.route('/admin/feedback')
def admin_feedback():
    if 'admin_logged_in' not in session or not session['admin_logged_in']:
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT f.feedback_id, f.user_id, u.username, f.feedback_text,
               f.status, f.created_at, f.updated_at
        FROM feedback f
        LEFT JOIN users u ON f.user_id = u.id
        ORDER BY f.created_at DESC
    """)
    all_feedback = cur.fetchall()
    cur.close()

    return render_template('admin/admin_feedback.html', feedback_list=all_feedback)


@app.route('/admin/feedback/update_status/<int:feedback_id>', methods=['POST'])
def update_feedback_status(feedback_id):
    if 'admin_logged_in' not in session or not session['admin_logged_in']:
        return redirect(url_for('login'))

    new_status = request.form.get('status')
    if new_status not in ['pending', 'read', 'resolved']:
        flash('Invalid status', 'danger')
        return redirect(url_for('admin_feedback'))

    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE feedback 
        SET status = %s, updated_at = CURRENT_TIMESTAMP 
        WHERE feedback_id = %s
    """, (new_status, feedback_id))
    mysql.connection.commit()
    cur.close()

    flash(f'Feedback status updated to: {new_status}', 'success')
    return redirect(url_for('admin_feedback'))

# ────────────────────────────────────────────────
#  ADMIN - VIEW ALL REGISTERED USERS
# ────────────────────────────────────────────────

@app.route('/admin/users')
def admin_users():
    if 'admin_logged_in' not in session or not session['admin_logged_in']:
        flash('Please login as admin first', 'danger')
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT id, username, email, first_name, last_name, 
               profile_picture
        FROM users
    """)
    users = cur.fetchall()
    cur.close()

    return render_template('admin/admin_users.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)