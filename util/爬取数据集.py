# 导包
import requests
import re
import csv

# 头文件
headers = {
    'Cookie': 'qgqp_b_id=2c657cd95fc22dace96357800607b1f4; EMFUND1=null; EMFUND2=null; EMFUND3=null; EMFUND4=null; EMFUND5=null; EMFUND6=null; EMFUND7=null; EMFUND8=null; EMFUND0=null; EMFUND9=09-12 00:15:32@#$%u6613%u65B9%u8FBE%u56FD%u9632%u519B%u5DE5%u6DF7%u5408A@%23%24001475; st_si=63042243553465; st_asi=delete; st_pvi=96640246213057; st_sp=2023-09-11%2019%3A00%3A26; st_inirUrl=http%3A%2F%2Ffund.eastmoney.com%2F; st_sn=4; st_psi=20230912143854371-112200305283-1308502594',
    'Host': 'api.fund.eastmoney.com',
    'Referer': 'http://fundf10.eastmoney.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.76',
}

# 爬取往期基金的走势
def scrape_fund_data(code, csv_file):
    # 定义目标基金代码
    fund_code = code
    # 设置自定义请求头
    for page in range(0, 200):
        url = f'http://api.fund.eastmoney.com/f10/lsjz?callback=jQuery18303033013401332505_1694500743958&fundCode={fund_code}&pageIndex={page}&pageSize=20&startDate=&endDate=&_=1694500744040'

        response = requests.get(url=url, headers=headers)
        try:
            data = response.text

            datas = re.findall('{(.*?)}', data)[0:]

            selected_fields = ["FSRQ", "DWJZ", "LJJZ", "JZZZL"]

            with open(csv_file, 'a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=selected_fields)
                if file.tell() == 0:
                    writer.writeheader()
                for row in datas:
                    data_dict = {}
                    fields = row.split(',')

                    fsrq_found = False
                    for field in fields:
                        key_value = field.split(':')
                        key = key_value[0].strip(' "')
                        value = key_value[1].strip(' "')

                        if key in selected_fields:
                            data_dict[key] = value

                        if key == 'FSRQ':
                            fsrq_found = True

                    if fsrq_found:
                        writer.writerow(data_dict)
        except IndexError : pass

    print(f"数据已成功写入CSV文件：{csv_file}")

if __name__ == '__main__':
    # 再此处添加你想要爬取的基金代码
    code = ['161725', '001475', '590009', '007689', '001592']

    # 调用函数进行爬虫并写入CSV文件
    for row in code:
        print(f"正在处理:{row}的数据文件")
        fund_code = row
        csv_file = f'csv/{row}.csv'
        scrape_fund_data(fund_code, csv_file)