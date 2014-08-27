import httplib2
import bs4
import pymysql

class DotaMax:

    """
    Get detail infomation of id
    @index: original url
    @self.url: index + id
    @login: login message for MySQL
    """

    index = "http://dotamax.com/player/detail/"
    hero_url = "http://dotamax.com/player/hero/"
    login = {'host': 'localhost',
             'user': 'root',
             'passwd': 'root',
             'db': 'dotamax',
             'charset': 'utf8'}
    h = httplib2.Http('.cache')
    my_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'}
    enc = 'utf-8'
    # url = "http://dotamax.com/player/detail/106777328/"
    # hero_url = "http://dotamax.com/player/hero/106777328/"

    def __init__(self, id):
        self.url = self.index + id
        self.hero_url = self.hero_url + id
        self.refresh()

    def changeID(self, id):
        self.url = self.index + id
        self.hero_url = self.hero_url + id
        self.refresh()

    def refresh(self):
        """
        refresh infomation
        """
        # try:
        #     # print(type(urlheader.AddHeader(self.url).request()))
        #     with urllib.request.urlopen(urlheader.AddHeader(self.url).request()) as conn:
        #         self.html = conn.read()
        #         self.enc = chardet.detect(self.html)['encoding']
        #         self.soup = bs4.BeautifulSoup(self.html,
        #                                       from_encoding=self.enc)
        try:
            response, html = self.h.request(self.url, headers=self.my_headers)
            if response.dict['status'] == '200':
                self.soup = bs4.BeautifulSoup(html,
                                              from_encoding=self.enc)
        except Exception as e:
            print(e)
            exit()

    def recentMatch(self):
        """
        get recentmatch infomation
        """
        foundClass = self.soup.find(text='最近比赛').parent.parent.find_all('tr')
        info = [looper.stripped_strings for looper in foundClass]
        return info

    def get_heros_information(self):
        """
        get hero infomation
        """
        try:
            response, html = self.h.request(self.url, headers=self.my_headers)
            if response.dict['status'] == '200':
                self.soup = bs4.BeautifulSoup(html,
                                              from_encoding=self.enc)
        except Exception as e:
            print(e)
            exit()

    def updateMySQL(self):
        """
        update database 'recentmatch' in MySQL
        """
        # try:
        #     conn = pymysql.connect(**self.login)
        #     info = self.recentMatch()
        #     for i in info:
        #         cursor = conn.cursor()
        #         ins = list(i)
        #         arg = (ins[0], ins[1] + ins[2], ins[4], ins[5], ins[6])
        #         cursor.callproc('updaterecentmatch', arg)
        #         cursor.close()
        # except Exception as e:
        #     print(e)
        # finally:
        #     conn.close()
        with pymysql.connect(**self.login) as cursor:
            info = self.recentMatch()
            for i in info[::-1]:
                ins = list(i)
                arg = (ins[0], ins[1] + ins[2], ins[4], ins[5], ins[6])
                cursor.callproc('updaterecentmatch', arg)
                while cursor.nextset() is not None:
                    pass
