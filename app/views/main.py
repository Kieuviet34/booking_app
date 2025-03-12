from flask import Blueprint, render_template

# Khởi tạo blueprint cho trang chủ, không cần url_prefix vì route sẽ là "/"
main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/')
def index():
    # Render trang chủ (index.html) nằm trong thư mục app/templates/
    return render_template('index.html')
