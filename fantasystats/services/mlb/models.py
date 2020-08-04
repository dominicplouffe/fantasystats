import pickle

MODELS = {
    'A': None,
    'B': None,
    'C': None,
    'D': None,
    'E': None
}


def init_models():

    global MODELS

    for y in ['A', 'B', 'C', 'D', 'E']:
        MODELS[y] = load_model(y)


def load_model(y):
    f = open('%s_model.dat' % y, 'rb')
    content = f.read()
    f.close()

    return pickle.loads(content)


def save_model(model, y):
    regs = pickle.dumps(model)
    f = open('%s_model.dat' % y, 'wb')
    f.write(regs)
    f.close()
