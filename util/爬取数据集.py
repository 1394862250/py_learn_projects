import requests
import re
import csv

# 定义目标基金代码
fund_code = '161725'
# 设置自定义请求头
'''
在请求网页爬取的时候，在检查语句正确之后，结果输出错误，这就是后台服务器禁止爬取，需要通过反爬机制去解决这个问题。
headers是解决requests请求反爬的方法之一，相当于我们进去这个网页的服务器本身，假装自己本身在爬取数据。
对反爬虫网页，可以设置一些headers信息，模拟成浏览器取访问网站 。
'''
headers = {
     'Cookie':'qgqp_b_id=2c657cd95fc22dace96357800607b1f4; EMFUND1=null; EMFUND2=null; EMFUND3=null; EMFUND4=null; EMFUND5=null; EMFUND6=null; EMFUND7=null; EMFUND8=null; EMFUND0=null; EMFUND9=09-12 00:15:32@#$%u6613%u65B9%u8FBE%u56FD%u9632%u519B%u5DE5%u6DF7%u5408A@%23%24001475; st_si=63042243553465; st_asi=delete; st_pvi=96640246213057; st_sp=2023-09-11%2019%3A00%3A26; st_inirUrl=http%3A%2F%2Ffund.eastmoney.com%2F; st_sn=4; st_psi=20230912143854371-112200305283-1308502594',
     'Host':'api.fund.eastmoney.com',
     'Referer':'http://fundf10.eastmoney.com/',
     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.76',
}
    # 构造URL
for page in range(1, 103):
    url = f'http://api.fund.eastmoney.com/f10/lsjz?callback=jQuery18303033013401332505_1694500743958&fundCode=161725&pageIndex={page}&pageSize=20&startDate=&endDate=&_=1694500744040'

# 发起请求并获取响应
# print(requests.get(url=url))
    response = requests.get(url=url, headers=headers)
# print(response.text)

# 获取数据
    data= response.text

#3.解析数据 筛选数据
# 第一个是正则表达式语法，第二个就是需要在哪里匹配
#     print(data)
    print(re.findall('{(.*?)}',data)[-1])
    datas=re.findall('{(.*?)}',data)[0:]
    print()
    i  = 102-page
    print(i)

# 提取需要的字段
    selected_fields = ["FSRQ", "DWJZ", "LJJZ", "JZZZL"]

# CSV文件路径
    csv_file = '161725.csv'

# 将数据保存到CSV文件

    with open(csv_file, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=selected_fields)
        if file.tell() == 0:
            writer.writeheader()
        for row in datas:
            data_dict = {}
            fields = row.split(',')

            # Skip the row if FSRQ field is empty or missing
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

print(f"数据已成功写入CSV文件：{csv_file}")