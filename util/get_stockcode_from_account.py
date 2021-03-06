import pandas as pd
import os
import argparse

SEPERATOR = ' '
parser = argparse.ArgumentParser(description='Conditionally get Stockcode List')
parser.add_argument('--account_path', type=str, default='account.csv', metavar='n',
                    help='/workspace/jazzstock_bot/simulation/result/TA/account.csv')


args = parser.parse_args()



def get_stockcode_from_account(path_log_cond):
    '''
    account.csv 를 읽어서 가장 최근기준 amount가 0 이상인 종목을 리스트로 반환함
    '''

    COLUMNS = ['STOCKCODE', 'DATE', 'HOLDPURCHASED', 'HOLDAMOUNT', 'PROFIT', 'HISTPURCHASED', 'HISTSELLED', 'CLOSEDAY']
    COLUMNS_NUMERIC = COLUMNS[2:]


    stockcode_list = []
    for eachfile in os.listdir(path_log_cond):
        if '.csv' in eachfile:
            df = pd.read_csv(os.path.join(path_log_cond, eachfile), header=None, dtype=str)
            df.columns = COLUMNS
            for each in COLUMNS_NUMERIC:
                df[each] = df[each].astype('float')

            # 최근일자 조회
            df= df[df['DATE']==df['DATE'].max()]

            # amount가 0이 아닌애들만
            if df.HOLDAMOUNT.values[0]>0:
                stockcode_list.append(df.STOCKCODE.values[0])

    # print('DEBUG : %s'%(stockcode_list))
    return stockcode_list

if __name__ =='__main__':

    # COMMAND LINE 에서 실행시, RETURN 값을 출력해서
    # STDOUT parsing해서 값을 가져가기 위함
    stockcode_list=get_stockcode_from_account(args.account_path)
    rt = SEPERATOR.join(stockcode_list)
    print(rt)