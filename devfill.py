from dynamic_schemas.models import (Schema, SchemaUrl, SchemaColumn, 
    SchemaResponse)


# To be used for functional testing, or as a command line tool to fill out
# database with a ton of data.

class Fill:
    def __init__(self, num=None):
        self.schemas = None

    def create_schemas(self, num):
        self.schemas = [Schema(name=f'TestSchema{i}', is_active=True) for i in range(num)]
        Schema.objects.bulk_create(self.schemas)
        self.schemas = Schema.objects.all()

    def create_columns(self, num):

        for s in self.schemas:
            columns = [
                SchemaColumn(schema=s, text=f'TestColumn{i}') 
                for i in range(num)
                ]
            SchemaColumn.objects.bulk_create(columns)

    def create_responses(self, num):
        columns = SchemaColumn.objects.filter(schema=self.schemas[0])
        url = SchemaUrl.objects.get_or_create(
            url='google.com', name='google', help_text='google'
            )

        qa_set = {c.text: f'ANSWER{i}' for i, c in enumerate(columns)}

        for s in self.schemas:
            responses = [
                SchemaResponse(schema=s, qa_set=qa_set, instruction=url[0])
                for i in range(num)
                ]
            SchemaResponse.objects.bulk_create(responses)


if __name__ == "__main__":
    if(str(sys.argv[1]) == 'create_schemas'):
        create_schemas(int(sys.argv[2]))

    elif(str(sys.argv[1]) == 'create_columns'):
        create_columns(int(sys.argv[2]))

    elif(str(sys.argv[1]) == 'create_responses'):
        create_responses(int(sys.argv[2]))

