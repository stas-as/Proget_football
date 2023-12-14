![header](https://github.com/stas-as/Proget_football/blob/master/assets/UK49ux8wKpc.jpg)
# Proget_football
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
        print(i)
        
        data_list = list()
        url_1 = f"https://soccer365.ru/competitions/{country[liga]}/{i}/results/"
        
        try:
            response_1 = requests.get(url_1,headers=headers[cikle[count_proxy][0]],proxies=proxy[cikle[count_proxy][1]])
        except ConnectionRefusedError:
            response_1 = requests.get(url_1,headers=headers[cikle[count_proxy][0]],proxies=proxy[cikle[count_proxy][1]])
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
            
            url_1 = f"https://soccer365.ru/games/{k}/"
        
            url_2 = f"https://soccer365.ru/games/{k}/&tab=form_teams"
    ```
    [код парсера](https://github.com/stas-as/Proget_football/blob/master/Parsing/parsing2_v2.0.ipynb)