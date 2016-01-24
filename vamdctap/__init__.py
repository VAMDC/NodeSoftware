import sys, os
if not 'DJANGO_SETTINGS_MODULE' in os.environ:
    sys.path.append(os.path.abspath('../..'))
    os.environ['DJANGO_SETTINGS_MODULE']='nodes.ExampleNode.settings_default'
