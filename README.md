# Array Element Template

This action apply a uniform template to each element in an array, ideal for generating standardized file
paths or other strings that require a consistent format.

## Usage

Example usages of running gradle tasks for a multi-project build:

#### With array of strings

```yaml
- uses: palacera/github-action-array-element-template@latest
  id: build-projects-tasks
  with:
    array: ${{ steps.third-party-var.outputs.projects }} # ie. '["core", "feature"]'
    template: 'build{{element}}Task'
    case: 'pascal' # is applied only to element

- run: echo ${{ steps.build-projects-tasks.outputs.json-array }}
```

#### With array of objects

```yaml
- uses: palacera/github-action-array-element-template@latest
  id: build-projects-tasks
  with:
    array: ${{ steps.third-party-var.outputs.projects }} # ie. '[{"type":"core", "version":""}, {"type":"feature", "version":"snapshot"}]'
    template: 'build{{element.type}}{{element.version}}Task'
    case: 'pascal' # is applied only to elements

- run: echo ${{ steps.build-projects-tasks.outputs.json-array }}
```

### Inputs

|        Input         | Description                                                                                                                                                                                                                                                                                                                                                                          | Required |
|:--------------------:|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:--------:|
|       `array`        | Array containing the elements to which the template will be applied.                                                                                                                                                                                                                                                                                                                 |   yes    |         
|      `template`      | String template that defines the format to be applied to each element in the array. It must contain at least one placeholder in the following format: <br/><br/>`{{element}}`<br/>`{{element.someProperty}}`<br/><br/> where `someProperty` is a property of an object in the array.<br/><br/>Example templates:<br/>`foo-{{element}}-bar`<br/>`foo-{{element.x}}-{{element.y}}-bar` |   yes    |          
|   `word-delimiter`   | Delimiter to be used between words.<br/><br/>Note: Words are only determined by existing spaces, symbols or changes in letter case.                                                                                                                                                                                                                                                  |    no    |         
|        `case`        | String case of array element in output.<br/><br/>**NOTE:** This is ONLY applied to each individual replacement string and not applied to the entire template.<br/><br/>Available options: `upper`, `lower`, `camel`, `pascal`.                                                                                                                                                       |    no    |
| `validation-pattern` | Validation pattern for array elements. Defaults to `^[a-zA-Z0-9 _./-]+$`. <br/><br /> **Warning**: Update only when input is trusted.                                                                                                                                                                                                                                                |    no    |

### Outputs

|      Output       | Description                                                         |
|:-----------------:|---------------------------------------------------------------------|
|   `json-array`    | JSON array with each element formatted to the specified template.   |



