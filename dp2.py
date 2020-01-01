import csv

sort_items = list()  #list to hold the sorted item
animal_dict = {'cat': '1000', 'dog': '0100', 'turtle': '0010', 'bird': '0001'}  #list for animals 
age_dict = {             #list for age 
	'0': '1000000000',
	'1': '0100000000', 
	'2': '0010000000', 
	'3': '0001000000', 
	'4': '0000100000', 
	'5': '0000010000', 
	'6': '0000001000', 
	'7': '0000000100', 
	'8': '0000000010', 
	'9': '0000000001'
	} 

def to_binary(row):
	animal = row[0]
	if int(row[1]) >= 1 and int(row[1]) <= 10:
		age = '0'
	elif int(row[1]) >= 11 and int(row[1]) <= 20:
		age = '1'
	elif int(row[1]) >= 21 and int(row[1]) <= 30:
		age = '2'
	elif int(row[1]) >= 31 and int(row[1]) <= 40:
		age = '3'
	elif int(row[1]) >= 41 and int(row[1]) <= 50:
		age = '4'
	elif int(row[1]) >= 51 and int(row[1]) <= 60:
		age = '5'
	elif int(row[1]) >= 61 and int(row[1]) <= 70:
		age = '6'
	elif int(row[1]) >= 71 and int(row[1]) <= 80:
		age = '7'
	elif int(row[1]) >= 81 and int(row[1]) <= 90:
		age = '8'
	elif int(row[1]) >= 91 and int(row[1]) <= 100:
		age = '9'

	if row[2] == 'True':
		adopted = '10'
	else:
		adopted = '01'

	return "{0}{1}{2}".format(animal_dict[animal], age_dict[age], adopted)

f = open("write.txt", "w")   #open the
with open('animals.txt', newline='') as csvfile:
	reader = csv.reader(csvfile)
	for row in reader:
		animal = row[0]
		if int(row[1]) > 0 and int(row[1]) <= 10:
			age = '1'
		else:
			age = str(int((int(row[1]) -1) / 10))
		if row[2] == 'True':
			adopted = '10'
		else:
			adopted = '01'

		bina = to_binary(row)
		f.write("{0}\r".format(bina))
		sort_items.append(row)
		
f.close()
sort_items.sort()
# print(sorted.sort())
j = open("sortwrite.txt", "w")
sorted_items = list()
for item in sort_items:
	blah = to_binary(item)
	j.write("{0}\n".format(blah))
	sorted_items.append(blah)
j.close()

'''

def bin_compress(rows,compress_len):
	final = list()
	zero = 0
	print(len(rows))
	for x in range(0, 16):
		col = list()
		for row in rows:
			if len(row) < compress_len:

			col.append(row[x])

		# print(col)
		if '1' in col:
			r = ''.join(['0'] + col)
			if zero != 0:
				final.append('1' + bin(zero)[2:].zfill(31))
				zero = 0
			final.append(r)
		else:
			zero += 1

	# print(final)
	return ''.join(final)

# print(''.join(bin_compress(sorted_items[0:31])))

def compress_file(filename, outputfile, compress_len):
    with open(outputfile, 'w') as of:
        with open(filename, 'r') as fp:
            x = 0
            bit_list = []
            for line in fp:
                bit_list.append(line)
                x += 1
                if x % (compress_len - 1) == 0:
                    of.write(bin_compress(bit_list,compress_len) + '\n')
                    x = 0
                    bit_list = []


compress_file('write.txt', 'write_compressed_32.txt', 32)
compress_file('sortwrite.txt', 'sortwrite_compressed_32.txt', 32)