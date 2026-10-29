import random

words_list = [
    "python", "code", "server", "client", "socket", "packet", "stream", "buffer",
    "queue", "thread", "async", "loop", "data", "json", "string", "integer",
    "boolean", "object", "class", "method", "function", "variable", "import", "export",
    "module", "package", "framework", "library", "database", "query", "index", "key",
    "value", "network", "protocol", "port", "host", "connection", "request", "response",
    "error", "exception", "debug", "testing", "deploy", "system", "process", "memory",
    "storage", "security"
]


class Wordle:
    def __init__(self):
        self.word = words_list[random.randint(0, 49)]
        self.output = ["_"] * len(self.word)
        self.state = "in process"
    def check(self,guess):
        if len(guess) != len(self.word):
            return False
        if guess == self.word:
            self.state = "over"
            self.output = list(self.word)
            return True
        else:
            for i in range(len(self.word)):
                if guess[i] == self.word[i]:
                    self.output[i] = self.word[i]
        return False

    def current(self):
        return "".join(self.output)




