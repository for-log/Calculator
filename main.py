import time

NUMBERS = "1234567890"


class Tree:
    def __init__(self, left, oper, right):
        self.left = left
        self.oper = oper
        self.right = right

    def exec(self):
        if self.oper.tp == Token.PLUS:
            return self.left.add(self.right)
        if self.oper.tp == Token.MINUS:
            return self.left.minus(self.right)
        if self.oper.tp == Token.MULTI:
            return self.left.multi(self.right)
        if self.oper.tp == Token.DIVIDE:
            return self.left.divide(self.right)
        if self.oper.tp == Token.POWER:
            return self.left.power(self.right)
        return 0

    def __repr__(self):
        return f"Operation({self.left}, {self.oper}, {self.right})"


class Token:
    FLOAT = 0
    INTEGER = 1
    PLUS = "+"
    MINUS = "-"
    MULTI = "*"
    DIVIDE = "/"
    POWER = "^"
    OPEN = "("
    CLOSE = ")"

    def __init__(self, tp, value):
        self.tp = tp
        self.value = value

    def add(self, other):
        result = other.value + self.value
        return Token(self.FLOAT if type(result) == float else self.INTEGER, result)

    def minus(self, other):
        result = self.value - other.value
        return Token(self.FLOAT if type(result) == float else self.INTEGER, result)

    def multi(self, other):
        result = other.value * self.value
        return Token(self.FLOAT if type(result) == float else self.INTEGER, result)

    def divide(self, other):
        result = self.value / other.value
        return Token(self.FLOAT, result)

    def power(self, other):
        result = self.value ** other.value
        return Token(self.FLOAT if type(result) == float else self.INTEGER, result)

    @staticmethod
    def get_plus():
        return Token(Token.PLUS, Token.PLUS)

    @staticmethod
    def get_minus():
        return Token(Token.CLOSE, Token.CLOSE)

    @staticmethod
    def get_multi():
        return Token(Token.MULTI, Token.MULTI)

    @staticmethod
    def get_divide():
        return Token(Token.DIVIDE, Token.DIVIDE)

    @staticmethod
    def get_power():
        return Token(Token.POWER, Token.POWER)

    @staticmethod
    def get_open():
        return Token(Token.OPEN, Token.OPEN)

    @staticmethod
    def get_close():
        return Token(Token.CLOSE, Token.CLOSE)

    def __eq__(self, other):
        return other.tp == self.tp and other.value == self.value

    def __repr__(self):
        return f"Token({self.tp}, {self.value})" if self.tp != self.value else f"Token({self.value})"


class Lexer:
    def __init__(self, req):
        self.req = req
        self.index = 0
        self.char = req[0]

    def next(self):
        if self.index >= len(self.req) - 1:
            self.char = None
        else:
            self.index += 1
            self.char = self.req[self.index]

    def parse(self):
        result = []
        while self.char is not None:
            if self.char == " ":
                self.next()
                continue
            if self.char in NUMBERS:
                v = Token(*self.parse_num())
                result.append(v)
                continue
            elif self.char in Token.PLUS:
                v = Token.get_plus()
            elif self.char in Token.MINUS and result[-1].tp in (Token.FLOAT, Token.INTEGER):
                v = Token.get_minus()
            elif self.char in Token.MINUS:
                v = Token(*self.parse_num())
                result.append(v)
                continue
            elif self.char in Token.MULTI:
                v = Token.get_multi()
            elif self.char in Token.DIVIDE:
                v = Token.get_divide()
            elif self.char in Token.POWER:
                v = Token.get_power()
            elif self.char in Token.OPEN:
                v = Token.get_open()
            elif self.char in Token.CLOSE:
                v = Token.get_close()
            else:
                raise Exception("Unexcepted token!")
            result.append(v)
            self.next()
        return result

    def parse_num(self):
        result = ""
        dot_counter = 0
        minus_counter = 0
        while self.char is not None and self.char in NUMBERS + ".-":
            if self.char == ".":
                dot_counter += 1
                if dot_counter > 1:
                    break
            if self.char == "-":
                minus_counter += 1
                if minus_counter > 1:
                    break
            result += self.char
            self.next()
        return Token.FLOAT if dot_counter > 0 else Token.INTEGER, float(result) if dot_counter > 0 else int(result)


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0
        self.token = self.tokens[self.index]

    def next(self):
        self.index += 1
        self.token = None if self.index > len(self.tokens) - 1 else self.tokens[self.index]

    def parse(self):
        return self.second()

    def factor(self):
        left = self.token
        if left.tp in (Token.INTEGER, Token.FLOAT):
            self.next()
            return left
        if left.tp == Token.OPEN:
            self.next()
            s = self.second()
            if self.token.tp == Token.CLOSE:
                self.next()
                return s

    def zeros(self):
        return self.create_operation([Token.POWER], self.factor)

    def first(self):
        return self.create_operation([Token.MULTI, Token.DIVIDE], self.zeros)

    def second(self):
        return self.create_operation([Token.PLUS, Token.MINUS], self.first)

    def create_operation(self, opers, func):
        left = func()
        while self.token is not None and self.token.tp in opers:
            oper = self.token
            self.next()
            right = func()
            left = Tree(left, oper, right)
        return left


def run(operations):
    left = operations.left
    oper = operations.oper
    right = operations.right
    if type(right) == Tree:
        right = run(right)
    if type(left) == Tree:
        left = run(left)
    return Tree(left, oper, right).exec()


def main():
    while 1:
        p = Lexer(input("Your example: "))
        start = time.time()
        r_l = p.parse()
        e = Parser(r_l)
        r_p = e.parse()
        i = run(r_p)
        print(i.value, time.time() - start)


if __name__ == "__main__":
    main()
