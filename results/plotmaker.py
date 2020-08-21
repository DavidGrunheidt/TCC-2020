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

def print_improvement(async_plots: list, ipc_plots: list, kernel: str):
	imp = kernel + ' & '

	best_improve = float("inf")
	best_improve_async_result = 0
	best_improve_ipc_result = 0
	best_improve_index = 0

	worst_improve = 0
	worst_improve_async_result = 0
	worst_improve_ipc_result = 0
	worst_improve_index = 0

	for index in range(len(async_plots)):
		async_result = async_plots[index]
		ipc_result = ipc_plots[index]

		improve = async_result / ipc_result

		if (improve > worst_improve):
			worst_improve = improve
			worst_improve_ipc_result = ipc_result
			worst_improve_async_result = async_result
			worst_improve_index = index

		elif (improve < best_improve):
			best_improve = improve
			best_improve_ipc_result = ipc_result
			best_improve_async_result = async_result
			best_improve_index = index

	worst_improve = round((1 - worst_improve) * 100, 2)
	best_improve = round((1 - best_improve) * 100, 2)

	def get_improved_iteration(is_km: bool, index: int):
		tiny = range(0, 5)
		small = range(5, 10)
		standard = range(10, 15)
		large = range(15,20)
		large_km = range(15, 19)
		huge = range(20, 25)
		huge_km = range(19, 23)

		imp_class = ""
		nclusters = 0

		def get_nclusters(class_size: str, is_km: bool, index: int):
			if (is_km and class_size in ["Large", "Huge"]):
				if (class_size == "Large"):
					return ["2", "4", "8", "16"][(index-15) % 4]
				else:
					return ["4", "8", "16"][(index-19) % 3]				
			else:
				return ["1", "2", "4", "8", "16"][index % 5]


		if (index in tiny):
			imp_class = "Tiny"
			nclusters = get_nclusters(imp_class, False, index)

		elif (index in small):
			imp_class = "Small"
			nclusters = get_nclusters(imp_class, False, index)

		elif (index in standard):
			imp_class = "Standard"
			nclusters = get_nclusters(imp_class, False, index)

		elif (not is_km and index in large):
			imp_class = "Large"
			nclusters = get_nclusters(imp_class, False, index)

		elif (index in large_km):
			imp_class = "Large"
			nclusters = get_nclusters(imp_class, True, index)

		elif (not is_km and index in huge):
			imp_class = "Huge"
			nclusters = get_nclusters(imp_class, False, index)

		elif (index in huge_km):
			imp_class = "Huge"
			nclusters = get_nclusters(imp_class, True, index)

		return imp_class, nclusters

	worst_class, worst_nclusters = get_improved_iteration(kernel == "KM", worst_improve_index)

	best_class, best_nclusters = get_improved_iteration(kernel == "KM", best_improve_index)

	worst_improve_str = worst_class + ' & ' + worst_nclusters + ' & ' + str(worst_improve_ipc_result) + ' & ' + str(worst_improve_async_result) + ' & ' + str(worst_improve)
	best_improve_str = best_class + ' & ' + best_nclusters + ' & ' + str(best_improve_ipc_result) + ' & ' + str(best_improve_async_result) + ' & ' + str(best_improve)

	imp += worst_improve_str + ' & ' + str(best_improve_str) + '\n'

	print(imp)

def main():
	colum_labels = ['kernel','class','nclusters','master','master_std','slave','slave_std','comm','comm_std','data_sent','data_received', 'power', 'power_std', 'energy', 'energy_std']
	labels = ['Tiny', 'Small', 'Standard', 'Large', "Huge"]
	kernels = ['FN', 'FAST', 'GF', 'KM', 'LU', 'IS']

	clusters_variations = 5
	classes_variations = 5
	column_index = 13

	show_improvement = True

	data = get_data('ipc_stats.csv', 'async_stats.csv', column_index)

	for kernel_index in range(6):
		file_name = kernels[kernel_index] + '_' + colum_labels[column_index] + '.pdf'
		kernel = data[kernel_index]

		async_plots = kernel[0]
		ipc_plots = kernel[1]

		if (show_improvement):
			if (column_index == 3 and kernel_index in [1, 2]):
				continue
			print_improvement(async_plots, ipc_plots, kernels[kernel_index])
			continue

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




