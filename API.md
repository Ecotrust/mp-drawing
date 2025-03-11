# API Documentation for Drawing Module 

Disclaimer: This document was bootstapped using Github Copilot and GPT-4o. The content has been re-written for accuracy.

This documentation provides information on the API endpoints available in the MP Drawing module. These endpoints allow you to query for drawing (AOI) records that your credentials allow you to access.

Please note: These endpoints currently rely on `django.contrib.auth.backends.ModelBackend` authentication system, meaning you will first need to authenticate with a browser, then capture the necessary `sessionid`  cookie to be sent along with your GET request (see curl examples below).

## Endpoints (living)

### Get Drawings

**URL:** `/drawing/get_drawings`

**Method:** `GET`

**Description:** Retrieves a list of all drawings viewable by the user

**Response:**
- `200 OK`: A JSON array containing the details of all drawings.
   - id: (int) primary key identifier of the Drawing record in the database
   - uid: (str) 'drawing_api_{pk}` -- a generated string used on the backend to identify both model type and ID for generic queries
   - name: (str) a human readable string name provided by the drawing creator
   - description: (str) a human readable string description provided by the drawing creator
   - attribites: (obj) {
        - event: "click",
        - attributes: [
            - {
                - title: "Area",
                - data: (str) "{x} sq miles" where X is a float representing the Area of the drawing (polygons only)
            - },
            - {
                - title: "Description",
                - data: (str) The description of the drawing record (same as above)
            - }
        - ]
   - }
   - shared: (boolean) Indicates if the drawing has been shared with a group
   - sharing_groups: (array) a list of string names representing the different groups this drawing has been shared with
   - shared_by_username: (str) The username of the user who shared it
        - TODO: Research if this can be any user other than the owner. This may be redundant.
   - shared_by_name: (str) The username of the shape's owner
   - owned_by_user: (bool) Indicates if the shape is owned by the user who originated the `get_drawings` request

## Deprecated Endpoints

### Wind Analysis Report

**URL:** `/wind_report/<drawing_id>`

**Method:** `GET`

**Description:** Generates a wind energy site analysis report for the specified drawing.

**Parameters:**
- `drawing_id` (integer): The ID of the drawing for which the wind analysis report is requested.

**Response:**
- `200 OK`: A JSON object containing the wind analysis report.
- `404 Not Found`: If the drawing with the specified ID does not exist.

### Area of Interest (AOI) Analysis Report

**URL:** `/aoi_report/<drawing_id>`

**Method:** `GET`

**Description:** Generates an area of interest analysis report for the specified drawing.

**Parameters:**
- `drawing_id` (integer): The ID of the drawing for which the AOI analysis report is requested.

**Response:**
- `200 OK`: A JSON object containing the AOI analysis report.
- `404 Not Found`: If the drawing with the specified ID does not exist.

## Example Usage

### Get Drawings

```sh
curl -v --cookie "sessionid=<your-sessionid-cookie>" https://<your-domain>/drawing/get_drawings
```


Replace `<your-sessionid-cookie>` with the value collected from logging in to the portal via a browser.
Replace `<your-domain>` with the actual domain where the MP Drawing module is hosted.


## Deprecated examples

### Wind Analysis Report

```sh
curl -v --cookie "sessionid=<your-sessionid-cookie>" https://<your-domain>/drawing/wind_report/<report-id>
```

### AOI Analysis Report

```sh
curl -v --cookie "sessionid=<your-sessionid-cookie>" https://<your-domain>/drawing/aoi_report/<drawing-id>
```

## Notes

- Ensure that you have the necessary permissions to access these endpoints.
- The responses are in JSON format.

For further assistance, please contact the support team.
