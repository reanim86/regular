import time

def logger(path):

    def __logger(old_function):

        def new_function(*args, **kwargs):
            start_time = time.ctime(time.time())
            result = old_function(*args, **kwargs)
            name = old_function.__name__
            arg = f'{args}{kwargs} '
            res = f'{result} '
            log = [f'{start_time} ', f'{name} ', arg, res, '\n']
            with open(path, 'a+', encoding='utf-8') as f:
                f.writelines(log)
            return result

        return new_function

    return __logger