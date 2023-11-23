from class_playinfo import Card_info
import card_db


def card_radiobutton(group, id):
    return f'<input type="radio" name="{group}" value="' + str(id) + '">'


def card_createcardhtml(cardview: Card_info, group, id):
    text = ""
    if cardview is not None:
        text = text + f"<font color='Blue'>={cardview.cost}=</font><br>"
        text = text + f"<img width=100 src='../uploads/{cardview.filename}'>"
        text = (
            text + f"<br>" + "<table width='100%' cellspacing='0' cellpadding='0'><tr>"
        )
        text = text + f"<td><font color='Red'>({cardview.attack})</font></td>"
        text = (
            text
            + f"<td><div style='float: right;'><font color='Green'>({cardview.hp})</font></div></td>"
        )
        text = text + f"</tr></table>"
        name = cardview.name
    else:
        filename = card_db.getfilename_fromupname("land")
        text = text + f"<img width=100 src='../uploads/{filename}'>"
        name = ""
    text = text + f"<div style='text-align: center;'>{name}"
    text = text + f'<input type="radio" name="{group}" value="' + str(id) + '">'
    text = text + f"</div>"
    return text


def card_createcardhtmlp2():
    filename = card_db.getfilename_fromupname("sleeve")
    text = "<img width=50 src='../uploads/" + filename + "'>"
    return text
