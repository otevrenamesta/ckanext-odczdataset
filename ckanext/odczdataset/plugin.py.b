# -*- coding: utf-8 -*-

import logging
import ckan.plugins as p
import ckan.plugins.toolkit as tk
import ckan.plugins.interfaces as interfaces

def md_sharing_levels():
  #return [('internal', _('interní')), ('shared', _('městská')), ('partially_open', _('částečně otevřená')), ('open', _('otevřená'))]
  return [('internal', u'interní'), ('shared', u'městská'), ('partially_open', u'částečně otevřená'), ('open', u'otevřená')]

def md_states():
  return [('new', u'nový'), ('in_progress', u'zpracovávaný'), ('published', u'publikovaný'), ('closed', u'ukončený')]

def create_ruian_types():
    user = tk.get_action('get_site_user')({'ignore_auth': True}, {})
    context = {'user': user['name']}
    try:
        data = {'id': 'ruian_types'}
        logging.info("getting vocabulary show")
        tk.get_action('vocabulary_show')(context, data)
    except tk.ObjectNotFound:
        data = {'name': 'ruian_types'}
        logging.info("trying to create vocab");
        vocab = tk.get_action('vocabulary_create')(context, data)
        for tag in (u'AD', u'BPA', u'CO', u'KR', u'KU', u'MC', u'MP', u'OB', u'OK', u'OP', u'PA', u'PO', u'PU', u'RS', u'SO', u'SP', u'ST', u'UL', u'VC', u'VO', u'ZJ'):
            data = {'name': tag, 'vocabulary_id': vocab['id']}
            tk.get_action('tag_create')(context, data)

def ruian_types():
    logging.info("ruiantypes")
    create_ruian_types()
    try:
        tag_list = tk.get_action('tag_list')
        ruian_types = tag_list(data_dict={'vocabulary_id': 'ruian_types'})
        return ruian_types
    except tk.ObjectNotFound:
        return None


class ODCZDatasetFormPlugin(p.SingletonPlugin, tk.DefaultDatasetForm):
  p.implements(p.IDatasetForm)
  p.implements(p.IConfigurer)
  p.implements(p.ITemplateHelpers)
  p.implements(p.IResourceController, inherit=True)

  BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

  def set_SHA(self, context, resource):
    import sys
    import hashlib
    import ckan.lib.uploader as uploader

    upload = uploader.get_resource_uploader(resource)
    filepath = upload.get_path(resource['id'])
    print 'filepath: ' +filepath

    sha = hashlib.sha256()
    
    with open(filepath, 'rb') as f:
        while True:
            data = f.read(self.BUF_SIZE)
            if not data:
                break
            sha.update(data)
    
    print("SHA256: {0}".format(sha.hexdigest()))
    return True

  def after_create(self, context, resource):
    self.set_SHA(context, resource)


  def after_update(self, context, resource):
    self.set_SHA(context, resource)


  def get_helpers(self):
    return {
      'md_sharing_levels': md_sharing_levels,
      'md_states': md_states,
      'ruian_types': ruian_types
    }
  

  def _modify_package_schema(self, schema):
        schema.update({
            'md-private': [tk.get_validator('ignore_missing'),
                            tk.get_converter('convert_to_extras')],
            'md_sharing_level': [tk.get_validator('ignore_missing'),
                            tk.get_converter('convert_to_extras')],
            'md_state': [tk.get_validator('ignore_missing'),
                            tk.get_converter('convert_to_extras')],
            'md_gdpr': [tk.get_validator('ignore_missing'),
                            tk.get_converter('convert_to_extras')],
            'md_primary_source': [tk.get_validator('ignore_missing'),
                            tk.get_converter('convert_to_extras')],
            'md_ticket_private': [tk.get_validator('ignore_missing'),
                            tk.get_converter('convert_to_extras')],
            'md_ticket_public': [tk.get_validator('ignore_missing'),
                            tk.get_converter('convert_to_extras')],
            'md_harvester': [tk.get_validator('ignore_missing'),
                            tk.get_converter('convert_to_extras')],
            'md_harvested_url': [tk.get_validator('ignore_missing'),
                            tk.get_converter('convert_to_extras')],
            'md_delivery': [tk.get_validator('ignore_missing'),
                            tk.get_converter('convert_to_extras')],
            'publisher_name': [tk.get_validator('ignore_missing'),
                            tk.get_converter('convert_to_extras')],
            'publisher_uri': [tk.get_validator('ignore_missing'),
                            tk.get_converter('convert_to_extras')],
            'frequency': [tk.get_validator('ignore_missing'),
                            tk.get_converter('convert_to_extras')],
            'ruian_code': [tk.get_validator('ignore_missing'),
                            tk.get_converter('convert_to_extras')],
            'ruian_type': [tk.get_validator('ignore_missing'),
                            tk.get_converter('convert_to_extras')],
#                            tk.get_converter('convert_to_tags')('ruian_types')],
            'spatial_uri': [tk.get_validator('ignore_missing'),
                            tk.get_converter('convert_to_extras')],
            'theme': [tk.get_validator('ignore_missing'),
                            tk.get_converter('convert_to_extras')],
            'temporal_start': [tk.get_validator('ignore_missing'),
                            tk.get_converter('convert_to_extras')],
            'temporal_end': [tk.get_validator('ignore_missing'),
                            tk.get_converter('convert_to_extras')],
            'schema': [tk.get_validator('ignore_missing'),
                            tk.get_converter('convert_to_extras')],
            'license_link': [tk.get_validator('ignore_missing'),
                            tk.get_converter('convert_to_extras')],

        })

	schema['resources'].update({
            'license_link' : [ tk.get_validator('ignore_missing') ],
            'describedBy' : [ tk.get_validator('ignore_missing') ],
            'describedByType' : [ tk.get_validator('ignore_missing') ],
            'temporal_start' : [ tk.get_validator('ignore_missing') ],
            'temporal_end' : [ tk.get_validator('ignore_missing') ],
            'spatial_uri' : [ tk.get_validator('ignore_missing') ],
            'ruian_type' : [ tk.get_validator('ignore_missing') ],
            'ruian_code' : [ tk.get_validator('ignore_missing') ]
        })

        return schema

  def create_package_schema(self):
        # let's grab the default schema in our plugin
        schema = super(ODCZDatasetFormPlugin, self).create_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

  def update_package_schema(self):
        schema = super(ODCZDatasetFormPlugin, self).update_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

  def show_package_schema(self):
        schema = super(ODCZDatasetFormPlugin, self).show_package_schema()
        schema['tags']['__extras'].append(tk.get_converter('free_tags_only'))
        schema.update({
            'md-private': [tk.get_converter('convert_from_extras'),
                            tk.get_validator('ignore_missing')],
            'md_sharing_level': [tk.get_converter('convert_from_extras'),
                            tk.get_validator('ignore_missing')],
            'md_state': [tk.get_converter('convert_from_extras'),
                            tk.get_validator('ignore_missing')],
            'md_gdpr': [tk.get_converter('convert_from_extras'),
                            tk.get_validator('ignore_missing')],
            'md_primary_source': [tk.get_converter('convert_from_extras'),
                            tk.get_validator('ignore_missing')],
            'md_ticket_private': [tk.get_converter('convert_from_extras'),
                            tk.get_validator('ignore_missing')],
            'md_ticket_public': [tk.get_converter('convert_from_extras'),
                            tk.get_validator('ignore_missing')],
            'md_harvester': [tk.get_converter('convert_from_extras'),
                            tk.get_validator('ignore_missing')],
            'md_harvested_url': [tk.get_converter('convert_from_extras'),
                            tk.get_validator('ignore_missing')],
            'md_delivery': [tk.get_converter('convert_from_extras'),
                            tk.get_validator('ignore_missing')],
            'publisher_name': [tk.get_converter('convert_from_extras'),
                            tk.get_validator('ignore_missing')],
            'publisher_uri': [tk.get_converter('convert_from_extras'),
                            tk.get_validator('ignore_missing')],
            'frequency': [tk.get_converter('convert_from_extras'),
                            tk.get_validator('ignore_missing')],
            'ruian_code': [tk.get_converter('convert_from_extras'),
                            tk.get_validator('ignore_missing')],
            'ruian_type': [tk.get_converter('convert_from_extras'),
#            'ruian_type': [tk.get_converter('convert_from_tags')('ruian_types'),
                            tk.get_validator('ignore_missing')],
            'spatial_uri': [tk.get_converter('convert_from_extras'),
                            tk.get_validator('ignore_missing')],
            'theme': [tk.get_converter('convert_from_extras'),
                            tk.get_validator('ignore_missing')],
            'temporal_start': [tk.get_converter('convert_from_extras'),
                            tk.get_validator('ignore_missing')],
            'license_link': [tk.get_converter('convert_from_extras'),
                            tk.get_validator('ignore_missing')],
            'schema': [tk.get_converter('convert_from_extras'),
                            tk.get_validator('ignore_missing')],
            'temporal_end': [tk.get_converter('convert_from_extras'),
                            tk.get_validator('ignore_missing')],
         })

        schema['resources'].update({
            'license_link' : [ tk.get_validator('ignore_missing') ],
            'describedBy' : [ tk.get_validator('ignore_missing') ],
            'describedByType' : [ tk.get_validator('ignore_missing') ],
            'spatial_uri' : [ tk.get_validator('ignore_missing') ],
            'ruian_type' : [ tk.get_validator('ignore_missing') ],
            'ruian_code' : [ tk.get_validator('ignore_missing') ],
            'temporal_start' : [ tk.get_validator('ignore_missing') ],
            'temporal_end' : [ tk.get_validator('ignore_missing') ],
        })

        return schema

  def is_fallback(self):
        # Return True to register this plugin as the default handler for
        # package types not handled by any other IDatasetForm plugin.
        return False

  def package_types(self):
        # This plugin doesn't handle any special package types, it just
        # registers itself as the default (above).
        return []

  def update_config(self, config):
        # Add this plugin's templates dir to CKAN's extra_template_paths, so
        # that CKAN will use this plugin's custom templates.
        tk.add_template_directory(config, 'templates')
        tk.add_resource('fanstatic', 'odczdataset')

	# Add this plugin's public dir to CKAN's extra_public_paths, so
        # that CKAN will use this plugin's custom static files.
        tk.add_public_directory(config, 'public')
  
