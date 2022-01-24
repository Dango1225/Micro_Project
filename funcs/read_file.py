def read_file(fpath):
    with open(fpath, 'r') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            yield(row)