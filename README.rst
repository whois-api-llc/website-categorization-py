.. image:: https://img.shields.io/badge/License-MIT-green.svg
    :alt: website-categorization-py license
    :target: https://opensource.org/licenses/MIT

.. image:: https://img.shields.io/pypi/v/website-categorization.svg
    :alt: website-categorizations-py release
    :target: https://pypi.org/project/website-categorization

.. image:: https://github.com/whois-api-llc/website-categorization-py/workflows/Build/badge.svg
    :alt: website-categorization-py build
    :target: https://github.com/whois-api-llc/website-categorization-py/actions

========
Overview
========

The client library for
`Website Categorization API <https://website-categorization.whoisxmlapi.com/>`_
in Python language.

The minimum Python version is 3.7.

Installation
============

.. code-block:: shell

    pip install website-categorization

Examples
========

Full API documentation available `here <https://website-categorization.whoisxmlapi.com/api/documentation/v3/making-requests>`_

Create a new client
-------------------

.. code-block:: python

    from websitecategorization import *

    client = Client('Your API key')

Make basic requests
-------------------

.. code-block:: python

    # Get categories for a domain name.
    response = client.data('whoisxmlapi.com')
    print("Responded? " + "Yes" if response.website_responded else "No")
    if response.website_responded:
        for cat in response.categories:
            print("Cat: " + str(cat.name))

Advanced usage
-------------------

Extra request parameters

.. code-block:: python

    # Specifying minimal level of confidence
    response = client.data('whoisxmlapi.com', 0.75)

    # Getting raw API response in XML
    xml = client.raw_data('whoisxmlapi.com', output_format=Client.XML_FORMAT)
