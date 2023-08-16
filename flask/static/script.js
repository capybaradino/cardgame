async function fetchData() {
    var sid = getCookieValue("card_sid");
    try {
        const response = await fetch('/api/view/' + sid);
        const data = await response.json();

        // 共通キー情報
        const key_name = "name";
        const key_hp = "HP";
        const key_decknum = "decknum";
        const key_mp = "MP";
        const key_maxmp = "maxMP";

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
            var hand = player1["hand"];
            for (let i = 0; i < hand.length; i++) {
                const item = hand[i];
                const cost = item['cost'];
                const attack = item['attack'];
                const hp = item['hp'];
                const graphic = item['graphic'];
                setdivimage('p1card' + i, graphic);
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
                setdivvalue('p2card' + i, "Card")
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