import functools
import logging

LOGGER = logging.getLogger('refactor_test')

def refactor_test(comp_func):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kws):
            comp_res = comp_func(*args, **kws)
            res = func(*args, **kws)
            if res != comp_res:
                message = "not equals for function:{} from {} with arguments:{}-{}".format(func.__name__, 
                    comp_func.__name__, args, kws)
                LOGGER.debug(message)
                print(message)
            return res
        return wrapper
    return decorator

def refactor_from(message):
    return message

@refactor_test(refactor_from)
def refactor_to0(message):
    return message

@refactor_test(refactor_from)
def refactor_to1(message):
    return "!" + message

if __name__ == '__main__':
    refactor_to0('Hello python!')
    refactor_to1('Hello python!')

