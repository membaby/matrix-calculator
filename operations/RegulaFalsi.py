import parser
from math import *


class RegulaFalsi:
    def __init__(self):
        self.operation_name = 'False Position'
        self.solution_steps = []

    @staticmethod
    def round_sig(sig, x):
        if x == 0:
            return 0
        return round(x, sig - int(floor(log10(abs(x)))) - 1)

    def regula_falsi(self, eq, low, up, error, precision, max_iterations):
        estimate_roots = [low, up]
        low = self.round_sig(precision, low)
        up = self.round_sig(precision, up)
        code = parser.expr(eq).compile()
        x = low
        low_eval = self.round_sig(precision, eval(code))
        x = up
        up_eval = self.round_sig(precision, eval(code))
        text = f'> Initial Boundaries: Lower: f({low}) = {low_eval}, Upper: f({up}) = {up_eval}\n'
        self.solution_steps.append(text)
        if not (low_eval and up_eval):
            return low if not low_eval else up, self.solution_steps, estimate_roots
        if low_eval*up_eval > 0:
            return "Can't determine the presence of a root", self.solution_steps, estimate_roots
        if low_eval > 0:
            swap = up
            up = low
            low = swap
            swap = up_eval
            up_eval = low_eval
            low_eval = swap
        percent = 100
        x = self.round_sig(precision, self.round_sig(precision, self.round_sig(precision, low * up_eval) - self.round_sig(precision, up * low_eval)) / self.round_sig(precision, up_eval - low_eval))
        estimate_roots.append(x)
        value = self.round_sig(precision, eval(code))
        text = f'Iteration #1\n> Root = {x}\n> Root value: f({x}) = {value}, (E) = {percent} %\n'
        self.solution_steps.append(text)
        if value == 0:
            return x, self.solution_steps, estimate_roots
        elif value < 0:
            low = x
        else:
            up = x
        i = 2
        while percent > error and i <= max_iterations:
            old = x
            x = self.round_sig(precision, self.round_sig(precision, self.round_sig(precision, low * up_eval) - self.round_sig(precision, up * low_eval)) / self.round_sig(precision, up_eval - low_eval))
            estimate_roots.append(x)
            if x:
                percent = abs(x - old) / x * 100
            elif old:
                percent = abs(x - old) / old * 100
            else:
                percent = 0
            value = self.round_sig(precision, eval(code))
            text = f'Iteration #{i}\n> Lower Boundary = {low}, Upper Boundary = {up} | Root = {x}\n> Root value: f({x}) = {value}, (E) = {percent} %\n'
            self.solution_steps.append(text)
            if value == 0:
                break
            elif value < 0:
                low = x
            else:
                up = x
            i += 1
        return x, self.solution_steps, estimate_roots


if __name__ == '__main__':
    test_class = RegulaFalsi()
    test = "x**2*(x-0.165)+3.993*10**-4"

    s, ss = test_class.regula_falsi(test, 0, 0.11, 0.0001, 5, 100)
    print(s)
    for i in range(len(ss)):
        print(ss[i])
