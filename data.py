from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement  # WebElement class
from unidecode import unidecode
import time

import sys


def getId(team_name:str):
    team_name = unidecode(team_name)
    try:
        with open("teams.txt", "r+") as file:
            lines = file.readlines()
            last_id = len(lines)
            
            for line in lines:
                team_id, name = line.strip().split(';')
                if name == team_name:
                    return int(team_id)

            new_id = last_id + 1
            file.write(f"{new_id};{team_name}\n")
            
            return new_id
    except FileNotFoundError:
        print("Error: File 'teams.txt' not found")
        return None


def getMatch(browser: webdriver, match: WebElement) -> webdriver:
    # Extraer el resto del id después de "g_1_"
    match_id = browser.execute_script("return arguments[0].id.split('g_1_')[1];", match)
    link = f'https://www.flashscore.es/partido/{match_id}/#/resumen-del-partido/estadisticas-del-partido/0'
    option = webdriver.ChromeOptions()
    match_browser = webdriver.Chrome(options=option)
    match_browser.maximize_window()
    match_browser.get(link)
    return match_browser

def getRound(browser: webdriver) -> str:
    WebDriverWait(browser, 3).until(EC.visibility_of_element_located((By.XPATH, '//span[@class="tournamentHeader__country"]/a')))
    round_element = browser.find_element(By.XPATH, '//span[@class="tournamentHeader__country"]/a')
    round = round_element.text.split()[-1]
    return round

def getTime(browser: webdriver) -> tuple:
    WebDriverWait(browser, 3).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="duelParticipant__startTime"]/div')))
    date = browser.find_element(By.XPATH, '//div[@class="duelParticipant__startTime"]/div')
    return date.text.split() # Returns date and time splitted

def getTeams(browser: webdriver) -> tuple:
    WebDriverWait(browser, 3).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="participant__participantNameWrapper"]/div/a')))
    team_elements = browser.find_elements(By.XPATH, '//div[@class="participant__participantNameWrapper"]/div/a')
    teams = tuple(unidecode(team_element.text) for team_element in team_elements)
    return teams

def getResult(browser: webdriver) -> tuple:
    WebDriverWait(browser, 3).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="detailScore__wrapper"]/span')))
    result_elements = browser.find_elements(By.XPATH, '//div[@class="detailScore__wrapper"]/span')
    return ''.join(result_element.text for result_element in result_elements).split('-')
    
def getStats(browser: webdriver, stat: str) -> tuple:
    try:
        WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.XPATH, f'//strong[text()="{stat}"]')))
        parent = browser.find_element(By.XPATH, f'//strong[text()="{stat}"]/../..')
        local_stat = parent.find_element(By.XPATH, 'div[@class="_value_1c6mj_5 _homeValue_1c6mj_10"]/strong').text
        away_stat = parent.find_element(By.XPATH, 'div[@class="_value_1c6mj_5 _awayValue_1c6mj_14"]/strong').text
        return local_stat, away_stat
    except Exception as ex:
        print(f'Error al obtener {stat}')
        return '-1', '-1'
    
def getPossession(browser: webdriver) -> tuple:
    possession = getStats(browser, 'Posesión de balón')
    return tuple(element.replace('%', '') if element != '-1' else element for element in possession)
    
def getShots(browser: webdriver) -> tuple:
    return getStats(browser, 'Remates')

def getShotsOnGoal(browser: webdriver) -> tuple:
    return getStats(browser, 'Remates a puerta')

def getCorners(browser: webdriver) -> tuple:
    return getStats(browser, 'Córneres')


def getResultsLeague(league: str, start_year: int):
    try:
        link = f'https://www.flashscore.com/football/spain/{league}-{start_year}-{start_year+1}/results/'
        option = webdriver.ChromeOptions()
        browser = webdriver.Chrome(options=option)
        browser.maximize_window()
        browser.get(link)
    except Exception as ex:
        print('Error al abrir la página: ' + str(ex))
        exit()

    try:
        while True:
            # Esperar a que el botón sea clickeable
            mas_partidos_button = WebDriverWait(browser, 2).until(
                EC.element_to_be_clickable((By.XPATH, '//a[@class="event__more event__more--static"]'))
            )

            # Scroll hasta el elemento
            browser.execute_script("arguments[0].scrollIntoView();", mas_partidos_button)

            # Hacer clic en el botón
            mas_partidos_button.click()

            time.sleep(1)
    except Exception as ex:
        pass

    try:
        file_name = f'{league}_{start_year}_{start_year+1}'
        with open(f'data/results/{file_name}.txt', "a") as archivo:
            matches = browser.find_elements(By.XPATH, '//div[starts-with(@id, "g_1_")]')
            for match in matches:
                match_browser = getMatch(browser, match)
                match_round = getRound(match_browser)
                match_date = getTime(match_browser)[0]
                match_time = getTime(match_browser)[1]
                home_team = getTeams(match_browser)[0]
                away_team = getTeams(match_browser)[1]
                home_team_id = getId(home_team)
                away_team_id = getId(away_team)
                home_team_goals = getResult(match_browser)[0]
                away_team_goals = getResult(match_browser)[1]
                home_team_possession = getPossession(match_browser)[0]
                away_team_possession = getPossession(match_browser)[1]
                home_team_shots = getShots(match_browser)[0]
                away_team_shots = getShots(match_browser)[1]
                home_team_shots_on_goal = getShotsOnGoal(match_browser)[0]
                away_team_shots_on_goal = getShotsOnGoal(match_browser)[1]
                home_team_corners = getCorners(match_browser)[0]
                away_team_corners = getCorners(match_browser)[1]
                match_id = f'{home_team_id}v{away_team_id}d{match_date.replace(".", "")}'
                print(f'{match_id};{match_round};{match_date};{match_time};{home_team_id};{home_team};{away_team_id};{away_team};{home_team_goals};{away_team_goals};{home_team_possession};{away_team_possession};{home_team_shots};{away_team_shots};{home_team_shots_on_goal};{away_team_shots_on_goal};{home_team_corners};{away_team_corners}')
                archivo.write(f'{match_id};{match_round};{match_date};{match_time};{home_team_id};{home_team};{away_team_id};{away_team};{home_team_goals};{away_team_goals};{home_team_possession};{away_team_possession};{home_team_shots};{away_team_shots};{home_team_shots_on_goal};{away_team_shots_on_goal};{home_team_corners};{away_team_corners}\n')
                match_browser.quit()
        
        print("Finished")
        match_browser.quit()
        browser.quit()
    
    except Exception as ex:
        print(ex)
        match_browser.quit()
        browser.quit()