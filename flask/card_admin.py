from flask import render_template
import card_user


def card_admin_view():
    return render_template('admin.html', title='Admin')
