# -*- coding: utf-8 -*-
import scrapy
import requests
import re
import time
from BeautifulSoup import BeautifulSoup
from ..items import LianjiaprojectItem

class LianJiaProject(scrapy.Spider):
    name = 'lianjiaspider'
    start_urls = ['http://sh.lianjia.com/zufang/']

    def start_request(self):
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 \ Safari/537.36 SE 2.X MetaSr 1.0'
        headers = { 'User-Agent': user_agent }
        yield scrapy.Request(url=self.start_urls, headers=headers, method='GET', callback=self.parse)

    def parse(self, response):
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 \ Safari/537.36 SE 2.X MetaSr 1.0'
        headers = { 'User-Agent': user_agent }
        bs = BeautifulSoup(response.body)
        area_list = bs.find('div', { 'id': 'filter-options' }).find('dl', { 'class': 'dl-lst clear' }).find('dd').find('div', { 'class': 'option-list gio_district' }).findAll('a')
        for area in area_list:
            try:
                area_han = area.string
                area_pin = area['href'].split('/')[2]
                if area_pin:
                    area_url = 'http://sh.lianjia.com/zufang/{}/'.format(area_pin)
                    yield scrapy.Request(
                        url=area_url,
                        headers=headers,
                        callback=self.detail_url,
                        meta={'id1': area_han, 'id2': area_pin}
                    )
            except Exception:
                pass

    def detail_url(self, response):
        for i in range(1, 101):
            url = 'http://sh.lianjia.com/zufang/{}/d{}'.format(response.meta['id2'], str(i))
            time.sleep(2)
            try:
                contents = requests.get(url)
                bs = BeautifulSoup(contents.content)
                houselist = bs.find('ul', { 'id': 'house-lst' }).findAll('li')
                for house in houselist:
                    try:
                        item = LianjiaprojectItem()
                        infoPanel = house.find('div', { 'class': 'info-panel' })
                        infoTitle = infoPanel.find('h2')
                        infoCols = infoPanel.findAll('div', { 'class': re.compile(r'^col-\d') })
                        item['title'] = infoTitle.find('a', { 'name': 'selectDetail' })['title']
                        item['community'] = infoCols[0].find('div', { 'class': 'where' }).find('a', { 'class': 'laisuzhou' }).find('span', { 'class': 'nameEllipsis' }).string
                        item['model'] = infoCols[0].find('div', { 'class': 'where' }).findAll('span')[0].string
                        item['area'] = infoCols[0].find('div', { 'class': 'where' }).findAll('span')[1].string.replace('&nbsp;', '')
                        item['watch_num'] = infoCols[2].find('div', { 'class': 'square' }).find('div').find('span', { 'class': 'num' }).string
                        item['time'] = infoCols[1].findAll('div', { 'class': 'price-pre' })[0].string[0:11]
                        item['price'] = infoCols[1].findAll('span', { 'class': 'num' })[0].string
                        item['link'] = infoTitle.find('a', { 'name': 'selectDetail' })['href']
                        item['city'] = response.meta["id1"]
                        url_detail = 'http://sh.lianjia.com{}'.format(item['link'])
                        mapDic = self.get_latitude(url_detail)
                        item['latitude'] = mapDic['latitude']
                        item['longitude'] = mapDic['longitude']
                        print('item %s' % item)
                    except Exception:
                        pass
                    yield item
            except Exception:
                pass

    def get_latitude(self, url):
        mapDic = {}
        content = requests.get(url)
        bs = BeautifulSoup(content.content)
        mapDom = bs.find('div', { 'id': 'zoneMap' })
        mapDic = {
            'latitude': mapDom['latitude'],
            'longitude': mapDom['longitude']
        }
        time.sleep(3)
        return mapDic
