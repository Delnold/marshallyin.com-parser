from typing import Tuple, List, Any

from scrapy import Selector


def figure_wp_block_table_explanation_extractor_alphabet(xpath_str: str, response: Selector) -> Tuple[
    List[Any], List[Any], List[Any], List[Any]]:
    tips_text = []
    tips_image = []
    stroke_orders = []
    how_to_write = []
    table_arr = response.xpath(xpath_str)
    for table in table_arr:
        tip_text = table.xpath(".//tr[1]/td[2]")
        temp_arr = []
        td_ind = list(filter(None, tip_text.get().split("<br>")))
        for text in td_ind:
            text = Selector(text=text)
            parsed_text = text.xpath("string()").get().replace('\xa0', ' ')
            if parsed_text != '':
                temp_arr.append(parsed_text)
        tip_image = table.xpath(".//tr[1]/td[2]/img/@src").get()
        stroke_order = table.xpath(".//tr[2]/td[2]/img/@src").get()
        writing = table.xpath(".//tr[3]/td[2]/img/@src").get()

        tips_text.append(temp_arr)
        tips_image.append(tip_image)
        stroke_orders.append(stroke_order)
        how_to_write.append(writing)
    return tips_text, tips_image, \
        stroke_orders, how_to_write


def figure_wp_block_table_extractor_row_variation_alphabet(xpath_str: str, response: Selector) -> list:
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


def table_press_extractor_alphabet(xpath_str: str, response: Selector) -> list:
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