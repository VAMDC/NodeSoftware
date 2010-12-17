import sys, os
if not os.environ.has_key('DJANGO_SETTINGS_MODULE'):
    sys.path.append(os.path.abspath('../..'))
    os.environ['DJANGO_SETTINGS_MODULE']='nodes.ExampleNode.settings_default'
