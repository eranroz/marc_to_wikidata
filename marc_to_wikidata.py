#!/bin/python

from lxml import objectify

import pywikibot
from pywikibot import pagegenerators, WikidataBot

repo = pywikibot.Site().data_repository()
namespaces = {'slim': 'http://www.loc.gov/MARC21/slim'}
property_to_xpath = {
    'P569': 'slim:datafield[@tag="046"]/slim:subfield[@code="f"]',  # date of birth
    'P570': 'slim:datafield[@tag="046"]/slim:subfield[@code="g"]',  # date of death
    'P19': 'slim:datafield[@tag="370"]/slim:subfield[@code="a"]',  # place of birth
    'P20': 'slim:datafield[@tag="370"]/slim:subfield[@code="b"]',  # place of death
    'P214': 'slim:datafield[@tag="901"]/slim:subfield'  # VIAF
}


class MarcClaimRobot(WikidataBot):
    def __init__(self, claims, **kwargs):
        super(WikidataBot, self).__init__(**kwargs)
        self.claims = claims

    def run(self):
        for claim in self.claims:
            # if no viaf exist
            if 'P214' not in claim:
                # TODO: can we find relaxation that isn't based on VIAF? maybe just name?
                continue
            item = get_entity_by_viaf(claim['P214'])
            item.get()
            self.treat(item, claim)

    def treat(self, item, claim):
        print(claim)
        # TODO: create wikidata claims. see claimit to see how to do it
        raise NotImplemented


def parse_records(marc_records):
    for record in marc_records:
        wikidata_rec = dict()

        names = record.findall('slim:datafield[@tag="100"]/slim:subfield[@code="9"]/..', namespaces)
        for name in names:
            lang = name.find('slim:subfield[@code="9"]', namespaces)
            localname = name.find('slim:subfield[@code="a"]', namespaces)
            wikidata_rec[lang] = localname
            # date of birth
        for wikidata_prop, xpath_query in property_to_xpath.items():
            query_res = record.find(xpath_query, namespaces)
            if query_res:
                wikidata_rec[wikidata_prop] = query_res

        yield wikidata_rec


def get_entity_by_viaf(viaf):
    sparql = "SELECT ?item WHERE { ?item wdt:P214 ?VIAF filter(?VIAF = '%s') }" % viaf
    entities = pagegenerators.WikidataSPARQLPageGenerator(sparql, site=repo)
    entities = list(entities)
    if len(entities) == 0:
        # TODO: either associate existing record with VIAF or create a new entity
        raise NotImplemented
    elif len(entities) > 1:
        # TODO: is it possible to have multiple VIAFs?
        raise Exception('VIAF is expected to be unique')
    return entities[0]


def main():
    # TODO: for now we use the example XML. in post development this should be argument
    marc_records = objectify.parse(open('marcxml_example.xml', 'r')).getroot().find('slim:record', namespaces)
    claims = parse_records(marc_records)
    bot = MarcClaimRobot(claims)
    bot.run()


if __name__ == '__main__':
    main()
