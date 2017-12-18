from django.http import Http404
from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer

from .models import Schema, SchemaQuestion, SchemaResponse
from .forms import SchemaResponseForm, ResponseUpdateForm
from .serializers import SchemaResponseSerializer


class SchemaIndexView(LoginRequiredMixin, ListView):
    # login_url = '/accounts/login.html/'
    template_name = 'dynamic_schemas/index.html'
    context_object_name = 'all_schemas'

    def get_queryset(self):
        return Schema.objects.all()

# class SchemaView(ListView):
    # template_name = 'dynamic_schemas/schema.html'
    # context_object_name = 'schema'

    # def get_queryset(self, *args, **kwargs):
        # schema_instance = Schema.objects.get(pk=self.kwargs['pk'])
        # return SchemaQuestion.objects.filter(rel_schema=schema_instance)


@login_required
def form_view(request, pk):
    schema = Schema.objects.get(pk=pk)

    if request.method == 'POST':
        form = SchemaResponseForm(schema, request.POST)

        if form.is_valid():
            # This removes schema from qa_set only.
            del form.cleaned_data['schema']
            # del form.cleaned_data['user']

            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            
            # __import__('ipdb').set_trace()
            
            # TODO Write tests for this. 
            return redirect(reverse('dynamic_schemas:schema_view',
                                    kwargs={'pk': pk}))
    else:
        form = SchemaResponseForm(schema)
        # __import__('ipdb').set_trace()

    return render(request, f'dynamic_schemas/create.html', {'form': form})


@login_required
def form_update_view(request, pk, r_pk):
    schema = Schema.objects.get(pk=pk)
    instance = SchemaResponse.objects.get(schema=schema, pk=r_pk)
    

    # if request.method == 'GET':
    form = ResponseUpdateForm(instance, pk)
        # return render(request, f'dynamic_schemas/update.html', {'form_update': form})


    if request.method == 'POST':
        form = ResponseUpdateForm(instance, pk, request.POST or None)
        if form.is_valid():

            # form.user = request.user
            form.update()
            # __import__('ipdb').set_trace()
            
            return redirect(f'/dynamic_schemas/{pk}')
        
    return render(request, f'dynamic_schemas/update.html', {'form_update': form})


""" API Views """
class ResponseList(LoginRequiredMixin, APIView):

    """
    Lists responses according to schema.
    Purely for APIView for now. Not being used in the actual rendering af the
    tables.
    """

    def get(self, request, pk, format=None):
        schema = Schema.objects.get(pk=pk)
        responses = SchemaResponse.objects.filter(schema=schema)
        serializer = SchemaResponseSerializer(responses, many=True)
        return Response(serializer.data)


class SchemaView(LoginRequiredMixin, APIView):

    """
    Fetches the FIRST object from ResponseList. Makes it availabe for
    as a template for the table in schema.html

    Excludes schema.id, and the placeholder qa_set in the template.
    """

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'dynamic_schemas/schema.html'

    def make_date_readable(self, instances):
        """ 
        Helper function to change the dates to a format pleasing to the
        eyes, takes a bundle of instances and converts their time.
        """
		
        for instance in instances:
            instance.pub_date = instance.pub_date \
                    .strftime('%Y:%m:%d %H:%M:%S')

        return instances


    def get_object(self, pk):
        try:
            schema = Schema.objects.get(pk=pk)

            if SchemaQuestion.objects.filter(schema=schema).count() != 0:
                all_responses = SchemaResponse.objects.filter(schema=schema) 
                single_response = all_responses.first()
                serializer = SchemaResponseSerializer(single_response)
                return serializer.data
            # else:
                # pass

        except single_response.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        schema = Schema.objects.get(pk=pk)
        schema_help_urls = schema.help_field.all()

        all_responses = SchemaResponse.objects.filter(schema=schema) 
        self.make_date_readable(all_responses)

        serializer = SchemaResponseSerializer(all_responses, many=True)

        data = {'single_response': self.get_object(pk),
                'all_responses': serializer.data,
                'pk': pk,
                'schema': schema,
                'help_urls': schema_help_urls, }

        # __import__('ipdb').set_trace()
        return Response(data)


""" User Authentication Views """
