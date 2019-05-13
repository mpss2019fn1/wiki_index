import csv


class InMemoryCsv:

    @staticmethod
    def load(input_file, delimiter=";", encapsulated_in="\"", row_filter=None):
        with open(input_file, errors='replace') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=delimiter, quotechar=encapsulated_in)
            instance = InMemoryCsv()
            instance.keys = next(csv_reader)

            for line in csv_reader:
                row = {}
                for i in range(len(instance.keys)):
                    row[instance.keys[i]] = line[i]

                if row_filter and not row_filter(row):
                    continue
                instance._values.append(line)

            return instance

    def __init__(self):
        self.keys = []
        self._values = []

    def rows(self):
        for values in self._values:
            row = {}
            for i in range(len(self.keys)):
                row[self.keys[i]] = values[i]

            yield row
