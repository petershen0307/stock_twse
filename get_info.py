from bs4 import BeautifulSoup
import requests
import save_data


# log http://stackoverflow.com/questions/21069283/beautifulsoup-get-all-the-values-of-a-particular-column
# 從臺灣證交所TWSE取得上市公司每日的成交
def get_daily_info(start_year, start_month, stock_id):
    url = 'http://www.twse.com.tw/ch/trading/exchange/STOCK_DAY/genpage/Report201606/201606_F3_1_8_1234.php?STK_NO={}&myear={}&mmon={}'.format(
        stock_id, start_year, start_month)
    r = requests.get(url=url)
    return parse_stock_daily_info_row_first(r.content)


# 表格標頭: 日期 成交股數 成交金額 開盤價 最高價 最低價 收盤價 漲跌價差 成交筆數
# 只取 [日期, 成交股數, 收盤價] 這三種資訊
# return{'日期': [], '成交股數': [], '收盤價': []}
def parse_stock_daily_info_column_first(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    trade_table = soup.find('table', attrs={'class': 'board_trad'})
    # index 0, 1, 6
    columns = [td.find('div').string for td in trade_table.find('tr', attrs={'bgcolor': '#EBDCC9'}).find_all('td')]
    target_info = {'日期': [], '成交股數': [], '收盤價': []}
    # dict: for key in xxx_dict 取得的是key不是value
    # 如果要取得key與value, 要用dict.items(), 他會回傳一個tuple(key, value): for key, value in xxx_dict.items()
    for key in target_info:
        column_index = columns.index(key)
        if '日期' == key:
            target_info[key] = [td[column_index].find('div').string for td in
                                [tr.find_all('td') for tr in trade_table.find_all('tr', attrs={'bgcolor': '#FFFFFF'})]]
        else:
            target_info[key] = [td[column_index].string for td in
                                [tr.find_all('td') for tr in trade_table.find_all('tr', attrs={'bgcolor': '#FFFFFF'})]]
    # print(target_info)
    return target_info


# 表格標頭: 日期 成交股數 成交金額 開盤價 最高價 最低價 收盤價 漲跌價差 成交筆數
# 只取 [日期, 成交股數, 收盤價] 這三種資訊
# return[{'日期': str, '成交股數': str('123,123'), '收盤價': str('123.123')}]*n
def parse_stock_daily_info_row_first(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    trade_table = soup.find('table', attrs={'class': 'board_trad'})
    # index 0, 1, 6
    columns = [td.find('div').string for td in trade_table.find('tr', attrs={'bgcolor': '#EBDCC9'}).find_all('td')]
    using_info_index = ['日期', '成交股數', '收盤價']
    table_result = []  # input dict
    for tr in trade_table.find_all('tr', attrs={'bgcolor': '#FFFFFF'}):
        tr_result = {}
        td = tr.find_all('td')
        for key in using_info_index:
            col_index = columns.index(key)
            if td[col_index].string is None:
                tag_string = td[col_index].find('div').string
                # print(td[col_index].find('div').string)
            else:
                tag_string = td[col_index].string
                # print(td[col_index].string)
            tr_result[key] = tag_string
        table_result.append(tr_result)
    # print(table_result)
    return table_result


# 測試的程式碼, 感覺要從下面這個網址然後轉跳到正確的網址,但是目前還不知道怎麼做
# POST  to http://www.twse.com.tw/ch/trading/exchange/STOCK_DAY/STOCK_DAYMAIN.php
# myear=2016
# mmon=06
# STK_NO=1234
# login_btn
# GET window.location.replace("genpage/Report201606/201606_F3_1_8_1234.php?STK_NO=1234&myear=2016&mmon=06");
# r = requests.post('http://www.twse.com.tw/ch/trading/exchange/STOCK_DAY/STOCK_DAYMAIN.php',
#                   data={'myear': start_year, 'mmon': start_month, 'STK_NO': stock_id, 'login_btn': '%ACd%B8%DF'})
# print(r.status_code)
# print(r.headers)
# print(r.request.headers)
# print(r.content.decode('big5'))
# with open('got_html.html', mode='wb') as f:
#     f.write(r.content)

if '__main__' == __name__:
    info = get_daily_info(2016, 6, 1234)
    save_data.insert_daily_info(1234, info)
