import uuid
from flask import render_template
from flask.globals import request
from werkzeug.utils import redirect
import card_util
import card_db


def card_management_delete(filename, callback):
    card_db.deletefile_fromfilename_admin(filename)
    return redirect(callback)


def card_management_view():
    uploadedinfo = card_util.card_gettablehtml_admin('card_material')

    return render_template('manage_image.html', title='manage_image', 
                           uploadedinfo=uploadedinfo)
