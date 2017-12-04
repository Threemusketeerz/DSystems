from django.shortcuts import render, redirect
from django.views.generic import ListView 

from .models import Schema, SchemaQuestion
from .forms import SchemaResponseForm


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
