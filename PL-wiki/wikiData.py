import sys
from SPARQLWrapper import SPARQLWrapper, JSON

# ?player wdt: P106 wd: Q937857 .

def get_labels(wd):
    endpoint_url = "https://query.wikidata.org/sparql"
    query_new = """SELECT ?wdLabel ?ps_Label ?wdpqLabel ?pq_Label {
        VALUES (?player) {(wd:""" + wd + """)}
        ?player ?p ?statement .
        ?statement ?ps ?ps_ .

        ?wd wikibase:claim ?p.
        ?wd wikibase:statementProperty ?ps.

        OPTIONAL {
        ?statement ?pq ?pq_ .
        ?wdpq wikibase:qualifier ?pq .
        }

        SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
    } ORDER BY ?wd ?statement ?ps_"""
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query_new)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

def get_wikiData(wd):
    data = {}
    labels = get_labels(wd)['results']['bindings']
    for label in labels:
        property = {}
        try:
            attr = label['wdLabel']['value']
            value = label['ps_Label']['value']
            if attr in data:
                data[attr].append(value)
            else:
                data[attr] = []
                data[attr].append(value)

        except:
            pass   
    return data

# for result in results["results"]["bindings"]:
#     print(result)
get_wikiData('Qsdgv')