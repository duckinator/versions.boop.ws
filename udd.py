#!/usr/bin/env python3

import json
import psycopg2

class UltDebDb:
    debian_name_ver = {
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

    def debian_packages(self):
        # Builds a string along the lines of:
        #    release='stretch' OR release='buster'
        releases = " OR ".join([f"release='{key}'" for key in self.debian_name_ver.keys()])
        architecture='amd64'

        cursor = self.conn.cursor()
        cursor.execute(f"""
            SELECT distribution, release, package, version FROM packages
            WHERE ({releases}) AND architecture='{architecture}'
        """)
        results = cursor.fetchall()
        return [{
            "operating_system": "Debian " + self.debian_name_ver[release],
            "package": package,
            "version": version,
            } for (distribution, release, package, version) in results]

    def ubuntu_packages(self):
        # Builds a string along the lines of:
        #    release='xenial' OR release='bionic' OR <... and so on>
        releases = " OR ".join([f"release='{key}'" for key in self.ubuntu_name_ver.keys()])
        architecture='amd64'

        cursor = self.conn.cursor()
        cursor.execute(f"""
            SELECT distribution, release, package, version FROM ubuntu_packages
            WHERE ({releases}) AND architecture='{architecture}'
        """)
        results = cursor.fetchall()
        return [{
            "operating_system": "Ubuntu " + self.ubuntu_name_ver[release],
            "package": package,
            "version": version,
            } for (distribution, release, package, version) in results]

udd = UltDebDb()
with open("data/debian.json", "w") as f:
    print("Saving Debian data... ", end="")
    json.dump(udd.debian_packages(), f)
    print("Done!")

with open("data/ubuntu.json", "w") as f:
    print("Saving Ubuntu data... ", end="")
    json.dump(udd.ubuntu_packages(), f)
    print("Done!")
