from collections import defaultdict
from queue import Queue
from threading import Thread
from typing import List, Tuple, Dict, Union


# class Ref(int):
#     pass


class Param:
    def set(self, value):
        raise NotImplementedError()

    def get(self):
        raise NotImplementedError()

    def __call__(self, *args):
        if len(args) == 1:
            self.set(args[0])
        else:
            return self.get()


class Ref(Param):
    def __init__(self, interpreter, value):
        self._interpreter = interpreter
        self._value = value

    def set(self, value):
        self._interpreter[self._value] = value

    def get(self):
        return self._interpreter[self._value]

    def __repr__(self):
        return f"Ref({self._value})[{self()}]"


class Rel(Param):
    def __init__(self, interpreter: "Interpreter", value):
        self._interpreter = interpreter
        self._value = value

    def set(self, value):
        # FIXME maybe implement Param modes in the interpreter
        self._interpreter[self._value + self._interpreter._rbo] = value

    def get(self):
        return self._interpreter[self._value + self._interpreter._rbo]

    def __repr__(self):
        return f"Rel({self._value})[{self()}]"


class Var(Param):
    def __init__(self, value):
        self._value = value

    def set(self, value):
        raise Exception("Writing to a Var is permitted")

    def get(self):
        return self._value

    def __repr__(self):
        return f"Var[{self()}]"


class Interpreter:
    DEBUG = False

    def __init__(self, program: List[int]) -> None:
        super().__init__()
        self._memory: Dict[int, int] = defaultdict(
            int, {k: v for k, v in enumerate(program)}
        )
        self._ip = 0  # Instruction Counter
        self._rbo = 0  # Relative Base Offset
        self._finished = False
        self.stdout = Queue()
        self.stdin = Queue()

        self._log_prefix = ""

    @property
    def finished(self):
        return self._finished

    def log(self, *text):
        if self.DEBUG:
            print(self._log_prefix, *text)

    @staticmethod
    def from_file(file):
        with open(file) as f:
            program = [int(e) for e in f.read().split(",")]
        return Interpreter(program)

    def put(self, value):
        """Adds value to stdin"""
        self.stdin.put(value)

    def get(self):
        """Reads value from stdout, blocks if empty"""
        return self.stdout.get()

    def stream(self):
        while not self.finished:
            output_value = self.stdout.get()
            if output_value is not None:
                yield output_value

    def _read(self, amount, modes="") -> List[Ref]:
        modes = modes.zfill(amount)

        for mode in reversed(modes):
            cur = self._memory[self._ip]
            self._ip += 1

            if mode == "0":
                yield Ref(self, cur)
            elif mode == "1":
                yield Var(cur)
            elif mode == "2":
                yield Rel(self, cur)
            else:
                raise Exception("Unknown param mode")

    def __getitem__(self, key) -> Union[int, Tuple[int]]:
        """
        Returns value from memory. Can handle slices
        """

        if type(key) is slice:
            start = key.start
            stop = key.stop
            step = key.step

            if start is None:
                start = min(self._memory.keys())
            if stop is None:
                stop = max(self._memory.keys()) + 1
            if step is None:
                step = 1

            return tuple(self._memory[i] for i in range(start, stop, step))

        return self._memory[key]

    def __setitem__(self, key, value: int):
        self._memory[key] = value

    def start(self):
        thread = Thread(target=self.run, daemon=True)
        thread.start()
        return thread

    def run(self):
        try:
            while not self._finished:
                self.step()
        except Exception as e:
            print("Stopped execution:", str(e))

    def run_debug(self, log_prefix=""):
        self.DEBUG = True
        self._log_prefix = log_prefix

        self.log(f"  MEM| (IC: {self._ip}, RBO: {self._rbo})", self[:])
        while not self.finished:
            self.step()
            self.log(f"  MEM| (IC: {self._ip}, RBO: {self._rbo})", self[:])

    def step(self):
        op_code, *_ = self._read(1, modes="1")

        op = op_code() % 100
        modes = str(op_code())[:-2]

        if op == 1:  # Addition
            p1, p2, des = self._read(3, modes=modes)
            self.log(f"1 ADD| {des} = {p1} + {p2}")
            des(p1() + p2())

        elif op == 2:  # Multiply
            p1, p2, des = self._read(3, modes=modes)
            self.log(f"2 MUL| {des} = {p1} * {p2}")
            des(p1() * p2())

        elif op == 3:  # READ
            p1, *_ = self._read(1, modes=modes)
            value = self.stdin.get()
            self.log(f"3 RIN| {p1} = STDIN[{value}]")
            p1(value)

        elif op == 4:  # PRINT
            p1, *_ = self._read(1, modes=modes)
            self.log(f"4 PUT| STDOUT = {p1}")
            self.stdout.put(p1())

        elif op == 5:  # JUMP-IF-TRUE
            p1, p2, *_ = self._read(2, modes=modes)
            if p1() != 0:
                self.log(f"5 JIT| {p1} != 0 | IC = {p2}")
                self._ip = p2()
            else:
                self.log(f"5 JIT| {p1} != 0 | SKIP")

        elif op == 6:  # JUMP-IF-FALSE
            p1, p2, *_ = self._read(2, modes=modes)
            if p1() == 0:
                self.log(f"6 JIF| {p1} == 0 | IC = {p2}")
                self._ip = p2()
            else:
                self.log(f"6 JIF| {p1} == 0 | SKIP")

        elif op == 7:  # LESS-THEN
            p1, p2, p3, *_ = self._read(3, modes=modes)
            self.log(f"7 LET| {p3} = {p1} < {p2}")
            p3(int(p1() < p2()))

        elif op == 8:  # EQUAL
            p1, p2, p3, *_ = self._read(3, modes=modes)
            self.log(f"8 EQL| {p3} = {p1} == {p2}")
            p3(int(p1() == p2()))

        elif op == 9:  # SET RBO
            p1, *_ = self._read(1, modes=modes)
            self.log(f"9 RBO| RBO = {p1}")
            self._rbo += p1()

        elif op == 99:
            self.log("Stop program")
            self._finished = True
            self.stdout.put(None)
        else:
            self.log(f"ERR: Unknown OP Code {op}")
            raise Exception(f"Unknown OP code {op}")

    def dump(self) -> Dict[int, int]:
        return self._memory.copy()
