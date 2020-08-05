from fantasystats import context
from fantasystats.models import mlb, nhl


def create_indexes():

    for model in mlb.__all__:
        pkg = __import__('fantasystats.models.mlb.%s' % model)
        mod = getattr(pkg.models.mlb, model)

        if hasattr(mod, 'create_indexes'):
            mod.create_indexes()

    for model in nhl.__all__:
        pkg = __import__('fantasystats.models.nhl.%s' % model)
        mod = getattr(pkg.models.nhl, model)

        if hasattr(mod, 'create_indexes'):
            mod.create_indexes()


if __name__ == '__main__':
    create_indexes()
