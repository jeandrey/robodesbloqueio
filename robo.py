import pandas as pd
import xlrd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from dotenv import load_dotenv
import os
import time


jabloqueado = []
bloquei = []
temloja = []
commensagem = []
load_dotenv()
PATH = "C:/Users/andrey.barreto/Desktop/desbloqueiorobo/chromedriver.exe"


class robo_desbloqueio():
    def read_excel(self):
        df = pd.read_excel('base.xlsx', engine='openpyxl',skiprows=2)
        self.df_codigos = df['Usuário']
        self.df_setor = df['Perfil de Acesso']
        self.df_nome = df['Colaborador/Terceiro']
        self.df_observacao = df['Ação']
        self.acessar_site()

    def acessar_site(self):
        self.driver = webdriver.Chrome(PATH)
        self.driver.get("https://www.fontesassessoriafinanceira.com.br/")
        self.login()


    def login(self):
        self.driver.find_element_by_id('usuario').send_keys(os.environ['USER_FONTES'])
        self.driver.find_element_by_id('senha').send_keys(os.environ['PASSWORD_FONTES'])
        self.driver.find_element_by_class_name('btn').click()
        time.sleep(2)
        self.driver.find_element_by_class_name('ui-button-text').click()
        self.driver.get("https://www.fontesassessoriafinanceira.com.br/admin/index.php?rt=funcionarios")
        self.bloquear_users()
    
    def bloquear_users(self):
        select = Select(self.driver.find_element_by_id('searchField1'))
        select.select_by_value('fc_cod_fin')
        select = Select(self.driver.find_element_by_id('searchField2'))
        select.select_by_value('pr_descricao')
        select = Select(self.driver.find_element_by_id('searchField3'))
        select.select_by_value('fc_nome')
        for c in range(len(self.df_codigos)):
            time.sleep(2)
            self.driver.find_element_by_id('searchText1').clear()
            self.driver.find_element_by_id('searchText2').clear()
            self.driver.find_element_by_id('searchText3').clear()
            self.driver.find_element_by_id('searchText1').send_keys(self.df_codigos[c])
            self.driver.find_element_by_id('searchText2').send_keys(self.df_setor[c])
            self.driver.find_element_by_id('searchText3').send_keys(self.df_nome[c])
            self.driver.find_element_by_css_selector('[value="Procurar"]').click()
            time.sleep(1)
            try:
                time.sleep(2)
                loja = self.driver.find_elements_by_tag_name('td')[9].get_attribute('innerText')
                if loja != '':
                    temloja.append(str(self.df_codigos[c]))
                    continue
                self.driver.find_element_by_css_selector('[alt="Funcionário Ativo"]').click()

                try:
                    time.sleep(1)
                    self.driver.find_element_by_name('transfere_contratos').click()
                    self.driver.find_elements_by_tag_name('button')[2].click()
                    commensagem.append(str(self.df_codigos[c]))
                    continue
                except:
                    pass

                try:
                    time.sleep(1)
                    self.driver.find_element_by_name('limpa_clientes').click()
                    self.driver.find_elements_by_tag_name('button')[2].click()
                    commensagem.append(str(self.df_codigos[c]))
                    continue
                except:
                    pass



                # if str(self.df_codigos[c]) in commensagem:

                time.sleep(1)
                self.driver.find_element_by_id('obs_desativacao').send_keys(self.df_observacao[c])
                self.driver.find_elements_by_tag_name('button')[1].click()
                time.sleep(1)
                self.driver.find_elements_by_class_name('ui-button')[0].click()
                bloquei.append(str(self.df_codigos[c]))
                    



            except:
                jabloqueado.append(str(self.df_codigos[c]))



bot = robo_desbloqueio()
bot.read_excel()


with open("jabloqueado.txt", "w") as txt_file:
    for line in jabloqueado:
        txt_file.write(line + ",")

with open("bloquei.txt", "w") as txt_file:
    for line in bloquei:
        txt_file.write(line + "\n")
with open("temloja.txt", "w") as txt_file:
    for line in temloja:
        txt_file.write(line + "\n")

with open("commensagem.txt", "w") as txt_file:
    for line in commensagem:
        txt_file.write(line + "\n")