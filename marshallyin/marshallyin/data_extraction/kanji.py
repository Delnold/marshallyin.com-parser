from scrapy import Selector


# Table with tr tags
def figure_wp_block_table_extractor_kanji(xpath_str: str, response: Selector) -> list:
    try:
        content_xpath = response.xpath(xpath_str)
        tr_arr = content_xpath.xpath(".//tr")
        tr_size = len(tr_arr[0].xpath(".//td").getall())
        result_arr = [[] for _ in range(tr_size)]
        for tr_tag in tr_arr:
            for index in range(0, tr_size):
                td_ind = tr_tag.xpath(".//td")[index]
                if td_ind.xpath(".//br"):
                    temp_arr = []
                    td_ind = list(filter(None, td_ind.get().split("<br>")))
                    for text in td_ind:
                        text = Selector(text=text)
                        parsed_text = text.xpath("string()").get().replace('\xa0', ' ')
                        if parsed_text != '':
                            temp_arr.append(parsed_text)
                    result_arr[index].append(temp_arr)
                elif td_ind.xpath(".//img/@src"):
                    result_arr[index].append(td_ind.xpath(".//img/@src").get())
                else:
                    result_arr[index].append(td_ind.xpath("string()").get())

        return result_arr
    except Exception as e:
        print("Error parsing `figure-wp-block` table: ", e)
        return ''


# Text in quotes
def div_w_b_quote_extractor_kanji(xpath_str: str, response: Selector) -> list:
    try:
        result_arr = []
        content_xpath = response.xpath(xpath_str)
        for content in content_xpath:
            temp_arr = []
            content_arr = list(filter(None, content.get().split("<br>")))
            for text in content_arr:
                text = Selector(text=text)
                parsed_text = text.xpath("string()").get().replace('\xa0', ' ')
                if parsed_text != '':
                    temp_arr.append(parsed_text)
            result_arr.append(temp_arr)
        return result_arr
    except Exception as e:
        print("Error parsing `quote`: ", e)
        return []


# Table with columns (without thead)
def figure_wp_block_table_extractor_row_variation_kanji(xpath_str: str, response: Selector) -> list:
    try:
        content_xpath = response.xpath(xpath_str)
        tr_arr = content_xpath.xpath(".//tr")
        result_arr = []
        for tr_tag in tr_arr:
            temp_arr = []
            td_ind = tr_tag.xpath(".//td")
            for td_attr in td_ind:
                text = td_attr.xpath("string()").get()
                temp_arr.append(text)
            result_arr.append(temp_arr)
        return result_arr
    except Exception as e:
        print("Error parsing `row` table: ", e)
        return []


# Single image in wp-block
def div_wp_block_image(xpath_str: str, response: Selector) -> str:
    try:
        content_xpath = response.xpath(xpath_str)
        if content_xpath.xpath(".//img/@src"):
            return content_xpath.xpath(".//img/@src").get()
        return ''
    except Exception as e:
        print("Error parsing image: ", e)
        return ''


# Standard table with thead and tbody
def table_press_extractor_kanji(xpath_str: str, response: Selector) -> list:
    try:
        content_xpath = response.xpath(xpath_str)
        thead_arr = content_xpath.xpath(".//thead/tr/th")
        tbody_arr = content_xpath.xpath(".//tbody/tr")

        # Creating an array of arrays where the first value has to be column name of the table
        result_arr = [[column_name.xpath("string()").get()] for column_name in thead_arr]

        for tr in tbody_arr:
            td_arr = tr.xpath(".//td")
            for index, td_xpath in enumerate(td_arr):
                result_arr[index].append(td_xpath.xpath("string()").get())
        return result_arr
    except Exception as e:
        print("Error parsing `press` table: ", e)
        return []
