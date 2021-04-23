import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
load_dotenv()



logica = {"OUTROS":'89',"BANCO SANTADER":"55"}


FAKE_DATA = [{"user":"E552271"},{"user":"E547813"},{"user":"E552492"},{"user":"E551014"}]

#PASSOS
###############################
# Request URL: https://homologacao4.stormfin.com.br/consignado/Colaborador/carregaUsuariosBanco
# Request Method: POST
# ba_id: 55  -> fazer dicionario E BOTAR TUDO NUMA LISTA (users)
###############################

#Com essa lista feita vamos fazer o indexof com o codigo e fazendo n+1


class robo_request():


    def login(self):
        self.session = requests.Session()
        url =  'https://homologacao4.stormfin.com.br'
        data = {"usuario":os.environ['USER_HOMOLOG'],"senha":os.environ['PASS_HOMOLOG'],"forceLogout":"1","logar":"Entrar"}
        self.headers = {'content-type': 'application/x-www-form-urlencoded'}
        login = self.session.post(url, headers=self.headers, data=data)
        self.lista_usuario_por_banco('55')

    

    def lista_usuario_por_banco(self,id_banco):
        statico = {"ba_id":str(id_banco)}
        usuarios_por_banco = self.session.post('https://homologacao4.stormfin.com.br/consignado/Colaborador/carregaUsuariosBanco',headers=self.headers,data=statico)
        # usuarios_por_banco = usuarios_por_banco .text.split('<td><small>')
        usuarios_por_banco = usuarios_por_banco .text.split('tooltip"></i>\n')[1:]
        self.usuarios_filtrados=[]
        for c in range(len(usuarios_por_banco)):
            self.usuarios_filtrados.append(usuarios_por_banco[c].split('\n')[0].strip())
        self.ordem_id()

    def ordem_id(self):
        for c in range (len(FAKE_DATA)):
            if FAKE_DATA[c]['user'] in self.usuarios_filtrados:
                index = self.usuarios_filtrados.index(FAKE_DATA[c]['user'])
                statico = {"ba_id":'55',"ub_id":index+1}
                self.abrindo_formulario(statico)
                


    def abrindo_formulario(self,statico):
        resp_form = self.session.post('https://homologacao4.stormfin.com.br/consignado/Colaborador/editarUsuarioBanco',headers=self.headers,data=statico)
        form_estruture = BeautifulSoup(resp_form.text,'html.parser')
        self.ub_id = form_estruture.find('input', {'name':'ub_id'}).get('value')
        self.hash_user = form_estruture.find('input', {'name':'hash_usuario'}).get('value')
        self.ub_ba_id = form_estruture.find('input', {'name':'ub_ba_id'}).get('value')
        self.ba_nome = form_estruture.find('input', {'name':'ba_nome'}).get('value')
        self.ub_usuario = form_estruture.find('input', {'name':'ub_usuario'}).get('value')
        self.ub_agente_cpf_certificado = form_estruture.find('input', {'name':'ub_agente_cpf_certificado'}).get('value')

        self.is_usuario_robo = form_estruture.find('input', {'name':'is_usuario_robo'}).get('value') ##errado olhar depois

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

        post_final = {"ub_id":self.ub_id,"hash_user":self.hash_user,"ub_ba_id":self.ub_ba_id,"ba_nome":self.ba_nome,"ub_usuario":self.ub_usuario,

        }



        self.session.post('https://homologacao4.stormfin.com.br/consignado/Colaborador/salvarUsuarioBanco',
        headers=self.headers,
        )

start = robo_request()
start.login()