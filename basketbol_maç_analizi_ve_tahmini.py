import tkinter as tk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
import numpy as np


def euclidean_distance(vector1, vector2):
    return np.sqrt(np.sum((np.array(vector1) - np.array(vector2)) ** 2))


def search_team(team_name):
    url = "https://www.mackolik.com/basketbol/puan-durumu/turkey-ing-bsl/2022-2023/istatistik/c744bzsdcz9n7pz90phxoxuh9"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find_all('table')[0]
    rows = table.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        if len(cols) > 1:
            team = cols[1].text.strip()
            if team.lower() == team_name.lower():
                shots = float(cols[2].text.strip())
                turnovers = float(cols[9].text.strip())
                rebounds = float(cols[3].text.strip())
                free_throws = float(cols[4].text.strip())
                four_factors1 = int(0.4 * shots)
                four_factors2 = int(0.25 * turnovers)
                four_factors3 = int(0.20 * rebounds)
                four_factors4 = int(0.15 * free_throws)
                return four_factors1, four_factors2, four_factors3, four_factors4

    return None


def compare_teams(team1_name, team2_name):
    team1_result = search_team(team1_name)
    team2_result = search_team(team2_name)
    if team1_result is None or team2_result is None:
        return "Lütfen geçerli bir takım adı giriniz."
    if team1_result > team2_result:
        return f"{team1_name} takımı daha yüksek kazanma olasılığına sahip."
    elif team1_result < team2_result:
        return f"{team2_name} takımı daha yüksek kazanma olasılığına sahip."
    else:
        return "Takımlar eşit olasılıkta kazanacaklar."


def get_scores():
    url = "https://www.mackolik.com/basketbol/puan-durumu/turkey-ing-bsl/2022-2023/c744bzsdcz9n7pz90phxoxuh9"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find_all('table')[0]
    rows = table.find_all('tr')
    scores = {}
    for row in rows:
        cols = row.find_all('td')
        if len(cols) > 1:
            team = cols[1].text.strip()
            score = cols[8].text.strip()
            scores[team] = score
    return scores


def get_team_score(team1_name, team2_name):
    scores = get_scores()
    if team1_name and team2_name in scores:
        return f"{team1_name}: {scores[team1_name]},\n{team2_name}: {scores[team2_name]}"

    else:
        return f"{team1_name} ve {team2_name} adlı takımlar bulunamadı."


def get_team_score2(team_name):
    scores = get_scores()
    if team_name in scores:
        return scores[team_name]
    else:
        return 0




def risk_analysis(team1, team2):
    url = "https://www.mackolik.com/basketbol/puan-durumu/turkey-ing-bsl/2022-2023/istatistik/c744bzsdcz9n7pz90phxoxuh9"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find_all('table')[0]
    rows = table.find_all('tr')
    team1_puan = 0
    team2_puan = 0
    team1_sayi = 0
    team2_sayi = 0
    for row in rows:
        cols = row.find_all('td')
        if len(cols) > 1:
            team = cols[1].text.strip()
            if team.lower() == team1.lower():
                team1_puan = float(get_team_score2(team1).strip())
                team1_sayi = float(cols[3].text.strip())
            elif team.lower() == team2.lower():
                team2_puan = float(get_team_score2(team2).strip())
                team2_sayi = float(cols[3].text.strip())

    match_risk = int((1 / (((abs(team1_puan - team2_puan) * 0.60) + (abs(team1_sayi - team2_sayi) * 0.40)))) * 100)
    return match_risk


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        tk.Frame.__init__(self, master)
        master.geometry("800x300")
        self.grid()
        self.create_widgets()


    def create_widgets(self):
        self.team_label = tk.Label(self, text="Takım Adı:")
        self.team_label.grid(row=500, column=400, pady=10, ipadx=10, sticky='nsew')
        self.team_entry = tk.Entry(self)
        self.team_entry.grid(row=500, column=410, pady=10, ipadx=10, sticky='nsew')
        self.four_factors_for_first_team_button = tk.Button(self, text="Dört Faktör Modeli 1. Takım",
                                                            command=self.four_factors_for_first_team)
        self.four_factors_for_first_team_button.grid(row=600, column=450, pady=10, ipadx=20, ipady=10, sticky='nsew')
        self.four_factors_for_second_team_button = tk.Button(self, text="Dört Faktör Modeli 2. Takım",
                                                             command=self.four_factors_for_second_team)
        self.four_factors_for_second_team_button.grid(row=600, column=500, pady=10, ipadx=20, ipady=10, sticky='nsew')
        self.compare_teams_button = tk.Button(self, text="Takımları Karşılaştır", command=self.compare_teams)
        self.compare_teams_button.grid(row=700, column=450, pady=10, ipadx=20, ipady=10, sticky='nsew')
        self.scores_button = tk.Button(self, text="Puanları Listele", command=self.scores)
        self.scores_button.grid(row=700, column=500, pady=10, ipadx=20, ipady=10, sticky='nsew')
        self.team_score_button = tk.Button(self, text="Takım Puanını Listele", command=self.team_score)
        self.team_score_button.grid(row=800, column=450, pady=10, ipadx=20, ipady=10, sticky='nsew')
        self.risk_button = tk.Button(self, text="Risk", command=self.riskk)
        self.risk_button.grid(row=800, column=500, pady=10, ipadx=20, ipady=10, sticky='nsew')
        self.team_entry2 = tk.Entry(self)
        self.team_entry2.grid(row=500, column=420, pady=10, ipadx=10, sticky='nsew')

    def riskk(self):
        team1_name = self.team_entry.get()
        team2_name = self.team_entry2.get()
        result = risk_analysis(team1_name, team2_name)
        messagebox.showinfo("Sonuç", f"Risk orani= %: {result}")

    def four_factors_for_first_team(self):
        team_name = self.team_entry.get()
        result = search_team(team_name)
        if result is not None:
            messagebox.showinfo("Sonuç", f"{team_name} için dört faktör modeli sonucu: {result}")
        else:
            messagebox.showerror("Hata", f"{team_name} adlı takım bulunamadı.")

    def four_factors_for_second_team(self):
        team_name = self.team_entry2.get()
        result = search_team(team_name)
        if result is not None:
            messagebox.showinfo("Sonuç", f"{team_name} için dört faktör modeli sonucu: {result}")
        else:
            messagebox.showerror("Hata", f"{team_name} adlı takım bulunamadı.")

    def compare_teams(self):
        team1_name = self.team_entry.get()
        team2_name = self.team_entry2.get()
        result = compare_teams(team1_name, team2_name)
        messagebox.showinfo("Sonuç", result)

    def scores(self):
        scores = get_scores()
        score_list = ""
        for team, score in scores.items():
            score_list += f"{team} takımının puanı: {score}\n"
        messagebox.showinfo("Puanlar", score_list)

    def team_score(self):
        team1_name = self.team_entry.get()
        team2_name = self.team_entry2.get()
        result = get_team_score(team1_name, team2_name)
        messagebox.showinfo("Puan", f"{result}")


root = tk.Tk()
root.title("Basketbol Maç Analizi")
root.tk_setPalette('#f7752f')
app = Application(master=root)
app.mainloop()
