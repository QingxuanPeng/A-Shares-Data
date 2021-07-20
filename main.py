
from __future__ import (absolute_import, division, print_function,)

import argparse

import pandas as pd

from  datetime  import  *


from foo import *

def parse_args(pargs=None):
    '''to add command line arguments which can externally control:initialize and store data'''
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=(
            'Sample Skeleton'
        )
    )

    parser.add_argument('--config', default='./config.csv',
                        required=False, help='Configuration File')
    # every stock will be presented in a config CSV file as a line of a dataframe
    parser.add_argument('--data', default='./data',
                        required=False, help='Data dir')
    # every stock will be stored as a individual file in the data dictionary
    parser.add_argument('--init',action='store_true', default=False,
                        required=False, help='init')
    # at the beginning or at the time you want to initialize files, you need to call this argument
    # in the terminal.
    # in the next, the config file will be remade

    return parser.parse_args(pargs)

def run():

    args = parse_args()


    if args.init:
        # if need to remake the config file
        config = pd.DataFrame(columns=['股票代码', '股票名称', '开始日期', '结束日期', '增量更新', '更新时间'])
        lst = tushare_list()
        # the stock basis list (dataframe class) got from tushare api
        for index1, row1 in lst.iterrows():
            config = config.append({'股票代码':row1['ts_code'], '股票名称':row1['name']}, ignore_index=True)
            # add every stock codes and stock names into the config file
    else:
        # if only need to update the data of each stocks
        config = pd.read_csv(args.config)
        row_count = config.shape[0]
        for index, row in config.iterrows():
            print(f'{index + 1}/{row_count}----{row["股票代码"]}|{row["股票名称"]}')
            # know the update progress and which stock have been updated
            syn_stock(args.data,row)
            # get the stock data from tushare api
            config['更新时间'].iloc[index] = row["更新时间"]
            config['开始日期'].iloc[index] = row['开始日期']
            config['结束日期'].iloc[index] = row["结束日期"]
            config['增量更新'] = 'Y'
            # update the important timing of the update and let the next update be incremental updating


    config.to_csv(args.config,index=False)


if __name__ == '__main__':
    run()
