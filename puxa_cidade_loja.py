from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

def puxa_lojas():

    options = Options()
    options.add_argument("--incognito")
    options.add_argument("--window-size=2560,1440")
    options.add_argument("--start-maximized")
    #options.add_argument('--headless=new') ## modo oculto.
    driver = webdriver.Chrome(options=options)

    # Wait for initialize, in seconds
    wait = WebDriverWait(driver, 10)

    driver.get("https://mercado.carrefour.com.br/#crfimt=home|shop|seletor|mercado_4p_161020|2")

    button_insira_cep = driver.find_elements(By.XPATH,"//button[ text()='Insira seu CEP']")
    button_insira_cep[1].click()

    button_retire_na_loja = driver.find_elements(By.XPATH,"//span[@class='w-[7rem] mx-[.75rem]' ]")
    button_retire_na_loja[1].click()

    button_selecione_cidade = driver.find_elements(By.XPATH,"//select[@id='selectCity' ]//option")[2:]
    contador = 0
    lista_cidades ={}
    for i in button_selecione_cidade:
        lista_cidades[i.text] = contador
        contador += 1
    time.sleep(2)
    button_selecione_cidade[ lista_cidades['SÃO PAULO - SP'] ].click()
    
    #aguarda ate o botao loja estar visivel:
    wait.until(EC.visibility_of_element_located((By.XPATH,"//div[@class='grid grid-flow-col']//h3")))

    button_loja = driver.find_elements(By.XPATH,"//div[@class='grid grid-flow-col']//h3")

    lista_de_lojas = {}
    contador = 0
    for i in button_loja:
        lista_de_lojas[i.text] = contador
        contador += 1
    
    button_loja[ lista_de_lojas['Hipermercado Pamplona'] ].click()
    time.sleep(6)
    ## codigo que puxa toda a relacao de Estado/Loja disponiveis no site do carrefour mercado:
    
    base = []
    for cidade in list(lista_cidades.keys()):

        wait.until(EC.visibility_of_element_located((By.XPATH,'//span[@class="flex hover:underline hover:underline-offset-2 font-bold col-span-2"]')))
        button_muda_loja = driver.find_element(By.XPATH,'//span[@class="flex hover:underline hover:underline-offset-2 font-bold col-span-2"]')
        button_muda_loja.click()
        time.sleep(2)
        button_selecione_cidade_2 = driver.find_elements(By.XPATH,"//select[@id='selectCity' ]//option")[2:]
        button_selecione_cidade_2[ lista_cidades[ cidade ] ].click()
        time.sleep(2)
        button_loja = driver.find_elements(By.XPATH,"//div[@class='grid grid-flow-col']//h3")
        lista_de_lojas = {}
        contador = 0
        for i in button_loja:
            lista_de_lojas[i.text] = contador
            contador += 1
        button_loja[0].click()
        time.sleep(2)
        cidade_ = [cidade for i in range(len(button_loja))]
        data = pd.DataFrame({'cidade':cidade_,'Lojas':list(lista_de_lojas.keys())})
        base.append(data)
        print(f'cidade analisada: {cidade}')

    ## gera a base de dados:
    base_de_lojas = pd.concat(base,ignore_index=True)
    base_de_lojas.to_excel("base de lojas --2.xlsx")

    driver.quit()
    
if __name__ == '__main__':

    puxa_lojas()
