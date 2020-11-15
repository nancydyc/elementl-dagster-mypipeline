import pickle

# data = {"value": 100}
data = 100


def write_pickle_file(data):
    with open("data.pickle", "wb") as f:
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)


write_pickle_file(data)

# if __name__ == "__main__":
