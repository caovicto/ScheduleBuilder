## USAGE
All responses will have the form
'''json
{
    "data": "mixed type containing response",
    "message": "description of what happened"
}
'''

### List all courses

**Definition**
'GET /courses'
**Response**
- '200 OK' (200 status score) on success
'''json
{[
    {
        "identifier": "Cid",
        "name": "Cid, name of course",
        "semester": "semesters that course runs",
        "credits": " credits for the course",
        "prerequisites": "courses that must be completed previous to taking course"

    }

]}
'''

### Adding a course

**Definition**
'POST /courses'
**Arguments**
- "identifier": string Cid
**Response**
- '201 Created' on success
- Sub-Functions: Retrieve device
'''json
{
    "identifier": "Cid",
    "name": "Cid, name of course",
    "semester": "semesters that course runs",
    "credits": " credits for the course",
    "prerequisites": "courses that must be completed previous to taking course"

}
'''


### Course lookup
**Arguments**
- "identifier": string Cid
**Response**
- '404 Not Found' if course does not exist
'''json
{
    "identifier": "Cid",
    "name": "Cid, name of course",
    "semester": "semesters that course runs",
    "credits": " credits for the course",
    "prerequisites": "courses that must be completed previous to taking course"

}
'''

### Delete a course
**Definition**
'DELETE /courses/<identifier>'
**Response**
-


### Student information
**Arguments**
'''json{
    "major": list of strings majors
    "minor": list of strings miniors
    "completed_courses": list of strings completed courses
    "sem": semesters left
}
'''
