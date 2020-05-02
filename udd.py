#!/usr/bin/env python3

import psycopg2

class UltDebDb:
    deb_name_ver = {
        "stretch": "9",
        "buster": "10",
        "bullseye": "11",
        "bookworm": "12",
    }

    ubuntu_name_ver = {
        "xenial": "16.04 LTS",
        "bionic": "18.04 LTS",
        "eoan": "19.10",
        "focal": "20.04 LTS",
        "groovy": "20.10",
    }

    def __init__(self):
        self.conn = psycopg2.connect(
            host="udd-mirror.debian.net",
            dbname="udd",
            user="udd-mirror",
            password="udd-mirror",
        )

    def deb_packages(self):
        # Builds a string along the lines of:
        #    release='stretch' OR release='buster'
        releases = " OR ".join([f"release='{key}'" for key in self.deb_name_ver.keys()])
        architecture='amd64'

        cursor = self.conn.cursor()
        cursor.execute(f"""
            SELECT distribution, release, package, version FROM packages
            WHERE ({releases}) AND architecture='{architecture}'
        """)
        results = cursor.fetchall()
        return [{
            "operating_system": "Debian " + self.deb_name_ver[release],
            "package": package,
            "version": version,
            } for (distribution, release, package, version) in results]


udd = UltDebDb()
print(udd.deb_packages())
