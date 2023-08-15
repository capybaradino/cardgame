async function fetchData() {
    var sid = getCookieValue("card_sid");
    try {
        const response = await fetch('/api/view/' + sid);
        const data = await response.json();

        // 共通キー情報
        const key_name = "name";

        // Player1関連情報
        {
            const key_p1 = "player1";
            const player1 = data[key_p1];
            const value = player1[key_name];

            const divElement = document.getElementById('playername1_left');
            divElement.textContent = value; // データを<div>要素に表示
        }

        // Player2関連情報
        {
            const key_p2 = "player2";
            const player2 = data[key_p2];
            const value = player2[key_name];

            const divElement = document.getElementById('playername2_right');
            divElement.textContent = value; // データを<div>要素に表示        
        }

    } catch (error) {
        console.error('Get data was failed:', error);
    }
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