import yaml


class ConfigReader(object):
    """QA object which tolerates key missing in Environment Settting"""
    vals = (
        ('url', str),
        ('headless', str)
    )

    def __init__(self, env='default', fileName = ''):
        '''

        :param env:
        :param fileName:
        '''
        self.name = env
        try:
            with open(fileName) as fp:
                envs = yaml.load(fp, Loader=yaml.Loader)
        except IOError:
            raise Warning

        env = envs.get(env, {})
        for attr, type_ in self.vals:
            setattr(self, attr, env.get(attr, type_()))