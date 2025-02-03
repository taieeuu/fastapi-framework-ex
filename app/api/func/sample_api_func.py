
def get_latest_open_date(collection):
    return collection.find_one(sort=[('f_1', -1)])['f_1']
