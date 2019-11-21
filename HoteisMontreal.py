from bs4 import BeautifulSoup as bs
import requests


class HoteisMontreal(object):
    def __init__(self, url):
        self.url_city = url
        self.hoteis_site_ordem = self.retornar_hoteis(url)

    @staticmethod
    def retornar_hoteis(url):
        content = requests.get(url=url).content
        resultado = bs(content, 'html.parser')
        hoteis = resultado.find_all('h4', {'class':'box-title'})
        hoteis_site = [ ]
        for hotel_desc in hoteis:
            hotel_nome = hotel_desc.find('a').text
            hoteis_site.append(hotel_nome)
        return hoteis_site

    def select_order_hotel(self):
        print('Exemplo de seleção: \nHoteis em ordem: 1 4 5 3')
        self.show_site_order()

        escolha = input('Hoteis em ordem: ').split(' ')
        hoteis_ordem_usuario = [self.hoteis_site_ordem[int(index) - 1] for index in escolha]

        for hotel in self.hoteis_site_ordem:
            if hotel not in hoteis_ordem_usuario:
                hoteis_ordem_usuario.append(hotel)

        self.show_user_order(hoteis_ordem_usuario)
        print()
        return hoteis_ordem_usuario

    def show_user_order(self, order):
        for index, hotel in enumerate(order):
            print(f'{index + 1}º', hotel)

    def show_site_order(self):
        for index, hotel in enumerate(self.hoteis_site_ordem):
            print(f'{index + 1}º', hotel)

    def update_url(self, url):
        self.__init__(url)

    def get_hoteis_site(self):
        return self.hoteis_site_ordem

