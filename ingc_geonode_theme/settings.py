# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright (C) 2017 OSGeo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#########################################################################

# Django settings for the GeoNode project.
import os
import sys
import importlib
from django.utils.translation import ugettext_lazy as _

# Load more settings from a file called local_settings.py if it exists
try:
    from ingc_geonode_theme.local_settings import *
#    from geonode.local_settings import *
except ImportError:
    # Load from current settings file
    settings_file = os.environ.get(
        'DJANGO_SETTINGS_MODULE', 'geonode.settings')
    if settings_file not in sys.modules:
        current_settings = importlib.import_module(settings_file)
        sys.modules[settings_file] = current_settings
    else:
        current_settings = sys.modules[settings_file]

    locals().update(
    {
        k: getattr(current_settings, k)
        for k in dir(current_settings) if not k.startswith('_')
    })

#
# General Django development settings
#
PROJECT_NAME = 'ingc_geonode_theme'

# add trailing slash to site url. geoserver url will be relative to this
if not SITEURL.endswith('/'):
    SITEURL = '{}/'.format(SITEURL)

SITENAME = os.getenv("SITENAME", 'ingc_geonode_theme')

# Defines the directory that contains the settings file as the _LOCAL_ROOT
# It is used for relative settings elsewhere.
_LOCAL_ROOT = os.path.abspath(os.path.dirname(__file__))

WSGI_APPLICATION = "{}.wsgi.application".format(PROJECT_NAME)


# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = os.getenv('LANGUAGE_CODE', "en")

if PROJECT_NAME not in INSTALLED_APPS:
    INSTALLED_APPS += (PROJECT_NAME,)

# Location of url mappings
ROOT_URLCONF = os.getenv('ROOT_URLCONF', '{}.urls'.format(PROJECT_NAME))

# Additional directories which hold static files
STATICFILES_DIRS.append(
    os.path.join(_LOCAL_ROOT, "static"),
)

_LOCALE_DIR = os.path.join(_LOCAL_ROOT, 'locale')
_TEMPLATE_DIR = os.path.join(_LOCAL_ROOT, 'templates')

if not THEME_APP_PATH:
    # Prioritize custom translations
    LOCALE_PATHS = list(LOCALE_PATHS)
    LOCALE_PATHS.insert(0, _LOCALE_DIR)

    # Prioritize custom theme
    template_dirs = list(TEMPLATES[0]['DIRS'])
    template_dirs.insert(0, _TEMPLATE_DIR)

    TEMPLATES[0]['DIRS'] = template_dirs

# Override qgis report template settings for INGC
_LOCALIZED_QGIS_REPORT_TEMPLATE = {
    'en': os.path.join(
        _TEMPLATE_DIR, 'geosafe', 'qgis_templates',
        'en', 'map-report.qpt'),
    'pt': os.path.join(
        _TEMPLATE_DIR, 'geosafe', 'qgis_templates',
        'pt', 'map-report.qpt')
}

if 'LOCALIZED_QGIS_REPORT_TEMPLATE' in locals():
    LOCALIZED_QGIS_REPORT_TEMPLATE.update(
        _LOCALIZED_QGIS_REPORT_TEMPLATE
    )
else:
    LOCALIZED_QGIS_REPORT_TEMPLATE = _LOCALIZED_QGIS_REPORT_TEMPLATE

# Hazard settings.
# Do not forget to add also the icon when adding new hazard.
HAZARD_DEFINITION = {
    'key': 'hazard',
    'name': _('hazard'),
    'categories': ['flood', 'earthquake', 'cyclone'],
    'list_titles': [
        _('Select a flood layer'),
        _('Select an earthquake layer'),
        _('Select a cyclone layer'),
    ]
}

# Define language list for INGC
LANGUAGES = (
    ('pt', 'Portuguese'),
    ('en', 'English'),
)
