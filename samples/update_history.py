###########################################################################
#   Project_name:   keyargsprojects
#   File_name:      update_history
#   Creat_time:     2024/5/19   19:34
#   Author:         富视投资 
#   Description:
###########################################################################
import beehive

if __name__ == '__main__':
    print(beehive.update_history(symbols='600848, 000520'))
    # print(beehive.update_history(symbols='600848, 000520', period='m'))
    # print(beehive.update_history(symbols='600848, 000520', start='20000101'))

    # print(beehive.update_history(symbols='600848, 000520', period='s',
    #                              start='20010101', end='20220222',
    #                              adjust='-1', path="E://temp"))

    # print(beehive.update_history())
