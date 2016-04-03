# from django.db import models
from django.db.models.fields.files import FileField,FieldFile
import sae.storage
import sae
# import tempfile
from django.conf import settings
#tempfile.tempdir = sae.core.get_tmp_dir()

class SAEFieldFile(FieldFile):

	def getUploadTo(self):
 		return self.upload_to

	def save(self, name, content, save=True):

		# for develop
		if settings.DEBUG:
			super(SAEFieldFile,self).save(name,content,save)
		# for sae
		else:
			print 'sae save'
			name = self.field.generate_filename(self.instance, name)
			#for SAE
			s = sae.storage.Client()
			ob = sae.storage.Object(content._get_file().read())
			url =s.put('resources', name, ob)

	def delete(self,save=True):
		if not settings.DEBUG:
			sae.storage.Client().delete('resources',self.name)
		else:
			super(SAEFieldFile, self).delete()


class SAEFileField(FileField):
	attr_class = SAEFieldFile

	def save(self, name, content, save=True):
		super(SAEFieldFile, self).save(name, content, save=True)

	def delete(self, save=True):
		super(SAEFieldFile, self).delete(save=True)