###########################################################################
#   Project_name:   keyargsprojects
#   File_name:      load_history
#   Creat_time:     2024/5/19   19:08
#   Author:         富视投资 
#   Description:
###########################################################################
import beehive

if __name__ == '__main__':
    print(beehive.load_history(symbols='600848'))

    # print(beehive.load_history(symbols='600848, 000520'))

    # print(beehive.load_history(path="E://keyargsprojects/beehive/datas/history/d/000520.csv"))

    # print(beehive.load_history(path="E://keyargsprojects/beehive/datas/history/d"))

    # print(beehive.load_history(symbols='600848,000520', path="E://keyargsprojects/beehive/datas/history/d"))

    # print(beehive.load_history())

    print(beehive.load_history(symbols='600848', fields='open, close'))