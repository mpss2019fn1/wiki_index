class InMemoryCsv:

    @staticmethod
    def load(input_file, delimiter=";", encapsulated_in="\"", new_line="\n", row_filter=None):
        with open(input_file, "r", errors='ignore') as csv:
            instance = InMemoryCsv()
            instance.keys = InMemoryCsv._split_csv_line(next(csv), delimiter, encapsulated_in, new_line)

            for line in csv:
                values = InMemoryCsv._split_csv_line(line, delimiter, encapsulated_in, new_line)
                row = {}
                for i in range(len(instance.keys)):
                    row[instance.keys[i]] = values[i]

                if row_filter and not row_filter(row):
                    continue
                instance._values.append(values)

    @staticmethod
    def _split_csv_line(line, delimiter, encapsulated_in, new_line):
        return line.replace(encapsulated_in, "").replace(new_line, "").split(delimiter)

    def __init__(self):
        self.keys = []
        self._values = []

    def rows(self):
        for values in self._values:
            row = {}
            for i in range(len(self.keys)):
                row[self.keys[i]] = values[i]

            yield row
