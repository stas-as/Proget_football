from bs4 import BeautifulSoup
from pydantic import BaseModel, ConfigDict, Field, ValidationError
import requests

class Proxy(BaseModel):
    id: str
    ip: str
    port: str
    user: str
    password: str = Field(validation_alias='pass')

class ListProxy(BaseModel):
    items : dict[str,Proxy] = Field(validation_alias='list')
    list_count : int
    
class Math(BaseModel):
    id: str
    info : str
    date: str
    temperature: str
    weather : str
    coeficent: 'Coeficent'
    home_team: 'MatchTeam'
    guest_team: 'MatchTeam'
    
    @classmethod
    def from_response(cls,id_math:str,header: tuple[dict],proxy: tuple[dict]):
        url_1 = f"https://soccer365.ru/games/{id_math}/"
        url_2 = f"https://soccer365.ru/games/{id_math}/&tab=form_teams"

        response_1 = requests.get(url_1,headers=header[0],proxies=proxy[0])
        response_2 = requests.get(url_2,headers=header[1],proxies=proxy[1])
        
        soup_1 = BeautifulSoup(response_1.text,'lxml')
        soup_2 = BeautifulSoup(response_2.text,'lxml')
        
        my_data = {}
        my_data["id"] = id_math
        my_data["info"] = soup_1.find("div",class_="block_header bkcenter").text.replace("\n","")
        my_data["date"] = " ".join(my_data["info"].split()[-2:]) 
        result_match_1= soup_1.find("div",class_="live_game left")
        result_match_2= soup_1.find("div",class_="live_game right")


        preview_st = soup_1.find("div",class_="preview_item st")

        my_data["temperature"] = preview_st.find("span",class_="red").text
        my_data["weather"] = preview_st.find_all("span",class_="min_gray")[1].text

        coeficent_all = soup_1.find_all("div",class_="block_body_nopadding")[3]
        coficient = coeficent_all.find_all('div',class_='odds_item odds_logo')

        def cof_func(coficient):
            list_coef = list()
            for i in coficient:
                odds_coeff = i.find_all('div',class_='odds_coeff')
                for j in odds_coeff:
                    if j == '\n':
                        continue
                    if j == '\xa0':
                        list_coef.clear()
                        break
                    list_coef.append(float(j.text))
                if len(list_coef) == 5:
                    return  list_coef  

        my_data.setdefault('coeficent',{}).update(dict(zip(("c_wins", "c_draws", "c_defeats", "c_total_lеss", "c_total_more"), cof_func(coficient))))

        my_data.setdefault("home_team",{})["id"] = id_math
        my_data["home_team"]["name"] = result_match_1.find("div",class_="live_game_ht").text.replace("\n","")
        my_data["home_team"]["score"] = result_match_1.find("div",class_="live_game_goal").text.replace("\n","")
        my_data["home_team"]["date"] = my_data["date"]

        my_data.setdefault("guest_team",{})["id"] = id_math
        my_data["guest_team"]["name"] = result_match_2.find("div",class_="live_game_at").text.replace("\n","")
        my_data["guest_team"]["score"]= result_match_2.find("div",class_="live_game_goal").text.replace("\n","")
        my_data["guest_team"]["date"] = my_data["date"]

        result_matches_to10 = soup_2.find_all("div", class_="block_body_nopadding")
        Summary_statistics = result_matches_to10[3] 
        table_tr_1 = Summary_statistics.find_all("td")
        Summary_statistics2 = result_matches_to10[4] 
        table_tr_2 = Summary_statistics2.find_all("td")

        def reformed_tabl_1(table):
            lens = len(table)
            lister_res = list()
            for i in range(0,lens):
                if i in [1,4,7,10,13,16,19,22,25,28,31,34,37]:
                    pass
                else:
                    lister_res.append(table[i].text.replace("\xa0"," "))
            return(lister_res)

        test_res1 = reformed_tabl_1(table_tr_1)

        def reformed_tabl_2(table):
            lens = len(table)
            lister_res = list()
            for i in range(0,lens):
                if i in [1,4,7,10,13,16,19,22,25,28,31,34,37,40,43,46]:
                    pass
                else:
                    lister_res.append(table[i].text.replace("\xa0"," "))
            return(lister_res)
        test_res2 = reformed_tabl_2(table_tr_2)

        
        final_test_res = test_res1 + test_res2

        it = iter(final_test_res)
        words = ("count","rest","wins","draws","defeats","goals_scored","пoals_conceded","goals_scored_game","пoals_conceded_game","dry_matches","both_will_score","total_more","total_less","punches","punches_opponent","punches_gates","punches_gates_opponent","ownership","ownership_opponent","corner","corner_opponent","violations","violations_opponnent","offsides","offsides_opponent","yellow_cards","yellow_cards_opponent","red_cards","red_cards_opponent")
        for word, home, guest in zip(words,it,it):
            my_data["home_team"][word]  = home
            my_data["guest_team"][word] = guest
        return cls.model_validate()
    

class Coeficent(BaseModel):
    c_wins: float
    c_draws: float
    c_defeats: float
    c_total_lеss: float
    c_total_more: float

class MatchTeam(BaseModel):
    id: str
    name: str
    score: str
    date: str
    count: str  #матчи
    rest: str #отдых
    wins: str #
    draws: str #
    defeats: str #
    goals_scored: str  #забито голов
    пoals_conceded: str  #пропущено голов
    goals_scored_game: str  #Забито голов за игру 
    пoals_conceded_game: str  #пропущено голов за игру
    dry_matches: str  #
    both_will_score: str #обе забьют
    total_more: str  #Тотал больше 2.5 1
    total_less: str  #Тотал меньше 2.5 1
    punches: str  #удары
    punches_opponent: str #удары соперник
    punches_gates: str  #Удары в створ 1
    punches_gates_opponent: str  #Удары в створ  (соперник) 1
    ownership: str  #владение
    ownership_opponent: str #владение
    corner: str #Угловые
    corner_opponent: str #Угловые соперник
    violations: str #Нарушения
    violations_opponnent: str #Нарушения соперник
    offsides: str #Офсайды
    offsides_opponent: str #Офсайды соперник
    yellow_cards: str #Желтые
    yellow_cards_opponent: str #Желтые соперник
    red_cards: str #Красные
    red_cards_opponent: str #Красные соперник
