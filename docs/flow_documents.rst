==============
Flow documents
==============


Methods
=======

Get supported documents for given flow
--------------------------------------

.. note::

   To obtain ``token`` refer to ``airslate.addons.access_token()`` function.

.. code-block:: python

   import json
   from airslate.client import Client

   client = Client(
       token='6yWAkqNQaebbJUN14sen7e43ABiDpt1LlqHDkXekZjTH23ubYl8o9ae6osKynsgo',
       headers={
           'Organization-Id': '057C5000-0000-0000-0000D981'
       }
   )

   documents = client.flow_documents.collection(
       '04415300-0000-0000-0000BA29',  # Flow ID
       query={'include': 'fields'},    # URL param
   )

   print(json.dumps(documents, indent=2))

**Output:**

.. code-block::

    {
      "data": [
        {
          "type": "documents",
          "id": "5ED5E800-0000-0000-000021F6",
          "attributes": {
            "name": "Untitled Form",
            "status": "DRAFT",
            "type": "HTML_FORM_NEW",
            "editor_type": "HTML_FORM_NEW",
            "version": 8,
            "is_filled": true,
            "is_hidden": false,
            "content_version": 660,
            "processing_status": "COMPLETED",
            "properties": {
              "template": "simple_web_form"
            },
            "created_at": "2021-01-24 07:51:52",
            "updated_at": "2021-01-24 07:52:02"
          },
          "relationships": {
            "author": {
              "data": {
                "type": "users",
                "id": "7596C700-0000-0000-00009BC6"
              }
            },
            "parent": {
              "data": null
            },
            "pages_file": {
              "data": null
            },
            "attributes_file": {
              "data": {
                "type": "files",
                "id": "63413B20-0000-0000-000045B9"
              }
            },
            "content_file": {
              "data": {
                "type": "files",
                "id": "2BA99B20-0000-0000-000045B9"
              }
            },
            "fields_file": {
              "data": {
                "type": "files",
                "id": "F3F57B20-0000-0000-000045B9"
              }
            },
            "roles_file": {
              "data": null
            },
            "comments_file": {
              "data": null
            },
            "original_file": {
              "data": {
                "type": "files",
                "id": "E28C8B20-0000-0000-000045B9"
              }
            },
            "doc_gen_converted_file": {
              "data": null
            },
            "pdf_file": {
              "data": null
            },
            "doc_gen_content_file": {
              "data": null
            },
            "doc_gen_fields_file": {
              "data": null
            },
            "doc_gen_blocks_file": {
              "data": null
            },
            "final_pdf_file": {
              "data": null
            },
            "signing_certificate_pdf_file": {
              "data": null
            },
            "fields": {
              "data": [
                {
                  "type": "dictionary",
                  "id": "5ED5E800-0000-0000-000021F6-0001"
                },
                {
                  "type": "dictionary",
                  "id": "5ED5E800-0000-0000-000021F6-0002"
                },
                {
                  "type": "dictionary",
                  "id": "5ED5E800-0000-0000-000021F6-0003"
                }
              ]
            }
          },
          "meta": {
            "pdf_file_url": null,
            "fillable_fields_count": 3,
            "num_pages": 1,
            "num_visible_pages": 0
          }
        }
      ],
      "included": [
        {
          "type": "dictionary",
          "id": "5ED5E800-0000-0000-000021F6-0001",
          "attributes": {
            "name": "heading1.title",
            "field_type": "text",
            "value": "Title",
            "dropdown_options": null,
            "radio_buttons_group": null,
            "format": null,
            "editors_config_enabled": false,
            "role_label": null,
            "roleable": false,
            "required": false,
            "number_value": null,
            "triggers": null,
            "comparable": false,
            "timestamp_value": null,
            "restrict_sub_types": null,
            "single_use": false,
            "readonly": false
          },
          "relationships": {
            "editors": {
              "data": []
            }
          }
        },
        {
          "type": "dictionary",
          "id": "5ED5E800-0000-0000-000021F6-0002",
          "attributes": {
            "name": "heading1.description",
            "field_type": "text",
            "value": "",
            "dropdown_options": null,
            "radio_buttons_group": null,
            "format": null,
            "editors_config_enabled": false,
            "role_label": null,
            "roleable": false,
            "required": false,
            "number_value": null,
            "triggers": null,
            "comparable": false,
            "timestamp_value": null,
            "restrict_sub_types": null,
            "single_use": false,
            "readonly": false
          },
          "relationships": {
            "editors": {
              "data": []
            }
          }
        },
        {
          "type": "dictionary",
          "id": "5ED5E800-0000-0000-000021F6-0003",
          "attributes": {
            "name": "singlelinetext1",
            "field_type": "text",
            "value": "",
            "dropdown_options": null,
            "radio_buttons_group": null,
            "format": null,
            "editors_config_enabled": false,
            "role_label": null,
            "roleable": true,
            "required": false,
            "number_value": null,
            "triggers": null,
            "comparable": false,
            "timestamp_value": null,
            "restrict_sub_types": null,
            "single_use": false,
            "readonly": false
          },
          "relationships": {
            "editors": {
              "data": []
            }
          }
        }
      ]
    }
