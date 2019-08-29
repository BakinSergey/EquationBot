import webbrowser, random
from contextlib import contextmanager
from .equation_solver import Solve_Square_Eq, getEQ
import sys, os

# Если латех не генерит пдф, нужно включить отладку чтобы смотреть ошибки.
debug = False

# webbrowser.open_new(Solve_Square_Eq(*getEQ(), debug_mode=debug))

@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout



# решим 50 квадратных уравнений с целыми коэффициентами в интервале (-1000, 1000)
cnt = 0
solved = []
a, b, c = 0, 0, 0

while cnt < 5:
    a, b, c = tuple(map(lambda x: random.randint(-1000, 1000), [a, b, c]))

    key = '{}x2{:+}x{:+}=0'.format(a, b, c)

    if key in solved:
        continue
    else:
        solved.append(key)
        link = Solve_Square_Eq(a, b, c, debug_mode=debug)
        cnt += 1
        # with suppress_stdout():
        #     print('{} is {}x2{:+}x{:+}=0 solution: {}'.format(cnt, a, b, c, link))


#print(solved)
