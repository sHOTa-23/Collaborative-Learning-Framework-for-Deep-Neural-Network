def print_colored(color, text):
    from colored import fg
    clr = fg(color)
    print (clr + text)
    clr = fg('white')
    print(clr)

def assert_equals(expected, actual, error_text):
    if expected == actual:
        return True
    else:
        print_colored('orange_1', error_text)
        return False

def assert_higher(a, b, error_text):
    if a > b:
        return True
    else:
        print_colored('orange_1', error_text)
        return False

def assert_not_equals(exp, actual, error_text):
    if exp != actual:
        return True
    else:
        print_colored('orange_1', error_text)
        return False

def assert_true(expected, error_text):
    return assert_equals(expected, True, error_text)

def assert_false(expected, error_text):
    return assert_equals(expected, False, error_text)

def final_score(*methods):
    res = 0

    for method in methods:
        res += assert_true(method(), method.__name__ + " failed!!")
    
    if res == len(methods):
        print_colored('green_1', "------------------------ All test passed successfully!! ------------------------")
    else:
        print_colored('red_1', '------------------------ Only {}/{} tests have passed!! ------------------------'.format(res,len(methods)))
