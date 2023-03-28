import requests
import PySimpleGUI as sg
import webbrowser


# Define a janela da GUI
sg.theme('LightGreen')
layout = [
    [sg.Text("Escolha o tipo de pesquisa:"), sg.Radio('Código de barras', 'RADIO1',
                                                      default=True, key="-EAN-"), sg.Radio('Descrição', 'RADIO1', key="-DESC-")],
    [sg.Text("Insira o código EAN ou descrição do produto:"),
     sg.Input(key="-SEARCH-"), sg.Button("Buscar")],
    [sg.Multiline("", size=(60, 5), key="-OUTPUT-", font=("Helvetica", 12))],
    [sg.Text("Desenvolvido por Rafael Moreira Fernandes, Rurópolis-Pará, whatsapp:(93)9911-60523")],
    [sg.Button('Instagram', font=('Helvetica', 10, 'underline'), button_color=('white', 'purple'), key='-INSTAGRAM-'),
     sg.Button('Copiar erro', font=('Helvetica', 10), key='-COPY-')],
]

window = sg.Window("Consulta de Produto CosmoS 1.0", layout, size=(800, 250))

tokens = ["UJTBhybMZx96n33FzUfp2w",
          "mPMEj7VdRYJ4u4qVXfvbEg", "k9wmJau-n3jaYFYriECRwA"]
token_idx = 0  # índice do token a ser usado

# Loop para ler os eventos da janela
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

    if event == "Buscar":
        if values["-EAN-"]:
            search_type = "gtins"
        else:
            search_type = "products"

        search_term = values["-SEARCH-"]
        url = f"https://api.cosmos.bluesoft.com.br/{search_type}/{search_term}"
        headers = {"X-Cosmos-Token": tokens[token_idx]}

        response = requests.get(url, headers=headers)

        if response.status_code == 429:
            window["-OUTPUT-"].update(
                "Erro na consulta: Limite de requisições excedido. Tente novamente em alguns minutos.")
        elif response.status_code == 404:
            window["-OUTPUT-"].update("Produto não encontrado.")
        elif response.status_code == 200:
            data = response.json()
            if search_type == "gtins":
                descricao = data.get("description")
                ncm = data.get("ncm")
                codigo = data.get("gtin")
            else:
                produto = data[0]
                descricao = produto.get("description")
                ncm = produto.get("ncm")
                codigo = produto.get("gtin")
            if not descricao or not ncm:
                window["-OUTPUT-"].update(
                    "Informações do produto não disponíveis.")
            else:
                window["-OUTPUT-"].update(
                    f"Código EAN: {codigo}\nDescrição: {descricao}\nNCM: {ncm}")
        else:
            error = response.json()["error"]
            window["-OUTPUT-"].update(
                f"Erro na consulta: {error}. Código de erro: {response.status_code}")
            token_idx = (token_idx + 1) % len(tokens)  # troca o token usado

    if event == '-INSTAGRAM-':
        webbrowser.open_new_tab(
            'https://www.instagram.com/RAFAELMOREIRAFERNANDES/')

    if event == '-COPY-':
        sg.clipboard_set(window["-OUTPUT-"].get())

window.close()
