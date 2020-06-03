
<img src="https://raw.githubusercontent.com/eshta/toute/master/docs/res/toute.png" align="left" height="200px"/>
<img align="left" width="0" height="192px" hspace="10"/>

> **toute** - **E**lastic**S**earch **O**bject **D**ocument **M**apper

[![PyPI](https://img.shields.io/pypi/v/toute.svg)](https://pypi.python.org/pypi/toute)
[![versions](https://img.shields.io/pypi/pyversions/toute.svg)](https://pypi.python.org/pypi/toute)
[![downloads](https://img.shields.io/pypi/dw/toute.svg)](https://pypi.python.org/pypi/toute)
[![Travis CI](https://travis-ci.org/eshta/toute.svg?branch=master)](https://travis-ci.org/eshta/toute)
[![Coverage Status](https://coveralls.io/repos/github/eshta/toute/badge.svg)](https://coveralls.io/github/eshta/toute)
[![Code Health](https://landscape.io/github/catholabs/toute/master/landscape.svg?style=flat)](https://landscape.io/github/eshta/toute/master)


**Toute** is an ODM (**O**bject **D**ocument **M**apper) it maps Python classes in to **E**lastic**S**earch **index/doc_type** and **object instances()** in to Elasticsearch documents.

It is a fork of seek-ai/esengine with compatibility with recent ElasticSearch 6/7 and more...
<br><br>

### Modeling

Out of the box toute takes care only of the Modeling and CRUD operations including:

- Index, DocType and Mapping specification 
- Fields and its types coercion
- basic CRUD operations (Create, Read, Update, Delete)

### Communication
toute does not communicate directly with ElasticSearch, it only creates the basic structure, 
To communicate it relies on an ES client providing the transport methods (index, delete, update etc). 

### ES client
toute does not enforce the use of the official ElasticSearch client,
but you are encouraged to use it because it is well maintained and has the support to **bulk** operations. But you are free to use another client or create your own (useful for tests).

### Querying the data
toute does not enforce or encourage you to use a DSL language for queries, out of the box you have to
write the elasticsearch **payload** representation as a raw Python dictionary. However toute comes with **utils.payload** helper module to help you building payloads in a less verbose and Pythonic way.

### Why not elasticsearch_dsl?

ElasticSearch DSL is an excellent tool, a very nice effort by the maintainers of the official ES library, it is handy in most of the cases, but because it is built on top of operator overiding, sometimes leads to a **confuse query building**, sometimes it is better to write raw_queries or use a simpler payload builder having more control and visibility of what os being generated. 

ElasticSearch_DSL as a high level abstraction promotes **Think only of Python objects, dont't worry about Elastic queries** while toute promotes **Know well the Elastic queries and then write them as Python objects**.

ElasticSearch_DSL is more powerful and more complete, tight more with ES specifications while toute is simpler, lightweight shipping only the basics.

### Project Stage

It is in beta-Release, working in production, but missing a lot of features, you can help using, testing,, discussing or coding!


# Getting started

## Installation

toute needs a client to communicate with E.S, you can use one of the following:

- elasticsearch (official)
- Create your own implementing the same api-protocol
- Use the MockES provided as py.test fixture (only for tests)

### in short

Install the client and then install toute

- for 7.0 + use "elasticsearch>=7.0.0,<8.0.0"
- for 6.0 + use "elasticsearch>=6.0.0,<7.0.0"


For the latest use:

```sh
$ pip install elasticsearch
$ pip install toute
```

The above command will install toute and the elasticsearch library specific for you ES version.

# Usage

```python
# importing

from elasticsearch import ElasticSearch
from toute import Document, KeywordField

# Defining a document
class Person(Document):
    # define _meta attributes
    _doctype = "person"  # optional, it can be set after using "having" method
    _index = "universe"  # optional, it can be set after using "having" method
    _es = ElasticSearch(host='host', port=port)  # optional, it can be explicit passed to methods
    
    # define fields
    name = KeywordField()

# Initializing mappings and settings
Person.init()
```

> If you do not specify an "id" field, toute will automatically add "id" as KeywordField. It is recommended that when specifying you use KeywordField for ids.


## TIP: import base module

A good practice is to import the base module, look the same example

```python
import toute

class Person(toute.Document):
    name = toute.KeywordField()
```

## Fields

### Base Fields

```python
name = KeywordField()
age = IntegerField()
weight = FloatField()
factor = LongField()
active = BooleanField()
birthday = DateField()
```

### Special Fields

#### GeoPointField

A field to hold GeoPoint with modes dict|array|string and its mappings

```python
class Obj(Document):
    location = GeoPointField(mode='dict')  # default
    # An object representation with lat and lon explicitly named

Obj.init() # important to put the proper mapping for geo location

obj = Obj()

obj.location = {"lat": 40.722, "lon": -73.989}}

class Obj(Document):
    location = GeoPointField(mode='string')
    # A string representation, with "lat,lon"

obj.location = "40.715, -74.011"

class Obj(Document):
    location = GeoPointField(mode='array')
    # An array representation with [lon,lat].

obj.location = [-73.983, 40.719]
```

#### ObjectField

A field to hold nested one-dimension objects, schema-less or with properties validation.

```python
# accepts only dictionaries having strct "street" and "number" keys
address = ObjectField(properties={"street": "string", "number": "integer"})

# Accepts any Python dictionary
extravalues = ObjectField() 
```

#### ArrayField

A Field to hold arrays (python lists)

In the base, any field can accept **multi** parameter

```python
colors = KeywordField(multi=True)   # accepts ["blue", "green", "yellow", ....]
```

But sometimes (specially for nested objects) it is better to be explicit, and also it generates a better mapping

```python
# accepts an array of strings ["blue", "green", "yellow", ....]
colors = ArrayField(KeywordField()) 
```

It is available for any other field

```
locations = ArrayField(GeoPointField())
numbers = ArrayField(IntegerField())
fractions = ArrayField(FloatField())
addresses = ArrayField(ObjectField(properties={"street": "string", "number": "integer"}))
list_of_lists_of_strings = ArrayField(ArrayField(KeywordField()))
```

## Indexing

```python
person = Person(id=1234, name="Gonzo")
person.save()  # or pass .save(es=es_client_instance) if not specified in model 
```

## Getting by id

```python
Person.get(id=1234)
```

## filtering by IDS

```python
ids = [1234, 5678, 9101]
power_trio = Person.filter(ids=ids)
```


## filtering by fields

```python
Person.filter(name="Gonzo")
```

## Searching

toute does not try to create abstraction for query building, 
by default toute only implements search transport receiving a raw ES query 
in form of a Python dictionary.

```python
query = {
    "query": {
        "filtered": {
            "query": {
                "match_all": {}
            },
            "filter": {
                "ids": {
                    "values": [1, 2]
                }
            }
        }
    }
}
Person.search(query, size=10)
```

## Getting all documents (match_all)

```python
Person.all()

# with more arguments

Person.all(size=20)

```


## Counting

```python
Person.count(name='Gonzo')
```

## Updating

###  A single document

A single document can be updated simply using the **.save()** method

```python

person = Person.get(id=1234)
person.name = "Another Name"
person.save()

```

### Updating a Resultset

The Document methods **.get**, **.filter** and **.search** will return an instance
of **ResultSet** object. This object is an Iterator containing the **hits** reached by 
the filtering or search process and exposes some CRUD methods[ **update**, **delete** and **reload** ]
to deal with its results.


```python
people = Person.filter(field='value')
people.update(another_field='another_value')
```

> When updating documents sometimes you need the changes done in the E.S index reflected in the objects 
of the **ResultSet** iterator, so you can use **.reload** method to perform that action.


### The use of **reload** method
 
```python
people = Person.filter(field='value')
print people
... <Resultset: [{'field': 'value', 'another_field': None}, 
                 {'field': 'value', 'another_field': None}]>

# Updating another field on both instances
people.update(another_field='another_value')
print people
... <Resultset: [{'field': 'value', 'another_field': None}, {'field': 'value', 'another_field': None}]>

# Note that in E.S index the values weres changed but the current ResultSet is not updated by defaul
# you have to fire an update
people.reload()

print people
... <Resultset: [{'field': 'value', 'another_field': 'another_value'},
                 {'field': 'value', 'another_field': 'another_value'}]>


```

### Deleting documents


#### A ResultSet

```python
people = Person.all()
people.delete()
```

#### A single document

```python
Person.get(id=123).delete()
```

#### Using the **create** shortcut

The above could be achieved using **create** shortcut


##### A single

```python
Person.create(name='Eddy Merckx', active=False)
```

> Create will return the instance of the indexed Document

##### All using list comprehension

```python
top_5_racing_bikers = [
    Person.create(name=name, active=False)
    for name in ['Eddy Merckx', 
                 'Bernard Hinault', 
                 'Jacques Anquetil', 
                 'Sean Kelly', 
                 'Lance Armstrong']
]

```
> NOTE: **.create** method will automatically save the document to the index, and
will not raise an error if there is a document with the same ID (if specified), it will update it acting as upsert.

#### Updating all

Turning the field **active** to **True** for all documents

```python
Person.update_all(top_5_racing_bikes, active=True)
```

#### Deleting all

```python
Person.delete_all(top_5_racing_bikes)
```


#### Chunck size

chunk_size is number of docs in one chunk sent to ES (default: 500)
you can change using **meta** argument.

```python
Person.update_all(
    top_5_racing_bikes, # the documents
    active=True,  # values to be changed
    meta={'chunk_size': 200}  # meta data passed to **bulk** operation    
)
```

#### Utilities

#### Mapping and Mapping migrations

toute does not saves mappings automatically, but it offers an utility to generate and save mappings on demand
You can create a cron job to refresh mappings once a day or run it every time your model changes

##### Using the document

```python
class Person(Document):
    # define _meta attributes
    _doctype = "person"  # optional, it can be set after using "having" method
    _index = "universe"  # optional, it can be set after using "having" method
    _es = ElasticSearch(host='host', port=port)  # optional, it can be explicit passed to methods
    
    # define fields
    name = KeywordField()
    
```

##### You can use **init()** class method to initialize/update mappings, settings and analyzers    

```
Person.init()  # if not defined in model, pass an **es=es_client** here
```

> Include above in your the last line of your model files or cron jobs or migration scripts


#### Dynamic meta attributes

In toute Document all attributes starting with _ is a meta attribute, sometimes you can't define them hardcoded in your models and want them to be dynamic.
you can achieve this by subclassing your base document, but sometimes you really need to change at runtime.

> Sometimes it is useful for sharding.

```python
from models import Person

BrazilianUsers = Person.having(index='another_index', doctype='brasilian_people', es=Elasticsearch(host='brazil_datacenter'))
AmericanUsers = Person.having(index='another_index', doctype='american_people', es=Elasticsearch(host='us_datacenter'))

brazilian_users = BrasilianUsers.filter(active=True)
american_users = AmericanUsers.search(query=query)

```

#### Validators

##### Field Validator

To validate each field separately you can set a list of validators, each 
validator is a callable receiving field_name and value as arguments and
should return None to be valid. If raise or return the data will be invalidated

```python
from toute.exceptions import ValidationError

def category_validator(field_name, value):
    # check if value is in valid categories
    if value not in ["primary", "secondary", ...]:
        raise ValidationError("Invalid category!!!")
    
class Obj(Document):
    category = KeywordField(validators=[category_validator])

obj = Obj()
obj.category = "another"
obj.save()
Traceback: ValidationError(....)

```

##### Document Validator

To validate the whole document you can set a list of validators, each 
validator is a callable receiving the document instance and
should return None to be valid. If raise or return the data will be invalidated

```python
from toute.exceptions import ValidationError

def if_city_state_is_required(obj):
    if obj.city and not obj.state:
        raise ValidationError("If city is defined you should define state")
        
class Obj(Document):
    _validators = [if_city_state_is_required]
    
    city = KeywordField()
    state = KeywordField()

obj = Obj()
obj.city = "Sao Paulo"
obj.save()
Traceback: ValidationError(....)

```

#### Refreshing

Sometimes you need to force indices-shards refresh for testing, you can use

```python
# Will refresh all indices
Document.refresh()
```

#### Payload builder

Sometimes queries turns in to complex and verbose data structures, to help you
(use with moderation) you can use Payload utils to build queries.


###### Example using a raw query:

```python
query = {
    "query": {
        "filtered": {
            "query": {
                "match_all": {}
            },
            "filter": {
                "ids": {
                    "values": [1, 2]
                }
            }
        }
    }
}

Person.search(query=query, size=10)
```

###### Same example using payload utils

```python
from toute import Payload, Query, Filter
payload = Payload(query=Query.filtered(query=Query.match_all(), filter=Filter.ids([1, 2])))
Person.search(payload, size=10)
```

> Payload utils exposes Payload, Query, Filter, Aggregate, Suggesters

You can also set model on payload initialization to create a more complete payload definition

```python
from toute import Payload, Query, Filter
payload = Payload(
    model=Person,
    query=Query.filtered(query=Query.match_all(), filter=Filter.ids([1, 2]))
    sort={"name": {"order": "desc"}},
    size=10
)
payload.search()
```

###### More examples

You can use Payload, Query or Filter direct in search

```python
from toute import Payload, Query, Filter

Person.search(Payload(query=Query.match_all()))

Person.search(Query.bool(must=[Query.match("name", "Gonzo")]))

Person.search(Query.match_all())

Person.search(Filter.ids([1, 2, 3]))

```

###### chaining

Payload object is chainable so you can do:
```python
payload = Payload(query=query).size(10).sort("field", order="desc")
Document.search(payload) 
# or the equivalent
payload.search(Document)
```


#### Pagination

You can paginate a payload, lets say you have indexed 500 documents under 'test' category and now you need to retrieve 50 per page.

> Result will be included in **pagination.items** 

```python
from toute import Payload, Filter
from models import Doc

payload = Payload(Doc, filter=Filter.term('category', 'test'))

# Total documents
payload.count()
500

# Paginate it
current_page = 1  # you have to increase it on each pagination
pagination = payload.paginate(page=current_page, per_page=50)

pagination.total
500

pagination.pages
10

pagination.has_prev
False

pagination.has_next
True

pagination.next_num
2

len(pagination.items)
50

for item in pagination.items:
    # do something with item

# Turn the page

current_page += 1
pagination = payload.paginate(page=current_page, per_page=50)
pagination.page
2
pagination.has_prev
True

# Another option to move pages

pagination  = pagination.next_page()
pagination.page
3

pagination = pagination.prev_page()
pagination.page
2

# Turn the page in place

pagination.backward()
pagination.page
1

pagination.forward()
pagination.page
2
```

##### Create a paginator in Jinja template

So you want to create buttons for pagination in your jinja template

```html+jinja
{% macro render_pagination(pagination, endpoint) %}
  <div class=pagination>
  {%- for page in pagination.iter_pages() %}
    {% if page %}
      {% if page != pagination.page %}
        <a href="{{ url_for(endpoint, page=page) }}">{{ page }}</a>
      {% else %}
        <strong>{{ page }}</strong>
      {% endif %}
    {% else %}
      <span class=ellipsis>…</span>
    {% endif %}
  {%- endfor %}
  </div>
{% endmacro %}
```


# Contribute

toute is OpenSource! join us!
<a href="http://smallactsmanifesto.org" title="Small Acts Manifesto"><img src="http://smallactsmanifesto.org/static/images/smallacts-badge-80x15-blue.png" style="border: none;" alt="Small Acts Manifesto" /></a>

**MADE WITH #LOVE AND #PYTHON

# Credits
<a href='https://www.freepik.com/free-photos-vectors/background'>vector created by frimufilms - www.freepik.com</a>
