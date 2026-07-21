# fylr-plugin-custom-data-type-iucn

Custom data type "IUCN" for fylr.

The plugin provides a custom data type for references to the IUCN Red List of Threatened Species [*(IUCN 2024. IUCN Red List of Threatened Species. Version 2024-2 <www.iucnredlist.org>)*](https://www.iucnredlist.org/). This is an external repository managed by the *International Union for Conservation of Nature and Natural Resources*.

## Scope and limitations

The plugin only reads and displays data from this repository. The displayed content depends completely on the content of the external repository.

The plugin connects to the [API version 4](https://api.iucnredlist.org/api-docs/index.html). The functionality of the plugin is limited by the functionality of this API. External changes in the API can happen at any time. Such changes affect the plugin.

The plugin provides a search in the record editor (see [below](#adding-entries-from-the-repository)). It also provides an updater, which fylr runs in the background. The updater collects the existing entries of this custom data type. It updates an entry if the external repository has changed.

The updater can also add or remove a "Red List" tag on the records that link to such an entry. This tag must be configured (see [below](#red-list-tag)). It indicates whether the referenced species is on the red list.

## Configuration

The plugin is configured in the base configuration under the category "IUCN".

### API settings

The plugin connects to the IUCN API. This API requires authentication with an API token.

* The "URL" has the default value `https://api.iucnredlist.org/api/v4`. This should not be changed.
* The "Token" must be requested and entered here. For more information see [API Usage: https://api.iucnredlist.org/](https://api.iucnredlist.org/).

### "Red List" tag

The tag which is used as the "Red List" tag must be configured in the tag manager. It can be named and configured in any way. Select it in the base configuration under "Settings" -> "Red list tag".

Multiple fields in different objecttypes can be selected under "Settings" -> "IUCN Fields". The plugin uses these fields to decide if the tag is added to a record or removed from it. Only fields of records with tag management enabled in the data model are available here.

*Please note*: this feature is optional. Selecting a tag or fields is not necessary. Searching and displaying references to the IUCN repository is not affected by these settings.

### Updater

The updater needs no configuration. fylr runs it in the background and updates each entry once per day.

The updater runs as the user `system:root`. It needs these rights to add and remove the "Red List" tag on all records.

## Adding entries from the repository

In the editor select a field with this custom data type and search for a repository entry.

### Searching by SIS ID

If the entered search term is numerical, the plugin treats it as a *SIS ID*. It looks up the entry with the `/api/v4/taxa/sis/` endpoint.

### Searching by genus and species

To search a species by name, the *latin binomial nomenclature* must be entered. It consists of the genus name and the species name, for example "Canis lupus".

The plugin looks up the entry with the `/api/v4/taxa/scientific_name` endpoint.
