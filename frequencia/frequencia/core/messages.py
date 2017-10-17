from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

class SuccessMessageMixin(SuccessMessageMixin):

	def form_valid(self, form):				
		success_message = self.get_success_message(form.cleaned_data)
		if success_message:
			messages.info(self.request, success_message)
		return super(SuccessMessageMixin, self).form_valid(form)