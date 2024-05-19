###########################################################################
#   Project_name:   keyargsprojects
#   File_name:      get_history
#   Creat_time:     2024/5/19   15:19
#   Author:         富视投资 
#   Description:
###########################################################################
import beehive

if __name__ == '__main__':
    # his = beehive.get_history(symbols='600478,000520', path="E://keyargsprojects/beehive/datas/history")
    # his = beehive.get_history(symbols='600478,000520')
    # his = beehive.get_history(symbols='600478')
    # his = beehive.get_history(symbols=['000520'])
    # his = beehive.get_history(symbols='600478,000520', start='20100101', end='20200303', period='y')
    # his = beehive.get_history(period='d')
    # his = beehive.get_history(symbols='600478,000520', fields='open, close')
    his = beehive.get_history(symbols='600478,000520')






    print(his)

