import flet as ft
import asyncio
from datetime import datetime
import sqlite3


dia_semana = datetime.now().strftime('%A').capitalize() 

if dia_semana == 'Monday':
    dia_semana = 'Segunda-feira'

if dia_semana == 'Tuesday':
    dia_semana = 'Terça-feira' 

if dia_semana == 'Wednesday':
    dia_semana = 'Quarta-feira'

if dia_semana == 'Thursday':
    dia_semana = 'Quinta-feira'

if dia_semana == 'Friday':
    dia_semana = 'Sexta-feira'

if dia_semana == 'Saturday':
    dia_semana = 'Sábado' 

if dia_semana == 'Sunday':
    dia_semana = 'Domingo'    


dia_mes = datetime.now().strftime('%d')
mes = datetime.now().strftime('%B').capitalize()

if mes == 'January':
    mes = 'Janeiro'

if mes == 'February':
    mes = 'Fevereiro'

if mes == 'March':
    mes = 'Março'

if mes == 'April':
    mes = 'Abril'

if mes == 'May':
    mes = 'Maio'

if mes == 'June':
    mes = 'Junho'

if mes == 'July':
    mes = 'Julho'

if mes == 'August':
    mes = 'Agosto'

if mes == 'September':
    mes = 'Setembro'

if mes == 'October':
    mes = 'Outubro'

if mes == 'November':
    mes = 'Novembro'

if mes == 'December':
    mes = 'Dezembro'

data_mes = datetime.now().strftime('%B %Y')

ultimo_login = datetime.now().strftime('%d/%m/%Y')

data_hora_completa = datetime.now().strftime('%d/%m/%Y, %H:%M:%S')

def banco_dados():
    conn = sqlite3.connect('database.db')    
    cursor = conn.cursor()
    
    cursor.execute(f'''create table if not exists _config (
                   id integer,
                   nome_meta_atual text,
                   meta_atual bool,
                   status bool,
                   valor_mensal float,
                   valor_semanal float,
                   semanas integer,
                   data_inicio_completa text,
                   barra_nav bool)''')
    
    id_meta = cursor.execute(f'''select id from _config ''').fetchone()
    
    if id_meta is None:
        cursor.execute(f'''insert into _config (id, meta_atual, status, barra_nav) values (1, False, False, True)''')
        conn.commit()

    meta_atual = cursor.execute(f'''select meta_atual from _config ''').fetchone()[0]
    nome_meta_atual = cursor.execute(f'''select nome_meta_atual from _config ''').fetchone()[0]
    valor_mensal = cursor.execute(f'''select valor_mensal from _config ''').fetchone()[0]
    valor_semanal = cursor.execute(f'''select valor_semanal from _config ''').fetchone()[0]
    semanas = cursor.execute(f'''select semanas from _config ''').fetchone()[0]
    data_inicio_completa = cursor.execute(f'''select data_inicio_completa from _config ''').fetchone()[0]

    if nome_meta_atual is not None:
            cursor.execute(f'''create table if not exists "{nome_meta_atual}"(
                            id integer,
                            valor_mensal float,
                            valor_semanal float,
                            total_gasto text,
                            semanas integer,
                            data_inicio text,
                            data_inicio_completa text,
                            ultimo_login text,
                            numero_compras integer,
                            restaurar_dinheiro_semana bool
                            ) ''')

            id_ = cursor.execute(f'''select id from "{nome_meta_atual}" ''').fetchone()

            if id_ is None:
                cursor.execute(f'''insert into "{nome_meta_atual}" (
                id, valor_mensal, valor_semanal, total_gasto, semanas, data_inicio_completa, numero_compras, restaurar_dinheiro_semana) 
                values (1, {valor_mensal}, {valor_semanal}, "0,00", {semanas}, "{data_inicio_completa}", 0, False)''')
            
            cursor.execute(f'''create table if not exists carrinho_compras
                           (
                           id integer,
                           nome_da_compra text,
                           valor_da_compra float,
                           data_da_compra text,
                           total_gasto float
                           )''')


            conn.commit()


def main(page: ft.Page):
    page.update()
    page.clean()
    page.title = 'Semanalize'
    page.bgcolor = 'white'
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER

    page.locale_configuration = ft.LocaleConfiguration(
        supported_locales=[
            ft.Locale('pt', 'BR'),
        ],
        current_locale=ft.Locale('pt', 'BR')
    )
    
    texto_superior = ft.Container(
            content= ft.Text(value='Semanalize', color='black', size=27),
            padding=ft.padding.only(top=30, left=5)
        )
    
    banco_dados()

    def atualizar_config(item, valor):
            conn = sqlite3.connect('database.db')    
            cursor = conn.cursor()

            cursor.execute(f'''update _config set "{item}" = "{valor}" where id = 1 ''')

            conn.commit()
            conn.close()

    def listar_config(item):
                conn = sqlite3.connect('database.db')    
                cursor = conn.cursor()

                itens = cursor.execute(f'''select "{item}" from _config ''').fetchone()[0]

                conn.commit()
                conn.close()     

                return itens   

    status = (listar_config('status'))
        
    def navegacao(e):
            if barra_navegacao.selected_index == 0:
                tabelas(page)
            

            elif barra_navegacao.selected_index == 1:
                main(page)
                

            elif barra_navegacao.selected_index == 2:
                compras(page)
    
    def fechar_popup():
            page.dialog.open = False
            atualizar_config('status', False)
            
            page.update()
            main(page)


    if status == 'True':

        def fim_todas_semanas():

            atualizar_config('meta_atual', True)

            popup = ft.AlertDialog(
                title=ft.Text(value='Tabela Finalizada', color='black' ),
                content=ft.Text('Sua tabela antingiu o limite maximo de semanas. Crie uma nova tabela para iniciar uma nova semana', color='black'),
                modal=True,
                bgcolor='white',
                actions=[

                    ft.TextButton(
                        text='Entendi',
                        style=ft.ButtonStyle(color='black'),
                        on_click=lambda e: fechar_popup()
                        
                    )
                ],

                actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                
            )

            page.dialog = popup
            popup.open = True
            page.update()         


        def calcular_dias():
            # Obter a data de início como número do banco de dados (ex: 5 para dia 5 do mês)
            data_completa = listar_itens('data_inicio_completa')

            # Criar a data com base no dia do início e mês/ano atual
            data_inicio = datetime.strptime(data_completa, '%d/%m/%Y')

            # Converter a string de ultima_atualizacao para um objeto datetime usando o formato correto
            ultimo_login = datetime.strptime(listar_itens('ultimo_login'), '%d/%m/%Y')

            # Diferença de dias desde a última atualização
            dias_passados = (ultimo_login - data_inicio).days
            
            semana = 1
            
            # Se passaram mais de 7 dias, atualize a semana
            if dias_passados >= 7:
                semanas_adicionais = dias_passados // 7
                dias = (dias_passados % 7) + 1  # Reseta os dias para 1 depois de 7
                semana = (semana + semanas_adicionais - 1) % 5 + 1  # Atualiza a semana e reseta após 5
                
            else:
                # Se não passaram 7 dias, mantenha os dias atualizados mas sem resetar a semana
                dias = (dias_passados % 7) + 1


            if semana > listar_itens('semanas'):
                fim_todas_semanas()

            resete_ligado = listar_itens('restaurar_dinheiro_semana')
            valor_semanal = listar_itens('valor_semanal')
            valor_restaurado = listar_itens('valor_mensal') / listar_itens('semanas')

            if semana == 2 and not resete_ligado:

                if valor_semanal < 0:
                    valor_final = valor_restaurado - abs(valor_semanal)
                    
                    atualizar_itens('valor_semanal', valor_final)

                else:
                    somar_itens('valor_semanal', valor_restaurado)
                
                atualizar_itens('restaurar_dinheiro_semana', True)


            if semana == 3 and resete_ligado:
                if valor_semanal < 0:
                    valor_final = valor_restaurado - abs(valor_semanal)
                    
                    atualizar_itens('valor_semanal', valor_final)

                else:
                    somar_itens('valor_semanal', valor_restaurado)
                
                atualizar_itens('restaurar_dinheiro_semana', False)


            if semana == 4 and not resete_ligado:
                if valor_semanal < 0:
                    valor_final = valor_restaurado - abs(valor_semanal)
                    
                    atualizar_itens('valor_semanal', valor_final)

                else:
                    somar_itens('valor_semanal', valor_restaurado)
                
                atualizar_itens('restaurar_dinheiro_semana', True)


            if semana == 5 and resete_ligado:
                if valor_semanal < 0:
                    valor_final = valor_restaurado - abs(valor_semanal)
                    
                    atualizar_itens('valor_semanal', valor_final)

                else:
                    somar_itens('valor_semanal', valor_restaurado)
                
                atualizar_itens('restaurar_dinheiro_semana', False)


            return dias, semana
        
        def atualizar_itens(item, valor):
                conn = sqlite3.connect('database.db')    
                cursor = conn.cursor()

                cursor.execute(f'''update "{listar_config('nome_meta_atual')}" set "{item}" = "{valor}" where id = 1 ''')

                conn.commit()
                conn.close()
        
        def somar_itens(item, valor):
                conn = sqlite3.connect('database.db')    
                cursor = conn.cursor()

                cursor.execute(f'''update "{listar_config('nome_meta_atual')}" set "{item}" = "{item}" + "{valor}" where id = 1 ''')

                conn.commit()
                conn.close()

        def atualizar_compras(item, valor, index):
                conn = sqlite3.connect('database.db')    
                cursor = conn.cursor()

                cursor.execute(f'''update carrinho_compras set "{item}" = "{valor}" where id = "{index}" ''')

                conn.commit()
                conn.close()

        def listar_itens(item):
                conn = sqlite3.connect('database.db')    
                cursor = conn.cursor()

                itens = cursor.execute(f'''select "{item}" from "{listar_config('nome_meta_atual')}" ''').fetchone()[0]


                conn.commit()
                conn.close()     

                return itens   
            
        def mostrar_nome_compras(item, index):
            conn = sqlite3.connect('database.db')    
            cursor = conn.cursor()

            itens = cursor.execute(f'''select "{item}" from carrinho_compras where id = "{index}" ''').fetchone()[0]

            conn.commit()
            conn.close()     

            return itens
        
        def calcular_percentual_da_barra():
                valor_total = float(listar_itens('valor_mensal')) / float(listar_itens('semanas')) #significa os 100%
                valor_atual = float(listar_itens('valor_semanal')) #meu valor
                
                percentual = min(valor_atual / valor_total, 1.0)

                if percentual < 0:

                    return 0

                else:
                    return percentual
        
        atualizar_itens(item='ultimo_login', valor=f'{ultimo_login}')


        dias, semanas = calcular_dias()

        inicio = ft.Container(
    bgcolor=ft.colors.BLUE_GREY_900,
    width=390,
    height=160,
    shadow=ft.BoxShadow(spread_radius= 1, blur_radius=10, color='grey'),
    border_radius=10,
    content= ft.Row(
        controls=[
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Icon(ft.icons.CALENDAR_TODAY_OUTLINED, color=ft.colors.GREY_200, size=30),
                        ft.Text('DIAS', size=25, color=ft.colors.AMBER),
                        dia_texto := ft.Text(f'{dias}/7', size=40, color=ft.colors.AMBER),
                    ],
                    alignment=ft.MainAxisAlignment.START,  # Alinhamento dos textos dentro do Column
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=5,  # Espaçamento entre os textos
                ),
                alignment=ft.alignment.center,
                padding=ft.padding.only(left=50, top=10)
            ),

            #por algum motivo esse divider parou de aparecer, mas continua dividindo os elemensto, então vou deixar
            ft.VerticalDivider(width=110, leading_indent=11, trailing_indent=500),

            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Icon(ft.icons.CALENDAR_MONTH_OUTLINED, color=ft.colors.GREY_200, size=30),
                        ft.Text('SEMANAS', size=25, color=ft.colors.AMBER),
                        semana_texto := ft.Text(f'{semanas}/{listar_itens("semanas")}', size=40, color=ft.colors.AMBER),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=5,
                ),
                alignment=ft.alignment.center,
                padding=ft.padding.only(right=20, top=10)
            ),
    
        ]
    )
)
        barra = ft.Container(
            bgcolor=ft.colors.AMBER,
            width=390,
            height=90,
            border_radius=10,
            shadow=ft.BoxShadow(spread_radius= 1, blur_radius=10, color='grey'),
            content=ft.Column(
                controls=[
                    ft.Column(
                        controls=[
                            ft.Text(value=f'{dia_semana}, {dia_mes} de {mes}', color=ft.colors.BLUE_GREY_900, size=18)
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        width=500,
                        height=40
                        
                    ),

                    ft.Row(
                        controls=[
                            ft.Text(''),
                            ft.ProgressBar(
                                width=267, 
                                height=15, 
                                color=ft.colors.BLUE_ACCENT, 
                                bgcolor=ft.colors.WHITE, 
                                value=calcular_percentual_da_barra(),
                                border_radius=6,                                 
                            ),
                            
                            ft.Text(value=f'R$ {listar_itens("valor_semanal"):.2f}'.replace('.',','), color=ft.colors.BLUE_GREY_900, size=20)
                        ],              
                    ),
                ]
                

            ),
            on_long_press=lambda e: olhar_data_inicio(e),
        )

        def olhar_data_inicio(e):
            popup = ft.AlertDialog(
                    title=ft.Text(value='Data de início', color='black' ),
                    content=ft.Text(f'{listar_config("data_inicio_completa")}', color='black', size=18),
                    bgcolor='white',
                    actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    
                )

            page.dialog = popup
            popup.open = True
            page.update()


        dinheiro = ft.Row(
            
            controls=[
                
                ft.Container(
                    bgcolor=ft.colors.GREEN_400,
                    width=190,
                    height=250,
                    border_radius=30,
                    shadow=ft.BoxShadow(spread_radius= 1, blur_radius=10, color='grey'),
                    content=ft.Column(
                        controls=[
                            ft.Text(''),
                            ft.Icon(
                                name=ft.icons.ATTACH_MONEY,
                                size=60,
                                color=ft.colors.BLUE_GREY_800
                            ),
                            ft.Text('Total', color=ft.colors.AMBER, size=40),
                            ft.Text(f'R$ {listar_itens("valor_mensal"):,.2f}'.replace(",", "#").replace(".", ",").replace("#", "."), color=ft.colors.WHITE, size=25)
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=0,  
                    )

                ),

                ft.Container(
                    bgcolor=ft.colors.BLUE_700,
                    width=190,
                    height=250,
                    border_radius=30,
                    shadow=ft.BoxShadow(spread_radius= 1, blur_radius=10, color='grey'),
                    content=ft.Column(
                        controls=[
                            ft.Text(''),
                            ft.Icon(
                                name=ft.icons.WALLET,
                                size=60,
                                color=ft.colors.WHITE70
                            ),
                            ft.Text('Semanal', color=ft.colors.AMBER, size=40),
                            ft.Text(f'R$ {listar_config("valor_mensal") / listar_itens("semanas"):.2f}'.replace('.', ','), color=ft.colors.WHITE, size=25)
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=0,  
                    )
                    

                )
            ],
            spacing=10
        )

        valor_semanal = listar_itens('valor_semanal')
        valor_restaurado = listar_itens('valor_mensal') / listar_itens('semanas')
        if valor_semanal < 0:
            valor_final = valor_restaurado - abs(valor_semanal)
        
        elif valor_semanal >= 0:
            valor_final = valor_restaurado + abs(valor_semanal)

        proxima_semana = ft.Container(
            bgcolor=ft.colors.BLUE_GREY_800,
            width=390,
            height=80,
            border_radius=10,
            shadow=ft.BoxShadow(spread_radius= 1, blur_radius=10, color='grey'),
            content=ft.Column(
                controls=[
                    ft.Text(value='Próxima Semana', color=ft.colors.AMBER, size=25),
                    ft.Text(value=f'R$ {valor_final:.2f}'.replace('.',','), color=ft.colors.GREY_200, size=25)
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=0
            )
        )

        botao = ft.Stack([
        ft.IconButton(
            top=1,
            left=333,
            icon= ft.icons.ADD,
            icon_color= ft.colors.WHITE,
            bgcolor=ft.colors.BLACK54,
            on_click= lambda e:criar_tabela(page),
            scale=1.2
            ),
        ])
             

        barra_navegacao = ft.NavigationBar(
            selected_index=1,
            bgcolor=ft.colors.BLACK87,
            height=70,
            on_change=navegacao, 
            destinations=[
               ft.NavigationBarDestination(icon=ft.icons.FORMAT_LIST_BULLETED_OUTLINED, label='Tabelas'),
               ft.NavigationBarDestination(icon=ft.icons.HOME_OUTLINED, label='Início'),
               ft.NavigationBarDestination(icon=ft.icons.SHOPPING_CART_OUTLINED, label='Compras')
           ]

        )

        page.add(texto_superior, inicio, barra, proxima_semana, dinheiro, barra_navegacao, botao)

    else:
        botao = ft.Stack([
        ft.IconButton(
            top=200,
            left=333,
            icon=ft.icons.ADD,
            icon_color=ft.colors.WHITE,
            bgcolor=ft.colors.BLACK54,
            on_click=lambda e:criar_tabela(page),
            scale=1.2
            ),       
    ])

        texto_aviso = ft.Container(
            content=ft.Text('Nenhuma tabela adicionada ainda.',
                        color='black',
                        size=15),
            padding=ft.padding.only(top=350),
            alignment=ft.alignment.center
        )

        barra_navegacao = ft.NavigationBar(
            selected_index=1,
            bgcolor=ft.colors.BLACK87,
            height=70,
            on_change=navegacao, 
            destinations=[
               ft.NavigationBarDestination(icon=ft.icons.FORMAT_LIST_BULLETED_OUTLINED, label='Tabelas'),
               ft.NavigationBarDestination(icon=ft.icons.HOME_OUTLINED, label='Início'),
               ft.NavigationBarDestination(icon=ft.icons.SHOPPING_CART_OUTLINED, label='Compras')
           ]

        )
        page.add(texto_superior, texto_aviso, botao, barra_navegacao)


    def tabelas(page: ft.Page):
        page.clean()
        page.bgcolor = 'white'
        page.vertical_alignment = ft.MainAxisAlignment.START
        page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        page.locale_configuration = ft.LocaleConfiguration(
            supported_locales=[
                ft.Locale('pt', 'BR'),
            ],
            current_locale=ft.Locale('pt', 'BR')
        )
        texto_tabelas = ft.Container(
                content= ft.Text(value='Tabelas', color='black', size=27),
                padding=ft.padding.only(top=30, left=5)
            )

        texto_aviso = ft.Container(
            content=ft.Text('Em desenvolvimento.',
                        color='black',
                        size=15),
            padding=ft.padding.only(top=350),
            alignment=ft.alignment.center
        )
        
        page.add(texto_tabelas, texto_aviso, barra_navegacao)
    

    def compras(page: ft.Page):
        page.clean()
        page.bgcolor = 'white'
        page.vertical_alignment = ft.MainAxisAlignment.START
        page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        page.locale_configuration = ft.LocaleConfiguration(
            supported_locales=[
                ft.Locale('pt', 'BR'),
            ],
            current_locale=ft.Locale('pt', 'BR')
        )

        texto_compras = ft.Container(
                content= ft.Text(value='Compras', color='black', size=27),
                padding=ft.padding.only(top=30, left=5)
            )


        if status == 'True':
            
            def contabilizar_compras():
                conn = sqlite3.connect('database.db')    
                cursor = conn.cursor()

                cursor.execute(f'''update "{listar_config('nome_meta_atual')}" set numero_compras = numero_compras + 1 where id = 1 ''')

                numero_compras = cursor.execute(f'select numero_compras from "{listar_config("nome_meta_atual")}" ').fetchone()[0]

                conn.commit()
                conn.close()

                return numero_compras

            def deletar_itens(index, e):
                
                conn = sqlite3.connect('database.db')    
                cursor = conn.cursor()


                cursor.execute(f'''delete from carrinho_compras where id = {index+1} ''')
                cursor.execute(f'''update "{listar_config('nome_meta_atual')}" set numero_compras = numero_compras - 1 where id = 1 ''')
                
                ids = cursor.execute(f'select id from carrinho_compras order by id asc').fetchall()
                ids_atualizados = [linha[0] for linha in ids]

                for novo_id, id_antigo in enumerate(ids_atualizados, start=1):
                    cursor.execute(f'update carrinho_compras set id = {novo_id} where id = {id_antigo}')
                
                valor_formatado = e.control.data.replace(',','.')
                cursor.execute(f'''update "{listar_config('nome_meta_atual')}" set total_gasto = (total_gasto - "{valor_formatado}") where id = 1 ''')

                conn.commit()
                conn.close()
                
                
                obter_total_gasto()
                mostrar_compras(lista_itens)
                   
            def inserir_compras(nome_compra, valor_compra, data_compra, id_):
                conn = sqlite3.connect('database.db')    
                cursor = conn.cursor()

                cursor.execute(f'''insert into carrinho_compras (
                            id, nome_da_compra, valor_da_compra, data_da_compra)
                            values ("{id_}", "{nome_compra}", "{valor_compra}", "{data_compra}")''')
                
                compra_formatada = valor_compra.replace(',','.')

                cursor.execute(f'''update "{listar_config('nome_meta_atual')}" set total_gasto = (total_gasto + "{compra_formatada}") where id = 1 ''')
                conn.commit()
                conn.close()

                obter_total_gasto()

            def listar_compras():
                conn = sqlite3.connect('database.db')    
                cursor = conn.cursor()

                lista_compra = cursor.execute(f'select * from carrinho_compras ').fetchall()

                lista = []
                
                for compra in lista_compra:

                    lista.append(f'{compra[1]} R$ {compra[2]}')
                    

                conn.commit()
                conn.close()

                return lista

            def adicionar_itens(e):
                if valor_compras.value == 'R$ 0,00':
                    pass
                
                else:
                    n = contabilizar_compras() #numero de compras

                    valor = valor_compras.value[3:]

                    inserir_compras(f'compra {n}', f'{valor}', f'{data_hora_completa}', f'{n}')

                    valor_compras.value = 'R$ 0,00'
                    page.update()

                obter_total_gasto()
                mostrar_compras(lista_itens)
            
            def formatar_numeros(e):

                # Obtém o texto atual do campo
                texto_atual = e.control.value

                # Remove o prefixo e espaços, se houver
                if texto_atual.startswith("R$ "):
                    numero = texto_atual[3:].replace('.', '').replace(',', '')  # Remove R$ e caracteres de formatação
                else:
                    numero = texto_atual.replace('.', '').replace(',', '')

                # Adiciona lógica para impedir que o valor fique negativo ou inválido
                if not numero.isdigit():
                    numero = '0'

                # Converte o número em um inteiro para formatar os milhares
                valor_decimal = int(numero)

                # Divide o valor entre parte inteira e centavos
                parte_inteira = valor_decimal // 100
                parte_decimal = valor_decimal % 100

                # Formata a parte inteira com separador de milhar
                parte_inteira_formatada = f"{parte_inteira:,}".replace(',', '.')

                # Cria o valor final formatado
                novo_valor = f"R$ {parte_inteira_formatada},{parte_decimal:02}"

                # Atualiza o TextField
                e.control.value = novo_valor
                page.update()

            def alterar_nome_compra(novo_nome, i):

                atualizar_compras('nome_da_compra', novo_nome, i )

                page.update()

                fechar_popup()
                mostrar_compras(lista_itens)

            def duplicar_compra(i):
                
                conn = sqlite3.connect('database.db')    
                cursor = conn.cursor()

                n = contabilizar_compras()

                compras = cursor.execute(f'select * from carrinho_compras ').fetchall()[i]

                inserir_compras(compras[1], compras[2], compras[3], n)


                conn.commit()
                conn.close()

                mostrar_compras(lista_itens)

            def mostrar_compras(lista_itens):
                conn = sqlite3.connect('database.db')    
                cursor = conn.cursor()

                lista_itens.controls.clear()

                lista_de_compras = listar_compras()

                compras = cursor.execute(f'select * from carrinho_compras ').fetchall()

                for i, compra in enumerate(lista_de_compras):
                    lista_itens.controls.append(ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(
                                value=f'{compra}',
                                color='black',
                                size=15
                                    ),

                            ft.Row(
                                spacing=0,
                                controls=[

                                    ft.IconButton(
                                        icon=ft.icons.ADD,
                                        icon_color='black',
                                        on_click=lambda e, i = i: duplicar_compra(i)
                                        
                                    ),

                                    ft.IconButton(
                                        icon=ft.icons.MODE_EDIT_OUTLINED,
                                        icon_color='black',
                                        on_click=lambda e, i = i: abrir_popup(i),
                                        
                                    ),

                                    ft.IconButton(
                                        icon=ft.icons.DELETE_OUTLINE,
                                        icon_color='black',
                                        on_click=lambda e, i = i: deletar_itens(i, e),
                                        data=compras[i][2] # lista especifica | valor da compra
                                        
                                        
                                    ),
                                ],
                                
                            )
                            
                        ],
                        
                    ))
                
                page.update()
            
            def finalizar_compra(e):
                conn = sqlite3.connect('database.db')    
                cursor = conn.cursor()

                cursor.execute(f'''create table if not exists historico_das_compras 
                               as select * from carrinho_compras where 0''')
                
                cursor.execute(f'''insert into historico_das_compras 
                               select * from carrinho_compras ''')
                
                cursor.execute(f'''update "{listar_config('nome_meta_atual')}" set numero_compras = 0 ''')
                
                cursor.execute(f'delete from carrinho_compras ')

                cursor.execute(f'''update "{listar_config('nome_meta_atual')}" set valor_semanal = (valor_semanal - total_gasto) ''')
                cursor.execute(f'''update "{listar_config('nome_meta_atual')}" set total_gasto = "0.00" ''')

                conn.commit()
                conn.close()

                obter_total_gasto()
                mostrar_compras(lista_itens)

            def obter_total_gasto():
                conn = sqlite3.connect('database.db')    
                cursor = conn.cursor()
                valor_semanal = cursor.execute(f'SELECT valor_semanal FROM "{listar_config("nome_meta_atual")}" WHERE id = 1').fetchone()[0]
                total_gasto = cursor.execute(f'SELECT total_gasto FROM "{listar_config("nome_meta_atual")}" WHERE id = 1').fetchone()[0]
                conn.commit()
                conn.close()

                valor_semanal = float(valor_semanal)
                total_gasto = float(total_gasto.replace(',', '.'))

                valor_gasto.value = f'R$ {total_gasto:.2f}'.replace('.',',')
                valor_restante.value = f'R$ {valor_semanal - total_gasto:.2f}'.replace('.',',')

                page.update()
            
            def esconder_barra(e):   
                if e.name == 'focus':
                    #ao clicar na barra ela esconde
                    barra_navegacao.visible = False
                    lista_itens.height = 325
                    
                
                elif e.name == 'blur':
                    #ao sair da brra ela aparece
                    barra_navegacao.visible = True
                    lista_itens.height = 430           

                page.update()

            def abrir_popup(i):
                i = i + 1

                popup = ft.AlertDialog(
                    title=ft.Text(value='Digite um novo nome', color='black' ),
                    content=ft.Column(
                        controls=[
                            texto:=ft.TextField(
                                on_focus=esconder_barra,
                                on_blur=esconder_barra,
                                cursor_color='black',
                                border_color='black',
                                focused_border_color='black',
                                hint_text='Nome do produto',
                                color='black'

                            ),
                        ],
                        height=50
                    ),
                    bgcolor='white',
                    actions=[
                        ft.TextButton(
                            text='Cancelar',
                            style=ft.ButtonStyle(color='black'),
                            on_click=lambda e: fechar_popup()
                        ),

                        ft.TextButton(
                            text='Confirmar',
                            style=ft.ButtonStyle(color='black'),
                            on_click=lambda e: alterar_nome_compra(texto.value, i)
                            
                        )
                    ],

                    actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    
                )
                texto.value = mostrar_nome_compras('nome_da_compra', i)

                page.dialog = popup
                popup.open = True
                page.update()

            def fechar_popup():
                page.dialog.open = False
                page.update()

            compra = ft.Column(
                width=390,
                controls=[
                    ft.Text('Adicionar valor dos itens', color='black', size=18),

                    ft.Row(
                        controls=[
                            valor_compras:= ft.TextField(
                                keyboard_type=ft.KeyboardType.NUMBER,
                                border_color='black',
                                color='black',
                                cursor_color='black',
                                width=390,
                                on_submit=adicionar_itens,
                                on_change=formatar_numeros,
                                on_blur=esconder_barra,
                                on_focus=esconder_barra,
                                value='R$ 0,00',
                                          
                            ), 
                        ]),


                    ft.Row(
                        controls=[
                            ft.Container(
                                valor_restante:=ft.Text(
                                    value=f'R$ {listar_itens("valor_semanal"):.2f}'.replace('.',','), #valor semanal
                                    size=17
                                    
                                ),
                                bgcolor='green',
                                border_radius=8,
                                width=90,
  
                                
                            ),

                            ft.Container(
                                valor_gasto:=ft.Text(
                                    value=f'R$ {listar_itens("total_gasto")}'.replace('.',','), #valor das compras
                                    size=17
                                ),
                                bgcolor='blue',
                                border_radius=8,
                                width=90,
                        
                                
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),


                    lista_itens:= ft.Column(
                        controls=[
                                           
                        ],
                        scroll=ft.ScrollMode.ADAPTIVE,
                        auto_scroll=True,
                        width=390,
                        height=430,
                        spacing=0
                    ),

                    ft.Column(
                        controls=[
                            ft.OutlinedButton(
                                text='Finalizar Compras',
                                icon=ft.icons.SHOPPING_BAG_OUTLINED,
                                icon_color=ft.colors.BLUE_GREY_900,
                                style=ft.ButtonStyle(color=ft.colors.BLUE_GREY_900),
                                on_click=finalizar_compra,
                                scale=1.1
                            )
                        ],
                        width=390,
                        height=150,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.CENTER
                        
                    )
                    
                ]
            )
            
            obter_total_gasto()
            mostrar_compras(lista_itens)
  
            page.add(texto_compras, compra, barra_navegacao)

        else:
            texto_aviso = ft.Container(
                content=ft.Text('Crie uma tabela para começar as compras',
                            color='black',
                            size=15),
                padding=ft.padding.only(top=350),
                alignment=ft.alignment.center
            )
        
            page.add(texto_compras, texto_aviso, barra_navegacao)

    def criar_tabela(page: ft.Page):
        page.clean()
        page.bgcolor = 'white'
        page.vertical_alignment = ft.MainAxisAlignment.START
        page.horizontal_alignment = ft.MainAxisAlignment.CENTER
        page.locale_configuration = ft.LocaleConfiguration(
            supported_locales=[
                ft.Locale('pt', 'BR'),
            ],
            current_locale=ft.Locale('pt', 'BR')
        )

        def tabela_existe(nome_tabela):
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (nome_tabela,))
            resultado = cursor.fetchone()
            
            conn.close()

            # Retorna True se a tabela existe, ou False se não

            return resultado is not None

        def fechar_popup():
            page.dialog.open = False
            page.update()
        
        def cancelar_popup():
            page.dialog.open = False
            page.update()
            main(page)


        meta_atual = listar_config('meta_atual')

        if tabela_existe(listar_config('nome_meta_atual')) and meta_atual == 'True':
            atualizar_config('meta_atual', False)

            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()

            cursor.execute(f'alter table "{listar_config("nome_meta_atual")}" rename to "{listar_config("nome_meta_atual")}_old" ')
            
            conn.commit()
            conn.close()
   
        else:

            if tabela_existe(listar_config('nome_meta_atual')):

                popup = ft.AlertDialog(
                    title=ft.Text(value='Já existe uma tabela ativa', color='black' ),
                    content=ft.Text('Criar uma nova tabela nesse momento fará com que perca todos os seus dados, deseja continuar?', color='black'),
                    modal=True,
                    bgcolor='white',
                    actions=[
                        ft.TextButton(
                            text='Voltar',
                            style=ft.ButtonStyle(color='black'),
                            on_click=lambda e: cancelar_popup()
                        ),

                        ft.TextButton(
                            text='Continuar',
                            style=ft.ButtonStyle(color='black'),
                            on_click=lambda e: fechar_popup()
                            
                        )
                    ],

                    actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    
                )

                page.dialog = popup
                popup.open = True
                page.update()         

        def radio_opcao(e):

            valor_formatado = valor.value.replace('R$', '').replace('.','').replace(',','.')

            if caixa.value == '1':
                valor.hint_text = 'Dividir Valor'
                
                if valor.value == '':
                    resultado.value = ''
                
                elif valor.value and dp.value:
                    resultado.value = f'Gasto Semanal R$ {float(valor_formatado) / float(dp.value):.2f}'.replace('.', ',')
                    

            elif caixa.value == '2':
                valor.hint_text = 'Definir Valor'

                if valor.value == '':
                    resultado.value = ''
                
                elif valor.value and dp.value:
                    resultado.value = f'Mensal Necessário R$ {float(valor_formatado) * float(dp.value):.2f}'.replace('.', ',')
                    

            caixa_2.update()
        
        def selecionar_data(e):
            data.value = f"Data Escolhida: {e.control.value.strftime('%d/%m/%Y')}"

            global data_inicio, data_inicio_completa

            data_inicio = e.control.value.strftime('%B_%Y')
            data_inicio_completa = e.control.value.strftime('%d/%m/%Y')

            caixa_2.update()

        def desselecionar_data(e):
            data.value = ""
            caixa_2.update()
        
        def formatar_numeros(e):

                # Obtém o texto atual do campo
                texto_atual = e.control.value

                # Remove o prefixo e espaços, se houver
                if texto_atual.startswith("R$ "):
                    numero = texto_atual[3:].replace('.', '').replace(',', '')  # Remove R$ e caracteres de formatação
                else:
                    numero = texto_atual.replace('.', '').replace(',', '')

                # Adiciona lógica para impedir que o valor fique negativo ou inválido
                if not numero.isdigit():
                    numero = '0'

                # Converte o número em um inteiro para formatar os milhares
                valor_decimal = int(numero)

                # Divide o valor entre parte inteira e centavos
                parte_inteira = valor_decimal // 100
                parte_decimal = valor_decimal % 100

                # Formata a parte inteira com separador de milhar
                parte_inteira_formatada = f"{parte_inteira:,}".replace(',', '.')

                # Cria o valor final formatado
                novo_valor = f"R$ {parte_inteira_formatada},{parte_decimal:02}"

                # Atualiza o TextField
                e.control.value = novo_valor
                
                page.update()
                radio_opcao(e)

        def dadados_faltando(e):
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Preencha todos os campos acima!"),
                action="Fechar",
                on_action=lambda e: ...
            )
            page.snack_bar.open = True
            page.update()

        async def validar_dados(e):
            if not caixa.value or not valor.value or not resultado.value or not dp.value or not data.value:
                dadados_faltando(e)
                sem_dados.update()

            if caixa.value and valor.value and resultado.value and dp.value and data.value:
                sem_dados.color = 'green'
                sem_dados.value = 'Tabela criado com sucesso'
                sem_dados.update()
                
                await asyncio.sleep(1)

                if tabela_existe(listar_config('nome_meta_atual')):
                    conn = sqlite3.connect('database.db')    
                    cursor = conn.cursor()

                    cursor.execute(f'''delete from "{listar_config("nome_meta_atual")}" ''')

                    cursor.execute(f'''delete from carrinho_compras ''')

                    conn.commit()
                    conn.close()

                if caixa.value == '1':
                    valor_mensal = valor.value.replace('R$', '').replace('.','').replace(',','.')
                
                elif caixa.value == '2':
                    valor_mensal = valor.value.replace('R$', '').replace('.','').replace(',','.')
                    valor_mensal = float(valor_mensal) * float(dp.value)
                
                valor_semanal = float(valor_mensal) / float(dp.value)
                
                atualizar_config(item='status', valor= True)
                atualizar_config(item='nome_meta_atual', valor=f'{data_inicio}')
                atualizar_config(item='valor_mensal', valor=f'{valor_mensal}')
                atualizar_config(item='valor_semanal', valor=f'{valor_semanal}')
                atualizar_config(item='semanas', valor=dp.value)
                atualizar_config(item='data_inicio_completa', valor=f'{data_inicio_completa}')

                banco_dados()
                main(page)

        texto_superior = ft.Container(
            padding=ft.padding.only(top=25, bottom=20),
            content=ft.Row(
                controls=[
                ft.IconButton(icon=ft.icons.CLOSE, icon_color='black', scale=1, padding=ft.padding.only(right=20), on_click=lambda e: main(page)),
                ft.Text(value='Nova tabela', size=25, color='black',)],
                spacing=0     
            ),
            
        )

        caixa = ft.RadioGroup(
            content=ft.Column(
                controls=[

                ft.Radio(
                    value='1', label='Definir um valor mensal', label_style=ft.TextStyle(color='black'),
                    active_color='black', fill_color='black', scale=1.07),

                ft.Radio(
                    value='2', label='Definir um valor semanal', label_style=ft.TextStyle(color='black'),
                    active_color='black', fill_color='black', scale=1.07),
                
                ],
                
                ),
            on_change=radio_opcao
            
        )

        caixa_2 = ft.Column(
            controls=[
                dp := ft.Dropdown(
                    width=185,
                    label='Dividir em',
                    label_style=ft.TextStyle(color='black'), 
                    color='black',
                    bgcolor='white',
                    border_color='black',
                    border_width=1,
                    on_change=radio_opcao,
                    options=[
                        ft.dropdown.Option(key= '4', text='4 semanas'),
                        ft.dropdown.Option(key= '5', text='5 semanas'),
                    ]), 


                ft.Row([
                valor := ft.TextField(
                    width=185,
                    label='Digite o valor',
                    label_style=ft.TextStyle(color='black'), 
                    color='black', 
                    hint_text='Dividir valor',
                    keyboard_type=ft.KeyboardType.NUMBER,
                    border_color='black',
                    selection_color='black',
                    cursor_color='black',
                    border_width=1,
                    on_change=lambda e: formatar_numeros(e),
                    value='R$ 0,00'
                    ),
                
                resultado := ft.Text(value='', color='black')
                
                ]),
                ft.Row(
                    controls=[
                    ft.ElevatedButton(
                    text='Data de inicio', 
                    icon=ft.icons.CALENDAR_MONTH, 
                    color='black',
                    bgcolor='white',
                    width=187,
                    
                    on_click= lambda e: page.open(
                        ft.DatePicker(
                            keyboard_type=ft.KeyboardType.DATETIME,
                            field_hint_text='dia/mês/ano',
                            confirm_text='Confirmar',
                            cancel_text='Cancelar',
                            help_text='Selecione uma data',
                            field_label_text='Digite a data',
                            error_format_text='Formato inválido',                         
                            on_change=selecionar_data,
                            on_dismiss=desselecionar_data,
                            date_picker_entry_mode=ft.DatePickerEntryMode.CALENDAR_ONLY
                            ))
                    ),

                    data := ft.Text(value='', color='black')     
                    
                    ]
                    ),
                
                ft.Container(
                    alignment=ft.alignment.center,
                    padding=ft.padding.only(top=30),
                    content=ft.FilledButton(
                        text='Criar tabela',
                        width=350,
                        on_click=validar_dados
                        
                    )
                ),
                
                ft.Container(
                    sem_dados := ft.Text(value='', color='red', size=15),
                    alignment=ft.alignment.center
                )
                

                        
            ]
        )

        
        page.add(texto_superior, caixa, caixa_2)

ft.app(target=main)