import scrapy, re
from ..items import Formula1Item

class Formula1(scrapy.Spider):

    name = 'formula1'

    def start_requests(self):
        url = "https://www.formula1.com/en/results.html"
        yield scrapy.Request(url=url,callback=self.parse_links)

    def parse_links(self, response):

        year_links = response.css('div.resultsarchive-filter-container > '
                                  'div.resultsarchive-filter-wrap:nth-child(1) '
                                  'ul.resultsarchive-filter.ResultFilterScrollable > '
                                  'li.resultsarchive-filter-item a::attr(href)').extract()

        category_links = response.css('div.resultsarchive-filter-container > '
                                      'div.resultsarchive-filter-wrap:nth-child(2) '
                                      'ul.resultsarchive-filter.ResultFilterScrollable > '
                                      'li.resultsarchive-filter-item a::attr(href)').extract()

        location_links = response.css('div.resultsarchive-filter-container > '
                                      'div.resultsarchive-filter-wrap:nth-child(3) '
                                      'ul.resultsarchive-filter.ResultFilterScrollable > '
                                      'li.resultsarchive-filter-item a::attr(href)').extract()

        yield {'year_urls': year_links,
               'category_urls': category_links,
               'location_urls': location_links}


        items = Formula1Item()

        title_heading = response.css('h1.ResultsArchiveTitle::text').extract_first().strip()
        # items['title_heading'] = title_heading
        table_heading = response.css('thead th::text').extract()
        # items['table_heading'] = table_heading

        rows = response.css('tbody tr')
        for row in rows:
            grand_prix = row.css('td:not(.limiter)')[0].css('a::text').extract_first().strip()
            race_date = row.css('td:not(.limiter)')[1].css('td.dark.hide-for-mobile::text').extract_first().strip()
            winner = ' '.join(row.css('td:not(.limiter)')[2].css('span.hide-for-tablet::text,span.hide-for-mobile::text').extract())
            constructor = row.css('td:not(.limiter)')[3].css('td::text').extract_first().strip()
            no_of_laps = row.css('td:not(.limiter)')[4].css('td::text').extract_first().strip()
            time_taken = row.css('td:not(.limiter)')[5].css('td::text').extract_first().strip()

            items['grand_prix'] = grand_prix
            items['race_date'] = race_date
            items['winner'] = winner
            items['constructor'] = constructor
            items['no_of_laps'] = no_of_laps
            items['time_taken'] = time_taken

            yield items

        url = "https://www.formula1.com" + location_links[1]
        yield scrapy.Request(url=url,callback=self.parse_race_locations)

    def parse_race_locations(self,response):
        location = response.css('h1::text').extract_first()
        location = re.sub(r"\s",' ',location)
        date_circuit = response.css('p.date span::text').extract()
        date = ' - '.join(date_circuit[:-1])
        circuit = date_circuit[-1]
        heading = response.css('th:not(.limiter)').css('*::text').extract()
        rows = response.css('tbody tr')
        for row in rows:
            POS = row.xpath(".//td[@class='dark']/text()").extract()
            No = row.xpath(".//td[@class='dark hide-for-mobile']/text()").extract()
            Driver = ' '.join(row.xpath(".//span[@class='hide-for-tablet' or @class='hide-for-mobile']/text()").extract())
            Car = row.xpath(".//td[@class='semi-bold uppercase hide-for-tablet']/text()").extract()
            Laps = row.xpath(".//td[@class='bold hide-for-mobile']/text()").extract()

            print(POS,No,Driver,Car,Laps)
