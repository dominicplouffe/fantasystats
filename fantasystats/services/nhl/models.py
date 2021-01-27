import pickle

MODEL = None


def init_models():

    global MODEL

    MODEL = load_model()


def load_model():
    f = open('nhl_model.dat', 'rb')
    content = f.read()
    f.close()

    return pickle.loads(content)


def save_model(model):
    regs = pickle.dumps(model)
    f = open('nhl_model.dat', 'wb')
    f.write(regs)
    f.close()
