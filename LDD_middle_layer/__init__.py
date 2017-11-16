from flask import Flask, render_template, request, jsonify, make_response
import requests
import urllib

app = Flask(__name__)

app.debug = False
app.config['SECRET_KEY'] = 'WUR_PlantBreeding_LinkedDataDemo_2017'

# The SPARQL endpoint. Adjust accordingly!
# base_sparql_url = 'http://localhost:9999/blazegraph/namespace/ldd-demo/sparql'
base_sparql_url = 'http://snowball:9999/blazegraph/namespace/ldd-demo/sparql'

live_verification = False

valid_queryID = {
    '1': 'template1.sparql',
    '2': 'template2.sparql',
    '3': 'template3.sparql',
    '4': 'template4.sparql',
    '5': 'template5.sparql',
    '6': 'template6.sparql',
    '7': 'template7.sparql',
    '8': 'template8.sparql',
    'gBS': 'getBiologicalStatus.sparql',
    'gC': 'getCountries.sparql',
    'gVar': 'getPhenotypeVariables.sparql',
    'gVal': 'getPhenotypeValues.sparql'
}


# lists with valid values for each parameter. Originally retrieved from the server, but this is slow.
if live_verification:
    country_response = requests.get(base_sparql_url + '?format=json&query=prefix%20rdf%3A%20%3Chttp%3A%2F%2Fwww.w3.org%2F1999%2F02%2F22-rdf-syntax-ns%23%3E%0Aprefix%20WUR_ont%3A%20%3Chttp%3A%2F%2Fwww.wur.nl%2Fpurl%2Fontology%23%3E%0Aprefix%20dct%3A%20%3Chttp%3A%2F%2Fpurl.org%2Fdc%2Fterms%2F%3E%0Aprefix%20sio%3A%20%3Chttp%3A%2F%2Fsemanticscience.org%2Fresource%2F%3E%0Aprefix%20to%3A%20%3Chttp%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FTO%23%3E%0Aprefix%20WUR_acc%3A%20%3Chttp%3A%2F%2Fwww.wur.nl%2Fpurl%2Faccession%23%3E%0Aprefix%20dbp%3A%20%3Chttp%3A%2F%2Fdbpedia.org%2Fproperty%2F%3E%0Aprefix%20dct%3A%20%3Chttp%3A%2F%2Fpurl.org%2Fdc%2Fterms%2F%3E%0Aprefix%20dbr%3A%20%3Chttp%3A%2F%2Fdbpedia.org%2Fresource%2F%3E%0Aprefix%20rdfs%3A%20%3Chttp%3A%2F%2Fwww.w3.org%2F2000%2F01%2Frdf-schema%23%3E%0A%0Aselect%20distinct%0A%20%20%20%20(%3FcountryURI%20as%20%3Furl)%0A%20%20%20%20(%3FcountryName%20as%20%3Fvalue)%0Awhere%20%7B%0A%20%20%20%20%3Fexp%20a%20%3Chttp%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FAGRO_00000370%3E%20.%0A%20%20%20%20%3Fexp%20dbp%3Alocation%20%3FcountryURI%20.%0A%20%20%20%20%3FcountryURI%20rdfs%3Alabel%20%3FcountryName%20%20.%0A%20%20%20%20filter(lang(%3FcountryName)%20%3D%20%27en%27)%0A%7D%0A')
    valid_country = [item['url']['value'] for item in json.loads(country_response.text)['results']['bindings']]
    
    biologicalStatus_response = requests.get(base_sparql_url + '?format=json&query=prefix%20rdf%3A%20%3Chttp%3A%2F%2Fwww.w3.org%2F1999%2F02%2F22-rdf-syntax-ns%23%3E%0Aprefix%20WUR_ont%3A%20%3Chttp%3A%2F%2Fwww.wur.nl%2Fpurl%2Fontology%23%3E%0Aprefix%20dct%3A%20%3Chttp%3A%2F%2Fpurl.org%2Fdc%2Fterms%2F%3E%0Aprefix%20sio%3A%20%3Chttp%3A%2F%2Fsemanticscience.org%2Fresource%2F%3E%0Aprefix%20to%3A%20%3Chttp%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FTO%23%3E%0Aprefix%20WUR_acc%3A%20%3Chttp%3A%2F%2Fwww.wur.nl%2Fpurl%2Faccession%23%3E%0Aprefix%20dbp%3A%20%3Chttp%3A%2F%2Fdbpedia.org%2Fproperty%2F%3E%0Aprefix%20dct%3A%20%3Chttp%3A%2F%2Fpurl.org%2Fdc%2Fterms%2F%3E%0Aprefix%20dbr%3A%20%3Chttp%3A%2F%2Fdbpedia.org%2Fresource%2F%3E%0Aprefix%20rdfs%3A%20%3Chttp%3A%2F%2Fwww.w3.org%2F2000%2F01%2Frdf-schema%23%3E%0A%0Aselect%20distinct%0A%20%20%20%20(%3Fplaceholder%20as%20%3Furl)%0A%20%20%20%20(%3Fbstatus%20as%20%3Fvalue)%0A%20%20%20%20%23%3Facc%0Awhere%20%7B%0A%20%20%3Facc%20a%20WUR_ont%3Aid%20.%0A%20%20%3ForPlant%20WUR_ont%3Ahas_id%20%3Facc%20.%0A%20%20%3ForPlant%20WUR_ont%3Ahas_biological_status%20%3FbstatusURI%20.%0A%20%20%3FbstatusURI%20rdfs%3Alabel%20%3Fbstatus%20.%0A%7D')
    valid_biologicalStatus = [item['value']['value'] for item in json.loads(biologicalStatus_response.text)['results']['bindings']]
    
    phenoVariable_response = requests.get(base_sparql_url + '?format=json&query=prefix%20rdf%3A%20%3Chttp%3A%2F%2Fwww.w3.org%2F1999%2F02%2F22-rdf-syntax-ns%23%3E%0Aprefix%20WUR_ont%3A%20%3Chttp%3A%2F%2Fwww.wur.nl%2Fpurl%2Fontology%23%3E%0Aprefix%20dct%3A%20%3Chttp%3A%2F%2Fpurl.org%2Fdc%2Fterms%2F%3E%0Aprefix%20sio%3A%20%3Chttp%3A%2F%2Fsemanticscience.org%2Fresource%2F%3E%0Aprefix%20to%3A%20%3Chttp%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FTO%23%3E%0Aprefix%20WUR_acc%3A%20%3Chttp%3A%2F%2Fwww.wur.nl%2Fpurl%2Faccession%23%3E%0Aprefix%20dbp%3A%20%3Chttp%3A%2F%2Fdbpedia.org%2Fproperty%2F%3E%0Aprefix%20dct%3A%20%3Chttp%3A%2F%2Fpurl.org%2Fdc%2Fterms%2F%3E%0Aprefix%20dbr%3A%20%3Chttp%3A%2F%2Fdbpedia.org%2Fresource%2F%3E%0Aprefix%20rdfs%3A%20%3Chttp%3A%2F%2Fwww.w3.org%2F2000%2F01%2Frdf-schema%23%3E%0A%0Aselect%20distinct%0A%20%20%20%20%23(%3FtraitURI%20as%20%3Furl)%0A%20%20%20%20(%3Fplaceholder%20as%20%3Furl)%0A%20%20%20%20(%3FphenotypeVariableURI%20as%20%3Fvalue)%0Awhere%20%7B%0A%20%20%20%20%3Fexp%20a%20%3Chttp%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FAGRO_00000370%3E%20.%0A%20%20%20%20%3Fexp%20sio%3ASIO_000219%20%3FobsURI%20.%0A%20%20%20%20%3FobsURI%20to%3Ahas_phenotype_variable%20%3FtraitURI%20%20.%0A%20%20%20%20%3FtraitURI%20to%3Ahas_phenotype_score%20%3FtraitValue%20.%0A%20%20%20%20%3FtraitURI%20dct%3Atitle%20%3FphenotypeVariableURI%20.%0A%20%20%20%20%23filter%20(%3FtraitTitle%20%3D%20)%20.%0A%7D&format=json')
    valid_phenoVariable = [item['value']['value'] for item in json.loads(phenoVariable_response.text)['results']['bindings']]
    phenoValue_response = requests.get(base_sparql_url + '?format=json&query=prefix%20rdf%3A%20%3Chttp%3A%2F%2Fwww.w3.org%2F1999%2F02%2F22-rdf-syntax-ns%23%3E%0Aprefix%20WUR_ont%3A%20%3Chttp%3A%2F%2Fwww.wur.nl%2Fpurl%2Fontology%23%3E%0Aprefix%20dct%3A%20%3Chttp%3A%2F%2Fpurl.org%2Fdc%2Fterms%2F%3E%0Aprefix%20sio%3A%20%3Chttp%3A%2F%2Fsemanticscience.org%2Fresource%2F%3E%0Aprefix%20to%3A%20%3Chttp%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FTO%23%3E%0Aprefix%20WUR_acc%3A%20%3Chttp%3A%2F%2Fwww.wur.nl%2Fpurl%2Faccession%23%3E%0Aprefix%20dbp%3A%20%3Chttp%3A%2F%2Fdbpedia.org%2Fproperty%2F%3E%0Aprefix%20dct%3A%20%3Chttp%3A%2F%2Fpurl.org%2Fdc%2Fterms%2F%3E%0Aprefix%20dbr%3A%20%3Chttp%3A%2F%2Fdbpedia.org%2Fresource%2F%3E%0Aprefix%20rdfs%3A%20%3Chttp%3A%2F%2Fwww.w3.org%2F2000%2F01%2Frdf-schema%23%3E%0A%0Aselect%20distinct%0A%20%20%20%20(%3Fplaceholder%20as%20%3Furl)%0A%20%20%20%20(%3FphenotypeValueURI%20as%20%3Fvalue)%0Awhere%20%7B%0A%20%20%20%20%3Fexp%20a%20%3Chttp%3A%2F%2Fpurl.obolibrary.org%2Fobo%2FAGRO_00000370%3E%20.%0A%20%20%20%20%3Fexp%20sio%3ASIO_000219%20%3FobsURI%20.%0A%20%20%20%20%3FobsURI%20to%3Ahas_phenotype_variable%20%3FtraitURI%20%20.%0A%20%20%20%20%3FtraitURI%20to%3Ahas_phenotype_score%20%3FphenotypeValueURI%20.%0A%20%20%20%20%3FtraitURI%20dct%3Atitle%20%3FtraitTitle%20.%0A%20%20%20%20%23filter%20(%3FtraitTitle%20%3D%20)%20.%0A%7D%0A&format=json')
    valid_phenoValue = [item['value']['value'] for item in json.loads(phenoValue_response.text)['results']['bindings']]
else: 
    valid_country = ['http://dbpedia.org/resource/Israel', 'http://dbpedia.org/resource/Netherlands', 'http://dbpedia.org/resource/Spain', 'http://dbpedia.org/resource/Belgium', 'http://dbpedia.org/resource/France']
    valid_biologicalStatus = ['999 other biological status of accession', '300 traditional cultivar or landrace', '100 wild']
    valid_phenoVariable = ['Plant habit', 'Fruit color', 'Fruit length', 'Fruit height', 'Fruit width', 'Brix (degree brix)']
    valid_phenoValue = ['determinate', 'indeterminate', 'semi determinate', 'ultra determinate', 'NULL', 'apricot / Juans Flame', 'black', 'dark red', 'green', 'light red', 'orange', 'other', 'red', 'ripening', 'tangerine', 'yellow']

# print('country: ', 'http://dbpedia.org/resource/Netherlands' in valid_country)
# print('biological status: ', '100 wild' in valid_biologicalStatus)
# print('phenoVariable: ', 'Plant habit' in valid_phenoVariable)
# print('phenoValue: ', 'red' in valid_phenoValue)


@app.route('/')
def index():
    return jsonify(app='Linked data demonstrator', status=200,
                   parameters='qID, country, pVar, pVal, bioStat')


@app.route('/makeQuery')
def makeQuery():
    queryID = request.args.get('qID', None)
    country = request.args.get('country', None)
    phenotypeVariable = request.args.get('pVar', None)
    phenotypeValue = request.args.get('pVal', None)
    biologicalStatus = request.args.get('bioStat', None)
    callback = request.args.get('callback', '123_abc')

    if queryID not in valid_queryID:
        return jsonify(status='Invalid query ID: ' + queryID)
    if country not in valid_country and country is not None:
        return jsonify(status='Invalid country: ' + country)
    if biologicalStatus not in valid_biologicalStatus and biologicalStatus is not None:
        return jsonify(status='Invalid biological status: ' + biologicalStatus)
    if phenotypeVariable not in valid_phenoVariable and phenotypeVariable is not None:
        return jsonify(status='Invalid phenotype variable: ' + phenotypeVariable)
    if phenotypeValue is not None and phenotypeValue not in valid_phenoValue and not phenotypeValue.replace('.', '').isdigit():
        return jsonify(status='Invalid phenotype value: ' + phenotypeValue)
    if not callback.replace('_', '').isalnum():
        return jsonify(status='Invalid callback code: ' + callback)

    # print('queryFile: ' + str(valid_queryID[queryID]))
    # print('country: ' + str(country))
    # print('phenotypeVariable: ' + str(phenotypeVariable))
    # print('phenotypeValue: ' + str(phenotypeValue))
    # print('biologicalStatus: ' + str(biologicalStatus))
    # print('callback: ' + str(callback))

    queryText = render_template(valid_queryID[queryID],
                               phenotypeVariable=phenotypeVariable, phenotypeValue=phenotypeValue,
                               biologicalStatus=biologicalStatus, country=country)
    
    print(queryText)
    
    reqText = base_sparql_url + '?format=json&query=' + urllib.quote(queryText)
    print('request is: ' + reqText)
    result = requests.get(reqText)

    resp = make_response(callback + '(' + result.text + ')')
    print(result.text)
    resp.headers['Content-Type'] = 'application/sparql-results+json'
    return resp

if __name__ == '__main__':
    # app.run(debug=True)
    # app.debug = True
    app.run(host='0.0.0.0', port=5011)
    #app.run()

# http://localhost:5011/makeQuery?qID=1
