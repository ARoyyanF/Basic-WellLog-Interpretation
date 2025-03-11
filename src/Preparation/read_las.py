import lasio
def read_las(file, well_name, columns_to_rename, columns_to_keep, keep_original = False):
  file_name = file
  data = lasio.read(file_name).df().reset_index()

  data = data.rename(columns=columns_to_rename)
  data = data.filter(columns_to_keep)

  # Insert Well name columns in the first col index
  data.insert(0, 'WELL', well_name)

  if keep_original:
    data.fillna(-999.25, inplace=True)

  return data

if __name__ == "__main__":
    file_name = "data/raw/ll-4_wire_lima.las"
    well_name = "LL-4"
    renamed_columns = {'DEPTH' : 'DEPT', 'RT' : 'DR', 'ILM' : 'MR', 'LLS':'SR', 'NPHI_CORR':'NPHI'} # {nama_asli : nama_baru, ... , dst}
    columns = ["DEPT","GR", "CALI", "MR", "DR", "SR", "NPHI", "RHOB", "DT", "VSH", "RW", "WELL"]

    data = read_las(file_name, well_name, renamed_columns, columns, keep_original = False)

    print(data.head())