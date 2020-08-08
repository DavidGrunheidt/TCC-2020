import os

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

kernels_list = []
classes_list = []
nclusters_list = []

versions = get_folders(os.getcwd())

for version in versions:

	kernels = get_folders(enter_folder(version))

	# Create csv file

	for kernel in kernels:

		classes = get_folders(enter_folder(kernel))

		for kernel_class in classes:

			nclusters_list = get_folders(enter_folder(kernel_class))

			for nclusters in nclusters_list:

				actual_dir = enter_folder(nclusters)
				time_files = get_files(actual_dir)
				power_folders = get_folders(actual_dir)

				initial_csv_line = ','.join([kernel, kernel_class, nclusters])

				for time_file in time_files:

					# Read time file

				for power in power_folders:

					power_file = [f for f in get_files(enter_folder(power)) if not f.endswith('.pdf')]
					
					# Read power file

					back_folder()
				back_folder()
			back_folder()
		back_folder()
	back_folder()