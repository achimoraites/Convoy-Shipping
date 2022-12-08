import sqlite3
import json
from lxml import etree


def get_vehicle_score(vehicle, route_length=450):
    consumption = (int(vehicle['fuel_consumption']) / 100) * route_length
    number_of_pit_stops = consumption // int(vehicle['engine_capacity'])
    score = 0
    # Truck capacity. If the capacity is 20 tones or more, it gets 2 points.
    if int(vehicle['maximum_load']) >= 20:
        score += 2
    # Fuel consumed over the entire trip. If a truck burned 230 liters or less, 2 points are given. If more — 1 point
    if consumption <= 230:
        score += 2
    else:
        score += 1
    # Number of pit-stops. If there are two or more gas stops on the way, the object has 0 points. One stop at the
    # filling station means 1 point. No stops — 2 scoring points.
    if number_of_pit_stops >= 2:
        pass
    elif number_of_pit_stops == 1:
        score += 1
    else:
        score += 2

    return score


def dataframe_to_database(df, filename):
    db_path = filename.replace('[CHECKED]', '').split('.').pop(0)
    db_path = '{}.s3db'.format(db_path)
    con = sqlite3.connect(db_path)
    cursor = con.cursor()

    records = 0
    # create the convoy table
    cursor.execute("""CREATE TABLE IF NOT EXISTS convoy(
            vehicle_id INTEGER PRIMARY KEY,
            engine_capacity INTEGER NOT NULL,
            fuel_consumption INTEGER NOT NULL,
            maximum_load INTEGER NOT NULL,
            score INTEGER NOT NULL
            );""")
    for index, row in df.iterrows():
        score = get_vehicle_score(row)
        entry = (row['vehicle_id'],
                 row['engine_capacity'],
                 row['fuel_consumption'],
                 row['maximum_load'],
                 score)
        try:
            cursor.execute("""INSERT INTO 
            convoy(vehicle_id, engine_capacity, fuel_consumption, maximum_load, score) 
            VALUES (?, ?, ?, ?, ?)""", entry)
            records += 1
        except sqlite3.IntegrityError:
            # duplicate entry
            pass
    con.commit()

    msg = "record was" if records == 1 else "records were"
    print("{} {} inserted into {}".format(records, msg, db_path))

    # clean up
    cursor.close()
    con.close()
    # get the database path on completion
    return db_path


def database_to_json(db_path):
    con = sqlite3.connect(db_path)
    cursor = con.cursor()
    cursor.execute("""SELECT vehicle_id, engine_capacity, fuel_consumption, maximum_load, score FROM convoy""")
    vehicles = cursor.fetchall()
    vehicles_added = 0
    json_path = db_path.replace('.s3db', '.json')
    with open(json_path, 'w') as json_file:
        convoy_dict = dict()
        convoy_dict['convoy'] = []
        for v in vehicles:
            vehicle_id, engine_capacity, fuel_consumption, maximum_load, score = v
            if score > 3:
                convoy_dict['convoy'].append({
                    'vehicle_id': vehicle_id,
                    'engine_capacity': engine_capacity,
                    'fuel_consumption': fuel_consumption,
                    'maximum_load': maximum_load
                })
                vehicles_added += 1
        json.dump(convoy_dict, json_file)

        msg = "vehicle was" if vehicles_added == 1 else "vehicles were"
        print("{} {} inserted into {}".format(vehicles_added, msg, json_path))

    # clean up
    cursor.close()
    con.close()

    return json_path


def database_to_xml(db_path):
    con = sqlite3.connect(db_path)
    cursor = con.cursor()
    cursor.execute("""SELECT vehicle_id, engine_capacity, fuel_consumption, maximum_load, score FROM convoy""")
    vehicles = cursor.fetchall()
    vehicles_added = 0
    xml_path = db_path.replace('.s3db', '.xml')
    convoy_xml = "<convoy>"
    for v in vehicles:
        vehicle_id, engine_capacity, fuel_consumption, maximum_load, score = v
        if score <= 3:
            convoy_xml += (
                "<vehicle><vehicle_id>{}</vehicle_id><engine_capacity>{}</engine_capacity><fuel_consumption>{"
                "}</fuel_consumption><maximum_load>{}</maximum_load></vehicle>"
                .format(vehicle_id, engine_capacity, fuel_consumption, maximum_load))
            vehicles_added += 1

    convoy_xml += "</convoy>"
    root = etree.fromstring(convoy_xml)
    tree = etree.ElementTree(root)  # create an instance of ElementTree in order to save it
    # prevent creation of self-closing tags
    # https://stackoverflow.com/questions/41890415/keep-lxml-from-creating-self-closing-tags
    for node in tree.iter():
        if node.text is None:
            node.text = ''
    tree.write(xml_path)

    msg = "vehicle was" if vehicles_added == 1 else "vehicles were"
    print("{} {} inserted into {}".format(vehicles_added, msg, xml_path))

    # clean up
    cursor.close()
    con.close()

    return xml_path
