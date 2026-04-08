### JQ Crash Course

This document serves as a one-stop reference for revisiting core jq concepts. We will use api.github.com to fetch JSON responses and extract meaningful insights using jq commands.

Environment: Ubuntu 24.04

```
curl https://api.github.com/repos/kubernetes/kubernetes
```


#### Pretty print
```
echo '{"key1": "value1"}' | jq
echo '{"key1": "value1"}' | jq '.'
```
```
curl https://api.github.com/repos/kubernetes/kubernetes | jq
```


#### Object Identifier Index
**Syntax**:  jq '.key.subkey.subsubkey'
```
curl https://api.github.com/repos/kubernetes/kubernetes | jq '.license'
curl https://api.github.com/repos/kubernetes/kubernetes | jq '.license.name'
```


#### Array
**Syntax**:  jq '.key[].subkey[].subsubkey'
```
curl https://api.github.com/repos/kubernetes/kubernetes/issues?per_page=5 | jq '.[2]'
curl https://api.github.com/repos/kubernetes/kubernetes/issues?per_page=5 | jq '.[2:4]'
curl https://api.github.com/repos/kubernetes/kubernetes/issues?per_page=5 | jq '.[-2:]'
curl https://api.github.com/repos/kubernetes/kubernetes/issues?per_page=5 | jq '.[2].title'
curl https://api.github.com/repos/kubernetes/kubernetes/issues?per_page=5 | jq '.[].title' # fetch all titles
curl https://api.github.com/repos/kubernetes/kubernetes/issues?per_page=5 | jq -r '.[].title' # for raw output
```


#### Array Constructors
**Syntax**: jq '[ .key[].subkey ]'
```
curl https://api.github.com/repos/kubernetes/kubernetes/issues?per_page=5 | jq '[ .[].title ]' # from bunch of strings to array of strings
```


#### Object Constructors
**Syntax**: jq '{ "key1": <<jq_filter>>, "key2": <<jq_filter>> }'
```
curl https://api.github.com/repos/kubernetes/kubernetes/issues?per_page=5 | jq '[ .[].title, .[].number ]'
# Not what we want, we want array with objects in it.

curl https://api.github.com/repos/kubernetes/kubernetes/issues?per_page=5 | jq '[ { title: .[].title, number: .[].numb
er } ]
# Wrapped in object constructor. Better result but seeing cartesian product, [] is evaluated inside the object. Move it out?

curl https://api.github.com/repos/kubernetes/kubernetes/issues?per_page=5 | jq '[ .[] | { title: .title, number: .number } ]'

curl https://api.github.com/repos/kubernetes/kubernetes/issues?per_page=5 | jq '[ .[] | { title, number } ]'
# Label name same as field name
```


#### Sorting and Counting
**Syntax**: 
```
curl https://api.github.com/repos/kubernetes/kubernetes/issues?per_page=5 | jq '[ .[].title ]' | jq 'sort'

curl https://api.github.com/repos/kubernetes/kubernetes/issues?per_page=5 | jq '[ .[].title ] | sort'
# jq has internal pipe operator

curl https://api.github.com/repos/kubernetes/kubernetes/issues?per_page=5 | jq ' .[].title | length'
# length of all titles, note to remove the array constructor otherwise length will return length of array

curl https://api.github.com/repos/kubernetes/kubernetes/issues?per_page=5 | jq ' sort_by(.created_at) | .[] | { title, number, created_at }'
```