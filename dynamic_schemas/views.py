from django.http import Http404
from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView 

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer

from .models import Schema, SchemaQuestion, SchemaResponse
from .forms import SchemaResponseForm
from .serializers import SchemaResponseSerializer


class SchemaIndexView(ListView):
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


def form_view(request, pk):
    schema = Schema.objects.get(pk=pk)

    if request.method == 'POST':
        form = SchemaResponseForm(schema, request.POST)

        if form.is_valid():
            # This removes schema from qa_set only.
            del form.cleaned_data['schema']

            form.save()
            
            return redirect(f'/dynamic_schemas/{pk}')
    else:
        form = SchemaResponseForm(schema)

    return render(request, f'dynamic_schemas/create.html', {'form': form})



""" API Views """
# TODO Change this to class based views
class ResponseList(APIView):

    """
    Lists responses according to schema
    """

    def get(self, request, pk, format=None):
        schema = Schema.objects.get(pk=pk)
        responses = SchemaResponse.objects.filter(schema=schema)
        serializer = SchemaResponseSerializer(responses, many=True)
        return Response(serializer.data)


class SchemaView(APIView):

    """
    Fetches the FIRST object from ResponseList. Makes it availabe for
    schema.html
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
                                        .strftime('%a, %d %b %Y %H:%M:%S +0100')

        return instances


    def get_object(self, pk):
        try:
            schema = Schema.objects.get(pk=pk)
            single_response = SchemaResponse.objects.get(schema=schema, pk=1)
            serializer = SchemaResponseSerializer(single_response)
            return serializer.data
        except single_response.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        schema = Schema.objects.get(pk=pk)
        all_responses = SchemaResponse.objects.filter(schema=schema) 
        readable_responses = self.make_date_readable(all_responses)
        object_count = SchemaResponse.objects.filter(schema=schema).count()
        serializer = SchemaResponseSerializer(all_responses, many=True)

        return Response({'single_response': self.get_object(pk),
            'count': range(object_count),
            'all_responses': serializer.data,
            'pk': pk,
            })
