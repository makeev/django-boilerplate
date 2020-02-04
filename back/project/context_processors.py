from constance import config


def constance_context(request):
    conf_dict = {}
    for k in dir(config):
        conf_dict[k] = getattr(config, k)

    return {
        'CONSTANCE': conf_dict
    }
