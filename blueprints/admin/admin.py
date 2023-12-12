from flask import Blueprint, render_template, redirect, url_for

admin_bp = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

@admin_bp.route('/', methods=['GET'])
def admin():
    return render_template('admin.html')

@admin_bp.route('/workers', methods=['GET'])
def workers():
    return render_template('admin_workers.html')

@admin_bp.route('/machines', methods=['GET'])
def machines():
    return render_template('admin_machines.html')

@admin_bp.route('/work', methods=['GET'])
def work():
    return render_template('admin_work.html')

@admin_bp.route('/reports', methods=['GET'])
def reports():
    return render_template('admin_reports.html')

@admin_bp.route('/management', methods=['GET'])
def management():
    return render_template('admin_management.html')