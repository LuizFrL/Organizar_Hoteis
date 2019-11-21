import pyodbc
from Organizar_Hoteis.HoteisMontreal import HoteisMontreal


def remove_repetidos(lista):
    l = []
    for i in lista:
        if i not in l:
            l.append(i)
    l.sort()
    return l


def findEntCod(hoteisPesquisa):
    hoteis_entCod = {}
    for hotel in hoteisPesquisa:
        print('pesquisando EntCod de', hotel)
        cursor.execute(f"""select * from Entidades where ent_nome = '{hotel}'""")
        resultado = cursor.fetchall()
        ent_codigo = []
        for linha in resultado:
            ent_codigo.append(int(linha[0]))

        if len(ent_codigo) == 1:
            ent_codigo = ent_codigo[0]
            cursor.execute(f"""	select ent_codigo,
                                hot_nivel_interesse,
                                hot_codigo
                        from   dbo.Hoteis
                    where ent_codigo in ({ent_codigo})
                    """)
        else:
            ent_codigo = tuple(ent_codigo)
            cursor.execute(f"""	select ent_codigo,
                        hot_nivel_interesse,
                        hot_codigo
                from   dbo.Hoteis
            where ent_codigo in {ent_codigo}
            """)

        del ent_codigo
        ent_codigo = []
        resultado = cursor.fetchall()
        for linha in resultado:
            ent_codigo.append(str(linha[0]))

        hoteis_entCod[hotel] = ent_codigo

    return hoteis_entCod


def returnNiv_Hot(hot):
    nivel = 4
    nivel_hotel = { }
    geral = []

    auxiliar = []

    for index, hote in enumerate(hot):
        if hot[index - 1] < hote:
            auxiliar.append(hote)
        else:
            geral.append(auxiliar)
            auxiliar = [hote]
    geral.append(auxiliar)

    nivel_1 = []

    for ni in geral:
        if not ni: continue
        nivel_hotel[nivel] = remove_repetidos(ni)
        if nivel == 1:
            nivel_1.extend(ni)
            nivel_hotel[nivel] = nivel_1
            continue
        nivel -= 1

    return nivel_hotel


def removeFinalComma(string):
    nova = string[::-1].replace(',', ' ', 1)
    return nova[::-1]


driver = '{SQL Server}'
server = '172.31.0.6'
database = 'montreal'
usuario = 'nfe'
pasword = 'nfe2019'
conexao = pyodbc.connect(f'DRIVER={driver};'
                         f'SERVER={server};'
                         f'DATABASE={database};'
                         f'UID={usuario};'
                         f'PWD={pasword}')

cursor = conexao.cursor()

informacoes = HoteisMontreal('https://www.clubemontreal.com.br/hoteis-cidade/5299-so-lus-MA/')

hoteis = informacoes.select_order_hotel()

hoteis_entCodigo = findEntCod(hoteis)

nivel_hotel = returnNiv_Hot(hoteis)

for nivel, lista_hoteis in nivel_hotel.items():
    string = ''
    for hotel in lista_hoteis:
        for entCod in hoteis_entCodigo[hotel]:
            string += f"{entCod}, "
        string += f"-- {hotel} \n"
    newString = removeFinalComma(string)

    print(f"""
UPDATE dbo.Hoteis
SET hot_nivel_interesse = {nivel}
WHERE ent_codigo in ({newString})""")
