import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def search_line(key: str, file) -> str:
	file.seek(0)

	line = file.readline()
	while (key not in line): line = file.readline()

	return line

def get_data(ipc_file_path: 'file', async_file_path: 'file', data_column: int):
	ipc_stats = open(ipc_file_path, 'r')
	async_stats = open(async_file_path, 'r')

	# Skip titles
	ipc_stats.readline()

	async_data = list()
	ipc_data = list()
	data = list()

	kernel = ""

	for line in ipc_stats:
		
		ipc_line_list = line.split(';')

		key = ';'.join(ipc_line_list[:3])

		async_line_list = search_line(key, async_stats).split(';')

		if (ipc_line_list[0] != kernel and kernel != ""):
			data.append([async_data, ipc_data])
			async_data = list()
			ipc_data = list()

		async_data.append(float(async_line_list[data_column]))
		ipc_data.append(float(ipc_line_list[data_column]))

		kernel = ipc_line_list[0]

	data.append([async_data, ipc_data])

	return data

def create_plot(async_groups: list, ipc_groups: list, kernel: str, labels: list, file_name: str):
	width = 0.07
	offset = 0.045
	color_palette = ['#383838', '#606060', '#808080', '#A9A9A9', '#D0D0D0']

	x = np.arange(len(labels))
	x_list = [x, x + (2 * width) + offset, x + (4 * width) + (2 * offset), x + (6 * width) + (3 * offset), x + (8 * width) + (4 * offset)]

	fig, ax = plt.subplots()
	rects_list = list()

	for i in range(len(async_groups)):
		rects_list.append(ax.bar(x_list[i], ipc_groups[i], width, color=color_palette[i], edgecolor ='#101010', linewidth=0.1))
		rects_list.append(ax.bar(x_list[i] + width, async_groups[i], width, color=color_palette[i], edgecolor ='#101010', linewidth=0.1, hatch='xxx'))

	# Add some text for labels, title and custom x-axis tick labels, etc.
	ax.set_title(kernel)
	ax.set_xticks(x_list[2] + (width/2))
	ax.set_xticklabels(labels)
	ax.set_axisbelow(True)
	ax.set_yscale('log', base=2)

	plt.grid(axis='y', color='#000000', linestyle=':', alpha=0.7)
	plt.xticks(fontsize=16)
	plt.yticks(fontsize=16)

	matplotlib.rcParams['hatch.linewidth'] = 0.1

	fig.tight_layout()
	fig.savefig(file_name, bbox_inches='tight', dpi=1000)


def main():
	colum_labels = ['kernel','class','nclusters','master','master_std','slave','slave_std','comm','comm_std','data_sent','data_received', 'power', 'power_std', 'energy', 'energy_std']
	labels = ['Tiny', 'Small', 'Standard', 'Large', "Huge"]
	kernels = ['FN', 'FAST', 'GF', 'KM', 'LU', 'IS']

	clusters_variations = 5
	classes_variations = 5
	column_index = 13

	data = get_data('ipc_stats.csv', 'async_stats.csv', column_index)

	for kernel_index in range(6):
		file_name = kernels[kernel_index] + '_' + colum_labels[column_index] + '.pdf'
		kernel = data[kernel_index]

		async_plots = kernel[0]
		ipc_plots = kernel[1]

		if (kernel_index == 3):
			async_plots = async_plots[:15] + [0] + async_plots[15:19] + [0, 0] + async_plots[19:]
			ipc_plots = ipc_plots[:15] + [0] + ipc_plots[15:19] + [0, 0] + ipc_plots[19:]


		async_reshaped = np.asarray(async_plots).reshape(classes_variations, clusters_variations)
		ipc_reshaped = np.asarray(ipc_plots).reshape(classes_variations, clusters_variations)

		async_hsplit = np.hsplit(async_reshaped, clusters_variations)
		ipc_hsplit = np.hsplit(ipc_reshaped, clusters_variations)

		async_groups = [x.flatten().tolist() for x in async_hsplit]
		ipc_groups = [x.flatten().tolist() for x in ipc_hsplit]

		create_plot(async_groups, ipc_groups, kernels[kernel_index], labels, file_name)

if __name__ == '__main__':
	main()




