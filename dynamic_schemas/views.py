from django.shortcuts import render, redirect
from django.views.generic import ListView 

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Schema, SchemaQuestion, SchemaResponse
from .forms import SchemaResponseForm
from .serializers import SchemaResponseSerializer


class SchemaIndexView(ListView):
    template_name = 'dynamic_schemas/index.html'
    context_object_name = 'all_schemas'

    def get_queryset(self):
        return Schema.objects.all()


class SchemaView(ListView):
    template_name = 'dynamic_schemas/schema.html'
    context_object_name = 'schema'

    def get_queryset(self, *args, **kwargs):
        schema_instance = Schema.objects.get(pk=self.kwargs['pk'])
        return SchemaQuestion.objects.filter(rel_schema=schema_instance)


def form_view(request, pk):
    schema = Schema.objects.get(pk=pk)

    if request.method == 'POST':
        form = SchemaResponseForm(schema, request.POST)

        if form.is_consistent():
            form.save()
            
            return redirect('success/', pk=pk)


    else:
        form = SchemaResponseForm(schema)

    return render(request, 'dynamic_schemas/schema.html', {'form': form})


def success_view(request, pk):
    return redirect(f'/dynamic_schemas/{pk}/')


""" API Views """


@api_view(['GET', 'POST'])
def schema_responses(request, pk):
    """
    List instance schema data, or create new?
    """

    if request.method == 'GET':
        schema = Schema.objects.get(pk=pk)
        responses = SchemaResponse.objects.filter(schema=schema)
        serializer = SchemaResponseSerializer(responses, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = SchemaResponseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
def schema_response_details(request, pk):
    """
    Retrive, update or delete a response.
    """

    try:
        response = SchemaResponse.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SchemaResponseSerializer(response)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SchemaResponseSerializer(response, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
