# -*- coding:utf-8 -*-
import scrapy
from scrapy import Request
import json


class XiciSpider(scrapy.Spider):
    name = 'xici_proxy'
    allowed_domains = ["www.xicidaili.com"]

    def start_requests(self):
        for i in range(1, 4):
            yield Request('http://www.xicidaili.com/nn/%s' % i)

    def parse(self, response):
        
        for sel in response.xpath('//table[@id="ip_list"]/tobdy/tr[position()>1]'):
            #提取代理的IP、port、scheme(http or https //*[@id="ip_list"]/tbody/tr[2]
            print set
            ip = sel.css('td:nth-child(2)::text').extract_first()
            port = sel.css('td:nth-child(3)::text').extract_first()
            scheme = sel.css('td:nth-child(6)::text').extract_first()
            # 使用爬取到的代理再次发送请求到http(s)://httpbin.org/ip, 验证代理是否可用
            print ip
            print port
            print scheme
            url = '%s://httpbin.org/ip' % scheme
            proxy = '%s://%s:%s' % (scheme, ip, port)

            meta = {
                'proxy': proxy,
                'dont_retry': True,
                'download_timeout': 10,

                # 以下两个字段是传递给check_available方法的信息，方便检测
                '_proxy_scheme': scheme,
                '_proxy_ip': ip,
            }

            #yield Request(url, callback=self.check_available, meta=meta, dont_filter=True)
        pass

    def check_available(self, response):
        proxy_ip = response.meta['_proxy_ip']

        # 判断代理是否具有隐藏IP功能
        # if proxy_ip == json.loads(response.text)['origin']:
        #     yield {
        #         'proxy_scheme': response.meta['_proxy_scheme'],
        #         'proxy': response.meta['proxy'],
        #     }
