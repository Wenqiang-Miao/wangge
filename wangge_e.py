"""
# 根据E的网格计划更改    
"""
import os
import sys
import pandas as pd
import numpy as np
import math

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
    scale_ratio_li = [0.16, 0.17, 0.2, 0.17, 0.16, 0.2]
    
    assert len(data_li) == len(scale_ratio_li)
    for idx, data_file_name in enumerate(data_li):
         rescale_stratdgey(data_dir=data_dir, dst_dir=dst_dir, 
                           data_file_name=data_file_name, scale_ratio=scale_ratio_li[idx])
    





if __name__ == '__main__':
    
    get_my_stratdgey()
    
    
    print('')
