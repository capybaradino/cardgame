from flask import render_template
import card_user
import card_db


def card_admin_view(sid):
    userinfo = "<table border=1>"
    userinfo += "<tr>"
    userinfo += "<td>" + "Mail Address" + "</td><td>" + \
        card_db.getemail_fromsid(sid) + "</td>"
    userinfo += "</tr>"
    userinfo += "<tr>"
    userinfo += "<td>" + "Nickname" + "</td><td>" + \
        card_db.getnickname_fromsid(sid) + "</td>"
    userinfo += "</tr>"
    userinfo += "</table>"
    return render_template('admin.html', title='Admin', userinfo=userinfo)
