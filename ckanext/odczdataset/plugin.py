# -*- coding: utf-8 -*-

import logging
import ckan.plugins as p
import ckan.plugins.toolkit as tk
import ckan.plugins.interfaces as interfaces
from ckan.common import config

asbool = tk.asbool


ignore_missing = tk.get_validator('ignore_missing')
ignore_not_package_admin = tk.get_validator('ignore_not_package_admin')
boolean_validator = tk.get_validator('boolean_validator')
datasets_with_no_organization_cannot_be_private = tk.get_validator('datasets_with_no_organization_cannot_be_private')

def frequencies():
  return [
    {'value': 'R/2Y', 'text': u'2 roky'},
    {'value': 'R/1Y', 'text': u'roční'},
    {'value': 'R/4M', 'text': u'čtvrtletní'},
    {'value': 'R/1M', 'text': u'měsíční'},
    {'value': 'R2/1M', 'text': u'2x měsíčně'},
    {'value': 'R/7D', 'text': u'týdenní'},
    {'value': 'R/1D', 'text': u'denní'},
    {'value': 'R/T1H', 'text': u'hodinová'},
    {'value': 'R/T30M', 'text': u'30 minut'},
    {'value': 'R/T2M', 'text': u'2 minuty'},
    {'value': 'R/PT1S', 'text': u'průběžná'},
    ]

def md_sharing_levels():
  #return [('internal', _('interní')), ('shared', _('městská')), ('partially_open', _('částečně otevřená')), ('open', _('otevřená'))]
  #return [('internal', u'interní'), ('shared', u'městská'), ('partially_open', u'částečně otevřená'), ('open', u'otevřená'), ('blbost', u'blbost')]
  return [
      {'value': 'internal', 'text': u'interní'},
      {'value': 'shared', 'text': u'městská'},
      {'value': 'partially_open', 'text': u'částečně otevřená'},
      {'value': 'open', 'text': u'otevřená'},
      ]

def md_states():
  return [
      {'value': 'new', 'text': u'nový'},
      {'value': 'in_progress', 'text': u'zpracovávaný'},
      {'value': 'published', 'text': u'publikovaný'},
      {'value': 'closed', 'text': u'ukončený'},
      ]

def md_gdprs():
  return [
      {'value': 'True', 'text': u'ano'},
      #unchecked checkbox is hidden
      ]

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

def md_ruian_types():
  return [
    {'value': 'AD', 'text': u'Adresní místo'},
    {'value': 'BPA', 'text': u'Bonitovaný díl parcely'},
    {'value': 'CO', 'text': u'Část obce'},
    {'value': 'DAM', 'text': u'Definiční bod adresního místa'},
    {'value': 'DKU', 'text': u'Definiční bod přehledové mapy katastrálního území'},
    {'value': 'DPA', 'text': u'Definiční bod katastrální mapy pro parcely'},
    {'value': 'DSO', 'text': u'Definiční bod stavebního objektu'},
    {'value': 'DUC', 'text': u'Definiční bod přehledové mapy pro vyšší územní celky, VO a ZSJ.'},
    {'value': 'DUL', 'text': u'Definiční čára ulice'},
    {'value': 'DUP', 'text': u'Def. Bod účelového prvku'},
    {'value': 'GKU', 'text': u'Generalizované hranice katastrálního území'},
    {'value': 'GOB', 'text': u'Generalizované hranice obce, vojenského újezdu'},
    {'value': 'GUP', 'text': u'Gen. polygon účelového prvku'},
    {'value': 'HKU', 'text': u'Hranice katastrálního území'},
    {'value': 'HMC', 'text': u'Hranice městského obvodu nebo městské části územně členěného statutárního města'},
    {'value': 'HOB', 'text': u'Hranice pro vyšší územní celky'},
    {'value': 'HVO', 'text': u'Hranice volebního okrsku'},
    {'value': 'HZJ', 'text': u'Hranice území základní sídelní jednotky'},
    {'value': 'IKU', 'text': u'Generalizované polygony katastrálního území'},
    {'value': 'KR', 'text': u'Území kraje'},
    {'value': 'KU', 'text': u'Katastrální území'},
    {'value': 'MC', 'text': u'Území městského obvodu nebo městské části územně členěného statutárního města'},
    {'value': 'MP', 'text': u'Území městského obvodu v hlavním městě Praze'},
    {'value': 'OB', 'text': u'Území obce, území vojenského újezdu'},
    {'value': 'OK', 'text': u'Území okresu'},
    {'value': 'OP', 'text': u'Správní obvod obce s rozšířenou působností'},
    {'value': 'PA', 'text': u'Pozemek v podobě parcely'},
    {'value': 'PKU', 'text': u'Polygony katastrálního území'},
    {'value': 'PMC', 'text': u'Polygony území městského obvodu nebo městské části územně členěného statutárního města'},
    {'value': 'PO', 'text': u'Adresní pošta'},
    {'value': 'PPA', 'text': u'Polygony pozemku v podobě parcely'},
    {'value': 'PSO', 'text': u'Polygony stavebního objektu'},
    {'value': 'PU', 'text': u'Správní obvod obce s pověřeným obecním úřadem'},
    {'value': 'PUP', 'text': u'Polygon účelového prvku'},
    {'value': 'PVO', 'text': u'Polygony volebního okrsku'},
    {'value': 'PZJ', 'text': u'Polygony území základní sídelní jednotky'},
    {'value': 'RS', 'text': u'Území regionu soudržnosti'},
    {'value': 'SO', 'text': u'Stavební objekt'},
    {'value': 'SP', 'text': u'Správní obvod v hlavním městě Praze'},
    {'value': 'ST', 'text': u'Území státu'},
    {'value': 'TEA', 'text': u'Detailní technicko ekonomické atributy'},
    {'value': 'UL', 'text': u'Ulice nebo jiné veřejné prostranství'},
    {'value': 'UP', 'text': u'Účelový prvek'},
    {'value': 'VC', 'text': u'Území vyššího územně samosprávného celku'},
    {'value': 'VO', 'text': u'Volební okrsek'},
    {'value': 'ZJ', 'text': u'Území základní sídelní jednotky'},
    {'value': 'ZPA', 'text': u'Způsob ochrany parcely'},
    {'value': 'ZSO', 'text': u'Způsob ochrany stavebního objektu'},
    ]
      
def md_ruian_codes():
  return [
    {'value': '1', 'text': u'Městská část'},
    {'value': '2', 'text': u'Městský obvod'},
    ]

def md_get_item_value_text(options, value):
  item, = [item for item in options if item['value'] == value]
  return item['text']

def get_is_private_catalog():
  return asbool(config.get('ckan.odczdataset.is_private_catalog', False))

def md_get_syndicate_manually():
  return asbool(config.get('ckan.odczdataset.syndicate_manually', True))

def set_syndicate_flag_by_sharing_level(key, data, errors, context):
      if md_get_syndicate_manually():
        return 

      value = data.get(("md_sharing_level",))
      if value and value == "open":
        data[("md_syndicate",)] = True
      else:
        data[("md_syndicate",)] = False


class ODCZDatasetFormPlugin(p.SingletonPlugin, tk.DefaultDatasetForm):
  p.implements(p.IDatasetForm, inherit=True)
  p.implements(p.IConfigurer)
  p.implements(p.ITemplateHelpers)
  p.implements(p.IResourceController, inherit=True)

  #XXX
  #p.implements(p.IResourceView, inherit=True)
  #p.implements(p.IResourcePreview)

  #def preview_template(self, data, ctx):
  #  #print data
  #  #print ctx
  #  return 'package/test.html'

  #def can_preview(self, x):
  #  return True

  #def setup_template_variables(self, context, data_dict):
  #  d = dict(data_dict)
  #  d['md_sha'] = 'test'
  #  print 'lala'
  #  return d


  BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

  def set_SHA(self, context, resource):
    import sys
    import hashlib
    import ckan.model
    import ckan.lib.uploader as uploader

    upload = uploader.get_resource_uploader(resource)
    filepath = upload.get_path(resource['id'])

    #if resource['url_type'] and resource['url_type'] == 'upload':
    if resource['url_type']:
        sha = hashlib.sha256()

        with open(filepath, 'rb') as f:
            while True:
                data = f.read(self.BUF_SIZE)
                if not data:
                    break
                sha.update(data)

        print("hash SHA256: {0}".format(sha.hexdigest()))

        x = ckan.model.Resource.get(resource['id']) #Should be toolkit/plugin?
        #print('fingerprint' +x.md_fingerprint)
        #print('x.md_fingerprint PRED: ' +x.extras['md_fingerprint'])

        x.hash = sha.hexdigest() #it exists in standard sechame but is not being used by standard code. Own would be more safety x I don't know how

        session = context['session']
        session.add(x)
        session.flush()
        session.commit()
        #0/0

    else:
        if resource['hash']:
            x = ckan.model.Resource.get(resource['id'])
            x.hash = ''
            session = context['session']
            session.add(x)
            session.flush()
            session.commit()
    
    return True

  def after_courceseate(self, context, resource):
    print('Updating SHA256 hash after create')
    self.set_SHA(context, resource)

  def after_update(self, context, resource):
    print('AFTER UPDATE')
    print('Updating SHA256 hash after update')
    self.set_SHA(context, resource)

  def before_update(self, context, data, x):
    print('BEFORE UPDATE')

  def before_show(self, data):
    #print data
    #assert 'extras' in data
    return data

  def get_helpers(self):
    return {
      'frequencies': frequencies,
      'md_sharing_levels': md_sharing_levels,
      'md_states': md_states,
      'md_gdprs': md_gdprs,
      'md_ruian_types': md_ruian_types,
      'md_ruian_codes': md_ruian_codes,
      'md_get_item_value_text': md_get_item_value_text,
      'md_get_syndicate_manually': md_get_syndicate_manually,
    }

  
  def _modify_package_schema(self, schema):
        schema.update({
            'private': [ignore_missing, boolean_validator, datasets_with_no_organization_cannot_be_private, tk.get_validator('ignore_not_group_admin')],
            'md_syndicate': [tk.get_validator('ignore_missing'),
                            tk.get_converter('convert_to_extras')],
            'md_syndicated_id': [tk.get_validator('ignore_missing'),
                            tk.get_converter('convert_to_extras')],
            'md_ticket_url': [tk.get_validator('ignore_missing'),
                            tk.get_converter('convert_to_extras')],
            'md_sharing_level': [tk.get_validator('ignore_missing'),
                            tk.get_converter('convert_to_extras')],
            '__before': [ set_syndicate_flag_by_sharing_level],
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
            'md_harvester': [tk.get_validator('ignore_missing'),
                            tk.get_converter('convert_to_extras')],
            'md_harvested_url': [tk.get_validator('ignore_missing'),
                            tk.get_converter('convert_to_extras')],
            'schema': [tk.get_validator('ignore_missing'),
                            tk.get_converter('convert_to_extras')],
            'license_link': [tk.get_validator('ignore_missing'),
                            tk.get_converter('convert_to_extras')],
            })

	schema['resources'].update({
            'md_fingerprint' : [ tk.get_validator('ignore_missing') ],
            'testing' : [ tk.get_validator('ignore_missing') ],
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
            'md_syndicate': [tk.get_converter('convert_from_extras'),
                            tk.get_validator('ignore_missing')],
            'md_syndicated_id': [tk.get_converter('convert_from_extras'),
                            tk.get_validator('ignore_missing')],
            'md_ticket_url': [tk.get_converter('convert_from_extras'),
                            tk.get_validator('ignore_missing')],
            'md_sharing_level': [tk.get_converter('convert_from_extras'),
                            tk.get_validator('ignore_missing')],
            '__before': [ set_syndicate_flag_by_sharing_level],
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
            'md_harvester': [tk.get_converter('convert_from_extras'),
                            tk.get_validator('ignore_missing')],
            'md_harvested_url': [tk.get_converter('convert_from_extras'),
                            tk.get_validator('ignore_missing')],
            })

        schema['resources'].update({
            'md_fingerprint' : [ tk.get_validator('ignore_missing') ],
            'testing' : [ tk.get_validator('ignore_missing') ],
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
        return True
        #return False

  def package_types(self):
        # This plugin doesn't handle any special package types, it just
        # registers itself as the default (above).
        return []

  def update_config(self, config):
        # Add this plugin's templates dir to CKAN's extra_template_paths, so
        # that CKAN will use this plugin's custom templates.
        tk.add_template_directory(config, 'templates')
        tk.add_resource('fanstatic', 'odczdataset')
        tk.add_resource('fanstatic/bootstrap-datepicker', 'bootstrap-datepicker')


	# Add this plugin's public dir to CKAN's extra_public_paths, so
        # that CKAN will use this plugin's custom static files.
        tk.add_public_directory(config, 'public')


