###########################################################################
#   Project_name:   keyargsprojects
#   File_name:      metahistory
#   Creat_time:     2024/5/19   13:26
#   Author:         富视投资 
#   Description:
###########################################################################

class MetaHistory(type):
    """历史数据采集类的元类"""

    def __new__(mcs, cls_name, cls_bases, cls_attrs):
        return super().__new__(mcs, cls_name, cls_bases, cls_attrs)

    def __init__(cls, cls_name, cls_bases, cls_attrs):
        super().__init__(cls_name, cls_bases, cls_attrs)


if __name__ == '__main__':
    print(__file__)
