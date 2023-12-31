// API処理
function play_post(url) {
    var xhr = new XMLHttpRequest();
    xhr.open("post", url, true);
    xhr.onload = function () {
        var result = xhr.responseText;
        // if (xhr.readyState == 4 && xhr.status == "200") {
        if (xhr.readyState == 4) {
            var json = JSON.parse(result);
            // document.cookie = "card_lastlog=" + JSON.stringify(json);
            document.getElementById("p1leader_log").textContent = JSON.stringify(json);
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
function system_surrender() {
    var sid = getCookieValue("card_sid");
    var url = "/api/system/" + sid + "/surrender";
    play_post(url);
}
var temp_url = "";
function play_left(src, dst) {
    var sid = getCookieValue("card_sid");
    var url = "/api/play/" + sid + "/" + src + "/" + dst;
    var effect_array = [];
    if (src != "hand_10") {
        // 召喚時効果チェック
        var numbersArray = src.match(/\d+/g);
        var hand_no = numbersArray[0];
        var data = fetchdata;
        const key_p1 = "player1";
        const player1 = data[key_p1];
        const hand = player1["hand"];
        const item = hand[hand_no];
        effect_array = item["effect"].split(",");
    }
    var onplay = false;
    for (var i = 0; i < effect_array.length; i++) {
        effect = effect_array[i];
        if (effect.startsWith("onplay")) {
            // TODO 他の召喚時効果対応
            if (effect.includes("dmg")) {
                if (!effect.includes("leader")) {
                    // 3枚目の選択に進む
                    temp_url = url;
                    document.getElementById("middle3_boarder").textContent = "Select target.";
                    onplay = true;
                }
            }
            if (effect.includes("attack")) {
                // 3枚目の選択に進む
                temp_url = url;
                document.getElementById("middle3_boarder").textContent = "Select target.";
                onplay = true;
            }
        }
    }
    if (onplay == false) {
        // url = "/api/play/hogehoge/card1/card2"
        play_post(url);
    }
}
function play_attack(src, dst) {
    var sid = getCookieValue("card_sid");
    var url = "/api/play/" + sid + "/" + src + "/" + dst;
    play_post(url);
}

function bottomSetting() {
    if (confirm("Surrender?")) {
        // ユーザーがOKボタンをクリックした場合の処理
        system_surrender();
    } else {
        // ユーザーがキャンセルボタンをクリックした場合の処理
    }
}

function changeBgColor(id, color) {
    // 背景色を変更する要素を取得
    var divElement = document.getElementById(id);
    // 新しい背景色を設定
    divElement.style.backgroundColor = color;
}

function changeBorderColor(id, color) {
    var divElement = document.getElementById(id);
    divElement.style.borderColor = color;
    divElement.style.borderWidth = "5px";
}

function resetBorderColor(id) {
    var divElement = document.getElementById(id);
    divElement.style.borderColor = "black";
    divElement.style.borderWidth = "1px";
}

var click2event = null;
var clicked = false;

function f_onclick(event) {
    if (temp_url != "") {
        var id_name_dst = event.target.id;
        var url = temp_url + "/" + id_name_dst;
        play_post(url);
    } else if (click2event != null) {
        //API発行
        id_name_src = click2event.target.id;
        id_name_dst = event.target.id;
        if (id_name_src.startsWith("hand_")) {
            if (id_name_dst.startsWith("leftboard_")) {
                play_left(id_name_src, id_name_dst);
            }
            if (id_name_dst.startsWith("rightboard_")) {
                play_attack(id_name_src, id_name_dst);
            }
        }
        if (id_name_src.startsWith("leftboard_")) {
            if (id_name_dst.startsWith("rightboard_")) {
                play_attack(id_name_src, id_name_dst);
            }
        }
        click2event.target.style.backgroundColor = "rgba(255, 255, 255, 0)";
        click2event = null;
        clicked = false;
    } else {
        f_onclick2(event);
    }
}

// クリックバージョン
function f_onclick2(event) {
    // divの色を半透明の赤にする
    if (clicked == false) {
        event.target.style.backgroundColor = "rgba(255, 0, 0, 0.5)";
        click2event = event;
        clicked = true;
    } else {
        event.target.style.backgroundColor = "rgba(255, 255, 255, 0)";
        click2event = null;
        clicked = false;
    }
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
        if (id_name_dst.startsWith("rightboard_")) {
            play_attack(id_name_src, id_name_dst);
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

var fetchdata;
var turn = "p2turn";
var intervalId;

async function fetchData() {
    fetchData_impl();
    intervalId = setInterval(function () {
        fetchData_impl();
    }, 1000);
}

var intervalId2;

async function pageReload() {
    intervalId2 = setInterval(function () {
        location.reload();
    }, 1000);
}

var intervalId3;
var timer = 60;
var preturn = "";

async function countdown() {
    intervalId3 = setInterval(function () {
        document.getElementById("p1leader_time").textContent = timer;
        timer--;
        if (timer < 0) {
            clearInterval(intervalId3);
            time = 60;
            system_turnend();
        }
    }, 1000);
}

async function fetchData_impl() {
    var sid = getCookieValue("card_sid");
    try {
        const response = await fetch('/api/view/' + sid);
        if (response.status != 200) {
            if (response.status != 500) {
                pageReload();
            }
        }
        const data = await response.json();
        fetchdata = data;

        // ターン情報
        const key_turn = "turn";
        turn = data[key_turn];
        if (turn == "p1turn") {
            clearInterval(intervalId);
            if (preturn != turn) {
                // id="p1leader_time"のdivに60秒のカウントダウンタイマーを表示
                timer = data["timeout"];
                countdown();
            }
        } else {
            clearInterval(intervalId3);
        }
        preturn = turn;

        // ログ情報
        const key_log = "log";
        const log = data[key_log];
        const logs = log.split(",");
        var displog = "";
        var start = logs.length - 8;
        if (start < 0) {
            start = 0;
        }
        for (let i = start; i < logs.length; i++) {
            var line = logs[i];
            line = line.replace("[", "<b>[");
            line = line.replace("]", "]</b><br>");
            displog += line + "<br>";
        }
        setdivvalue("middle3_boarder", displog)

        // 画面初期化
        {
            setdivvalue('turndisp_button3', "");
            // 変数初期化
            temp_url = "";
        }

        // 共通キー情報
        const key_name = "name";
        const key_hp = "HP";
        const key_decknum = "decknum";
        const key_mp = "MP";
        const key_maxmp = "maxMP";

        // ターン情報
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
                if (attack >= 0) {
                    setdivvalue('p1card' + i + '_attack', attack);
                    setdivvalue('p1card' + i + '_hp', hp);
                } else {
                    setdivvalue('p1card' + i + '_attack', "");
                    setdivvalue('p1card' + i + '_hp', "");
                }
                setdivvalue('p1card' + i + '_name', "" + name + "");
                const effect = item['effect'];
                if (effect != "") {
                    seteffecttext('p1card' + i + '_text', effect);
                } else {
                    seteffecttext('p1card' + i + '_text', "");
                }
                if (player1[key_mp] >= cost) {
                    changeBorderColor('p1card' + i, "green");
                } else {
                    resetBorderColor('p1card' + i)
                }
                setdivimage('p1card' + i, graphic);
            }
            for (let i = hand.length; i < 10; i++) {
                setdivvalue('p1card' + i + '_cost', "");
                setdivvalue('p1card' + i + '_attack', "");
                setdivvalue('p1card' + i + '_hp', "");
                setdivvalue('p1card' + i + '_name', "");
                setdivvalue('p1card' + i + '_text', "");
                removedivimage('p1card' + i, "");
                resetBorderColor('p1card' + i);
            }
            // P1ボード
            const board = player1["board"];
            for (let i = 0; i < 6; i++) {
                flg = false;
                for (let j = 0; j < board.length; j++) {
                    const item = board[j];
                    if (i != item['location']) {
                        continue
                    }
                    flg = true;
                    const cost = item['cost'];
                    const attack = item['attack'];
                    const hp = item['hp'];
                    const name = item['name'];
                    const graphic = item['graphic'];
                    setdivvalue('p1board' + i + '_cost', cost);
                    setdivvalue('p1board' + i + '_attack', attack);
                    setdivvalue('p1board' + i + '_hp', hp);
                    setdivvalue('p1board' + i + '_name', name);
                    effect = item['effect'];
                    if (effect != "") {
                        seteffecttext('p1board' + i + '_text', effect);
                    } else {
                        seteffecttext('p1board' + i + '_text', "");
                    }
                    const active = item['active'];
                    if (active > 0) {
                        changeBorderColor('p1board' + i, "green");
                    } else {
                        resetBorderColor('p1board' + i)
                    }
                    const status = item['status'];
                    if (status.includes("stealth")) {
                        changeBgColor('p1board' + i, "gray");
                    } else {
                        if (effect.includes("stealth")) {
                            effect = effect.replace("stealth", "<s>stealth</s>");
                            seteffecttext('p1board' + i + '_text', effect);
                        }
                        if (status.includes("fortress")) {
                            changeBgColor('p1board' + i, "purple");
                        } else {
                            changeBgColor('p1board' + i, "aliceblue");
                        }
                    }
                    setdivimage('p1board' + i, graphic);
                }
                if (flg == false) {
                    setdivvalue('p1board' + i + '_cost', "");
                    setdivvalue('p1board' + i + '_attack', "");
                    setdivvalue('p1board' + i + '_hp', "");
                    setdivvalue('p1board' + i + '_name', "");
                    setdivvalue('p1board' + i + '_text', "");
                    removedivimage('p1board' + i, "");
                    resetBorderColor('p1board' + i);
                    changeBgColor('p1board' + i, "aliceblue");
                }
            }

            // P1テンション
            const tension = player1["tension"];
            for (let i = 0; i < 3; i++) {
                if (i < tension) {
                    changeBgColor("p1tension" + i, "purple");
                } else {
                    changeBgColor("p1tension" + i, "white");
                }
            }
            if (tension < 3) {
                const i = 10
                const graphic = "uploads/system/tension.png"
                const cost = 1;
                const attack = "";
                const hp = "";
                const name = "tension";
                setdivvalue('p1card' + i + '_cost', cost);
                setdivvalue('p1card' + i + '_attack', attack);
                setdivvalue('p1card' + i + '_hp', hp);
                setdivvalue('p1card' + i + '_name', name);
                setdivimage('p1card' + i, graphic);
                const active = player1['tension_active'];
                if (active > 0) {
                    if (player1[key_mp] >= cost) {
                        changeBorderColor('p1card' + i, "green");
                    } else {
                        resetBorderColor('p1card10');
                    }
                } else {
                    resetBorderColor('p1card10');
                }
                changeBgColor("p1tension" + "3", "white")
            } else {
                var job = player1["job"];
                const i = 10
                var graphic;
                var cost;
                var attack;
                var hp;
                var name;
                if (job == "wiz") {
                    graphic = "uploads/test/merami.png"  // TODO graphic
                    cost = "";
                    attack = "";
                    hp = "";
                    name = "guren fireball";
                } else if (job == "mnk") {
                    graphic = "uploads/system/tension_otenba.png"
                    cost = "";
                    attack = "";
                    hp = "";
                    name = "otenba princess";
                }
                setdivvalue('p1card' + i + '_cost', cost);
                setdivvalue('p1card' + i + '_attack', attack);
                setdivvalue('p1card' + i + '_hp', hp);
                setdivvalue('p1card' + i + '_name', name);
                setdivimage('p1card' + i, graphic);
                changeBorderColor('p1card' + i, "green");
                changeBgColor("p1tension" + "3", "red")
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
                // setdivvalue('p2card' + i, "C")
                setdivimage('p2card' + i, "uploads/system/sleeve.png");
            }
            for (let i = handnum; i < 10; i++) {
                setdivvalue('p2card' + i, "");
            }
            // P2ボード
            const board = player2["board"];
            for (let i = 0; i < 6; i++) {
                flg = false
                for (let j = 0; j < board.length; j++) {
                    const item = board[j];
                    if (i != item['location']) {
                        continue
                    }
                    flg = true
                    const cost = item['cost'];
                    const attack = item['attack'];
                    const hp = item['hp'];
                    const name = item['name'];
                    const graphic = item['graphic'];
                    setdivvalue('p2board' + i + '_cost', cost);
                    setdivvalue('p2board' + i + '_attack', attack);
                    setdivvalue('p2board' + i + '_hp', hp);
                    setdivvalue('p2board' + i + '_name', name);
                    var effect = item['effect'];
                    if (effect != "") {
                        seteffecttext('p2board' + i + '_text', effect);
                    }
                    const status = item['status'];
                    if (status.includes("stealth")) {
                        changeBgColor('p2board' + i, "gray");
                    } else {
                        if (effect.includes("stealth")) {
                            effect = effect.replace("stealth", "<s>stealth</s>");
                            seteffecttext('p2board' + i + '_text', effect);
                        }
                        if (status.includes("fortress")) {
                            changeBgColor('p2board' + i, "purple");
                        } else {
                            changeBgColor('p2board' + i, "aliceblue");
                        }
                    }
                    setdivimage('p2board' + i, graphic);
                }
                if (flg == false) {
                    setdivvalue('p2board' + i + '_cost', "");
                    setdivvalue('p2board' + i + '_attack', "");
                    setdivvalue('p2board' + i + '_hp', "");
                    setdivvalue('p2board' + i + '_name', "");
                    setdivvalue('p2board' + i + '_text', "");
                    removedivimage('p2board' + i, "");
                    resetBorderColor('p2board' + i);
                    changeBgColor('p2board' + i, "aliceblue");
                }
            }
            // P2テンション
            const tension = player2["tension"];
            for (let i = 0; i < 3; i++) {
                if (i < tension) {
                    changeBgColor("p2tension" + i, "purple")
                } else {
                    changeBgColor("p2tension" + i, "white")
                }
            }
            if (tension < 3) {
                const i = 10
                const graphic = "uploads/system/tension.png"
                const cost = 1;
                const attack = "";
                const hp = "";
                const name = "tension";
                setdivvalue('p2card' + i + '_cost', cost);
                setdivvalue('p2card' + i + '_attack', attack);
                setdivvalue('p2card' + i + '_hp', hp);
                setdivvalue('p2card' + i + '_name', name);
                setdivimage('p2card' + i, graphic);
                changeBgColor("p2tension" + "3", "white")
            } else {
                var job = player2["job"];
                const i = 10
                var graphic;
                var cost;
                var attack;
                var hp;
                var name;
                if (job == "wiz") {
                    graphic = "uploads/test/merami.png"  // TODO graphic
                    cost = "";
                    attack = "";
                    hp = "";
                    name = "guren fireball";
                } else if (job == "mnk") {
                    graphic = "uploads/system/tension_otenba.png"
                    cost = "";
                    attack = "";
                    hp = "";
                    name = "otenba princess";
                }
                setdivvalue('p2card' + i + '_cost', cost);
                setdivvalue('p2card' + i + '_attack', attack);
                setdivvalue('p2card' + i + '_hp', hp);
                setdivvalue('p2card' + i + '_name', name);
                setdivimage('p2card' + i, graphic);
                changeBgColor("p2tension" + "3", "red")
            }
        }

    } catch (error) {
        console.error('Get data was failed:', error);
    }
}
function seteffecttext(id, effect) {
    effect_text = effect.replace(",", '<br>');
    effect_text = effect_text.replace(":", ':<br>');
    check = effect_text.split("_");
    if (check.length > 1) {
        effect_text = effect_text.replace(check[0] + "_", check[0] + "<br>");
    }
    setdivvalue(id, effect_text);
    return effect_text;
}
function setdivimage(id, imageUrl) {
    const imageDiv = document.getElementById(id);
    const images = imageDiv.querySelectorAll("img");
    var flg = false;
    images.forEach(image => {
        image.src = "/" + imageUrl;
        flg = true;
    });
    if (flg == false) {
        const imageElement = document.createElement('img');
        imageElement.src = "/" + imageUrl;
        imageDiv.appendChild(imageElement);
    }
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
    // divElement.textContent = value; // データを<div>要素に表示  
    divElement.innerHTML = value;
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