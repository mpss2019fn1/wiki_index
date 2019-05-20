import csv


class InMemoryCsv:

    @staticmethod
    def load(input_file, delimiter=",", encapsulated_in=None, row_filter=None):
        with open(input_file, errors='replace') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=delimiter)
            instance = InMemoryCsv()
            instance.keys = [InMemoryCsv._remove_encapsulation(key, encapsulated_in) for key in next(csv_reader)]

            for line in csv_reader:
                row = {}
                for i in range(len(instance.keys)):
                    row[instance.keys[i]] = InMemoryCsv._remove_encapsulation(line[i], encapsulated_in)

                if row_filter and not row_filter(row):
                    continue
                instance._values.append(line)

            return instance

    @staticmethod
    def _remove_encapsulation(value, encapsulated_in="\""):
        if not encapsulated_in:
            return value

        length = len(encapsulated_in)
        return value[length: len(value) - length]

    def __init__(self):
        self.keys = []
        self._values = []

    def rows(self):
        for values in self._values:
            row = {}
            for i in range(len(self.keys)):
                row[self.keys[i]] = values[i]

            yield row
