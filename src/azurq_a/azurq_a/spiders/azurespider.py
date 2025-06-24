import scrapy


class AzureAnswersSpider(scrapy.Spider):
    name = "azure_answers"
    allowed_domains = ["learn.microsoft.com"]
    start_urls = [
        "https://learn.microsoft.com/en-us/answers/questions/?filterby=withacceptedanswer&page=1"
    ]

    def parse(self, response):
        # for question_box in response.css("div.box.margin-bottom-xxs"):
        #     title_tag = question_box.css("h2.title.is-6.margin-bottom-xxs a")
        #     # question_text = question_box.css("p.has-text-wrap::text").get()
        #     link = response.urljoin(title_tag.attrib["href"])
        #     # yield {
        #     #     "title": title_tag.css("::text").get(),
        #     #     "link": response.urljoin(title_tag.attrib["href"]),
        #     #     "question": question_text.strip() if question_text else None,
        #     # }
        #     yield response.follow(link, callback=self.parse_question)
        # Pagination
        nb_page = int(response.css("a.pagination-next::text").get())
       

        for x in range(0,nb_page):
            yield response.follow(f'https://learn.microsoft.com/en-us/answers/questions/?filterby=withacceptedanswer&page={x}', callback=self.parse_page)
        
       
    def parse_page(self, response):
        for question_box in response.css("div.box.margin-bottom-xxs"):
            title_tag = question_box.css("h2.title.is-6.margin-bottom-xxs a")
            # question_text = question_box.css("p.has-text-wrap::text").get()
            link = response.urljoin(title_tag.attrib["href"])
            # yield {
            #     "title": title_tag.css("::text").get(),
            #     "link": response.urljoin(title_tag.attrib["href"]),
            #     "question": question_text.strip() if question_text else None,
            # }

            yield response.follow(link, callback=self.parse_question)
        # print(response.url)

    def parse_question(self, response):
        question_title = response.css("h1.title.is-2::text").get()
        question_text = response.css("div.content.margin-top-xxs p::text").getall()
        accepted_answer = response.css("div.column.is-12 div.content ::text").getall()

        yield {
            "question": question_title,
            "question_text": question_text,
            "accepted_answer": accepted_answer if accepted_answer else "No accepted answer found"
        }



