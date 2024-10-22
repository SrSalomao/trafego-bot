import requests  # type: ignore # Importa a biblioteca para fazer requisições HTTP
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class TrafegoBot:
    def __init__(self):
        self.API_KEY = 'sua_chave_da_api_aqui'  # Substitua pela sua chave da API
        self.historico = []
        self.leads = 0
        self.finalizacoes = 0

    def obter_trafego(self, origem, destino, captar_lead):
        url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origem}&destination={destino}&key={self.API_KEY}"
        resposta = requests.get(url)

        if resposta.status_code != 200:
            return "Erro na requisição: " + str(resposta.status_code)

        dados = resposta.json()

        if dados['status'] == 'OK':
            rotas = dados['routes'][0]
            tempo = rotas['legs'][0]['duration']['text']
            distancia = rotas['legs'][0]['distance']['text']

            if captar_lead:
                self.leads += 1  # Incrementa o contador de leads

            # Salvar no histórico
            self.historico.append({
                'origem': origem,
                'destino': destino,
                'tempo': tempo,
                'distancia': distancia,
                'data': datetime.now().strftime('%Y-%m')
            })

            return (f"**Resultado da Rota:**\n- Origem: {origem}\n- Destino: {destino}\n"
                    f"- Tempo estimado: {tempo}\n- Distância: {distancia}")
        else:
            return "Erro ao obter dados de tráfego: " + dados['status']

    def mostrar_historico(self):
        if not self.historico:
            return "Nenhuma consulta realizada ainda."

        resultado_historico = "**Histórico de Consultas:**\n"
        for i, consulta in enumerate(self.historico, start=1):
            resultado_historico += (f"{i}. Origem: {consulta['origem']}, Destino: {consulta['destino']}, "
                                    f"Tempo: {consulta['tempo']}, Distância: {consulta['distancia']}\n")
        return resultado_historico

    def resumo_mensal(self):
        mes_atual = datetime.now().strftime('%Y-%m')
        total_leads = self.leads
        total_finalizacoes = len([c for c in self.historico if c['data'] == mes_atual])

        return (f"**Resumo Mensal:**\n- Total de Leads: {total_leads}\n"
                f"- Total de Finalizações: {total_finalizacoes}")


# Funções de integração com a interface gráfica
bot = TrafegoBot()

def buscar_trafego():
    origem = entrada_origem.get()
    destino = entrada_destino.get()
    captar_lead = var_lead.get()

    if origem and destino:
        resultado = bot.obter_trafego(origem, destino, captar_lead)
        area_resultado.delete(1.0, tk.END)  # Limpa a área de resultado
        area_resultado.insert(tk.END, resultado)
        bot.finalizacoes += 1  # Incrementa o contador de finalizações após uma consulta bem-sucedida
    else:
        messagebox.showwarning("Entrada Inválida", "Por favor, insira origem e destino.")

def mostrar_historico_gui():
    resultado_historico = bot.mostrar_historico()
    area_resultado.delete(1.0, tk.END)  # Limpa a área de resultado
    area_resultado.insert(tk.END, resultado_historico)

def mostrar_resumo_gui():
    resumo = bot.resumo_mensal()
    area_resultado.delete(1.0, tk.END)  # Limpa a área de resultado
    area_resultado.insert(tk.END, resumo)

# Criar a interface gráfica
root = tk.Tk()
root.title("Bot de Gestão de Tráfego")

# Entrada de Origem
tk.Label(root, text="Origem:").grid(row=0, column=0)
entrada_origem = tk.Entry(root)
entrada_origem.grid(row=0, column=1)

# Entrada de Destino
tk.Label(root, text="Destino:").grid(row=1, column=0)
entrada_destino = tk.Entry(root)
entrada_destino.grid(row=1, column=1)

# Checkbox para captação de leads
var_lead = tk.BooleanVar()
checkbox_lead = tk.Checkbutton(root, text="Captar Lead", variable=var_lead)
checkbox_lead.grid(row=2, columnspan=2)

# Botão para buscar tráfego
botao_buscar = tk.Button(root, text="Buscar Tráfego", command=buscar_trafego)
botao_buscar.grid(row=3, columnspan=2)

# Botão para mostrar histórico
botao_historico = tk.Button(root, text="Mostrar Histórico", command=mostrar_historico_gui)
botao_historico.grid(row=4, columnspan=2)

# Botão para mostrar resumo mensal
botao_resumo = tk.Button(root, text="Mostrar Resumo Mensal", command=mostrar_resumo_gui)
botao_resumo.grid(row=5, columnspan=2)

# Área de resultado
area_resultado = tk.Text(root, width=50, height=15)
area_resultado.grid(row=6, columnspan=2)

# Iniciar a interface
root.mainloop()