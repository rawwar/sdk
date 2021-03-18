"""Stream class for {{ cookiecutter.tap_id }}."""

import requests

from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

{% if cookiecutter.stream_type == "Other" %}
from singer_sdk.streams import Stream
{% else %}
from singer_sdk.streams import {{ cookiecutter.stream_type }}Stream
{% endif %}

{% if cookiecutter.stream_type in ["GraphQL", "REST"] %}
from singer_sdk.authenticators import (
    APIAuthenticatorBase,
    SimpleAuthenticator,
    OAuthAuthenticator,
    OAuthJWTAuthenticator
)
{% endif %}
from singer_sdk.helpers.typing import (
    ArrayType,
    BooleanType,
    DateTimeType,
    IntegerType,
    NumberType,
    ObjectType,
    PropertiesList,
    Property,
    StringType,
)

SCHEMAS_DIR = Path("./schemas")


{% if cookiecutter.stream_type in ["GraphQL", "REST"] %}
{% if cookiecutter.stream_type == "GraphQL" %}
class {{ cookiecutter.source_name }}Stream({{ cookiecutter.stream_type }}Stream):
    """{{ cookiecutter.source_name }} stream class."""

    url_base = "https://api.mysample.com"

{% elif cookiecutter.stream_type == "REST" %}
class {{ cookiecutter.source_name }}Stream({{ cookiecutter.stream_type }}Stream):
    """{{ cookiecutter.source_name }} stream class."""

    url_base = "https://api.mysample.com"

    def get_url_params(
        self,
        partition: Optional[dict],
        next_page_token: Optional[Any] = None
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization.

        If paging is supported, developers may override this method with specific paging
        logic.
        """
        params = {}
        starting_datetime = self.get_starting_datetime(partition)
        if starting_datetime:
            params.update({"updated": starting_datetime})
        return params

{% endif %}
{% if cookiecutter.auth_method == "Simple" %}
    @property
    def authenticator(self) -> APIAuthenticatorBase:
        http_headers = {"Private-Token": self.config.get("auth_token")}
        if self.config.get("user_agent"):
            http_headers["User-Agent"] = self.config.get("user_agent")
        return SimpleAuthenticator(stream=self, http_headers=http_headers)
{% elif cookiecutter.auth_method == "OAuth2" %}
    @property
    def authenticator(self) -> APIAuthenticatorBase:
        return OAuthAuthenticator(
            stream=self,
            auth_endpoint="TODO: OAuth Endpoint URL",
            oauth_scopes="TODO: OAuth Scopes",
        )
{% elif cookiecutter.auth_method == "JWT" %}
    @property
    def authenticator(self) -> APIAuthenticatorBase:
        return OAuthJWTAuthenticator(
            stream=self,
            auth_endpoint="TODO: OAuth Endpoint URL",
            oauth_scopes="TODO: OAuth Scopes",
        )
{% endif %}


{% endif %}

{% if cookiecutter.stream_type == "GraphQL" %}
# TODO: - Override `StreamA` and `StreamB` with your own stream definition.
#       - Copy-paste as many times as needed to create multiple stream types.
class StreamA({{ cookiecutter.source_name }}Stream):
    name = "users"
    schema = PropertiesList(
        Property("name", StringType),
        Property("id", StringType),
        Property("age", IntegerType),
        Property("email", StringType),
        Property(
            "address",
            ObjectType(
                Property("street", StringType),
                Property("city", StringType),
                Property("state", StringType),
                Property("zip", StringType),
            )
        ),
    ).to_dict()
    primary_keys = ["id"]
    replication_key = None
    graphql_query = """
        users {
            name
            id
            age
            email
            address {
                street
                city
                state
                zip
            }
        }
        """


class StreamB({{ cookiecutter.source_name }}Stream):
    name = "groups"
    schema = PropertiesList(
        Property("name", StringType),
        Property("id", StringType),
        Property("modified", DateTimeType),
    ).to_dict()
    primary_keys = ["id"]
    replication_key = "modified"
    graphql_query = """
        groups {
            name
            id
            modified
        }
        """


{% elif cookiecutter.stream_type in ["Other", "REST"] %}
# TODO: - Override `StreamA` and `StreamB` with your own stream definition.
#       - Copy-paste as many times as needed to create multiple stream types.
class StreamA({{ cookiecutter.source_name }}Stream):
    name = "users"
{% if cookiecutter.stream_type in ["REST"] %}
    path = "/users"
{% endif %}
    primary_keys = ["id"]
    replication_key = None
    schema = PropertiesList(
        Property("name", StringType),
        Property("id", StringType),
        Property("age", IntegerType),
        Property("email", StringType),
        Property("street", StringType),
        Property("city", StringType),
        Property("state", StringType),
        Property("zip", StringType),
    ).to_dict()


class StreamB({{ cookiecutter.source_name }}Stream):
    name = "groups"
{% if cookiecutter.stream_type in ["REST"] %}
    path = "/groups"
{% endif %}
    primary_keys = ["id"]
    replication_key = "modified"
    schema = PropertiesList(
        Property("name", StringType),
        Property("id", StringType),
        Property("modified", DateTimeType),
    ).to_dict()
{% endif %}

{% if cookiecutter.stream_type == "Database" %}
class {{ cookiecutter.source_name }}Stream(DatabaseStream):
    """Stream class for {{ cookiecutter.source_name }} database streams."""

    @classmethod
    def execute_query(cls, sql: Union[str, List[str]], config) -> Iterable[dict]:
        """Run a query in snowflake."""
        connection = cls.open_connection(config=config)
        """Connect to database."""
        # TODO: Define the process of executing a query against your database
        #       and returning a list or other iterable containing the resulting
        #       rows.
        raise NotImplementedError("The method is not yet implemented (TODO)")

    @classmethod
    def open_connection(cls, config) -> Any:
        """Connect to database."""
        # TODO: Define the process of connecting to your database and returning
        #       a connection object.
        raise NotImplementedError("The method is not yet implemented (TODO)")

{% elif cookiecutter.stream_type == "Other" %}

class {{ cookiecutter.source_name }}Stream(Stream):
    """Stream class for {{ cookiecutter.source_name }} streams."""

    def get_records(self, partition: Optional[dict]) -> Iterable[dict]:
        """Return a generator of row-type dictionary objects."""
        # TODO: Write logic to extract data from the upstream source.
        # rows = mysource.getall()
        # for row in rows:
        #     yield row.to_dict()
        raise NotImplementedError("The method is not yet implemented (TODO)")

{% endif %}
