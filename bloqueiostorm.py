from numpy import nan
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import logging
import pandas as pd
load_dotenv()

logging.basicConfig(filename='logs.log', encoding='utf-8', level=logging.DEBUG,format='%(asctime)s - %(levelname)s: %(message)s',
                datefmt='%d/%m/%Y %I:%M:%S %p',)




logica = {"OUTROS":'89',"BANCO SANTADER":"55","BANCO BMG":"52","BANCO DAYCOVAL":"93","BANCO ITAÚ CONSIGNADO":"95","BANCO OLÉ CONSIGNADO":"41","BANCO MERCANTIL DO BRASIL":"58","DAYCOVAL - CRÉDITO PESSOAL":"101","BANCO ITAÚ":"95","BANCO VOTORANTIM":"76","CCB BRASIL (BIC)":"97","CCB BRASIL FINANCEIRA (SUL FINANCEIRA)":"98","BANCO INTER":"99","BANCO SABEMI ":"83","BANCO CBSS":"119","BANCO PRIVADO-OUTROS":"111","CIASPREV":"124","BANCO PAN":"70","BANCO BANRISUL":"106","BANCO CETELEM":"110"}




class robo_request():



    def ler_excel(self):
        self.df = pd.read_excel('Bloqueios Acessos Bancários.xlsx')
        self.df = self.df[self.df['Ação']=='Bloquear na Fontes']
        self.tipo_bancos = self.df['Banco'].unique().tolist()
        self.login()

    def login(self):
        self.session = requests.Session()
        logging.info('Fazendo login')
        # url =  'https://homologacao4.stormfin.com.br'
        url =  'https://www.fontesassessoriafinanceira.com.br/'
        data = {"usuario":os.environ['USER_HOMOLOG'],"senha":os.environ['PASS_HOMOLOG'],"forceLogout":"1","logar":"Entrar"}
        self.headers = {'content-type': 'application/x-www-form-urlencoded','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
        login = self.session.post(url, headers=self.headers, data=data)
        logging.info('login Feito')
        self.para_cada_banco()


    def para_cada_banco(self):
        logging.info('mapeando campos')
        for element in self.tipo_bancos:
            logging.info(f'Lendo {element}')
            self.usuarios_bancos = self.df[self.df['Banco']==element].reset_index()
            if element==nan:
                continue
            try:
                self.id_banco = logica[element]
            except:
                logging.info(f'Banco não encontrado {element}')
                continue
            self.lista_usuario_por_banco(self.id_banco)
    

    def lista_usuario_por_banco(self,id_banco):
        statico = {"ba_id":str(id_banco)}
        # usuarios_por_banco = self.session.post('https://homologacao4.stormfin.com.br/consignado/Colaborador/carregaUsuariosBanco',headers=self.headers,data=statico)
        usuarios_por_banco = self.session.post('https://www.fontesassessoriafinanceira.com.br/consignado/Colaborador/carregaUsuariosBanco',headers=self.headers,data=statico)
        # usuarios_por_banco = usuarios_por_banco .text.split('<td><small>')
        usuarios_por_banco = usuarios_por_banco .text.split('tooltip"></i>\n')[1:]
        self.usuarios_filtrados = []
        self.todos_ub_id = []
        for c in range(len(usuarios_por_banco)):
            self.usuarios_filtrados.append(usuarios_por_banco[c].split('\n')[0].strip())
            self.todos_ub_id.append(usuarios_por_banco[c].split('Editar')[0].split('data-id=')[1].split('\n')[0].replace('"',''))
        self.ordem_id()

    def ordem_id(self):
        for usuario in range (len(self.usuarios_bancos)):
            if self.usuarios_bancos['Código Usuário Banco'][usuario] in self.usuarios_filtrados:
                index = self.usuarios_filtrados.index(self.usuarios_bancos['Código Usuário Banco'][usuario])
                statico = {"ba_id":self.id_banco,"ub_id":self.todos_ub_id[index]}
                continue###mudar depois
                self.abrindo_formulario(statico)
            elif str(self.usuarios_bancos['Código Usuário Banco'][usuario]).strip() in self.usuarios_filtrados:
                index = self.usuarios_filtrados.index(str(self.usuarios_bancos['Código Usuário Banco'][usuario]).strip())
                statico = {"ba_id":self.id_banco,"ub_id":self.todos_ub_id[index]}
                self.abrindo_formulario(statico)

            elif '0'+str(self.usuarios_bancos['Código Usuário Banco'][usuario]).strip() in self.usuarios_filtrados:
                index = self.usuarios_filtrados.index('0'+str(self.usuarios_bancos['Código Usuário Banco'][usuario]).strip())
                statico = {"ba_id":self.id_banco,"ub_id":self.todos_ub_id[index]}
                self.abrindo_formulario(statico)
                


    def abrindo_formulario(self,statico):
        # resp_form = self.session.post('https://homologacao4.stormfin.com.br/consignado/Colaborador/editarUsuarioBanco',headers=self.headers,data=statico)
        resp_form = self.session.post('https://www.fontesassessoriafinanceira.com.br/consignado/Colaborador/editarUsuarioBanco',headers=self.headers,data=statico)
        form_estruture = BeautifulSoup(resp_form.text,'html.parser')
        self.ub_id = form_estruture.find('input', {'name':'ub_id'}).get('value')
        self.hash_user = form_estruture.find('input', {'name':'hash_usuario'}).get('value')
        self.ub_ba_id = form_estruture.find('input', {'name':'ub_ba_id'}).get('value')
        self.ba_nome = form_estruture.find('input', {'name':'ba_nome'}).get('value')
        self.ub_usuario = form_estruture.find('input', {'name':'ub_usuario'}).get('value')
        self.ub_agente_cpf_certificado = form_estruture.find('input', {'name':'ub_agente_cpf_certificado'}).get('value')
        self.is_usuario_robo = form_estruture.find('input', {'name':'is_usuario_robo'}).get('value')
        self.senha_robo_tipos_cadastrados = form_estruture.find('input', {'name':'senha_robo_tipos_cadastrados'}).get('value')
        self.senha_robo_remover_flag = form_estruture.find('input', {'name':'senha_robo_remover_flag'}).get('value')
        self.ub_codigo_loja = form_estruture.find('input', {'name':'ub_codigo_loja'}).get('value')
        self.ub_observacao = form_estruture.find('input', {'name':'ub_observacao'}).get('value')
        self.colaborador_atual = form_estruture.find('input', {'name':'colaborador_atual'}).get('value')
        self.colaborador_atual_id = form_estruture.find('input', {'name':'colaborador_atual_id'}).get('value')
        self.ub_op_id = form_estruture.find('input', {'name':'ub_op_id'}).get('value')
        self.op_nome = form_estruture.find('input', {'name':'op_nome'}).get('value') 
        self.ub_usuario_averbacao = form_estruture.find('input', {'name':'ub_usuario_averbacao'}).get('value')
        self.operadores = form_estruture.find('input', {'name':'operadores'}).get('value')
        self.ub_criacao_contrato = form_estruture.find_all('option', selected=True)[1].get('value')
        self.ub_situacao = 'bloqueio-inatividade'
        logging.info(f'Bloqueando usuario {self.ub_usuario} do banco {self.ba_nome} com ba_id de {self.ub_id}')

        self.post_final = {"ub_id":self.ub_id,"hash_user":self.hash_user,"ub_ba_id":self.ub_ba_id,"ba_nome":self.ba_nome,"ub_usuario":self.ub_usuario,"ub_agente_cpf_certificado":self.ub_agente_cpf_certificado,
        "is_usuario_robo":"0","senha_robo_tipos_cadastrados":self.senha_robo_tipos_cadastrados,'senha_robo_remover_flag':self.senha_robo_remover_flag,"ub_codigo_loja":self.ub_codigo_loja,
        'ub_observacao':self.ub_observacao,"colaborador_atual":self.colaborador_atual,'colaborador_atual_id':self.colaborador_atual_id,'ub_op_id':self.ub_op_id,'op_nome':self.op_nome,'ub_usuario_averbacao':self.ub_usuario_averbacao,"operadores":self.operadores,"ub_criacao_contrato":self.ub_criacao_contrato,
        'ub_situacao':self.ub_situacao
        }

 
        # # # self.session.post('https://homologacao4.stormfin.com.br/consignado/Colaborador/salvarUsuarioBanco',headers=self.headers,data=self.post_final)
        self.session.post('https://www.fontesassessoriafinanceira.com.br/consignado/Colaborador/salvarUsuarioBanco',headers=self.headers,data=self.post_final)

start = robo_request()
start.ler_excel()