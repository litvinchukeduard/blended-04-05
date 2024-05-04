from mongoengine import Document, StringField, ReferenceField


class Category(Document):
    name = StringField(required=True)


class Book(Document):
    title = StringField(required=True)
    category = ReferenceField('Category')

    def __str__(self):
        return f'{self.title} | {self.category}'
    
    def __repr__(self):
        return f'{self.title} | {self.category}'

    # meta = {
    # 'indexes': [
    #     {'fields': ('title'), 'unique': True}
    # ]}
