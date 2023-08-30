// API処理
function play_post(url) {
    var xhr = new XMLHttpRequest();
    xhr.open("post", url, true);
    xhr.onload = function () {
        var result = xhr.responseText;
        // if (xhr.readyState == 4 && xhr.status == "200") {
        if (xhr.readyState == 4) {
            var json = JSON.parse(result);
            document.cookie = "card_lastlog=" + JSON.stringify(json);
            // window.location.reload();
            fetchData();
        } else {
        }
    }
    xhr.send(null);
}
function disp_lastlog() {
    var lastlog = getCookieValue("card_lastlog");
    if (lastlog) {
        document.getElementById("lastlog").textContent = lastlog;
    } else {
        document.getElementById("lastlog").textContent = "-";
    }
}
function system_turnend() {
    var sid = getCookieValue("card_sid");
    var url = "/api/system/" + sid + "/turnend";
    play_post(url);
}
function play_left(src, dst) {
    var sid = getCookieValue("card_sid");
    var url = "/api/play/" + sid + "/" + src + "/" + dst;
    // url = "/api/play/hogehoge/card1/card2"
    play_post(url);
}
function play_attack(src, dst) {
    var sid = getCookieValue("card_sid");
    var url = "/api/play/" + sid + "/" + src + "/" + dst;
    play_post(url);
}

// /***** ドラッグ開始時の処理 *****/
function f_dragstart(event) {
    //ドラッグするデータのid名をDataTransferオブジェクトにセット
    event.dataTransfer.setData("text", event.target.id);
}

// /***** ドラッグ要素がドロップ要素に重なっている間の処理 *****/
function f_dragover(event) {
    //dragoverイベントをキャンセルして、ドロップ先の要素がドロップを受け付けるようにする
    event.preventDefault();
}

// /***** ドロップ時の処理 *****/
function f_drop(event) {
    //ドラッグされたデータのid名をDataTransferオブジェクトから取得
    var id_name_src = event.dataTransfer.getData("text");
    //ドロップ先のid名を取得
    var id_name_dst = event.target.id;
    //API発行
    if (id_name_src.startsWith("hand_")) {
        if (id_name_dst.startsWith("leftboard_")) {
            play_left(id_name_src, id_name_dst);
        }
    }
    if (id_name_src.startsWith("leftboard_")) {
        if (id_name_dst.startsWith("rightboard_")) {
            play_attack(id_name_src, id_name_dst);
        }
    }
    //id名からドラッグされた要素を取得
    // var drag_elm = document.getElementById(id_name);
    //ドロップ先にドラッグされた要素を追加
    // event.currentTarget.appendChild(drag_elm);
    //エラー回避のため、ドロップ処理の最後にdropイベントをキャンセルしておく
    event.preventDefault();
}

async function fetchData() {
    var sid = getCookieValue("card_sid");
    // 画面初期化
    {
        setdivvalue('turndisp_button3', "");
        // P1ハンド
        for (let i = 0; i < 10; i++) {
            setdivvalue('p1card' + i + '_cost', "");
            setdivvalue('p1card' + i + '_attack', "");
            setdivvalue('p1card' + i + '_hp', "");
            setdivvalue('p1card' + i + '_name', "");
            removedivimage('p1card' + i, "");
        }
        // P1ボード
        for (let i = 0; i < 6; i++) {
            setdivvalue('p1board' + i + '_cost', "");
            setdivvalue('p1board' + i + '_attack', "");
            setdivvalue('p1board' + i + '_hp', "");
            setdivvalue('p1board' + i + '_name', "");
            removedivimage('p1board' + i, "");
        }
        // P2ハンド
        for (let i = 0; i < 10; i++) {
            setdivvalue('p2card' + i, "")
        }
        // P2ボード
        for (let i = 0; i < 6; i++) {
            setdivvalue('p2board' + i + '_cost', "");
            setdivvalue('p2board' + i + '_attack', "");
            setdivvalue('p2board' + i + '_hp', "");
            setdivvalue('p2board' + i + '_name', "");
            removedivimage('p2board' + i, "");
        }
    }
    try {
        const response = await fetch('/api/view/' + sid);
        if (response.status != 200) {
            location.reload();
        }
        const data = await response.json();

        // 共通キー情報
        const key_name = "name";
        const key_hp = "HP";
        const key_decknum = "decknum";
        const key_mp = "MP";
        const key_maxmp = "maxMP";

        // ターン情報
        const key_turn = "turn";
        const turn = data[key_turn];
        if (turn == "p1turn") {
            setdivvalue('turndisp_button3', "Turn end");
        } else {
            setdivvalue('turndisp_button3', "Enemy turn");
        }

        // Player1関連情報
        {
            const key_p1 = "player1";
            const player1 = data[key_p1];
            var value;
            value = player1[key_name];
            setdivvalue('playername1_left', value);
            // P1ステータス
            value = player1[key_hp];
            setdivvalue('p1stat_hp', value);
            value = player1[key_decknum];
            setdivvalue('p1stat_decknum', value);
            value = player1[key_mp];
            setdivvalue('p1stat_mp', value);
            value = player1[key_maxmp];
            setdivvalue('p1stat_maxmp', value);
            // P1ハンド
            const hand = player1["hand"];
            for (let i = 0; i < hand.length; i++) {
                const item = hand[i];
                const cost = item['cost'];
                const attack = item['attack'];
                const hp = item['hp'];
                const name = item['name'];
                const graphic = item['graphic'];
                setdivvalue('p1card' + i + '_cost', cost);
                setdivvalue('p1card' + i + '_attack', attack);
                setdivvalue('p1card' + i + '_hp', hp);
                setdivvalue('p1card' + i + '_name', name);
                setdivimage('p1card' + i, graphic);
            }
            // P1ボード
            const board = player1["board"];
            for (let j = 0; j < board.length; j++) {
                const item = board[j];
                const i = item['location'];
                const cost = item['cost'];
                const attack = item['attack'];
                const hp = item['hp'];
                const name = item['name'];
                const graphic = item['graphic'];
                setdivvalue('p1board' + i + '_cost', cost);
                setdivvalue('p1board' + i + '_attack', attack);
                setdivvalue('p1board' + i + '_hp', hp);
                setdivvalue('p1board' + i + '_name', name);
                setdivimage('p1board' + i, graphic);
            }
        }

        // Player2関連情報
        {
            const key_p2 = "player2";
            const player2 = data[key_p2];
            var value;
            value = player2[key_name];
            setdivvalue('playername2_right', value);
            // P2ステータス
            value = player2[key_hp];
            setdivvalue('p2stat_hp', value);
            value = player2[key_decknum];
            setdivvalue('p2stat_decknum', value);
            value = player2[key_mp];
            setdivvalue('p2stat_mp', value);
            value = player2[key_maxmp];
            setdivvalue('p2stat_maxmp', value);
            // P2ハンド
            const handnum = player2["handnum"];
            for (let i = 0; i < handnum; i++) {
                setdivvalue('p2card' + i, "C")
            }
            // P2ボード
            const board = player2["board"];
            for (let j = 0; j < board.length; j++) {
                const item = board[j];
                const i = item['location'];
                const cost = item['cost'];
                const attack = item['attack'];
                const hp = item['hp'];
                const name = item['name'];
                const graphic = item['graphic'];
                setdivvalue('p2board' + i + '_cost', cost);
                setdivvalue('p2board' + i + '_attack', attack);
                setdivvalue('p2board' + i + '_hp', hp);
                setdivvalue('p2board' + i + '_name', name);
                setdivimage('p2board' + i, graphic);
            }
        }

    } catch (error) {
        console.error('Get data was failed:', error);
    }
}
function setdivimage(id, imageUrl) {
    const imageDiv = document.getElementById(id);
    const imageElement = document.createElement('img');
    imageElement.src = imageUrl;
    imageDiv.appendChild(imageElement);
}
function removedivimage(id, imageUrl) {
    const parentDiv = document.getElementById(id);
    const images = parentDiv.querySelectorAll("img");
    images.forEach(image => {
        parentDiv.removeChild(image);
    });
}
function setdivvalue(id, value) {
    const divElement = document.getElementById(id);
    divElement.textContent = value; // データを<div>要素に表示  
}
function getCookieValue(key) {
    // Cookieの値を取得
    var cookies = document.cookie;
    var cookieArray = cookies.split(';');

    var cookieValue = null;
    for (var i = 0; i < cookieArray.length; i++) {
        var cookie = cookieArray[i].trim();
        var keystring = key + '='
        if (cookie.indexOf(keystring) === 0) {
            cookieValue = cookie.substring(keystring.length, cookie.length);
            break;
        }
    }
    return cookieValue;
}
function refreshPage() {
    // location.reload();
    fetchData();
}