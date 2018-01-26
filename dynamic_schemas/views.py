from django.http import Http404
from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer

from .models import Schema, SchemaColumn, SchemaResponse, SchemaUrl
from .forms import SchemaResponseForm, ResponseUpdateForm
from .serializers import SchemaResponseSerializer
from .prepare_data import getcolumns

import pytz

class SchemaIndexView(LoginRequiredMixin, ListView):
    # login_url = '/accounts/login.html/'
    template_name = 'dynamic_schemas/index.html'
    context_object_name = 'all_schemas'

    def get_queryset(self):
        return Schema.objects.all()


@login_required
def form_view(request, pk):
    schema = Schema.objects.get(pk=pk)
    urls = schema.help_field.all()

    if request.method == 'POST':
        form = SchemaResponseForm(schema, request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            
        return redirect(reverse('dynamic_schemas:schema_view',
                                kwargs={'pk': pk}))
    else:
        form = SchemaResponseForm(schema)

    return render(request, f'dynamic_schemas/create-form.html', \
        {
        'form': form,
        'schema': schema,
        'help_urls': urls,
        })


@login_required
def form_update_view(request, pk, r_pk):
    schema = Schema.objects.get(pk=pk)
    instance = SchemaResponse.objects.get(schema=schema, pk=r_pk)

    columns = SchemaColumn.objects.filter(schema=schema)

    ###################################################
    # This little snippet checks if the responses can be edited. If they can
    # the submit button will be provided. There is no restriction on
    # has_been_edited, but since the data cant be saved we're good for now.
    load_button = False
    aggr_editables = [c.is_editable_once for c in columns]

    if True in aggr_editables:
        load_button = True
    ###################################################

    form = ResponseUpdateForm(instance, pk)

    if request.method == 'POST':
        form = ResponseUpdateForm(instance, pk, request.POST or None)
        if form.is_valid():
            form.update()
        return redirect(reverse('dynamic_schemas:schema_view',
                                        kwargs={'pk': pk}))
        
    return render(request, f'dynamic_schemas/update-form.html', 
            {'form_update': form,
            'load_button': load_button}
            )


""" API Views """
class ResponseList(APIView):

    """
    Lists responses according to schema.
    Purely for APIView for now. Not being used in the actual rendering af the
    tables.
    """
    def _make_date_tz(self, instance=None, tz=None):
        """ Takes an instance, and sets its timezone. 
        
            TODO: 
            Should this be a classmethod? Will a classmethod complicate the
            view in its context?

        """
        # Can this be moved to SETTINGS instead? Same for _make_date_readable.
        # Problem is probably that the UTC format gets overridden.
        if instance:
            if tz:
                tz = pytz.timezone(tz)
            return instance.pub_date.astimezone(tz)
        return

    def _make_date_readable(self, instances):
        """ 
        Helper function to change the dates to a format pleasing to the
        eyes, takes a bundle of instances and converts their time.
        How extensible do we want this?
        Function is kept private for now, since in Denmark the timezone is CET.
        """
		
        for instance in instances:
            inst_as_cet = self._make_date_tz(
                    instance=instance
                    # tz='Europe/Copenhagen'
                    )
            instance.pub_date = inst_as_cet \
                    .strftime('%d-%m/%Y %H:%M:%S')

        return instances

    def _make_user_readable(self, serializer):
        """ Helper to return the correct attributes to the front-end
        """
        for data in serializer.data:
            # import ipdb; ipdb.set_trace()
            user = data['user']
            instance = User.objects.get(id=user)

            user = instance.first_name + instance.last_name

            if instance.first_name == '':
                user = instance.username

            data['user'] = user
            # __import__('ipdb').set_trace()
            # import ipdb; ipdb.set_trace()

        return serializer 

    def _make_intruction_links_readable(self, serializer):
        for data in serializer.data:
            instr = data['instruction']
            instance = SchemaUrl.objects.get(id=instr)
            
            instr = '<a href="'+ instance.url +'">'+ instance.name +'</a>'

            data['instruction'] = instr

        return serializer

    def get(self, request, pk, format=None, *args):
        req = request.GET
        # Amount of data to fetch each pull
        start = int(req.get('start', 0))
        length = int(req.get('length', 30))
        end = start + length;

        draw = req.get('draw')

        # TODO Gonna require some thinking. Also need to user recordsFiltered.
        # search = req.get('search[value]')

        schema = Schema.objects.get(pk=pk)
        responses_count = SchemaResponse.objects.filter(schema=schema).count()
        responses = SchemaResponse.objects.filter(schema=schema)[start:end]
        responses = self._make_date_readable(responses)

        serializer = SchemaResponseSerializer(responses, many=True)
        serializer = self._make_user_readable(serializer)
        serializer = self._make_intruction_links_readable(serializer)

        return_data = {
            'draw': int(draw),
            'recordsTotal': responses_count,
            'recordsFiltered': responses_count,
            'data': serializer.data,
            }
        # __import__('ipdb').set_trace()
        return Response(return_data)

class ResponseColumns(APIView):
    def get(self, request, pk, format=None, *args):
        req = request.GET
        schema = Schema.objects.get(pk=pk)
        sr = SchemaResponse.objects.filter(schema=schema).first()
        columns = getcolumns(sr).getvalue()

        return Response(columns)



class SchemaView(LoginRequiredMixin, APIView):

    """
    Fetches the FIRST object from ResponseList. Makes it availabe for
    as a template for the table in main.html

    Excludes schema.id, and the placeholder qa_set in the template.

    """

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'dynamic_schemas/table_dev.html'


    def get_object(self, pk):
        try:
            schema = Schema.objects.get(pk=pk)

            if SchemaColumn.objects.filter(schema=schema).count() != 0:
                all_responses = SchemaResponse.objects.filter(schema=schema) 
                single_response = all_responses.first()
                serializer = SchemaResponseSerializer(single_response)
                return serializer.data

        except single_response.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        schema = Schema.objects.get(pk=pk)
        schema_help_urls = schema.help_field.all()
        schema_obsolete = schema.obsolete.all()
        schema_new = schema.new.all()
        

        all_responses = SchemaResponse.objects.filter(schema=schema) 
        # self._make_date_readable(all_responses)

        serializer = SchemaResponseSerializer(all_responses, many=True)

        data = {'single_response': self.get_object(pk),
                'all_responses': serializer.data,
                'pk': pk,
                'schema': schema,
                'help_urls': schema_help_urls,
                'schema_obsolete': schema_obsolete,
                'schema_new': schema_new,
                }

        # __import__('ipdb').set_trace()
        return Response(data)
