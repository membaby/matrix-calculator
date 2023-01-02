from math import *


class Bisection:
    def __init__(self):
        self.operation_name = 'Bisection'
        self.solution_steps = []

    @staticmethod
    def round_sig(sig, x):
        if x == 0:
            return 0
        return round(x, sig - int(floor(log10(abs(x)))) - 1)

    def bisection(self, eq, low, up, error, precision, max_iterations):
        estimate_roots = [low, up]
        code = str(eq)
        up = self.round_sig(precision, up)
        x = up
        up_eval = self.round_sig(precision, eval(code))
        low = self.round_sig(precision, low)
        x = low
        low_eval = self.round_sig(precision, eval(code))
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
        percent = 100
        x = self.round_sig(precision, (up + low) / 2)
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
            x = self.round_sig(precision, (up + low) / 2)
            estimate_roots.append(x)
            value = self.round_sig(precision, eval(code))
            if x:
                percent = abs(x - old) / x * 100
            elif old:
                percent = abs(x - old) / old * 100
            else:
                percent = 0
            text = f'Iteration #{i}\n> Lower Boundary = {low}, Upper Boundary = {up} | Root = {x}\n> Root value: f({x}) = {value}, (E) = {percent} %\n'
            self.solution_steps.append(text)
            self.solution_steps.append('')
            if value == 0: 
                break
            elif value < 0:
                low = x
            else:
                up = x
            i += 1
        return [x], self.solution_steps, estimate_roots


if __name__ == '__main__':
    test_class = Bisection()
    test = "exp(x)"

    s, ss, sss = test_class.bisection(test, 0, 0.11, 0.0001, 5, 100)
    for i in range(len(ss)):
        print(ss[i])
