
def search_line(key: str, file) -> str:
	file.seek(0)

	line = file.readline()
	while (key not in line): line = file.readline()

	return line


ipc_stats = open('ipc_stats.csv', 'r')
async_stats = open('async_stats.csv', 'r')

# Skip titles
ipc_stats.readline()
async_stats.readline()

for line in ipc_stats:
	
	ipc_line_list = line.split(';')

	key = ';'.join(ipc_line_list[:3])

	async_line_list = search_line(key, async_stats).split(';')

	last_key0 = key[0]
	last_key1 = key[1]
	last_key2 = key[2]


	




