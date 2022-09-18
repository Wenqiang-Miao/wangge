"""

# 分析部分内容
# 主要的网格：
159938_yiyao
159920_hengsheng-etf
513180_hengshengkeji
512880_zhengquan
515180_hongli
512980_chuanmei
    
"""
import pandas as pd
import numpy as np
import os
import sys





def get_list_by_index(file_pth='./data/159938_yiyao.csv', index='买入价'):
    """
    按照index返回csv数据中的内容
    Args:
        file_pth (str, optional): _description_. Defaults to './data/159938_yiyao.csv'.
        index (str, optional): _description_. Defaults to '买入价'.

    Returns:
        _type_: _description_
    """
    raw_df = pd.read_csv(file_pth)
    # 完成对None值的替换，并将数据转换为float型
    raw_df = raw_df.replace("None", 0.0).astype(np.float64)

    #res_array = raw_df[index]
    if index in ['入股数', '出股数', '买入是否成交']:
        raw_df[index] = raw_df[index].astype(np.int32)
    res_array = list(raw_df[index])
    
    #print(list(res_array))
    return res_array




def get_everage_cost(file_pth='./data/159938_yiyao.csv'):
    """
    # 计算平均的持仓成本
    """
    avg_cost = 0
    buy_money_li = get_list_by_index(file_pth=file_pth, index='买入金额')  
    buy_amount_li = get_list_by_index(file_pth=file_pth, index='入股数') 
    # 判断买入是否成交的
    done_flg_li = get_list_by_index(file_pth=file_pth, index='买入是否成交') 
    
    # 确定成交数量，持仓成本只更新已成交部分
    done_num = 0
    for done_flg in done_flg_li:
        if done_flg == 0:
            break
        done_num += 1
    
    total_money = sum(buy_money_li[:done_num])
    total_amount = sum(buy_amount_li[:done_num])
    if total_amount != 0:
        avg_cost = total_money / total_amount    
    
    print('{}:总入股数{}, 买入总金额{}, 持仓成本{}'.format(
        os.path.basename(file_pth), total_amount, total_money, avg_cost) )
    
    return avg_cost



def batch_get_everage_cost(file_dir='./data/'):
    data_li=['159938_yiyao.csv',
             '159920_hengsheng-etf.csv', 
             '513180_hengshengkeji.csv',
             '512880_zhengquan.csv',
             '515180_100hongli.csv', 
             '519280_chuanmei.csv'
             ]
    for file_name in data_li:
        if file_name.endswith('.csv'):
            #print(file_name)
            get_everage_cost(os.path.join(file_dir, file_name))
        


def get_buy_price_info(file_pth='./data/159938_yiyao.csv'):
    """
    获取买入价格相关的信息,确定E的网格设置间隔
    """
    buy_price_li = get_list_by_index(file_pth=file_pth, index='买入价') 
    res_li = [[0]*len(buy_price_li) for _ in range(len(buy_price_li))]
    
    for i in range(len(buy_price_li)):
        for j in range(i, len(buy_price_li)):
            res_li[i][j] = 100 * (buy_price_li[i] - buy_price_li[j]) / buy_price_li[i]
    
    print("buy_price_li", buy_price_li, '\n')
    
    for i in range(len(buy_price_li)):
        print(res_li[i])
    
    return



def batch_get_buy_price_info(file_dir='./data/'):
    data_li=['159938_yiyao.csv',
             '159920_hengsheng-etf.csv', 
             '513180_hengshengkeji.csv',
             '512880_zhengquan.csv',
             '515180_100hongli.csv', 
             '519280_chuanmei.csv'
             ]
    for file_name in data_li:
        if file_name.endswith('.csv'):
            print('\n', file_name, end='\t')
            get_buy_price_info(os.path.join(file_dir, file_name))



def get_buy_amount_money_info(file_pth='./data/159938_yiyao.csv', index='入股数'):
    """
    获取买入数量相关的信息,确定E的网格设置间隔
    """
    buy_amount_li = get_list_by_index(file_pth=file_pth, index=index) 
    res_li = [[0]*len(buy_amount_li) for _ in range(len(buy_amount_li))]
    
    for i in range(len(buy_amount_li)):
        for j in range(i, len(buy_amount_li)):
            res_li[i][j] = 100 * (buy_amount_li[j] - buy_amount_li[i]) / buy_amount_li[i]
    
    print("buy_amount_li", buy_amount_li, '\n')
    
    for i in range(len(buy_amount_li)):
        print(res_li[i])
    
    return



def batch_get_buy_amount_money_info(file_dir='./data/', index='入股数'):
    data_li=['159938_yiyao.csv',
             '159920_hengsheng-etf.csv', 
             '513180_hengshengkeji.csv',
             '512880_zhengquan.csv',
             '515180_100hongli.csv', 
             '519280_chuanmei.csv'
             ]
    for file_name in data_li:
        if file_name.endswith('.csv'):
            print('\n', file_name, end='\t')
            get_buy_amount_money_info(os.path.join(file_dir, file_name), index=index)



if __name__ == '__main__':
    batch_get_buy_amount_money_info(index='买入金额')
    
    print('')

