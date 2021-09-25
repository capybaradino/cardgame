from flask.templating import render_template
from class_playdata import Playdata


def card_play_view(sid):
    playdata = Playdata(sid)

    # table start
    contents = "<table border=1>"
    # card image
    contents += "<tr><td>"
    contents += "<img width=100 src='../uploads/"+playdata.p1_card0_filename+"'>"
    contents += "</td></tr>"
    # card name
    contents += "<tr><td>"+playdata.p1_card0_cardname+"</td></tr>"
    # log
    contents += "<tr><td>"+playdata.log+"</td></tr>"
    # card image
    contents += "<tr><td>"
    contents += "<img width=100 src='../uploads/"+playdata.p2_card0_filename+"'>"
    contents += "</td></tr>"
    # card name
    contents += "<tr><td>"+playdata.p2_card0_cardname+"</td></tr>"
    # table end
    contents += "</table>"

    playdata.gameover()

    return render_template('play.html', title='Play', contents=contents)
