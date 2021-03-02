# [WIP] Transformation types and record properties types 

# Problem

The supported transformation types can sometimes, after being applied to a column/property, result in the latter 
changing its type, which makes the resulting record to no longer match the schema.

## Example

Let’s assume we have a table address with a column `zip_code` of type `int`. We would like to hash this column at load 
time.

```
table_name: "address"
transformations:
    - column: "zip_code"
      type: "HASH"
```

`HASH` transformation will yield a string, causing a problem for the target which is expecting a value of type int.

This is an issue in both PipelineWise FastSync and pipelinewise-transform-field and there are no guardrails against 
this.

# Proposed Solution

The agreement is that transformations must not change the data type, thus, there should be a validation where 
the transformation-column type combinations are checked and fail if the transformation is not suitable for the column 
type.

## Allowed transformations-type combo:

* SET-NULL: Transforms any input to NULL
    * Expected Input type: any
    * Expected Output type: same as the original type, null is acceptable value in any type

* HASH: Transforms string input to hash
    * Expected Input type: string
    * Expected Output type:  string

* HASH-SKIP-FIRST-n: Transforms string input to hash skipping first n characters, e.g. HASH-SKIP-FIRST-2
    * Expected Input type: string
    * Expected Output type: string

* MASK-DATE: Replaces the months and day parts of date columns to be always 1st of Jan
    * Expected Input type: date
    * Expected Output type: date

* MASK-NUMBER: Transforms any numeric value to zero
    * Expected Input type: number
    * Expected Output type: number

* MASK-HIDDEN: Transforms any string to 'hidden'
    * Expected Input type: string
    * Expected Output type: string


## implementation:

Add a flag `--validate` to `pipelinewise-transform-field` to validate a transformation config file 
using the rules above:

`transform-field --validate --config /path/to/config.json --catalog /path/to/propeties.json`

The connector would use the column types in the schema message to do the validation:

```
// This is pseudo code
for every transformation:
    if transformation type = 'SET-NULL'  
        then success
    
    else if (transformation type = 'HASH' or transformation type = 'HASH-SKIP-FIRST-n' or transformation type =
    'MASK-HIDDEN')
        then if column type does not contain 'string' then fail
        else if column format != null then fail
        else success
    
    else if transformation type = 'MASK-DATE'
        then if column type does not contain 'string' then fail
        else if column format != 'date-time' then fail
        else success
    
    else if transformation type = 'MASK-NUMBER'
         then if column type does not contain 'number' or 'integer' then fail
         else success
```

Pipelinewise will then call this connector with the `--validate` flag as part of the post-import checks. Unfortunately, 
given that we don't have access to the sources at PR time,  we can only know the column types after new configs are 
deployed to production.


Also, given that columns could change types at load time, and if the new type is incompatible with the 
transformation applied to it, it would cause the target to fail, so we can add validation at runtime too, ie while the 
connector is receiving streams.

### Reasons for having the validation logic in transform-field connector

Separation of concerns:
* PipelineWise is merely an orchestrator to call commands where and when suitable.
* The connector already harbors the transformation logic, so supercharging with validation makes sense.

Convenience|Usability
* Having the logic in the connector means any user who uses it outside PipelineWise will benefit from it by 
  incorporating the validation in their workflow without having to use Pipelinewise.
