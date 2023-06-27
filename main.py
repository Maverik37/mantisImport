from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

#Fonction

def connexion(driver):
    url_connexion="https://www.mantisbt.org/bugs/login_page.php"
    #Récupération de la page de connexion
    driver.get(url_connexion)
    #on met le login
    input_login = driver.find_element(By.ID,"username").send_keys("Fourbasse37100")
    btn_click = driver.find_element(By.XPATH,"//*[@id='login-form']/fieldset/input[2]").click()
    print(driver.current_url)
    driver.implicitly_wait(30)
    input_password = driver.find_element(By.ID, "password").send_keys("uool7qho")
    #on va cliquer sur rester connecté
    keep_connected_elem = driver.find_element(By.XPATH,"//*[@id='remember-login']")
    ActionChains(driver).move_to_element(keep_connected_elem).click().perform()
    #on décoche la restriction d'ip
    ip_restreint = driver.find_element(By.XPATH,"//*[@id='secure-session']")
    ActionChains(driver).move_to_element(ip_restreint).click().perform()

    driver.find_element(By.XPATH,"//*[@id='login-form']/fieldset/input[3]").click()
    driver.implicitly_wait(20)
    return driver

def get_mantis_from_filter(driver,filter):
    select = driver.find_element(By.ID, 'filter-bar-query-id')
    obj_select = Select(select)

    obj_select.select_by_visible_text(filter)
    driver.implicitly_wait(10)
    return driver


def get_table_data (driver):
    Table_obj = driver.find_element(By.ID, "buglist")
    data = {}
    #On récupère les lignes
    obj_lines = Table_obj.find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")
    #On parcourt les lignes
    for row in obj_lines:
        cells = row.find_elements(By.TAG_NAME, "td") #On va récupèrer les cellules du tableau
        link = row.find_elements(By.TAG_NAME, 'a') #ici on récupère les liens (/!\ yen a 2
        try:
            nb_mantis = cells[3].text.replace('0', '')
            mant_cat = cells[6].text
            statut_list = cells[8].text.replace(' (','(').split("(")[:-1]
            statut = ""
            #Petite boucle pour renseigner le statut sous forme de string
            for i in statut_list:
                statut += i
            affect_to = cells[8].text.replace(' (', '(').split("(")[-1].replace(')','')

            #on ajoute les infos dans le dico
            data[nb_mantis] = {}
            data[nb_mantis]["Catégorie"] = mant_cat.replace("[","").replace("]","")
            data[nb_mantis]["Statut"] = statut
            data[nb_mantis]["Affecte a"] = affect_to

            href = url.replace('my_view_page.php', 'view.php?id='+nb_mantis)
            data[nb_mantis]["url"] = href
        except Exception as e:
            print(e)
            continue

    return data


#On paramètre le driver
driver = webdriver.Firefox()

url = "https://www.mantisbt.org/bugs/my_view_page.php"
#On se place sur la page web
connect_page = connexion(driver)
#on clique sur "afficher les bugs"

elem = driver.find_element(By.XPATH,"//*[@id='sidebar']/ul/li[2]/a").click()
#
get_mantis_from_filter(driver, 'Open Issues')
open_issue_data = get_table_data(driver)
#On récupère la table qui contient la liste des tickets
#

driver.close()
print(open_issue_data)
# for key,value in data.items():
#     driver = webdriver.Firefox()
#     driver.get(value["url"])
#     try:
#         submit_date = driver.find_element(By.XPATH,"//*[@id='main-container']/div[2]/div[2]/div/div[1]/div/div[2]/div[2]/div/table/tbody/tr[2]/td[5]").text
#     except NoSuchElementException as e:
#         continue
#     print("submit_date :", submit_date)
#     driver.close()
