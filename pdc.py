#!/usr/bin/env python3

from functools import lru_cache as memoize
from urllib.request import urlopen
import json
import time
import pdc_client

class Fedora:
    def __init__(self):
        pdc_url = "https://pdc.fedoraproject.org/rest_api/v1"
        self.pdc = pdc_client.PDCClient(pdc_url, develop=True, page_size=100)

    def _want_release(self, r):
        return (r['id_prefix'].lower() == 'fedora' and \
                r['state'] == 'current')

    @memoize()
    def supported_releases(self):
        bodhi_url = "https://bodhi.fedoraproject.org"
        url = f"{bodhi_url}/releases/?page=1&rows_per_page=50"
        releases = json.load(urlopen(url)).get('releases', [])
        releases = [str(r['version']) for r in releases if self._want_release(r)]
        return sorted(releases)

    @memoize()
    def package_names(self):
        names = []
        state=0
        for component in self.pdc.get_paged(self.pdc['global-components']._):
            if state == 0:
                print("\rFetching package names |", end='')
                state = 1
            else:
                print("\rFetching package names -", end='')
                state = 0
            names.append(component['name'])
            time.sleep(0.125)
        print("")
        return names

    def _mdapi(self, url):
        return json.load(geturl(f'https://mdapi.fedoraproject.org/{url}'))

    def package_info(self, package, fedora_release):
        info = self._mdapi(f'f{fedora_release}/srcpkg/{package}')
        return {
            'operating_system': 'Fedora ' + str(fedora_release),
            'package': package,
            'version': info['version']
        }

    def packages(self):
        results = []
        packages = self.package_names()
        for release in self.supported_releases():
            print(f"> Fedora {release}")
            for package in packages:
                results.append(self.package_info(package, release))
                print(results[-1])
                time.sleep(0.125)
        return results

fedora = Fedora()
fedora.packages()
