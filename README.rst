=============================
CrowdStrike API Python Client
=============================

Usage
-----

Sample code:

.. sourcecode:: python

    from crowdstrike_client.client import CrowdStrikeClient


    def main():
        base_url = "https://api.crowdstrike.com"
        client_id = "<client-id>"
        client_secret = "<client-secret>"

        cs_client = CrowdStrikeClient(base_url, client_id, client_secret)

        actors_api = cs_client.intel_api.actors

        result = actors_api.query_entities(limit=3, sort="created_date|desc")

        print(f"Meta: {result.meta}")

        for actor in result.resources:
            print(f"Actor name: {actor.name} ({actor.id}), {actor.created_date}")


    if __name__ == "__main__":
        main()
