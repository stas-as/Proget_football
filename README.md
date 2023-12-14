![header](https://github.com/stas-as/Proget_football/blob/master/assets/UK49ux8wKpc.jpg)
# Projet_football
## Цели проекта:
1. Обучить модель **ML** для предсказывания общего счета матча 
2. Организовать постояный и надежный поток данных о новых матчах для своевременного предикта.
3. Создать чат бота или информационный паблик с публикацией аналитики и предсказания по матчам


## Этапы работы:
1. Определение задач
2. Сбор данных 
3. пердобработка
4. Создание новых признаков
5. Моделирование
6. Введение в продакшн


## 1. Определение задач:
- Выберим таргет, одним из основных параметров исхода матча является общий счет матча (сумма голов обоих гоманд) или его еще называют "Тотал" .Так как это численый параметр и его можно предсказывать как при помощи **Линейной Регрессии** так и класификации если преобразуем его в признак >=2.5 то получится задача бинарной класификации.

## 2. Сбор данных:
- Какие же данные собирать? Популярный ответ все и чем больше тем лутче. 
Но на сбор всей информации о всех матчах уйдет много времени так что возьмём топ 5 лиг и попробуем собрать данные о них:

![ligi](https://github.com/stas-as/Proget_football/blob/master/assets/european-league-rankings-1024x717.jpg)

### Это следующие лиги:  
1. ***English* Premier League**
2. ***German* Bundesliga**
3. ***Spain* La Liga**
4. ***Italia* Serie A**
5. ***France* Ligue 1**

- Для парсинга был выбран следующий [сайт](https://soccer365.ru/online/).
логика работы сайта: так как данных много в url адрес матча встроен "навигатор" по матчам `https://soccer365.ru/games/1918136/` 
набор цифр это уникальный **id** каждого матча. от сюда следует можно собрать **id** сезона и прогнать по циклу .
- как же собрать **id** нужной лиги и сезона(спойлер так как сайт обновлялся, раньше 2019-2020 сезона не получится собрать всех данных так как некоротых признаков нету, они не собирались, и будут пропуски по этому данных младше 2019-2020 сезона нету),есть раздел результаты сезонов `https://soccer365.ru/competitions/17/2022-2023/results/` и уже не состовляет труда изменить сезон
    ```python
    lsit_data = ["2022-2023","2021-2022","2020-2021","2019-2020"]
    ``` 
    и изменить лигу по **id_competitions**  :
    ```python
    country = {
        "Bundes_liga":19,
        "liga_1":18,
        "Primera_liga":16,
        "Premier_liga":12,
        "Seria_A_liga":15
    }
    ```
    и уже выбрав нужную лигу и список сезонов можно запустить цикл для парсинга 
    ```python

    for i in list_data:     
        print(i)#вывод сезона для проверки работы
        
        data_list = list() #список для данных
        url_1 = f"https://soccer365.ru/competitions/{country[liga]}/{i}/results/"
        
        try:
            response_1 = requests.get(url_1,headers=headers[cikle[count_proxy][0]],proxies=proxy[cikle[count_proxy][1]])#основной запрос
        except ConnectionRefusedError:
            response_1 = requests.get(url_1,headers=headers[cikle[count_proxy][0]],proxies=proxy[cikle[count_proxy][1]])#основной запрос
            print(f"ProxyError")
        count_proxy +=1 
        if count_proxy == 25 :
            count_proxy = 0
            
        # тело цикла
        soup_1 = BeautifulSoup(response_1.text,'lxml')
        set1 = list()
        
        coeficent_all = soup_1.find_all('a', class_="game_link")
        for j in coeficent_all:
            set1.append(j.get("dt-id"))
        print(len(set1))
        for k in set1:
            
            url_1 = f"https://soccer365.ru/games/{k}/"#запрос общей информации о матче
        
            url_2 = f"https://soccer365.ru/games/{k}/&tab=form_teams"#запрос стат.информации о матче
    ```
    так же были проблемы с защитой сайта от спама, из-за этого пришлось пользоваться headers и proxy:
    ```python
    headers = [
        {'User-Agent': "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0"},
        {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:109.0) Gecko/20100101 Firefox/114.0'},
        {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"},
        {'User-Agent': "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"},
        {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}
        ]
    proxies = [
        {'https':'http://QJ0UDV:jyXWSQ@213.166.74.197:9253'},
        {'https':'http://QJ0UDV:jyXWSQ@213.166.74.14:9758'},
        {'https':'http://QJ0UDV:jyXWSQ@213.166.75.244:9096'},
        {'https':'http://QJ0UDV:jyXWSQ@185.191.142.68:9545'},
        {'https':'http://QJ0UDV:jyXWSQ@185.184.78.99:9504'}
        ]
    ```

    для просмотра всего кликай сюда [код парсера](https://github.com/stas-as/Proget_football/blob/master/Parsing/parsing2_v2.0.ipynb)

    ## 3. Предобработка:
    После парсинга получаем 71 признак из них 18 имеют тип object 
    так как последовательность матчей от сезона к сезону одинаковая было решене делать функцию для каждого сезона и функцию по подсчету очков и места в турнирной таблице:
    ```python
    def point_rang(df):# заполняет данные очками и рангом действующия
        # создаем оперативный датасет для сохранения прогреса
        d = pd.DataFrame({
            "team": list(df["Команда1"].value_counts().index),
            "point": [0] * len(list(df["Команда1"].value_counts().index)),
            "rang": [0] * len(list(df["Команда1"].value_counts().index)),
            "gool": [0] * len(list(df["Команда1"].value_counts().index)),
        })
        
        df = df.sort_values(by="Tour",axis=0)# сортируем по турам 

        tour = df.loc[df["id"] == list(df["id"])[0] ,["Tour"]].values[0][0]

        for i in list(df["id"]):
            if tour == df.loc[df["id"] == i ,["Tour"]].values[0][0]:
                num = list(df.loc[df["id"] == i,["Команда1", "счет1", "Команда2", "счет2"]].values[0])
                #запись данных в датафрейм:
                df.loc[df["id"] == i ,["Point_1"]] = d.loc[d["team"] == num[0],["point"]].values[0][0]
                df.loc[df["id"] == i ,["Point_2"]] = d.loc[d["team"] == num[2],["point"]].values[0][0]

                df.loc[df["id"] == i ,["rang_1"]] = d.loc[d["team"] == num[0],["rang"]].values[0][0]
                df.loc[df["id"] == i ,["rang_2"]] = d.loc[d["team"] == num[2],["rang"]].values[0][0]
                
                # обновление данных в опереативной таблице:
                if num[1] > num[3]:
                    d.loc[d["team"] == num[0],["point"]] +=  3
                elif num[1] < num[3]:
                    d.loc[d["team"] == num[2],["point"]] +=  3
                else:
                    d.loc[d["team"] == num[0],["point"]] +=  1
                    d.loc[d["team"] == num[2],["point"]] +=  1
                    
                d.loc[d["team"] == num[0],["gool"]] += num[1]
                d.loc[d["team"] == num[2],["gool"]] += num[3]
                
            else:
                #перезаписование тура
                tour = df.loc[df["id"] == i ,["Tour"]].values[0][0]
                #сортировка оперативной таблици, перезапись рангов
                d = d.sort_values(by=["point","gool"],ascending=[False,False])
                d.loc[:,"rang"] = range(1, len(list(df["Команда1"].value_counts().index))+1)
                
                num = list(df.loc[df["id"] == i,["Команда1", "счет1", "Команда2", "счет2"]].values[0])
                #запись данных в датафрейм:
                df.loc[df["id"] == i ,["Point_1"]] = d.loc[d["team"] == num[0],["point"]].values[0][0]
                df.loc[df["id"] == i ,["Point_2"]] = d.loc[d["team"] == num[2],["point"]].values[0][0]

                df.loc[df["id"] == i ,["rang_1"]] = d.loc[d["team"] == num[0],["rang"]].values[0][0]
                df.loc[df["id"] == i ,["rang_2"]] = d.loc[d["team"] == num[2],["rang"]].values[0][0]
                
                # обновление данных в опереативной таблице:
                if num[1] > num[3]:
                    d.loc[d["team"] == num[0],["point"]] +=  3
                elif num[1] < num[3]:
                    d.loc[d["team"] == num[2],["point"]] +=  3
                else:
                    d.loc[d["team"] == num[0],["point"]] +=  1
                    d.loc[d["team"] == num[2],["point"]] +=  1
                    
                d.loc[d["team"] == num[0],["gool"]] += num[1]
                d.loc[d["team"] == num[2],["gool"]] += num[3]
        d = d.sort_values(by=["point","gool"],ascending=[False,False])
        d.loc[:,"rang"] = range(1, len(list(df["Команда1"].value_counts().index))+1)    
        return df, d

    def preobr(df): #предобработка 
        if 'Unnamed: 0.1' in list(df.columns):
            df = df.drop('Unnamed: 0.1',axis=1)
        if 'Unnamed: 0' in list(df.columns):
            df = df.drop('Unnamed: 0',axis=1)
        # удаляем не нужные признаки
        df = df.drop('Матчи 1',axis=1)
        df = df.drop('Матчи 2',axis=1)
        df = df.astype({'счет1': 'int32'})
        df = df.astype({'счет2': 'int32'})
        
        df["тотал"] = df["счет1"] + df["счет2"]
        df["Дата"] = pd.to_datetime(df['Дата'],dayfirst=True)
        df['Температура'] = df['Температура'].apply(lambda x: int(x[1:-2]))
        
        #обрабатываем 2 пропуска в 2 матчах
        for i in [14919463, 14898101]:
            df.loc[df["id"] == i ,['Офсайды  (соперник) 2']] = 4.00
            df.loc[df["id"] == i ,['Офсайды 2']] = 1.00
        
        #mask_1 = df["id"] == 14898101
        #df['Офсайды  (соперник) 2'][mask_1] = 4.00
        #df['Офсайды 2'][mask_1] = 1.00
        
        df["rang_1"] = 0
        df["rang_2"] = 0  
        df["Point_1"] = 0
        df["Point_2"] = 0
        df["liga"] = df["общая информация"].apply(lambda x: x.split(",")[0])
        df["Tour"] = df["общая информация"].apply(lambda x: x.split(",")[1])
        
        df = df[df["Tour"] != " стыковые матчи"]
        df = df[df["Tour"] != " понижение/повышение - финал"]
        df = df[df["Tour"] != " дополнительный матч"]
        df["Tour"] = df["Tour"].apply(lambda x: int(x.strip()[:-6]))
        
        df = df.astype({'Офсайды  (соперник) 2': 'float32'})
        df = df.astype({'Офсайды 2': 'float32'})
        #преобразуем признаки типа object в числовые
        df["Сухие матчи 1"] = df["Сухие матчи 1"].apply(lambda x: int(x.split()[-1]))
        df["Сухие матчи 2"] = df["Сухие матчи 2"].apply(lambda x: int(x.split()[0]))

        df["обе забьют 1"] = df["обе забьют 1"].apply(lambda x: int(x.split()[-1]))
        df["обе забьют 2"] = df["обе забьют 2"].apply(lambda x: int(x.split()[0]))

        df["Тотал больше 2.5 1"] = df["Тотал больше 2.5 1"].apply(lambda x: int(x.split()[-1]))
        df["Тотал больше 2.5 2"] = df["Тотал больше 2.5 2"].apply(lambda x: int(x.split()[0]))

        df["Тотал меньше 2.5 1"] = df["Тотал меньше 2.5 1"].apply(lambda x: int(x.split()[-1]))
        df["Тотал меньше 2.5 2"] = df["Тотал меньше 2.5 2"].apply(lambda x: int(x.split()[0]))

        df["Поражения 1"] = df["Поражения 1"].apply(lambda x: int(x.split()[-1]))
        df["Поражения 2"] = df["Поражения 2"].apply(lambda x: int(x.split()[0]))

        df["Ничьи 1"] = df["Ничьи 1"].apply(lambda x: int(x.split()[-1]))
        df["Ничьи 2"] = df["Ничьи 2"].apply(lambda x: int(x.split()[0]))

        df["Победы 1"] = df["Победы 1"].apply(lambda x: int(x.split()[-1]))
        df["Победы 2"] = df["Победы 2"].apply(lambda x: int(x.split()[0]))

        df["Отдых: дни (часы) 1"] = df["Отдых: дни (часы) 1"].apply(lambda x: float(x.split()[-1]))
        df["Отдых: дни (часы) 2"] = df["Отдых: дни (часы) 2"].apply(lambda x: float(x.split()[0]))
        
        df, d = point_rang(df)
        return df
    ```
    для просмотра всего файла [код](https://github.com/stas-as/Proget_football/blob/master/Preprocessing/proverka_1.0.ipynb)