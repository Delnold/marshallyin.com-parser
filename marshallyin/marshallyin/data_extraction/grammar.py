from scrapy import Selector


def data_extractor_grammar(response: Selector, xpath_figure_wp_block_str: str = None,
                   xpath_div_w_b_quote_str: str = None) -> list:

    if xpath_figure_wp_block_str and response.xpath(xpath_figure_wp_block_str):
        return figure_wp_block_table_extractor_grammar(xpath_figure_wp_block_str, response)

    if xpath_div_w_b_quote_str and response.xpath(xpath_div_w_b_quote_str):
        return div_w_b_quote_extractor_grammar(xpath_div_w_b_quote_str, response)



def figure_wp_block_table_extractor_grammar(xpath_str: str, response: Selector) -> list:
    result_arr = []
    content_xpath = response.xpath(xpath_str)
    for content in content_xpath:
        temp_arr = []
        td_arr = content.xpath(".//td")
        for td_tag in td_arr:
            content_arr = list(filter(None, td_tag.get().split("<br>")))
            for text in content_arr:
                text = Selector(text=text)
                parsed_text = text.xpath("string()").get().replace('\xa0', ' ')
                if parsed_text != '':
                    temp_arr.append(parsed_text)
            result_arr.append(temp_arr)
    return result_arr


def div_w_b_quote_extractor_grammar(xpath_str: str, response: Selector) -> list:
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
