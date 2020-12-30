# UTRANS Attribute Rules

## Setup

1. create local database from sql management studio named `UTRANS`
1. enable as enterprise gdb via pro

    ```py
    import arcpy
    arcpy.management.EnableEnterpriseGeodatabase(r'...\utrans-attribute-rules\pro-project\localhost@utrans.sde', r'C:\Program Files\ESRI\License10.6\sysgen\keycodes')
    ```

    _If you receive errors, you may need to execute the following sql_

    ```sql
    ALTER DATABASE UTRANS
    SET ALLOW_SNAPSHOT_ISOLATION ON

    ALTER DATABASE UTRANS
    SET READ_COMMITTED_SNAPSHOT ON
    ```

1. import the XML Workspace for the existing UTRANS roads data

    ```py
    arcpy.management.ImportXMLWorkspaceDocument(r'...\utrans-attribute-rules\pro-project\localhost@utrans.sde', r'...\utrans-attribute-rules\data\roads_edit.XML', 'DATA', None)
    ```

1. import the reference data from [open sgid](https://gis.utah.gov/sgid/open-sgid/)

    1. County boundaries
    1. Metro Townships
    1. Municipal boundaries
    1. Utah state boundary
    1. Zip code boundaries
    1. National Grid
    1. Address system quadrants

    ```py
    arcpy.env.workspace = r' ...\agrc@opensgid.sde'
    in_features = ['opensgid.boundaries.county_boundaries','opensgid.boundaries.metro_townships','opensgid.boundaries.municipal_boundaries','opensgid.boundaries.state_boundary','opensgid.boundaries.zip_code_areas','opensgid.indices.national_grid','opensgid.location.address_system_quadrants']
    out_location = r'...\utrans-attribute-rules\pro-project\localhost@utrans.sde'
    arcpy.FeatureClassToGeodatabase_conversion(in_features, out_location)
    ```

1. Create a python conda workspace for the project

    ```sh
    conda create --clone arcgispro-py3 --name utrans
    ```

1. Activate the environment

    ```sh
    activate utrans
    ```

1. install the development requirements

    ```sh
    pip install -r requirements.dev.txt
    ```

## Installation

### Database Migrations

### Attribute Rules

1. add `localhost.sde`, `stage.sde`, and `prod.sde` to the pro-project
1. Install attribute rules
   - `python ar.py update --env=local, dev, prod`

This is a doc opt cli, so check the help for the tool.

## Releasing

1. Bump ar.py `VERSION` string
1. Bump ruletypes.py `Constraint.error_number` to match in the integer form
   - Bump before you run since it adds a record to the `Version_Information` table
