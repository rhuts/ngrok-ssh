from enum import Enum

class RH_STATUS(Enum):
    OK = 0
    FAIL = 1
    INVALID = 2
    NOT_IMPLEMENTED = 3

def log(pre_msg):
    """ Wrapper """
    def decorate(func):
        """ Decorator """
        def call(*args, **kwargs):
            """ Actual wrapping """
            print(pre_msg + ' in ' + func.__name__ + '() ...')

            status = func(*args, **kwargs)

            
            filler = ' with status: '
            if status != RH_STATUS.OK:
                state = '[ FAIL ]    '
                outcome = 'Failed'

            else:
                state = '[ OK ]    '
                outcome = 'Succeeded'

            print(state + outcome + filler + str(status.value) + ' (' + str(status.name) + ')\n')
            return status
        return call
    return decorate

def logTuple(pre_msg):
    """ Wrapper """
    def decorate(func):
        """ Decorator """
        def call(*args, **kwargs):
            """ Actual wrapping """
            print(pre_msg + ' in ' + func.__name__ + '() ...')

            status, tunnel_url = func(*args, **kwargs)

            
            filler = ' with status: '
            if status != RH_STATUS.OK:
                state = '[ FAIL ]    '
                outcome = 'Failed'

            else:
                state = '[ OK ]    '
                outcome = 'Succeeded'
                
            print(state + outcome + filler + str(status.value) + ' (' + str(status.name) + ')\n')
            return status, tunnel_url
        return call
    return decorate

def RH_LOG(status: RH_STATUS):
    if status != RH_STATUS.OK:
        print('[ FAIL ]    Failed with status: ' + str(status.value) + \
                ' (' + str(status) + ')')
    else:
        print('[ OK ]    Succeeded with status: ' + str(status.value) + \
                ' (' + str(status.name) + ')')
    return status

def RH_CHECK(status: RH_STATUS):
    if RH_LOG(status) != RH_STATUS.OK:
        exit(status)
    return status

def RH_RETURN_IF_FAIL(status: int):
    if status != 0:
        return(status)
