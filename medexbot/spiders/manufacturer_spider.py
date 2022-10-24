import re

import scrapy
from django.utils.text import slugify

from medexbot.items import ManufacturerItem


class ManufacturerSpider(scrapy.Spider):
    name = "manufacturer"
    allowed_domains = ['medex.com.bd']
    start_urls = ['https://medex.com.bd/companies?page=1']

    def parse(self, response, **kwargs):

        # manufacturer_name = response.css('div.data-row-top a ::text').extract()
        # "stat": company_info.xpath('//div[@class="data-row-top"]/following-sibling::node()[1]').get()
        # "stat": [int(s) for s in (company_info.css('div.col-xs-12 ::text').extract()[-1].strip()).split()
        # if s.isdigit()]
        for company_info in response.css('div.data-row'):
            item = ManufacturerItem()
            manufacturer_link = company_info.css('div.data-row-top a ::attr(href)').get()
            generic_counter, brand_name_counter = (int(s) for s in (
                company_info.css('div.col-xs-12 ::text').extract()[-1].strip()).split() if s.isdigit())

            item["manufacturer_id"] = re.findall("companies/(\d+)/", manufacturer_link)[0]
            item["manufacturer_name"] = company_info.css('div.data-row-top a ::text').get()
            item["generics_count"] = generic_counter
            item["brand_names_count"] = brand_name_counter
            item['slug'] = slugify(item['manufacturer_name'] + '-' + item['manufacturer_id'],
                                   allow_unicode=True)
            yield item

        pagination_links = response.css('a.page-link[rel="next"]  ::attr("href") ')
        yield from response.follow_all(pagination_links, self.parse)
