import csv

with open('file_uploads/LLOAN.txt', 'r') as in_file:
    # stripped = (line.strip() for line in in_file)
    # lines = (line.split(".") for line in stripped if line)
    print(in_file.readlines())
    # with open('log.csv', 'w') as out_file:
    #     writer = csv.writer(out_file)
    #     writer.writerow(('title', 'intro'))
    #     writer.writerows(lines)