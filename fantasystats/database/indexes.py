from fantasystats import context
from fantasystats.models import mlb


def create_indexes():

    for model in mlb.__all__:
        pkg = __import__('fantasystats.models.mlb.%s' % model)
        mod = getattr(pkg.models.mlb, model)

        if hasattr(mod, 'create_indexes'):
            mod.create_indexes()


if __name__ == '__main__':
    create_indexes()
