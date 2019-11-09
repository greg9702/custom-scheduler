#!/env/python

print('adas')

NUMBER_OF_NDOES = 3

result = {}

with open('output/usage.txt') as f:
    l = f.readlines()
    counter = 0
    date = ''
    for entry in l:
        entry = entry.rstrip('\n')
        if counter == 0:
            date = entry
            counter += 1
            continue

        record = date + ' ' + entry
        print (record)

        if entry.split(' ')[0] not in result:
            result[entry.split(' ')[0]] = []

        result[entry.split(' ')[0]].append(record)

        counter += 1
        if counter == NUMBER_OF_NDOES + 1:
            counter = 0

for record in result:
    filename = 'output/' + record
    with open(filename, 'w') as file:
        for el in result[record]:
            file.write(el)
            file.write('\n')

result = {}
# parse logger file
with open('/tmp/usage.log') as f:
    l = f.readlines()
    i = 0

    for entry in l:
        entry = entry.rstrip('\n')

        if i == 0:
            for i in range(4,len(entry.split(':'))):
                result[entry.split(':')[i]] = []
            i += 1
            continue

        date = entry[0:19]
        rest = entry.split(':')[4]
        node_name = rest.split(' ')[0]
        node_usage = rest.split(' ')[1] + 'Ki'
        result[node_name].append(date + ' ' + node_usage)

for record in result:
    filename = 'output/' + record + '_logger'
    with open(filename, 'w') as file:
        for el in result[record]:
            file.write(el)
            file.write('\n')
