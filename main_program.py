import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import requests
from bs4 import BeautifulSoup
import random

form_class = uic.loadUiType(".\Lotto_Analysis_Program\Main_Dialog.ui")[0]

def create_html():
    def lotto_num():
        response = requests.get("https://www.dhlottery.co.kr/gameResult.do?method=byWin&wiselog=C_A_1_1")
        soup = BeautifulSoup(response.text, "html.parser")
        elements = soup.select('meta#desc')[0]['content']
        temp = elements
        round_winningnum = [(temp.split('.')[0].split(' ')[1]), (temp.split('.')[0].split(' ')[3])]
        return round_winningnum

    temp = lotto_num()
    winning_num = (temp[1].split(',')[:-1])
    bonus_num = temp[1].split(',')[len(winning_num)].split('+')
    winning_num.append(bonus_num[0])
    bonus_num = bonus_num[1]
    print(winning_num, bonus_num)

    def select_ball_color(number):
        temp = int(number)
        if temp >= 1 and temp <= 10: return '1'
        elif temp >= 11 and temp <= 20: return '2'
        elif temp >= 21 and temp <= 30: return '3'
        elif temp >= 31 and temp <= 40: return '4'
        elif temp >= 41 and temp <= 45: return '5'
        else: return '1'

    html = '''<html>
        <head>
            <title>good</title>
        </head>
        <body>
            <style>
                .ball_645 {display:inline-block; border-radius:50%; text-align:center; vertical-align:middle; color:#fff; font-weight:500; /* text-shadow: 0px 0px 2px rgba(0, 0, 0, 1); */}
                .ball_645.lrg {width:60px; height:60px; line-height:56px; font-size:28px}
                .ball_645.sml {width:24px; height:24px; line-height:22px; font-size:13px}
                .ball_645.not {color:#777}
                .ball_645.sml.not {font-weight:300}
                .ball_645.ball1 {background:#fbc400; text-shadow: 0px 0px 3px rgba(73, 57, 0, .8); border-radius:50%}
                .ball_645.ball2 {background:#69c8f2; text-shadow: 0px 0px 3px rgba(0, 49, 70, .8); border-radius:50%}
                .ball_645.ball3 {background:#ff7272; text-shadow: 0px 0px 3px rgba(64, 0, 0, .8); border-radius:50%}
                .ball_645.ball4 {background:#aaa; text-shadow: 0px 0px 3px rgba(61, 61, 61, .8); border-radius:50%}
                .ball_645.ball5 {background:#b0d840; text-shadow: 0px 0px 3px rgba(41, 56, 0, .8); border-radius:50%}
                table tr td .ball_645.sml {margin:0 3px}
                [class*="content_winnum_"] .win_result {border:1px solid #ddd; background:#fff; text-align:center; margin-bottom:40px; padding:60px 60px 90px;}
            </style>
            <p>'''

    html += f'<span class="ball_645 lrg ball{select_ball_color(winning_num[0])}">{winning_num[0]}</span>\n<span class="ball_645 lrg ball{select_ball_color(winning_num[1])}">{winning_num[1]}</span>\n<span class="ball_645 lrg ball{select_ball_color(winning_num[2])}">{winning_num[2]}</span>\n<span class="ball_645 lrg ball{select_ball_color(winning_num[3])}">{winning_num[3]}</span>\n<span class="ball_645 lrg ball{select_ball_color(winning_num[4])}">{winning_num[4]}</span>\n<span class="ball_645 lrg ball{select_ball_color(winning_num[5])}">{winning_num[5]}</span>\n+\n<span class="ball_645 lrg ball{select_ball_color(bonus_num)}">{bonus_num}</span>\n</p>\n</body>\n</html>'

    print(html)
    return html

class WindowClass(QDialog, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        temp = self.lotto_num()
        self.lotto_round_display.display(temp[0][:-1])
        self.textedit_html_viewer.setHtml(create_html())
        
        self.Main_btn_CreateNum.clicked.connect(self.Main_btn_CreateNum_Function)
        
    def Main_btn_CreateNum_Function(self):
        # 단순히 랜덤한 값을 생성
        rand_lotto_num = random.sample(range(1, 45), 6)
        rand_lotto_num.sort()
        print(rand_lotto_num)
        temp_string = ""
        for idx, value in enumerate(rand_lotto_num):
            if idx == 5:
                temp_string += str(value)
            else:
                temp_string += str(value) + ", "
        current_text = self.test_label.text()
        print(current_text)
        self.test_label.setText(current_text +"\n["+ temp_string + "]\n")
        
    def Main_btn_AnalysisNum_Function(self):
        # 현재까지의 로또번호를 딥러닝하여 예측
        print("분석버튼 클릭")
    
    def lotto_num(self):
        response = requests.get("https://www.dhlottery.co.kr/gameResult.do?method=byWin&wiselog=C_A_1_1")
        soup = BeautifulSoup(response.text, "html.parser")
        elements = soup.select('meta#desc')[0]['content']
        temp = elements
        round_winningnum = [(temp.split('.')[0].split(' ')[1]), (temp.split('.')[0].split(' ')[3])]
        return round_winningnum

if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()