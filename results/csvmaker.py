from scipy.stats import variation
import statistics
import os
import re

def enter_folder(name: str):
	desired_dir = os.path.join(os.getcwd(), name)
	os.chdir(desired_dir)
	return desired_dir

def get_folders(actual_dir: str):
	return [f.name for f in os.scandir(actual_dir) if f.is_dir()]

def get_files(actual_dir: str):
	return [f.name for f in os.scandir(actual_dir) if f.is_file()]

def back_folder():
	os.chdir(os.path.join(os.getcwd(), ".."))

def calculate_stats(time_files: 'list(str)') -> str:
	master_times = list()
	slave_avg_times = list()
	comm_times = list()
	data_sent_list = list()
	data_received_list = list()
	power_avg_list = list()
	energy_list = list()

	for time_file in time_files:
		file = open(time_file, 'r')

		line = file.readline()

		while ('master:' not in line): line = file.readline()
		master_times.append(float(re.findall("\d+\.\d+", line).pop()))

		while ('slave avg:' not in line): line = file.readline()
		slave_avg_times.append(float(re.findall("\d+\.\d+", line).pop()))

		while('communication:' not in line): line = file.readline()
		comm_times.append(float(re.findall("\d+\.\d+", line).pop()))

		while('data sent:' not in line and 'data put:' not in line): line = file.readline()
		data_sent_list.append(int(re.findall("\d+", line).pop()))

		while('data received:' not in line and 'data get:' not in line): line = file.readline()
		data_received_list.append(int(re.findall("\d+", line).pop()))

		while('Power (avg):' not in line): line = file.readline()
		power_avg_list.append(float(re.findall("\d+\.\d+", line).pop()))

		while('Energy     :' not in line): line = file.readline()
		energy_list.append(float(re.findall("\d+\.\d+", line).pop()))

		file.close()

	stats = list()

	stats.append(str(round(statistics.mean(master_times), 2)))
	stats.append(str(variation(master_times) * 100))

	stats.append(str(round(statistics.mean(slave_avg_times), 2)))
	stats.append(str(variation(slave_avg_times) * 100))

	stats.append(str(round(statistics.mean(comm_times), 2)))
	stats.append(str(variation(comm_times) * 100))

	stats.append(str(round(statistics.mean(data_sent_list)/1048576, 2)))

	stats.append(str(round(statistics.mean(data_received_list)/1048576, 2)))

	stats.append(str(round(statistics.mean(power_avg_list), 2)))
	stats.append(str(variation(power_avg_list) * 100))

	stats.append(str(round(statistics.mean(energy_list), 2)))
	stats.append(str(variation(energy_list) * 100))

	return ';'.join(stats)

def main():
	versions = get_folders(os.getcwd())

	for version in versions:

		stats_file = open(version + '_stats.csv', 'w')

		stats_file.write("kernel [0];class [1];nclusters [2];master (s) [3];master relative stdev (%) [4];slave (s) [5];slave relative stdev (%) [6];comm (s) [7];comm relative stdev (%) [8];data sent (MB) [9];data received (MB) [10];power (W) [11];power relative stdev (%) [12];energy (J) [13];energy relative stdev (%) [14]\n")

		kernels = get_folders(enter_folder(version))

		# Create csv file

		for kernel in kernels:

			#We want a result sorted by this classes
			classes_folders = get_folders(enter_folder(kernel))
			classes = [x for x in ['tiny', 'small', 'standard', 'large', 'huge'] if x in classes_folders]

			for kernel_class in classes:

				#We want a result sorted by this list of nclusters
				nclusters_folders = get_folders(enter_folder(kernel_class))
				nclusters_list = [x for x in ['1', '2', '4', '8', '16'] if x in nclusters_folders]

				for nclusters in nclusters_list:

					actual_dir = enter_folder(nclusters)
					files = get_files(actual_dir)

					initial_csv_line = ';'.join([kernel, kernel_class, nclusters])

					stats = calculate_stats(files)

					line = initial_csv_line + ';' + stats + '\n'

					stats_file.write(line)

					back_folder()
				back_folder()
			back_folder()
		back_folder()

		stats_file.close()

if __name__ == '__main__':
	main()