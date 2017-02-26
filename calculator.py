import re

def add(x, y):
    answer = x + y
    return "<p>{x} + {y} = {answer}</p>".format(x=str(x), y=str(y), answer=str(answer))


def div(x, y):
    try:
        answer = x / y
    except ZeroDivisionError:
        raise ZeroDivisionError
    return "<p>{x} / {y} = {answer}</p>".format(x=str(x), y=str(y), answer=str(answer))


def home():
    return "<h1>WSGI Calculator</h1>"


def mult(x, y):
    answer = x * y
    return "<p>{x} * {y} = {answer}</p>".format(x=str(x), y=str(y), answer=str(answer))


def sub(x, y):
    answer = x - y
    return "<p>{x} - {y} = {answer}</p>".format(x=str(x), y=str(y), answer=str(answer))

def application(environ, start_response):
    headers = [("Content-type", "text/html")]
    try:
        path = environ.get('PATH_INFO', None)
        main_body = """
        <p>This is a calculator that takes input via the url.</p>
        <p>The first argument is the operation. Options: add, sub, mult, div</p>
        <p>The second and third arguments are the numbers.</p>
        <p>So http://localhost:8080/div/10/2 is 10 / 2 = 5</p>
        <p>Examples:</p>
        <ul>
        <li>Addition: http://localhost:8080/add/2/4</li>
        <li>Subtraction: http://localhost:8080/sub/6/92</li>
        <li>Multiplication: http://localhost:8080/mult/13/60</li>
        <li>Division: http://localhost:8080/div/23/60</li>
        </ul>
                """
        func, args = resolve_path(path)
        body = func(*args)
        body += main_body
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Invalid input</h1>"
    except ZeroDivisionError:
        status = "400 Bad Request"
        body = "<h1>You can't divide by zero.</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]


def resolve_path(path):
    url_list = path.split("/")
    func = url_list[1]
    str_nums = url_list[2:]
    print(url_list)
    try:
        nums = [float(x) for x in str_nums]
    except ValueError:
        raise ValueError("Sorry, that's not a valid path.")
    funcs = {
        "add": add,
        "sub": sub,
        "mult": mult,
        "div": div,
        "": home
    }
    if func in funcs:
        return funcs[func], nums
    else:
        raise NameError

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
