import requests
from logging import Logger


class Botsub:
    def __init__(self, base_url, sid, logger: Logger):
        self.base_url = base_url
        self.sid = sid
        self.logger = logger
        self.gamestatus = ""
        self.statuscount = 0

    def start_game(self):
        self.logger.info("start game start")
        response = requests.post(f"{self.base_url}/system/{self.sid}/newgame")
        self.logger.info(response.text.replace('\n', '').replace(' ', ''))
        self.logger.info("start game end")
        return response.status_code

    def get_status(self):
        # self.logger.info("get status start")
        response = requests.get(f"{self.base_url}/system/{self.sid}/status")
        text = response.text.replace('\n', '').replace(' ', '')
        if (text != self.gamestatus):
            self.gamestatus = text
            self.statuscount = 0
        else:
            self.statuscount = self.statuscount + 1
        if (self.statuscount < 1):
            self.logger.info(text)
        # self.logger.info("get status end")
        return response.status_code, response.text

    def get_view(self):
        # self.logger.info("get view start")
        response = requests.get(f"{self.base_url}/view/{self.sid}")
        # self.logger.info("get view end")
        return response.status_code, response.text

    def play_card(self, handno, boardno):
        self.logger.info(f"play card start handno={handno}, boardno={boardno}")
        response = requests.post(
            f"{self.base_url}/play/{self.sid}/hand_{handno}/leftboard_{boardno}")
        self.logger.info(response.text.replace('\n', '').replace(' ', ''))
        self.logger.info("play card end")
        return response.status_code

    def play_attack(self, cardno, boardno):
        self.logger.info(
            f"play attack start cardno={cardno}, boardno={boardno}")
        response = requests.post(
            f"{self.base_url}/play/{self.sid}/leftboard_{cardno}/rightboard_{boardno}")
        self.logger.info(response.text.replace('\n', '').replace(' ', ''))
        self.logger.info("play attack end")
        return response.status_code

    def get_result(self):
        self.logger.info("get result start")
        response = requests.get(f"{self.base_url}/system/{self.sid}/result")
        self.logger.info(response.text.replace('\n', '').replace(' ', ''))
        self.logger.info("get result end")
        return response.status_code

    def turn_end(self):
        self.logger.info("turn end start")
        response = requests.post(f"{self.base_url}/system/{self.sid}/turnend")
        self.logger.info(response.text.replace('\n', '').replace(' ', ''))
        self.logger.info("turn end end")
        return response.status_code

    def surrender(self):
        self.logger.info("surrender start")
        response = requests.post(
            f"{self.base_url}/system/{self.sid}/surrender")
        self.logger.info(response.text.replace('\n', '').replace(' ', ''))
        self.logger.info("surrender end")
