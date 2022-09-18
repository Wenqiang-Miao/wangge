"""
# 根据E的网格计划更改    
"""
import os
import sys
import pandas as pd
import numpy as np
import math

from utils.ana_utils import get_list_by_index

class DefaultCongfig(object):
    """
    一些全局参数的保存
    Args:
        object (_type_): _description_
    """
    def __init__(self, ):
        # 初始金额
        self.inital_amount = 2000
        # 买入递增金额
        self.groth_ratio = 1.05
        # 文件列表
        self.data_li=['159920_hengsheng-etf.csv', 
                      '159938_yiyao.csv', 
                      '512880_zhengquan.csv', 
                      '513050_zhonggaihulian.csv', 
                      '513180_hengshengkeji.csv', 
                      '513520_rijing225.csv', 
                      '515180_100hongli.csv', 
                      '519280_chuanmei.csv']
        # 
        self.scale_ratoi_li = [0.2] * len(self.da_li)
    
    def set_inital_amount(self, amount):
        self.inital_amount = amount
        
    def set_groth_ratio(self, groth_ratio):
        self.groth_ratio = groth_ratio
        


def read_raw_data(data_pth='./data/159938_yiyao.csv'):
    """
    读取csv文件
    Args:
        data_pth (str, optional): _description_. Defaults to './data/159938_yiyao.csv'.
    """
    raw_df = pd.read_csv(data_pth)
    # 完成对None值的替换，并将数据转换为float型
    raw_df = raw_df.replace("None", 0.0).astype(np.float64)
    
    return raw_df




def rescale_stratdgey(data_dir='./data/', dst_dir='./dst_stratgey/', data_file_name='159938_yiyao.csv', scale_ratio=0.2):
    """
    将e的策略，根据比例缩放;原始数据格式：
    档位,买入触发价,买入价,买入金额,入股数,卖出触发价,卖出价,出股数,卖出金额,买入是否成交
    Args:
        data_dir (str, optional): _description_. Defaults to './data/'.
        data_names_li (list, optional): _description_. Defaults to ['159938_yiyao.csv'].
    """
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
        
    try:
        raw_data_pth = os.path.join(data_dir, data_file_name)
        if not os.path.isfile(raw_data_pth):  # 确保路径存在
            print('File {} does not exist! '.format(raw_data_pth))
            return
        raw_df = read_raw_data(raw_data_pth)   # 读取原始数据
        # 处理入股数，由于入股数是100的整数倍，先除以100，在乘以ratio，并向上取整，最后乘以100
        raw_df['入股数'] = np.ceil((raw_df['入股数'] // 100) * 0.25)*100
        raw_df['买入金额'] = raw_df['入股数'] * raw_df['买入价']
        
        
        raw_df['出股数'] = np.ceil((raw_df['出股数'] // 100) * 0.25)*100
        raw_df['卖出金额'] = raw_df['出股数'] * raw_df['卖出价']
        
        # 完成格式转换
        raw_df['入股数'] = raw_df['入股数'].astype(np.int32)
        raw_df['出股数'] = raw_df['出股数'].astype(np.int32)
        raw_df['买入是否成交'] = raw_df['买入是否成交'].astype(np.int32)
        raw_df = raw_df.replace(0, "None")
        raw_df['买入是否成交'] = raw_df['买入是否成交'].replace("None", 0)
        
        #print(raw_df)  
        
        raw_df.to_csv(os.path.join(dst_dir, data_file_name), index=None, float_format='%.3f')
        
    except Exception as e:
        print(e)
    
    return 
    
    

def get_my_stratdgey(data_dir='./data/', dst_dir='./dst_stratgey/'):
    """
    对rescale_stratdgey 方法的进一步封装
    Args:
        data_dir (str, optional): _description_. Defaults to './data/'.
        dst_dir (str, optional): _description_. Defaults to './dst_stratgey/'.
        data_names_li (list, optional): _description_. Defaults to ['159938_yiyao.csv'].
    """
    
    data_li=['159938_yiyao.csv',
             '159920_hengsheng-etf.csv', 
             '513180_hengshengkeji.csv',
             '512880_zhengquan.csv',
             '515180_100hongli.csv', 
             '519280_chuanmei.csv'
             ]
    #scale_ratio_li = [0.16, 0.17, 0.2, 0.17, 0.16, 0.2]
    scale_ratio_li = [0.08, 0.085, 0.1, 0.085, 0.08, 0.01]
    
    assert len(data_li) == len(scale_ratio_li)
    for idx, data_file_name in enumerate(data_li):
         rescale_stratdgey(data_dir=data_dir, dst_dir=dst_dir, 
                           data_file_name=data_file_name, scale_ratio=scale_ratio_li[idx])
    



def banlu_shangche(data_pth='./dst_stratgey/159938_yiyao.csv', cur_price=0.724, dst_dir='./banlu_shangche/'):
    """
    根据当前价格cur_price，确定半路上车的买入量；并根据价格，更新需要设置的卖出参数
    网格价格高于cur_price的，求策略中所有的买入量，然后以cur_price买入这么多，并按照相同的参数设置卖出
    Args:
        data_pth (str, optional): _description_. Defaults to './data/159938_yiyao.csv'.
        cur_price (float, optional): _description_. Defaults to 0.98.
    """
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    
    raw_df = read_raw_data(data_pth=data_pth)
    #print(raw_df)
    #print(raw_df['买入价'][0])
    
    buy_price_li = get_list_by_index(file_pth=data_pth, index='买入价') # 以列表方式返回对应值
    buy_amount_li = get_list_by_index(file_pth=data_pth, index='入股数') 
    # 判断买入是否成交的
    done_flg_li = get_list_by_index(file_pth=data_pth, index='买入是否成交') 
    
    # 确定成交数量，持仓成本只更新已成交部分
    done_num = 0
    for done_flg in done_flg_li:
        if done_flg == 0:
            break
        done_num += 1
    # 用于判断，哪个买入价格的索引是高于cur_price的
    shangche_head_ind = -1
    for idx in range(done_num):
        if buy_price_li[idx] > cur_price:
            shangche_head_ind = idx
    # 网格高于当前价格的部分，才是要半路上车的买入量
    shangche_amount = 0
    if shangche_head_ind > 0:
        shangche_amount = sum(buy_amount_li[:shangche_head_ind+1])
    
    total_money = shangche_amount * cur_price
    
    print('#'*20, os.path.basename(data_pth), '#'*20)
    res_str = '卖出触发价,卖出价,出股数,卖出金额\n'
    res_info_str = '{}, 当前价格{:.3f}, 共买入{:.0f}份, 总价{:.1f}元;'.format(os.path.basename(data_pth), cur_price, shangche_amount, total_money)
    print(res_info_str, '设置卖出：')
    for i in range(shangche_head_ind+1):
        
        print('\t卖出触发价{:*>6.3f},卖出价{:*>6.3f},出股数{:*>8.1f},卖出金额{:*>8.1f}'.format(raw_df['卖出触发价'][i], 
                        raw_df['卖出价'][i], raw_df['出股数'][i], raw_df['卖出金额'][i]))
        res_str += "{:.3f},{:.3f},{:d},{:.1f}\n".format(raw_df['卖出触发价'][i], 
                        raw_df['卖出价'][i], int(raw_df['出股数'][i]), raw_df['卖出金额'][i])
    #print('#'*8, os.path.basename(data_pth), '#'*8)
    
    with open(os.path.join(dst_dir, os.path.basename(data_pth)), 'w', encoding='utf-8') as f2_obj:
        f2_obj.write(res_str)
        
    return res_info_str, total_money
    
            
  
def batch_banlu_shangche(data_dir='./dst_stratgey/', dst_dir='./banlu_shangche/'): 
    """
    对半路上车的进一步封装
    Args:
        data_dir (str, optional): _description_. Defaults to './dst_stratgey/'.
    """
    data_li=['159938_yiyao.csv',
             '159920_hengsheng-etf.csv', 
             '513180_hengshengkeji.csv',
             '512880_zhengquan.csv',
             '515180_100hongli.csv', 
             '519280_chuanmei.csv'
             ]
    cur_price_li = [0.724, 1.071, 0.519, 0.869, 1.288, 0.565]
    
    assert len(data_li) == len(cur_price_li)
    
    res_info_str = ''
    total_money = 0
    for idx, data_file in enumerate(data_li):
        data_pth = os.path.join(data_dir, data_file)
        cur_info, cur_money = banlu_shangche(data_pth=data_pth, cur_price=cur_price_li[idx], dst_dir=dst_dir)
        res_info_str += cur_info + '\n'
        total_money += cur_money
    res_info_str = "总共{}个网格产品, 共买入{:.1f}元, 买入详情:\n".format(len(data_li), total_money) + res_info_str
    
    with open(os.path.join(dst_dir, 'buy_info.txt'), 'w', encoding='utf-8') as f2_obj:
        f2_obj.write(res_info_str)



if __name__ == '__main__':
    # 使用方法：
    # 1.先用get_my_stratdgey 获取自己的策略，记得按照自己的资金，更改scale_ratio_li 内容
    # 2.再调用batch_banlu_shangche，确定半路上车买入的情况，以及设置的卖出结果;记得按照交易日当天的结果，更新cur_price_li
    
    raw_data_dir = './data/'
    my_stratdgey_dir = './dst_stratgey/'
    shangche_dir = './banlu_shangche/'
    #get_my_stratdgey(data_dir=raw_data_dir, dst_dir=my_stratdgey_dir)
    #batch_banlu_shangche(data_dir=my_stratdgey_dir, dst_dir=shangche_dir)
    
    
    print('')
