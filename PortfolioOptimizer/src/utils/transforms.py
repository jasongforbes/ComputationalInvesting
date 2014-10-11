'''
Created on Oct 11, 2014

@author: Jason
'''


def wrap(src,classinfo):
    '''
    wrap
    wraps the src object in type classinfo:
        classinfo must implement the append function
    '''
    if not isinstance(src, classinfo):
        returnval = classinfo()
        returnval.append(src.copy())
        return returnval
    else:
        return src