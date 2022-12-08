from utils import read_file, clean_up_integers_in_column, get_checked_filename
from database import dataframe_to_database, database_to_json, database_to_xml

sheet_name = 'Vehicles'
file_name = input('Input file name\n')

# Handle csv and xlsx files
if file_name.endswith('.csv') or file_name.endswith('.xlsx'):
    my_df = read_file(file_name, sheet_name)

    # cell correction if is not a CHECKED file
    if not file_name.endswith('[CHECKED].csv'):
        cells_fixed = 0
        columns = ['vehicle_id', 'engine_capacity', 'fuel_consumption', 'maximum_load']
        for column in columns:
            cells_fixed += clean_up_integers_in_column(my_df, column)

        checked_csv_file_name = get_checked_filename(file_name)
        print("{} cells were corrected in {}".format(cells_fixed, checked_csv_file_name))
        my_df.to_csv(checked_csv_file_name, index=None, header=True)

    db_path = dataframe_to_database(my_df, file_name)
    database_to_json(db_path)
    database_to_xml(db_path)

elif file_name.endswith('.s3db'):
    database_to_json(file_name)
    database_to_xml(file_name)
