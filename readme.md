# UTRANS Attribute Rules

## Setup

1. create local database from sql management studio named `UTRANS`
1. enable as enterprise gdb via pro

    ```py
    import arcpy
    arcpy.management.EnableEnterpriseGeodatabase(r'...\utrans-attribute-rules\pro-project\localhost.sde', r'C:\Program Files\ESRI\License10.6\sysgen\keycodes')
    ```

    _If you receive errors, you may need to execute the following sql_

    ```sql
    ALTER DATABASE UTRANS
    SET ALLOW_SNAPSHOT_ISOLATION ON

    ALTER DATABASE UTRANS
    SET READ_COMMITTED_SNAPSHOT ON
    ```

1. import the XML Workspace for the existing UTRANS database

    ```py
    arcpy.management.ImportXMLWorkspaceDocument(r'...\utrans-attribute-rules\pro-project\localhost.sde', r'...\utrans-attribute-rules\data\STAGING.XML', 'SCHEMA_ONLY', None)
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

#### Add reference data

1. County boundaries
1. Municipal boundaries
1. Zip code boundaries

### Attribute Rules

1. add `localhost.sde`, `stage.sde`, and `prod.sde` to the pro-project
1. Install attribute rules
   - `python ar.py update --env=local, dev, prod`

This is a doc opt cli, so check the help for the tool.

## Releasing

1. Bump ar.py `VERSION` string
1. Bump ruletypes.py `Constraint.error_number` to match in the integer form
   - Bump before you run since it adds a record to the `Version_Information` table
