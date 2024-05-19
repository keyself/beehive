###########################################################################
#   Project_name:   keyargsprojects
#   File_name:      history_update
#   Creat_time:     2024/5/19   11:55
#   Author:         富视投资 
#   Description:
###########################################################################
from beehive.history import EastHistory


def update_history(*args, **kwargs):
    """
    update已在get_history判断过，这里已失效
    """
    # 实例化指定的spider
    spider_class = kwargs.get('spider')
    if spider_class:
        spider = spider_class(*args, **kwargs)
    else:
        spider = EastHistory(*args, **kwargs)
    # 爬取
    history_dict = spider.update()

    return history_dict

