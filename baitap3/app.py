from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:131206@localhost/dbtest'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Mô hình dữ liệu cho sinh viên
class Student(db.Model):
    __tablename__ = 'sinhvien'  # Tên bảng trong PostgreSQL
    mssv = db.Column(db.String(13), primary_key=True)
    hoten = db.Column(db.String(200), nullable=False)
    ngaysinh = db.Column(db.Date, nullable=False)
    lop = db.Column(db.String(50), nullable=False)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)

    def set_password(self, password):
        """Hàm mã hóa mật khẩu"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Hàm kiểm tra mật khẩu"""
        return check_password_hash(self.password_hash, password)

def create_default_user():
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin')
        admin.set_password('admin')  # Đặt mật khẩu là "admin" (mã hóa)
        db.session.add(admin)
        db.session.commit()

# Đăng nhập
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == "postgres" and password == "131206":
            session['username'] = username
            return redirect(url_for('index'))
        else:
            flash("Tên đăng nhập hoặc mật khẩu không đúng", "danger")
    return render_template('login.html')

# Đăng xuất
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# Trang chủ
@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    students = Student.query.order_by(Student.mssv).all()
    # Truyền số thứ tự vào context
    return render_template('index.html', students=students, start_index=1)



# Thêm sinh viên
@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        mssv = request.form['mssv']
        hoten = request.form['hoten']
        ngaysinh = request.form['ngaysinh']
        lop = request.form['lop']
        if mssv and hoten and ngaysinh and lop:
            student = Student(mssv=mssv, hoten=hoten, ngaysinh=ngaysinh, lop=lop)
            db.session.add(student)
            db.session.commit()
            flash("Thêm sinh viên thành công!", "success")
            return redirect(url_for('index'))
        else:
            flash("Vui lòng điền đầy đủ thông tin", "warning")
    return render_template('add_student.html')

# Sửa sinh viên
@app.route('/edit_student/<mssv>', methods=['GET', 'POST'])
def edit_student(mssv):
    if 'username' not in session:
        return redirect(url_for('login'))
    student = Student.query.get_or_404(mssv)
    if request.method == 'POST':
        student.hoten = request.form['hoten']
        student.ngaysinh = request.form['ngaysinh']
        student.lop = request.form['lop']
        db.session.commit()
        flash("Cập nhật thông tin thành công!", "success")
        return redirect(url_for('index'))
    return render_template('edit_student.html', student=student)

# Xóa sinh viên
@app.route('/delete_student/<mssv>', methods=['POST'])
def delete_student(mssv):
    if 'username' not in session:
        return redirect(url_for('login'))
    student = Student.query.get_or_404(mssv)
    db.session.delete(student)
    db.session.commit()
    flash("Xóa sinh viên thành công!", "success")
    return redirect(url_for('index'))

# Chạy ứng dụng
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8080)
