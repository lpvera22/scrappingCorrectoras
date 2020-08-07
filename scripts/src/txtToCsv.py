import csv
pathData='data/CEP-dados-2018-UTF8/'
with open(pathData+'ceps.txt', 'r') as in_file:
    stripped = (line.strip() for line in in_file)
    lines = (line.split(" ") for line in stripped if line)
    print(lines)
    with open(pathData+'ceps.csv', 'w') as out_file:
        writer = csv.writer(out_file)    
        writer.writerows(lines)