# import modules
import requests


class Server(object):
    """
    Server object to embody tasks needed to accomplish with a server.
    """

    def __init__(self, url, username, password):
        self.url = url
        self._url_admin = "{site_url}/arcgis/admin".format(site_url=url)
        self._token = self.get_token(username, password)

    @staticmethod
    def _test_response_json(response_json):
        """
        Check for error keys in json response, and raise error with messages if something goes wrong.
        :param response_json: JSON from response. 
        """
        # based on the response, determine if an error has occurred, and if so, raise an error,
        if 'messages' in response_json.keys() and 'error' in response_json.keys():
            raise Exception(response_json['messages'][0])

    def get_token(self, username, password):
        """
        Secure a token from the server for subsequent requests.
        :param url_admin: Administrative url to the ArcGIS Server site.
        :param username: Administrative username for the site.
        :param password: Administrative password for the site.
        :return: Token string.
        """
        # make a request to the ArcGIS Server to retrieve the token
        response = requests.post(
            url="{admin_url}/generateToken".format(admin_url=self._url_admin),
            data={
                "username": username,
                "password": password,
                "client": "requestip",
                "expiration": 120,
                "f": "json"
            }
        )

        # retrieve the json from the body as a dictionary
        response_json = response.json()

        # test to make sure it did not bomb out
        self._test_response_json(response_json)

        # return token
        return response_json['token']

    def export_site(self, path_to_save_file):
        """
        Export a backup .agssite file
        :param path_to_save_file: Where the file is going to be saved.
        :return: Path to successfully saved .agssite file.
        """
        # make a call to the rest endpoint to back up the site
        response = requests.post(
            url="{admin_url}/exportSite".format(admin_url=self._url_admin),
            data={
                "token": self._token,
                "f": "json"
            }
        )

        # retrieve the json from the body as a dictionary
        response_json = response.json()

        # check for errors
        self._test_response_json(response_json)

        # download the file
        response = requests.get(
            url="{}/download".format(response_json["location"]),
            params={"token": self._token},
            stream=True
        )

        # throw an error for bad status codes
        response.raise_for_status()

        # write the blocks downloaded by requests
        with open(path_to_save_file, "wb") as handle:
            for block in response.iter_content(1024):
                handle.write(block)

        return response_json
