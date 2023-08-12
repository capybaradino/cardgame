import requests


class Botsub:
    def __init__(self, base_url, sid):
        self.base_url = base_url
        self.sid = sid

    def start_game(self):
        response = requests.post(f"{self.base_url}/system/{self.sid}/newgame")
        print(response.text)
        return response.status_code

    def get_status(self):
        response = requests.get(f"{self.base_url}/system/{self.sid}/status")
        print(response.text)
        return response.status_code, response.text

    def get_view(self):
        response = requests.get(f"{self.base_url}/view/{self.sid}")
        return response.status_code, response.text

    def play_card(self, handno, boardno):
        print("[INFO] play card start")
        response = requests.post(
            f"{self.base_url}/play/{self.sid}/hand_{handno}/leftboard_{boardno}")
        print(response.text)
        print("[INFO] play card end")
        return response.status_code

    def play_attack(self, cardno, boardno):
        print("[INFO] play attack start")
        response = requests.post(
            f"{self.base_url}/play/{self.sid}/leftboard_{cardno}/rightboard_{boardno}")
        print(response.text)
        print("[INFO] play attack end")
        return response.status_code

    def get_result(self):
        response = requests.get(f"{self.base_url}/system/{self.sid}/result")
        print(response.text)
        return response.status_code

    def turn_end(self):
        response = requests.post(f"{self.base_url}/system/{self.sid}/turnend")
        print(response.text)
        return response.status_code

    def end_game(self):
        response = requests.post(f"{self.base_url}/end_game")
        print(response.json()["message"])
